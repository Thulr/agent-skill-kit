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


def public_skill_dirs() -> list[Path]:
    dirs = [
        p
        for p in (ROOT / "skills").iterdir()
        if p.is_dir() and p.name not in {"_shared", ".experimental"}
    ]
    experimental = ROOT / "skills" / ".experimental"
    if experimental.exists():
        dirs.extend(p for p in experimental.iterdir() if p.is_dir())
    return sorted(dirs)


def repo_local_skill_dirs() -> list[Path]:
    base = ROOT / ".agents" / "skills"
    return sorted(p for p in base.iterdir() if p.is_dir()) if base.exists() else []


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

    data = load_json(skill_dir / "skill.json", failures)
    if data is None:
        return

    validate_schema(skill_dir / "skill.json", SKILL_SCHEMA, failures)

    expected_name = skill_dir.name
    if data.get("name") != expected_name:
        fail(failures, f"{rel}/skill.json: name must be {expected_name}, got {data.get('name')!r}")

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
