#!/usr/bin/env python3
"""Validate minimal-modular-code behavior eval fixtures.

This is intentionally local to the skill. The catalog-wide trigger eval schema
covers activation routing; this check covers the semantic behavior fixture that
feeds thulr/agent comparison runs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_CRITERIA = {
    "reuse_first",
    "shortcut_resistance",
    "deletion_safety",
    "legibility",
    "scope_control",
    "boundary_discipline",
    "right_sizing",
}

REQUIRED_CASE_FIELDS = {
    "id",
    "expected_route",
    "prompt",
    "expected_behavior",
    "failure_modes",
    "criteria",
    "example_pass",
    "example_fail",
}


def fail(message: str) -> None:
    print(f"FAIL behavior-cases.json: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing file: {path}")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")


def require_text(value: object, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path(
        "skills/minimal-modular-code/evals/behavior-cases.json"
    )
    data = load(path)

    if data.get("skill") != "minimal-modular-code":
        fail("skill must be minimal-modular-code")
    require_text(data.get("version"), "version")

    criteria = data.get("criteria")
    if not isinstance(criteria, dict):
        fail("criteria must be an object")
    missing_criteria = REQUIRED_CRITERIA - set(criteria)
    if missing_criteria:
        fail(f"missing criteria: {', '.join(sorted(missing_criteria))}")
    for criterion_id, description in criteria.items():
        require_text(description, f"criteria.{criterion_id}")

    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) < 6:
        fail("cases must contain at least six behavior cases")

    seen_ids: set[str] = set()
    covered_criteria: set[str] = set()

    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            fail(f"cases[{index}] must be an object")
        missing_fields = REQUIRED_CASE_FIELDS - set(case)
        if missing_fields:
            fail(f"{case.get('id', f'case {index}')} missing fields: {', '.join(sorted(missing_fields))}")

        case_id = case["id"]
        require_text(case_id, f"cases[{index}].id")
        if case_id in seen_ids:
            fail(f"duplicate case id: {case_id}")
        seen_ids.add(case_id)

        for field in ("expected_route", "prompt", "expected_behavior", "example_pass", "example_fail"):
            require_text(case[field], f"{case_id}.{field}")

        failure_modes = case["failure_modes"]
        if (
            not isinstance(failure_modes, list)
            or not failure_modes
            or not all(isinstance(mode, str) and mode for mode in failure_modes)
        ):
            fail(f"{case_id}.failure_modes must be a non-empty string list")

        case_criteria = case["criteria"]
        if not isinstance(case_criteria, list) or not case_criteria:
            fail(f"{case_id}.criteria must be a non-empty list")
        unknown = set(case_criteria) - set(criteria)
        if unknown:
            fail(f"{case_id}.criteria contains unknown ids: {', '.join(sorted(unknown))}")
        covered_criteria.update(case_criteria)

        if case["example_pass"].strip() == case["example_fail"].strip():
            fail(f"{case_id} example_pass and example_fail must differ")

    missing_coverage = REQUIRED_CRITERIA - covered_criteria
    if missing_coverage:
        fail(f"criteria not covered by any case: {', '.join(sorted(missing_coverage))}")

    print("minimal-modular-code behavior eval fixture passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
