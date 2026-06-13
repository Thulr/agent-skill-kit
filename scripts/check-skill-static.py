#!/usr/bin/env python3
"""Shared static checks for declared skill shapes.

Per-skill `evals/run-static-checks.sh` files are adapters: they declare the
skill id, shape, intents, tracking policy, and local extra facts. This module
owns the repeated implementation behind that seam.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from routing_graph import build_routing_graph

try:
    import jsonschema
except ImportError:
    print(
        "error: jsonschema not installed. In CI: apt-get install -y python3-jsonschema. "
        "Locally: pip install jsonschema",
        file=sys.stderr,
    )
    sys.exit(2)


VALID_SHAPES = {
    "two-layer-audit",
    "two-layer-design",
    "one-layer-audit",
    "one-layer-design",
    "front-door",
    "routed-singleton",
    "repo-local",
}

PLAYBOOK_REQUIRED_SECTIONS = (
    "## Scope",
    "## Grounding",
    "## Good signals",
    "## Common failures",
    "## Heuristics",
    "## Quick diagnostic",
    "## Cross-references",
)

DEFAULT_AUTHOR_STOPWORDS = {
    "Committee",
    "Council",
    "Foundation",
    "Group",
    "Parliament",
    "Working",
    "contributors",
}


@dataclass
class Finding:
    message: str


@dataclass
class CheckContext:
    repo_root: Path
    skill_dir: Path
    skill: str
    shape: str
    intents: list[str]
    tracking: str
    failures: list[Finding] = field(default_factory=list)

    def fail(self, message: str) -> None:
        self.failures.append(Finding(message))

    def rel(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.repo_root))
        except ValueError:
            return str(path)

    def path(self, rel_path: str) -> Path:
        return self.skill_dir / rel_path


def read_json(path: Path, ctx: CheckContext) -> dict | None:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        ctx.fail(f"missing file: {ctx.rel(path)}")
    except json.JSONDecodeError as exc:
        ctx.fail(f"{ctx.rel(path)}: invalid JSON ({exc})")
    return None


def read_csv_rows(path: Path, ctx: CheckContext) -> list[dict[str, str]]:
    try:
        with path.open(newline="") as fh:
            lines = [
                line
                for line in fh
                if line.strip() and not line.lstrip().startswith("#")
            ]
    except FileNotFoundError:
        ctx.fail(f"missing file: {ctx.rel(path)}")
        return []
    reader = csv.DictReader(lines)
    return list(reader)


def split_semicolon(value: str | None) -> list[str]:
    if not value:
        return []
    return [piece.strip() for piece in value.split(";") if piece.strip()]


def word_count(path: Path) -> int:
    return len(path.read_text().split())


def require_file(ctx: CheckContext, rel_path: str) -> None:
    path = ctx.path(rel_path)
    if not path.is_file():
        ctx.fail(f"missing file: {ctx.rel(path)}")


def forbid_file(ctx: CheckContext, rel_path: str) -> None:
    path = ctx.path(rel_path)
    if path.exists() or path.is_symlink():
        ctx.fail(f"forbidden file present: {ctx.rel(path)}")


def require_pattern(ctx: CheckContext, spec: str) -> None:
    try:
        label, rel_path, pattern = spec.split("::", 2)
    except ValueError:
        ctx.fail(f"invalid --require-pattern value {spec!r}; expected label::path::regex")
        return
    path = ctx.path(rel_path)
    try:
        text = path.read_text()
    except FileNotFoundError:
        ctx.fail(f"{label}: missing file: {ctx.rel(path)}")
        return
    if not re.search(pattern, text, flags=re.MULTILINE):
        ctx.fail(f"{label}: pattern not found in {ctx.rel(path)}")


def forbid_pattern(ctx: CheckContext, spec: str) -> None:
    try:
        label, rel_path, pattern = spec.split("::", 2)
    except ValueError:
        ctx.fail(f"invalid --forbid-pattern value {spec!r}; expected label::path::regex")
        return
    path = ctx.path(rel_path)
    try:
        text = path.read_text()
    except FileNotFoundError:
        return
    if re.search(pattern, text, flags=re.MULTILINE):
        ctx.fail(f"{label}: forbidden pattern found in {ctx.rel(path)}")


def validate_schema(ctx: CheckContext, data_path: Path, schema_path: Path) -> None:
    data = read_json(data_path, ctx)
    schema = read_json(schema_path, ctx)
    if data is None or schema is None:
        return
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    for err in errors:
        location = "/".join(str(p) for p in err.absolute_path) or "<root>"
        ctx.fail(f"{ctx.rel(data_path)}: {location}: {err.message}")


def check_skill_json(ctx: CheckContext) -> dict | None:
    path = ctx.path("skill.json")
    validate_schema(ctx, path, ctx.repo_root / "schemas" / "skill.schema.json")
    data = read_json(path, ctx)
    if data is None:
        return None
    actual = data.get("name")
    if actual != ctx.skill:
        ctx.fail(f"{ctx.rel(path)}: name must be {ctx.skill}, got {actual!r}")
    return data


def check_trigger_evals(ctx: CheckContext) -> None:
    path = ctx.path("evals/trigger-evals.json")
    validate_schema(ctx, path, ctx.repo_root / "schemas" / "trigger-evals.schema.json")
    data = read_json(path, ctx)
    if data is None:
        return
    actual = data.get("skill")
    if actual != ctx.skill:
        ctx.fail(f"{ctx.rel(path)}: 'skill' must be {ctx.skill}, got {actual!r}")


def check_frontmatter_basics(ctx: CheckContext, word_max: int) -> None:
    path = ctx.path("SKILL.md")
    if not path.is_file():
        ctx.fail(f"missing file: {ctx.rel(path)}")
        return
    text = path.read_text()
    if not text.startswith("---"):
        ctx.fail("SKILL.md missing YAML frontmatter delimiter (---)")
    if not re.search(rf"^name:\s*{re.escape(ctx.skill)}$", text, flags=re.MULTILINE):
        ctx.fail(f"frontmatter name: pattern not found in {ctx.rel(path)}")
    if not re.search(r"^license:", text, flags=re.MULTILINE):
        ctx.fail(f"frontmatter license: pattern not found in {ctx.rel(path)}")
    count = len(text.split())
    if count >= word_max:
        ctx.fail(f"SKILL.md word count {count} exceeds {word_max} (runtime-only bound)")


def check_source_leaks(
    ctx: CheckContext,
    skill_json: dict | None,
    author_stopwords: set[str],
) -> None:
    if skill_json is None:
        return
    path = ctx.path("SKILL.md")
    if not path.is_file():
        return
    text = path.read_text()
    for entry in skill_json.get("inspired_by", []):
        if not isinstance(entry, dict):
            continue
        author = str(entry.get("author", "")).strip()
        if author:
            last = author.split()[-1]
            if last in author_stopwords or author == last:
                if author in text:
                    ctx.fail(f"SKILL.md leaks source author: {author}")
            elif re.search(rf"\b{re.escape(last)}\b", text):
                ctx.fail(f"SKILL.md leaks source author last name: {last}")
        title = str(entry.get("name", "")).strip()
        if title and title in text:
            ctx.fail(f"SKILL.md leaks source title: {title}")


def resolve_csv(ctx: CheckContext, rel_path: str) -> Path | None:
    rel_path = rel_path.strip()
    if not rel_path.endswith(".csv"):
        return None
    for base in (ctx.skill_dir, ctx.skill_dir / "references"):
        path = base / rel_path
        if path.is_file():
            return path
    return None


def infer_routing_shape(ctx: CheckContext) -> str:
    root = ctx.path("references/intent-router.csv")
    if not root.is_file():
        return "flat"
    layers: list[list[Path]] = [[root]]
    while True:
        next_layer: list[Path] = []
        seen: set[Path] = set()
        for csv_path in layers[-1]:
            for row in read_csv_rows(csv_path, ctx):
                for value in row.values():
                    for piece in split_semicolon(value):
                        resolved = resolve_csv(ctx, piece)
                        if resolved and resolved not in seen:
                            seen.add(resolved)
                            next_layer.append(resolved)
        if not next_layer:
            break
        layers.append(next_layer)
    depth = len(layers)
    if depth == 1:
        return "one-layer"
    if depth == 2:
        return "two-layer"
    return f"depth-{depth}"


def check_declared_shape(ctx: CheckContext) -> None:
    if ctx.shape not in VALID_SHAPES:
        ctx.fail(f"declared shape {ctx.shape!r} is not recognized")
        return
    inferred = infer_routing_shape(ctx)
    if ctx.shape.startswith("two-layer") and inferred != "two-layer":
        ctx.fail(f"declared shape {ctx.shape}, found {inferred}")
    elif ctx.shape.startswith("one-layer") and inferred != "one-layer":
        ctx.fail(f"declared shape {ctx.shape}, found {inferred}")
    if not ctx.shape.startswith("two-layer-"):
        ctx.fail(
            f"declared shape {ctx.shape} is not implemented by this first-slice checker"
        )


def check_intent_router(ctx: CheckContext, forbid_intents: list[str]) -> None:
    router = ctx.path("references/intent-router.csv")
    rows = read_csv_rows(router, ctx)
    seen = [row.get("intent", "") for row in rows]
    if seen != ctx.intents:
        ctx.fail(
            "intent-router.csv: expected intents "
            f"{','.join(ctx.intents)}, got {','.join(seen)}"
        )
    for forbidden in forbid_intents:
        if forbidden in seen:
            ctx.fail(
                f"intent-router.csv: {forbidden!r} belongs outside {ctx.skill}"
            )


def playbook_paths(ctx: CheckContext) -> list[Path]:
    paths: list[Path] = []
    for rel_dir in ("references/playbooks", "references/layers"):
        directory = ctx.path(rel_dir)
        if directory.is_dir():
            paths.extend(p for p in directory.glob("*.md") if p.is_file())
    return sorted(paths)


def check_playbooks(
    ctx: CheckContext,
    tag_regex: str,
    word_min: int,
    word_max: int,
) -> set[str]:
    paths = playbook_paths(ctx)
    if not paths:
        ctx.fail("no playbooks found in references/playbooks")
        return set()
    surfaces: set[str] = set()
    tag_re = re.compile(tag_regex)
    for path in paths:
        surfaces.add(path.stem)
        text = path.read_text()
        for section in PLAYBOOK_REQUIRED_SECTIONS:
            if section not in text:
                ctx.fail(f"{path.name} missing section {section.removeprefix('## ')}")
        if not tag_re.search(heuristics_block(text)):
            ctx.fail(f"{path.name}: Heuristics has no intent tags")
        count = word_count(path)
        if count < word_min or count > word_max:
            ctx.fail(f"{path.name} word count {count} outside {word_min}-{word_max}")
    return surfaces


def heuristics_block(text: str) -> str:
    match = re.search(r"^## Heuristics\s*$", text, flags=re.MULTILINE)
    if not match:
        return ""
    rest = text[match.end() :]
    next_heading = re.search(r"^## ", rest, flags=re.MULTILINE)
    if next_heading:
        return rest[: next_heading.start()]
    return rest


def check_registry_integrity(ctx: CheckContext) -> dict[str, set[str]]:
    referenced_by_intent: dict[str, set[str]] = {intent: set() for intent in ctx.intents}
    for intent in ctx.intents:
        csv_path = ctx.path(f"references/intents/{intent}.csv")
        rows = read_csv_rows(csv_path, ctx)
        for row in rows:
            for rel_path in split_semicolon(row.get("playbook")):
                referenced_by_intent[intent].add(rel_path)
                if not ctx.path(rel_path).is_file():
                    ctx.fail(f"{intent}.csv references missing playbook: {rel_path}")
            for rel_path in split_semicolon(row.get("core_refs")):
                if not ctx.path(rel_path).is_file():
                    ctx.fail(f"{intent}.csv references missing core_ref: {rel_path}")
    return referenced_by_intent


def check_orphan_playbooks(
    ctx: CheckContext,
    surfaces: set[str],
    referenced_by_intent: dict[str, set[str]],
) -> None:
    all_referenced = set().union(*referenced_by_intent.values()) if referenced_by_intent else set()
    for path in playbook_paths(ctx):
        rel_path = path.relative_to(ctx.skill_dir).as_posix()
        if rel_path not in all_referenced:
            ctx.fail(f"{rel_path} is not referenced by any intent CSV (orphan)")


def check_inspired_by_playbooks(
    ctx: CheckContext,
    skill_json: dict | None,
    surfaces: set[str],
) -> None:
    if skill_json is None:
        return
    valid = set(surfaces)
    valid.add("all")
    valid.update(f"{intent}-intent" for intent in ctx.intents)
    for entry in skill_json.get("inspired_by", []):
        if not isinstance(entry, dict):
            continue
        for slug in entry.get("playbooks", []):
            if slug not in valid:
                ctx.fail(f"skill.json inspired_by.playbooks has unknown value: {slug}")


def check_tracking(
    ctx: CheckContext,
    tracking_reports: list[str],
    tracking_intents: list[str],
) -> None:
    if ctx.tracking == "none":
        return
    if ctx.tracking not in {"optional", "required"}:
        ctx.fail(f"tracking must be none, optional, or required, got {ctx.tracking!r}")
        return

    require_file(ctx, "references/trackable-findings.md")
    require_file(ctx, "templates/findings-ledger.md")
    require_file(ctx, "templates/workflow-state.json")

    common_specs = [
        (
            "creates tracking state by default",
            "SKILL.md",
            "Create, resume, or close tracking state",
        ),
        (
            "ledger filename has skill prefix",
            "SKILL.md",
            rf"{re.escape(ctx.skill)}-findings-ledger-<YYYY-MM-DD>-<scope-slug>\.md",
        ),
        (
            "workflow-state filename has skill prefix",
            "SKILL.md",
            rf"{re.escape(ctx.skill)}-workflow-state-<YYYY-MM-DD>-<scope-slug>\.json",
        ),
        (
            "tracking fallback path preserved",
            "SKILL.md",
            rf"audit-artifacts/{re.escape(ctx.skill)}-",
        ),
        ("roadmaps and issues opt-in", "SKILL.md", "roadmaps,"),
        ("closeout resumes saved state", "SKILL.md", "saved state first"),
        ("closeout verifies before status update", "SKILL.md", "verification rule"),
        ("ledger template has skill field", "templates/findings-ledger.md", r"^\*\*Skill:\*\*"),
        (
            "ledger template has skill-prefixed markdown path",
            "templates/findings-ledger.md",
            r"<skill-name>-findings-ledger-<YYYY-MM-DD>-<scope-slug>\.md",
        ),
        (
            "workflow-state template has state_file",
            "templates/workflow-state.json",
            r'"state_file": "docs/audits/<skill-name>-workflow-state-<YYYY-MM-DD>-<scope-slug>\.json"',
        ),
    ]
    for label, rel_path, pattern in common_specs:
        require_pattern(ctx, f"{label}::{rel_path}::{pattern}")

    for rel_path in tracking_reports:
        require_pattern(ctx, f"{Path(rel_path).name} has findings ledger section::{rel_path}::^## Findings ledger")

    for intent in tracking_intents:
        require_pattern(
            ctx,
            f"{intent} CSV loads tracking reference::references/intents/{intent}.csv::references/trackable-findings\\.md",
        )


def check_calibration(ctx: CheckContext, calibration_reports: list[str]) -> None:
    if not calibration_reports:
        return
    require_pattern(
        ctx,
        "SKILL.md has calibration step::SKILL.md::calibrate to project scale",
    )
    for rel_path in calibration_reports:
        require_pattern(ctx, f"{Path(rel_path).name} declares project tier::{rel_path}::Project tier")


def run(ctx: CheckContext, args: argparse.Namespace) -> int:
    for rel_path in (
        "SKILL.md",
        "skill.json",
        "references/intent-router.csv",
        "evals/trigger-evals.json",
    ):
        require_file(ctx, rel_path)
    for intent in ctx.intents:
        require_file(ctx, f"references/intents/{intent}.csv")
    for rel_path in args.require_file:
        require_file(ctx, rel_path)
    for rel_path in args.forbid_file:
        forbid_file(ctx, rel_path)

    check_declared_shape(ctx)
    graph = build_routing_graph(ctx.skill_dir)
    for failure in graph.failures:
        ctx.fail(f"routing graph: {failure}")
    check_frontmatter_basics(ctx, args.word_max)
    skill_json = check_skill_json(ctx)
    check_trigger_evals(ctx)
    check_source_leaks(ctx, skill_json, set(args.author_stopword))
    check_intent_router(ctx, args.forbid_intent)
    surfaces = check_playbooks(
        ctx,
        args.playbook_intent_tag_regex,
        args.playbook_word_min,
        args.playbook_word_max,
    )
    referenced = check_registry_integrity(ctx)
    check_orphan_playbooks(ctx, surfaces, referenced)
    check_inspired_by_playbooks(ctx, skill_json, surfaces)
    check_tracking(ctx, args.tracking_report, args.tracking_intent)
    check_calibration(ctx, args.calibration_report)

    for spec in args.require_pattern:
        require_pattern(ctx, spec)
    for spec in args.forbid_pattern:
        forbid_pattern(ctx, spec)

    if ctx.failures:
        for finding in ctx.failures:
            print(f"FAIL {finding.message}", file=sys.stderr)
        print(
            f"\n{ctx.skill} static eval failed with {len(ctx.failures)} issue(s).",
            file=sys.stderr,
        )
        return 1
    print(f"{ctx.skill} static eval passed.")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--skill", required=True)
    parser.add_argument("--shape", required=True)
    parser.add_argument("--intents", required=True, help="Comma-separated intent ids")
    parser.add_argument("--tracking", choices=["none", "optional", "required"], required=True)
    parser.add_argument("--word-max", type=int, default=800)
    parser.add_argument("--playbook-word-min", type=int, default=400)
    parser.add_argument("--playbook-word-max", type=int, default=1500)
    parser.add_argument(
        "--playbook-intent-tag-regex",
        default=r"\((audit|design|debug)",
    )
    parser.add_argument("--forbid-intent", action="append", default=[])
    parser.add_argument("--require-file", action="append", default=[])
    parser.add_argument("--forbid-file", action="append", default=[])
    parser.add_argument(
        "--require-pattern",
        action="append",
        default=[],
        help="label::relative/path::python-regex",
    )
    parser.add_argument(
        "--forbid-pattern",
        action="append",
        default=[],
        help="label::relative/path::python-regex",
    )
    parser.add_argument("--tracking-report", action="append", default=[])
    parser.add_argument("--tracking-intent", action="append", default=[])
    parser.add_argument("--calibration-report", action="append", default=[])
    parser.add_argument(
        "--author-stopword",
        action="append",
        default=sorted(DEFAULT_AUTHOR_STOPWORDS),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    ctx = CheckContext(
        repo_root=args.repo_root.resolve(),
        skill_dir=args.skill_dir.resolve(),
        skill=args.skill,
        shape=args.shape,
        intents=[intent for intent in args.intents.split(",") if intent],
        tracking=args.tracking,
    )
    return run(ctx, args)


if __name__ == "__main__":
    sys.exit(main())
