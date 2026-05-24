#!/usr/bin/env python3
"""Validate a scaffolded skill against shape-specific structural rules.

Usage:
  validate-generated-skill.py <skill_dir> [--shape flat|single-layer|two-level]
                              [--report <path>]

Detects shape from file layout if --shape is omitted. Runs deterministic
checks that the existing per-skill run-static-checks.sh scripts do not
cover: playbook section uniformity, registry orthogonality (two-level),
inspired_by[]/playbooks mapping, activation-cases shape (counts,
sibling-naming on negatives), and shape anti-patterns from
references/depth-rubric.md.

Exit codes:
  0 — no blocking findings (warnings/notes may still print)
  1 — blocking findings (skill is not ready for skill-reviewer handoff)
  2 — usage error or could not read the skill directory

This is invoked by skill-curator's Phase 5 validation. The LLM
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


def detect_shape(skill_dir: Path) -> str:
    """Heuristic shape detection from file layout."""
    intents_dir = skill_dir / "references" / "intents"
    playbooks_dir = skill_dir / "references" / "playbooks"
    intent_router = skill_dir / "references" / "intent-router.csv"

    if intents_dir.is_dir() and playbooks_dir.is_dir():
        return "two-level"
    if intent_router.is_file():
        return "single-layer"
    return "flat"


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

    pos_min = 10 if shape == "two-level" else 3
    neg_min = 8 if shape == "two-level" else 3
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


def check_two_level_orthogonality(skill_dir: Path, report: Report) -> None:
    intents_dir = skill_dir / "references" / "intents"
    intent_csvs = sorted(intents_dir.glob("*.csv"))
    if len(intent_csvs) < 3:
        report.add(
            SEVERITY_BLOCKING,
            "two-level intent dimension",
            str(intents_dir),
            f"only {len(intent_csvs)} intent(s); need ≥3 (anti-pattern: collapsed axis)",
        )
    surface_sets: dict[str, set[str]] = {}
    for csv_path in intent_csvs:
        rows = read_csv(csv_path)
        surfaces = {r.get("surface", "") for r in rows if r.get("surface")}
        surface_sets[csv_path.stem] = surfaces
        if len(surfaces) < 3:
            report.add(
                SEVERITY_BLOCKING,
                "two-level surface dimension",
                str(csv_path),
                f"only {len(surfaces)} surface(s); need ≥3",
            )
    if len(surface_sets) >= 2:
        all_identical = (
            len({frozenset(s) for s in surface_sets.values()}) == 1
        )
        if all_identical:
            report.add(
                SEVERITY_WARNING,
                "two-level matrix curation",
                str(intents_dir),
                "every intent loads the same surface set — Cartesian product with no curation. Confirm this is intentional.",
            )


def check_single_layer_registry(skill_dir: Path, report: Report) -> None:
    registry = skill_dir / "references" / "intent-router.csv"
    if not registry.is_file():
        report.add(
            SEVERITY_BLOCKING,
            "intent-router.csv present",
            str(registry),
            "file missing",
        )
        return
    rows = read_csv(registry)
    if not rows:
        report.add(
            SEVERITY_BLOCKING, "registry non-empty", str(registry), "no rows"
        )
        return
    detail_signatures = {tuple(sorted((r.get("detail_file") or "").split(";"))) for r in rows}
    if len(detail_signatures) == 1 and len(rows) > 1:
        report.add(
            SEVERITY_BLOCKING,
            "registry routes meaningfully",
            str(registry),
            "all rows load identical detail_file set — registry is not routing (anti-pattern: collapse to flat)",
        )


def collect_registered_slugs(skill_dir: Path, shape: str) -> tuple[set[str], set[str]]:
    """Return (playbook_slugs, intent_slugs) used as accepted inspired_by playbooks."""
    playbooks: set[str] = set()
    intents: set[str] = set()
    if shape == "two-level":
        pb_dir = skill_dir / "references" / "playbooks"
        if pb_dir.is_dir():
            playbooks = {p.stem for p in pb_dir.glob("*.md")}
        router = skill_dir / "references" / "intent-router.csv"
        if router.is_file():
            intents = {r.get("intent", "") for r in read_csv(router) if r.get("intent")}
    elif shape == "single-layer":
        router = skill_dir / "references" / "intent-router.csv"
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

    if shape in ("single-layer", "two-level"):
        if shape == "two-level":
            pb_dir = skill_dir / "references" / "playbooks"
            severity = SEVERITY_BLOCKING
        else:
            pb_dir = skill_dir / "references"
            severity = SEVERITY_WARNING
        if pb_dir.is_dir():
            for pb in sorted(pb_dir.glob("*.md")):
                check_playbook_sections(pb, report, severity)

    if shape == "two-level":
        check_two_level_orthogonality(skill_dir, report)

    if shape == "single-layer":
        check_single_layer_registry(skill_dir, report)

    check_activation_cases(skill_dir, shape, report)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument(
        "--shape",
        choices=["flat", "single-layer", "two-level"],
        default=None,
        help="Override shape detection",
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
