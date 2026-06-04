#!/usr/bin/env python3
"""Validate repo-level release contracts across skill lanes.

This is the lane-level gate that runs before each skill's own static checks.
Per-skill scripts still own skill-specific assertions; this script owns the
shared contract that must not depend on a skill remembering to check itself.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_SCHEMA = ROOT / "schemas" / "skill.schema.json"
TRIGGER_SCHEMA = ROOT / "schemas" / "trigger-evals.schema.json"
VALIDATE = ROOT / "scripts" / "validate-against-schema.py"

ROUTE_RE = re.compile(r"^[a-z0-9][a-z0-9._/-]*$")

# Hard ceiling on the parsed SKILL.md frontmatter `description`. The Codex CLI
# and the `skills` loader both reject a description over 1024 chars and SKIP the
# skill (observed: Codex logged "invalid description: exceeds maximum length of
# 1024 characters" and refused to load docs-design/docs-audit). The skill.json
# description mirrors this string, so gating the parsed value covers both files.
MAX_DESCRIPTION_CHARS = 1024


def fail(failures: list[str], message: str) -> None:
    failures.append(message)
    print(f"FAIL {message}", file=sys.stderr)


def is_internal(skill_dir: Path) -> bool:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False
    text = skill_md.read_text()
    return bool(re.search(r"(?m)^metadata:\s*\n(?:^[ \t]+[^\n]*\n)*^[ \t]+internal:\s*true\s*$", text))


def load_json(path: Path, failures: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        fail(failures, f"missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(failures, f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
    return None


def validate_schema(path: Path, schema: Path, failures: list[str]) -> None:
    proc = subprocess.run(
        [sys.executable, str(VALIDATE), str(schema), str(path)],
        cwd=ROOT,
        text=True,
    )
    if proc.returncode != 0:
        fail(failures, f"{path.relative_to(ROOT)}: schema validation failed")


def _git_ignored(paths: list[Path]) -> set[Path]:
    """Return the subset of `paths` that git ignores.

    Gitignored directories are not release artifacts — a developer's local
    install (e.g. a `bmad*` skill set dropped under `.agents/skills/`, which
    `.gitignore` excludes) must not gate the release contract. CI runs on a
    clean checkout, so this filter is a no-op there; it only spares local
    working trees that carry ignored clutter. Falls back to "nothing ignored"
    (the original behavior) if git is unavailable or errors.
    """
    if not paths:
        return set()
    by_str = {str(p): p for p in paths}
    try:
        proc = subprocess.run(
            ["git", "check-ignore", "--stdin"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            input="\n".join(by_str),
        )
    except OSError:
        return set()
    if proc.returncode not in (0, 1):  # 0 = some ignored, 1 = none; >1 = error
        return set()
    return {by_str[line] for line in proc.stdout.splitlines() if line in by_str}


def public_skill_dirs() -> list[Path]:
    dirs = [
        p
        for p in (ROOT / "skills").iterdir()
        if p.is_dir() and p.name not in {"_shared", ".experimental"}
    ]
    experimental = ROOT / "skills" / ".experimental"
    if experimental.exists():
        dirs.extend(p for p in experimental.iterdir() if p.is_dir())
    ignored = _git_ignored(dirs)
    return sorted(p for p in dirs if p not in ignored)


def repo_local_skill_dirs() -> list[Path]:
    base = ROOT / ".agents" / "skills"
    if not base.exists():
        return []
    dirs = [p for p in base.iterdir() if p.is_dir()]
    ignored = _git_ignored(dirs)
    return sorted(p for p in dirs if p not in ignored)


def check_trigger_evals(skill_dir: Path, expected_name: str, failures: list[str]) -> None:
    path = skill_dir / "evals" / "trigger-evals.json"
    data = load_json(path, failures)
    if data is None:
        return

    validate_schema(path, TRIGGER_SCHEMA, failures)

    if data.get("skill") != expected_name:
        fail(
            failures,
            f"{path.relative_to(ROOT)}: skill must be {expected_name}, got {data.get('skill')!r}",
        )

    for index, query in enumerate(data.get("queries", [])):
        route = query.get("expected_route")
        should_activate = query.get("should_activate")
        category = query.get("category")

        if category not in {"positive", "negative", "edge"}:
            fail(
                failures,
                f"{path.relative_to(ROOT)}: queries[{index}].category must be positive, negative, or edge",
            )
        if route is not None and not ROUTE_RE.match(route):
            fail(
                failures,
                f"{path.relative_to(ROOT)}: queries[{index}].expected_route has invalid route id {route!r}",
            )
        if should_activate is False and route is not None:
            fail(
                failures,
                f"{path.relative_to(ROOT)}: queries[{index}] should not activate but has expected_route {route!r}",
            )


def check_skill_md_frontmatter(skill_dir: Path, failures: list[str]) -> dict | None:
    """Assert SKILL.md frontmatter is parseable YAML with name + description.

    Per-skill run-static-checks.sh only `grep`s for `^description:`, which a
    malformed frontmatter passes — but the `skills` CLI runs a real YAML parser
    and silently SKIPS a skill whose frontmatter won't parse (observed: an
    unquoted description containing `: ` colon-space made a published skill
    invisible to `npx skills add . --list`). PyYAML is apt-installed in CI
    (python3-yaml); if it's missing locally this check degrades to a skip.
    """
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return  # already reported by the required-artifacts loop
    try:
        import yaml  # type: ignore
    except ImportError:
        return
    rel = skill_dir.relative_to(ROOT)
    text = skill_md.read_text()
    if not text.startswith("---"):
        fail(failures, f"{rel}/SKILL.md: missing opening '---' YAML frontmatter delimiter")
        return
    parts = text.split("---", 2)
    if len(parts) < 3:
        fail(failures, f"{rel}/SKILL.md: frontmatter not closed with a second '---'")
        return
    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        detail = str(exc).splitlines()[0]
        fail(
            failures,
            f"{rel}/SKILL.md: frontmatter is not valid YAML ({detail}); the skills "
            f"CLI will silently skip this skill — quote the value or use a '>-' block scalar",
        )
        return
    if not isinstance(meta, dict):
        fail(failures, f"{rel}/SKILL.md: frontmatter must be a YAML mapping")
        return
    for key in ("name", "description"):
        if not meta.get(key):
            fail(failures, f"{rel}/SKILL.md: frontmatter missing required key '{key}'")
    description = meta.get("description")
    if isinstance(description, str) and len(description) > MAX_DESCRIPTION_CHARS:
        fail(
            failures,
            f"{rel}/SKILL.md: description is {len(description)} chars, over the "
            f"{MAX_DESCRIPTION_CHARS}-char limit; the Codex CLI and skills loader "
            f"silently skip the skill — trim routing prose (move marketing/provenance "
            f"to metadata.catalog_summary) until it fits",
        )
    return meta


def check_public_skill(skill_dir: Path, failures: list[str]) -> None:
    rel = skill_dir.relative_to(ROOT)
    required = [
        "SKILL.md",
        "skill.json",
        "evals/run-static-checks.sh",
        "evals/trigger-evals.json",
        "evals/activation-cases.md",
    ]
    for item in required:
        if not (skill_dir / item).exists():
            fail(failures, f"{rel}: missing required artifact {item}")

    meta = check_skill_md_frontmatter(skill_dir, failures)

    data = load_json(skill_dir / "skill.json", failures)
    if data is None:
        return

    validate_schema(skill_dir / "skill.json", SKILL_SCHEMA, failures)

    expected_name = skill_dir.name
    if data.get("name") != expected_name:
        fail(failures, f"{rel}/skill.json: name must be {expected_name}, got {data.get('name')!r}")

    # Single canonical routing string: skill.json description must mirror the
    # parsed SKILL.md frontmatter description. Marketing/provenance belongs in
    # metadata.catalog_summary (drives the README) + inspired_by, not a second
    # divergent description that drifts (the perf-design ux-design dead route
    # lived independently in both copies). Compares the PARSED YAML value, not the
    # raw token, so quoted or '>-' block-scalar descriptions are handled; skips
    # when PyYAML is unavailable (meta is None) or for internal templates.
    if meta and not is_internal(skill_dir) and data.get("description") != meta.get("description"):
        fail(
            failures,
            f"{rel}: skill.json description must match the SKILL.md frontmatter "
            f"description (single routing string; put marketing/provenance in "
            f"metadata.catalog_summary)",
        )

    if not is_internal(skill_dir) and data.get("status") != "published":
        fail(
            failures,
            f"{rel}/skill.json: installable skills must have status published, got {data.get('status')!r}",
        )

    check_trigger_evals(skill_dir, expected_name, failures)


def check_experimental_lane_empty(failures: list[str]) -> None:
    experimental = ROOT / "skills" / ".experimental"
    if not experimental.exists():
        return
    for path in experimental.iterdir():
        if path.name == ".gitkeep":
            continue
        fail(failures, f"skills/.experimental must stay empty; found {path.relative_to(ROOT)}")


def check_repo_local_skill(skill_dir: Path, failures: list[str]) -> None:
    rel = skill_dir.relative_to(ROOT)
    required = [
        "SKILL.md",
        "evals/run-static-checks.sh",
        "evals/activation-cases.md",
    ]
    for item in required:
        if not (skill_dir / item).exists():
            fail(failures, f"{rel}: missing repo-local skill artifact {item}")

    check_skill_md_frontmatter(skill_dir, failures)


def main() -> int:
    failures: list[str] = []

    check_experimental_lane_empty(failures)

    for skill_dir in public_skill_dirs():
        check_public_skill(skill_dir, failures)

    for skill_dir in repo_local_skill_dirs():
        check_repo_local_skill(skill_dir, failures)

    if failures:
        print(f"\nrelease contract failed with {len(failures)} issue(s).", file=sys.stderr)
        return 1

    print("release contract passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
