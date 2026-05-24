#!/usr/bin/env python3
"""Validate a scaffolded skill against shape-specific structural rules.

Usage:
  validate-generated-skill.py <skill_dir> [--shape flat|single-layer|two-level|depth-N]
                              [--report <path>]

Detects routing depth from file layout if --shape is omitted by walking
the CSV chain starting at references/intent-router.csv. Names depths
0/1/2 as flat/single-layer/two-level; deeper depths are reported as
depth-N. Runs deterministic checks that the existing per-skill
run-static-checks.sh scripts do not cover: playbook section uniformity,
per-layer registry orthogonality (every CSV at depth ≥1 has ≥3 rows
that route differently),  inspired_by[]/playbooks mapping,
activation-cases shape (counts, sibling-naming on negatives), and shape
anti-patterns from references/depth-rubric.md.

Exit codes:
  0 — no blocking findings (warnings/notes may still print)
  1 — blocking findings (skill is not ready for informed-skill-reviewer handoff)
  2 — usage error or could not read the skill directory

This is invoked by informed-skill-curator's Phase 5 validation. The LLM
self-review (parallel sub-agents grading per-shape rubrics) is a
separate concern; this script runs the *deterministic* layer.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SEVERITY_BLOCKING = "blocking"
SEVERITY_WARNING = "warning"
SEVERITY_NOTE = "note"

PLAYBOOK_REQUIRED_SECTIONS = (
    "## Scope",
    "## Grounding",
    "## Good signals",
    "## Common failures",
    "## Heuristics",
    "## Quick diagnostic",
    "## Cross-references",
)


@dataclass
class Finding:
    severity: str
    check: str
    location: str
    detail: str

    def line(self) -> str:
        return f"[{self.severity}] {self.check} — {self.location} — {self.detail}"


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, severity: str, check: str, location: str, detail: str) -> None:
        self.findings.append(Finding(severity, check, location, detail))

    def has_blocking(self) -> bool:
        return any(f.severity == SEVERITY_BLOCKING for f in self.findings)

    def render(self) -> str:
        if not self.findings:
            return "validate-generated-skill: no findings.\n"
        buckets: dict[str, list[Finding]] = {
            SEVERITY_BLOCKING: [],
            SEVERITY_WARNING: [],
            SEVERITY_NOTE: [],
        }
        for f in self.findings:
            buckets.setdefault(f.severity, []).append(f)
        out: list[str] = []
        for sev in (SEVERITY_BLOCKING, SEVERITY_WARNING, SEVERITY_NOTE):
            entries = buckets.get(sev, [])
            if not entries:
                continue
            out.append(f"## {sev} ({len(entries)})")
            for f in entries:
                out.append(f"- {f.line()}")
            out.append("")
        return "\n".join(out)


SHAPE_BY_DEPTH = {0: "flat", 1: "single-layer", 2: "two-level"}


def resolve_csv(skill_dir: Path, rel: str) -> Path | None:
    """Resolve a CSV path from a registry row, trying both skill_dir and skill_dir/references."""
    rel = rel.strip()
    if not rel or not rel.endswith(".csv"):
        return None
    for base in (skill_dir, skill_dir / "references"):
        p = base / rel
        if p.is_file():
            return p
    return None


def walk_registry_chain(
    skill_dir: Path,
) -> list[list[Path]]:
    """Return the chain of CSV layers reachable from references/intent-router.csv.

    Layer 0 is [intent-router.csv]. Layer N is the list of CSV files referenced
    by any cell in layer N-1's rows. Stops when no row in the current layer
    points to a further .csv. Used for depth detection and per-layer
    orthogonality checks at any depth ≥1.
    """
    root = skill_dir / "references" / "intent-router.csv"
    if not root.is_file():
        return []
    layers: list[list[Path]] = [[root]]
    while True:
        next_layer: list[Path] = []
        seen: set[Path] = set()
        for csv_path in layers[-1]:
            for row in read_csv(csv_path):
                for val in row.values():
                    if val is None:
                        continue
                    for piece in str(val).split(";"):
                        resolved = resolve_csv(skill_dir, piece)
                        if resolved and resolved not in seen:
                            seen.add(resolved)
                            next_layer.append(resolved)
        if not next_layer:
            break
        layers.append(next_layer)
    return layers


def detect_shape(skill_dir: Path) -> str:
    """Depth-based shape detection. Returns 'flat', 'single-layer', 'two-level', or 'depth-N' for N>=3."""
    layers = walk_registry_chain(skill_dir)
    depth = len(layers)
    return SHAPE_BY_DEPTH.get(depth, f"depth-{depth}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def load_skill_json(skill_dir: Path, report: Report) -> dict | None:
    sj = skill_dir / "skill.json"
    if not sj.is_file():
        report.add(
            SEVERITY_BLOCKING, "skill.json present", str(sj), "file missing"
        )
        return None
    try:
        return json.loads(sj.read_text())
    except json.JSONDecodeError as e:
        report.add(
            SEVERITY_BLOCKING, "skill.json parses", str(sj), f"invalid JSON ({e})"
        )
        return None


def check_inspired_by(
    skill_json: dict,
    shape: str,
    registered_playbooks: set[str],
    registered_intents: set[str],
    report: Report,
) -> None:
    inspired_by = skill_json.get("inspired_by")
    if not isinstance(inspired_by, list) or not inspired_by:
        report.add(
            SEVERITY_BLOCKING,
            "inspired_by present",
            "skill.json:inspired_by",
            "missing or empty",
        )
        return

    accepted_slugs = registered_playbooks | registered_intents | {"all"}
    accepted_slugs |= {f"{intent}-intent" for intent in registered_intents}

    for i, entry in enumerate(inspired_by):
        loc = f"skill.json:inspired_by[{i}]"
        if not isinstance(entry, dict):
            report.add(
                SEVERITY_BLOCKING,
                "inspired_by object shape",
                loc,
                "must be object, not string (Rule from two-level shape anatomy)",
            )
            continue
        playbooks = entry.get("playbooks", [])
        if shape in ("single-layer", "two-level") and not playbooks:
            report.add(
                SEVERITY_BLOCKING,
                "inspired_by playbooks non-empty",
                loc,
                f"source '{entry.get('name', '<unnamed>')}' has empty playbooks[]",
            )
        if isinstance(playbooks, list) and accepted_slugs:
            for slug in playbooks:
                if slug not in accepted_slugs:
                    report.add(
                        SEVERITY_WARNING,
                        "inspired_by playbook slug recognized",
                        loc,
                        (
                            f"playbooks references '{slug}'; not a known surface, "
                            f"intent, '<intent>-intent', or 'all' for this skill"
                        ),
                    )

    if len(inspired_by) < 2 and shape != "flat":
        report.add(
            SEVERITY_WARNING,
            "inspired_by source count",
            "skill.json:inspired_by",
            f"only {len(inspired_by)} source; consider adding at least one critical/dissenting take",
        )


def check_playbook_sections(
    playbook_path: Path, report: Report, severity: str
) -> None:
    text = playbook_path.read_text()
    for section in PLAYBOOK_REQUIRED_SECTIONS:
        if section not in text:
            report.add(
                severity,
                "playbook canonical section",
                str(playbook_path),
                f"missing '{section}'",
            )
    headings = re.findall(r"^## .+", text, flags=re.MULTILINE)
    heuristics_idx = next(
        (i for i, h in enumerate(headings) if h.startswith("## Heuristics")), None
    )
    if heuristics_idx is not None:
        next_heading = (
            headings[heuristics_idx + 1] if heuristics_idx + 1 < len(headings) else None
        )
        if next_heading:
            heur_block = text.split(headings[heuristics_idx], 1)[1].split(
                next_heading, 1
            )[0]
        else:
            heur_block = text.split(headings[heuristics_idx], 1)[1]
        heuristic_bullets = [
            ln for ln in heur_block.splitlines() if ln.lstrip().startswith("-")
        ]
        if len(heuristic_bullets) < 3:
            report.add(
                SEVERITY_WARNING,
                "playbook heuristic count",
                str(playbook_path),
                f"only {len(heuristic_bullets)} heuristics (target ≥3)",
            )


def parse_activation_cases(text: str) -> dict[str, list[str]]:
    """Crude parse of activation-cases.md into {positive, negative, edge}."""
    sections: dict[str, list[str]] = {"positive": [], "negative": [], "edge": []}
    current: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        m = re.match(r"^##\s+(positive|negative|edge|boundary)\b", stripped, re.IGNORECASE)
        if m:
            key = m.group(1).lower()
            current = "edge" if key == "boundary" else key
            continue
        if current and stripped.startswith("-"):
            sections[current].append(stripped)
    return sections


def check_activation_cases(skill_dir: Path, shape: str, report: Report) -> None:
    path = skill_dir / "evals" / "activation-cases.md"
    if not path.is_file():
        report.add(
            SEVERITY_BLOCKING,
            "activation-cases.md present",
            str(path),
            "file missing",
        )
        return
    sections = parse_activation_cases(path.read_text())
    total = sum(len(v) for v in sections.values())
    if total == 0:
        report.add(
            SEVERITY_WARNING,
            "activation-cases parseable",
            str(path),
            "file exists but no '## positive / ## negative / ## boundary' sections "
            "with bullet cases were found; using a non-canonical layout",
        )
        return

    deeper = shape == "two-level" or shape.startswith("depth-")
    pos_min = 10 if deeper else 3
    neg_min = 8 if deeper else 3
    if len(sections["positive"]) < pos_min:
        report.add(
            SEVERITY_BLOCKING,
            "activation-cases positive count",
            str(path),
            f"{len(sections['positive'])} positive (need ≥{pos_min} for {shape})",
        )
    if len(sections["negative"]) < neg_min:
        report.add(
            SEVERITY_BLOCKING,
            "activation-cases negative count",
            str(path),
            f"{len(sections['negative'])} negative (need ≥{neg_min} for {shape})",
        )
    if not sections["edge"]:
        report.add(
            SEVERITY_WARNING,
            "activation-cases boundary/edge",
            str(path),
            "no boundary/edge cases; recommended ≥1",
        )

    sibling_re = re.compile(
        r"(use|prefer|route(?:s)? to|see|try)\s+[`*]?(?:skill[-_])?[a-z][a-z0-9-]*",
        re.IGNORECASE,
    )
    for case in sections["negative"]:
        if not sibling_re.search(case):
            report.add(
                SEVERITY_WARNING,
                "negative names sibling skill",
                str(path),
                f"negative case does not name a sibling skill: {case[:80]}",
            )


def check_layer_orthogonality(
    layers: list[list[Path]], skill_dir: Path, report: Report
) -> None:
    """At every CSV layer at depth ≥1, assert ≥3 rows and that they route differently.

    Walks the chain produced by walk_registry_chain. For each CSV file in
    each layer beyond the root, checks:
      - row count (anti-pattern: collapsed axis)
      - downstream-target diversity (anti-pattern: rows that all load
        identical sets)
    Also flags fully-uniform "Cartesian product" matrices at deeper layers
    as a soft warning (intentional fan-out may be fine; flag for review).
    """
    if not layers:
        return
    for depth_idx, layer in enumerate(layers):
        for csv_path in layer:
            rows = read_csv(csv_path)
            if depth_idx >= 1 and len(rows) < 3:
                report.add(
                    SEVERITY_BLOCKING,
                    "registry layer dimension",
                    str(csv_path),
                    f"only {len(rows)} row(s) at depth {depth_idx}; "
                    f"need ≥3 (anti-pattern: collapsed axis)",
                )
            if len(rows) > 1:
                load_signatures = {
                    tuple(
                        sorted(
                            (v or "")
                            for k, v in row.items()
                            if k not in ("name", "when_to_use", "notes", "trigger_examples")
                        )
                    )
                    for row in rows
                }
                if len(load_signatures) == 1:
                    report.add(
                        SEVERITY_BLOCKING,
                        "registry layer routes meaningfully",
                        str(csv_path),
                        f"all rows at depth {depth_idx} load identical downstream "
                        "targets — registry is not routing (anti-pattern: collapse this layer)",
                    )
    # Cartesian uniformity: at any depth ≥2, sibling CSVs at the same layer
    # all loading identical downstream sets is a smell.
    for depth_idx, layer in enumerate(layers):
        if depth_idx < 2 or len(layer) < 2:
            continue
        downstream_sets: dict[Path, set[str]] = {}
        for csv_path in layer:
            rows = read_csv(csv_path)
            keys = {
                (row.get("surface") or row.get("intent") or "")
                for row in rows
            }
            downstream_sets[csv_path] = {k for k in keys if k}
        unique = {frozenset(v) for v in downstream_sets.values()}
        if len(unique) == 1 and len(downstream_sets) > 1:
            report.add(
                SEVERITY_WARNING,
                "registry layer matrix curation",
                str(layer[0].parent),
                f"every CSV at depth {depth_idx} loads the same row set — "
                "Cartesian product with no curation. Confirm intentional.",
            )


def collect_registered_slugs(skill_dir: Path, shape: str) -> tuple[set[str], set[str]]:
    """Return (playbook_slugs, intent_slugs) used as accepted inspired_by playbooks.

    Depth-aware: for any depth ≥2, leaf playbooks live under
    references/playbooks/; intents are top-level registry rows. For
    single-layer, intents and playbooks share the same vocabulary.
    """
    playbooks: set[str] = set()
    intents: set[str] = set()
    pb_dir = skill_dir / "references" / "playbooks"
    router = skill_dir / "references" / "intent-router.csv"
    is_deeper = shape == "two-level" or shape.startswith("depth-")
    if is_deeper:
        if pb_dir.is_dir():
            playbooks = {p.stem for p in pb_dir.glob("*.md")}
        if router.is_file():
            intents = {r.get("intent", "") for r in read_csv(router) if r.get("intent")}
    elif shape == "single-layer":
        if router.is_file():
            intents = {r.get("intent", "") for r in read_csv(router) if r.get("intent")}
            playbooks = intents
    return playbooks, intents


def run_checks(skill_dir: Path, shape: str, report: Report) -> None:
    skill_json = load_skill_json(skill_dir, report)

    registered_playbooks, registered_intents = collect_registered_slugs(skill_dir, shape)

    if skill_json is not None:
        check_inspired_by(
            skill_json, shape, registered_playbooks, registered_intents, report
        )

    is_deeper = shape == "two-level" or shape.startswith("depth-")
    if shape in ("single-layer",) or is_deeper:
        if is_deeper:
            pb_dir = skill_dir / "references" / "playbooks"
            severity = SEVERITY_BLOCKING
        else:
            pb_dir = skill_dir / "references"
            severity = SEVERITY_WARNING
        if pb_dir.is_dir():
            for pb in sorted(pb_dir.glob("*.md")):
                check_playbook_sections(pb, report, severity)

    if is_deeper or shape == "single-layer":
        layers = walk_registry_chain(skill_dir)
        check_layer_orthogonality(layers, skill_dir, report)

    check_activation_cases(skill_dir, shape, report)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument(
        "--shape",
        default=None,
        help=(
            "Override shape detection. Accepts 'flat', 'single-layer', "
            "'two-level', or 'depth-N' for N>=3."
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Write report to this path in addition to stdout",
    )
    args = parser.parse_args()

    skill_dir: Path = args.skill_dir
    if not skill_dir.is_dir():
        print(f"error: {skill_dir} is not a directory", file=sys.stderr)
        return 2

    shape = args.shape or detect_shape(skill_dir)
    report = Report()
    report.add(
        SEVERITY_NOTE,
        "shape detected",
        str(skill_dir),
        f"running checks for shape={shape}",
    )

    run_checks(skill_dir, shape, report)

    rendered = report.render()
    sys.stdout.write(rendered)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            f"# validate-generated-skill report\n\n"
            f"- skill: {skill_dir}\n- shape: {shape}\n\n{rendered}"
        )

    return 1 if report.has_blocking() else 0


if __name__ == "__main__":
    sys.exit(main())
