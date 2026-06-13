#!/usr/bin/env python3
"""Fixture tests for scripts/routing_graph.py."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from routing_graph import build_routing_graph


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def build_fixture(root: Path) -> Path:
    skill = root / "skill"
    write(
        skill / "references" / "intent-router.csv",
        "intent,name,when_to_use,registry_file,default_template\n"
        "audit,Audit,Use it,references/intents/audit.csv,templates/audit-report.md\n",
    )
    write(
        skill / "references" / "intents" / "audit.csv",
        "surface,name,when_to_use,playbook,core_refs\n"
        "api,API,Use it,references/playbooks/api.md,references/core/severity.md\n",
    )
    write(skill / "references" / "playbooks" / "api.md", "# API\n")
    write(skill / "references" / "core" / "severity.md", "# Severity\n")
    write(skill / "templates" / "audit-report.md", "# Audit\n")
    write(
        skill / "evals" / "trigger-evals.json",
        json.dumps(
            {
                "skill": "skill",
                "version": "0.1.0",
                "queries": [
                    {
                        "query": "audit api",
                        "should_activate": True,
                        "expected_route": "audit/api",
                        "category": "positive",
                    }
                ],
            }
        ),
    )
    return skill


def run_case(name: str, mutate=None, should_pass: bool = True) -> bool:
    with tempfile.TemporaryDirectory(prefix="routing-graph-") as tmp:
        skill = build_fixture(Path(tmp))
        if mutate:
            mutate(skill)
        graph = build_routing_graph(skill)
    passed = not graph.failures
    if passed == should_pass:
        print(f"OK   {name}")
        return True
    print(f"FAIL {name}: expected pass={should_pass}, failures={graph.failures}", file=sys.stderr)
    return False


def main() -> int:
    cases = [
        ("valid graph", None, True),
        (
            "missing playbook target",
            lambda skill: (skill / "references" / "playbooks" / "api.md").unlink(),
            False,
        ),
        (
            "ragged csv row",
            lambda skill: write(
                skill / "references" / "intents" / "audit.csv",
                "surface,name,when_to_use,playbook,core_refs\napi,API\n",
            ),
            False,
        ),
        (
            "trigger route drift",
            lambda skill: write(
                skill / "evals" / "trigger-evals.json",
                json.dumps(
                    {
                        "skill": "skill",
                        "version": "0.1.0",
                        "queries": [
                            {
                                "query": "audit db",
                                "should_activate": True,
                                "expected_route": "review/db",
                                "category": "positive",
                            }
                        ],
                    }
                ),
            ),
            False,
        ),
    ]
    failures = 0
    for name, mutate, should_pass in cases:
        if not run_case(name, mutate, should_pass):
            failures += 1
    if failures:
        print(f"routing graph tests failed with {failures} issue(s).", file=sys.stderr)
        return 1
    print("routing graph tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
