#!/usr/bin/env python3
"""Smoke-test trigger-evals schema invariants with valid and invalid cases."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "trigger-evals.schema.json"
VALIDATE = ROOT / "scripts" / "validate-against-schema.py"


def payload(case: dict) -> dict:
    return {
        "skill": "schema-smoke",
        "version": "0.1.0",
        "queries": [case],
    }


CASES = [
    (
        "valid positive with route",
        payload(
            {
                "query": "audit this repo with clean architecture",
                "should_activate": True,
                "expected_route": "audit/all",
                "category": "positive",
            }
        ),
        True,
    ),
    (
        "valid positive single-route null",
        payload(
            {
                "query": "review the tests",
                "should_activate": True,
                "expected_route": None,
                "category": "positive",
            }
        ),
        True,
    ),
    (
        "valid negative null route",
        payload(
            {
                "query": "what is the weather",
                "should_activate": False,
                "expected_route": None,
                "category": "negative",
            }
        ),
        True,
    ),
    (
        "invalid missing category",
        payload(
            {
                "query": "audit this repo with clean architecture",
                "should_activate": True,
                "expected_route": "audit/all",
            }
        ),
        False,
    ),
    (
        "invalid missing expected_route",
        payload(
            {
                "query": "audit this repo with clean architecture",
                "should_activate": True,
                "category": "positive",
            }
        ),
        False,
    ),
    (
        "invalid bad route id",
        payload(
            {
                "query": "audit this repo with clean architecture",
                "should_activate": True,
                "expected_route": "Audit All",
                "category": "positive",
            }
        ),
        False,
    ),
    (
        "invalid negative has route",
        payload(
            {
                "query": "what is the weather",
                "should_activate": False,
                "expected_route": "audit/all",
                "category": "negative",
            }
        ),
        False,
    ),
]


def main() -> int:
    failures = 0
    with tempfile.TemporaryDirectory(prefix="trigger-evals-schema-") as tmp:
        tmp_path = Path(tmp)
        for index, (name, data, should_pass) in enumerate(CASES, start=1):
            path = tmp_path / f"case-{index}.json"
            path.write_text(json.dumps(data, indent=2) + "\n")
            proc = subprocess.run(
                [sys.executable, str(VALIDATE), str(SCHEMA), str(path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            passed = proc.returncode == 0
            if passed == should_pass:
                print(f"OK   {name}")
                continue

            failures += 1
            expected = "pass" if should_pass else "fail"
            actual = "pass" if passed else "fail"
            print(f"FAIL {name}: expected {expected}, got {actual}", file=sys.stderr)
            if proc.stdout:
                print(proc.stdout, file=sys.stderr)
            if proc.stderr:
                print(proc.stderr, file=sys.stderr)

    if failures:
        print(f"trigger-evals schema smoke failed with {failures} issue(s).", file=sys.stderr)
        return 1

    print("trigger-evals schema smoke passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
