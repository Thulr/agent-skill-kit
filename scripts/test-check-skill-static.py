#!/usr/bin/env python3
"""Fixture tests for scripts/check-skill-static.py."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check-skill-static.py"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def write_json(path: Path, data: dict) -> None:
    write(path, json.dumps(data, indent=2) + "\n")


def build_fixture(root: Path) -> Path:
    skill = root / "fixture-skill"
    write(
        skill / "SKILL.md",
        """---
name: fixture-skill
description: Fixture static-check skill.
license: MIT
---

# Fixture Skill

Use `references/intent-router.csv`; show the intent menu. The skill uses a
subagent dispatch section, three lenses, and `trackable-findings.md`.

Create, resume, or close tracking state in
`fixture-skill-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and
`fixture-skill-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
Use `audit-artifacts/fixture-skill-` as the fallback path. roadmaps,
saved state first, and the verification rule are required. Always calibrate to project scale.
""",
    )
    write_json(
        skill / "skill.json",
        {
            "name": "fixture-skill",
            "description": "Fixture static-check skill.",
            "version": "0.1.0",
            "license": "MIT",
            "status": "published",
            "maintainers": ["@owner"],
            "inspired_by": [
                {
                    "name": "Fixture Source",
                    "author": "Example Author",
                    "kind": "book",
                    "contribution": "Grounds fixture behavior.",
                    "playbooks": ["api", "audit-intent"],
                }
            ],
            "metadata": {
                "family": "heuristics",
                "function": "audit",
                "catalog_summary": "Fixture summary.",
            },
        },
    )
    write_json(
        skill / "evals" / "trigger-evals.json",
        {
            "skill": "fixture-skill",
            "version": "0.1.0",
            "queries": [
                {
                    "query": "audit the developer experience",
                    "should_activate": True,
                    "expected_route": "audit/api",
                    "category": "positive",
                }
            ],
        },
    )
    write(
        skill / "references" / "intent-router.csv",
        """intent,name,when_to_use,registry_file,default_template
audit,Audit,Use for audits,references/intents/audit.csv,templates/audit-report.md
debug,Debug,Use for debug,references/intents/debug.csv,templates/debug-runbook.md
edge-pass,Edge pass,Use for edge pass,references/intents/edge-pass.csv,templates/edge-checklist.md
""",
    )
    write(
        skill / "references" / "intents" / "audit.csv",
        """surface,name,when_to_use,playbook,core_refs
api,API,Use API, references/playbooks/api.md, references/core/severity-rubric.md;references/core/score-rubric.md;references/core/personas.md;references/trackable-findings.md
""",
    )
    write(
        skill / "references" / "intents" / "debug.csv",
        """surface,name,when_to_use,playbook,core_refs
api,API debug,Use API, references/playbooks/api.md, references/core/severity-rubric.md;references/core/personas.md
""",
    )
    write(
        skill / "references" / "intents" / "edge-pass.csv",
        """surface,name,when_to_use,playbook,core_refs
api,API edge,Use API, references/playbooks/api.md, references/core/severity-rubric.md;references/trackable-findings.md
""",
    )
    for rel in (
        "references/core/severity-rubric.md",
        "references/core/score-rubric.md",
        "references/core/personas.md",
        "references/trackable-findings.md",
        "templates/debug-runbook.md",
    ):
        write(skill / rel, "# Fixture\n")
    write(
        skill / "references" / "playbooks" / "api.md",
        """# API Playbook

## Scope
Fixture scope.

## Grounding
Fixture grounding.

## Good signals
Fixture signals.

## Common failures
Fixture failures.

## Heuristics
- (audit) Check the API.
- (debug) Debug the API.

## Quick diagnostic
Fixture diagnostic.

## Cross-references
Fixture cross-reference.
""",
    )
    write(
        skill / "templates" / "audit-report.md",
        """# Audit

Project tier: small.

## Findings ledger
Use audit-artifacts/fixture-skill- when docs/audits is unavailable.

## Later
Defer as it grows.
""",
    )
    write(
        skill / "templates" / "audit-report-multi.md",
        """# Multi Audit

Project tier: small.

## Findings ledger
""",
    )
    write(
        skill / "templates" / "edge-checklist.md",
        """# Edge Checklist

## Findings ledger
""",
    )
    write(
        skill / "templates" / "findings-ledger.md",
        """**Skill:** <skill-name>

Path: <skill-name>-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md
""",
    )
    write(
        skill / "templates" / "workflow-state.json",
        """{
  "state_file": "docs/audits/<skill-name>-workflow-state-<YYYY-MM-DD>-<scope-slug>.json"
}
""",
    )
    return skill


def command(skill_dir: Path, *extra: str) -> list[str]:
    return [
        sys.executable,
        str(CHECKER),
        "--repo-root",
        str(ROOT),
        "--skill-dir",
        str(skill_dir),
        "--skill",
        "fixture-skill",
        "--shape",
        "two-layer-audit",
        "--intents",
        "audit,debug,edge-pass",
        "--tracking",
        "required",
        "--playbook-word-min",
        "1",
        "--playbook-word-max",
        "200",
        "--forbid-intent",
        "design",
        "--require-file",
        "references/core/severity-rubric.md",
        "--require-file",
        "references/core/score-rubric.md",
        "--require-file",
        "references/core/personas.md",
        "--require-file",
        "templates/audit-report.md",
        "--require-file",
        "templates/audit-report-multi.md",
        "--require-file",
        "templates/debug-runbook.md",
        "--require-file",
        "templates/edge-checklist.md",
        "--tracking-report",
        "templates/audit-report.md",
        "--tracking-report",
        "templates/audit-report-multi.md",
        "--tracking-report",
        "templates/edge-checklist.md",
        "--tracking-intent",
        "audit",
        "--tracking-intent",
        "edge-pass",
        "--calibration-report",
        "templates/audit-report.md",
        "--calibration-report",
        "templates/audit-report-multi.md",
        "--require-pattern",
        "audit report preserves fallback path::templates/audit-report.md::audit-artifacts/fixture-skill-",
        "--require-pattern",
        "report has Later/as-it-grows bucket::templates/audit-report.md::as it grows",
        *extra,
    ]


def run_case(name: str, mutate=None, extra: tuple[str, ...] = (), should_pass=True) -> bool:
    with tempfile.TemporaryDirectory(prefix="check-skill-static-") as tmp:
        skill_dir = build_fixture(Path(tmp))
        if mutate:
            mutate(skill_dir)
        proc = subprocess.run(
            command(skill_dir, *extra),
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
    passed = proc.returncode == 0
    if passed == should_pass:
        print(f"OK   {name}")
        return True
    expected = "pass" if should_pass else "fail"
    actual = "pass" if passed else "fail"
    print(f"FAIL {name}: expected {expected}, got {actual}", file=sys.stderr)
    if proc.stdout:
        print(proc.stdout, file=sys.stderr)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    return False


def main() -> int:
    cases = [
        ("valid two-layer audit", None, (), True),
        (
            "explicit shape mismatch",
            None,
            ("--shape", "one-layer-audit"),
            False,
        ),
        (
            "missing route target",
            lambda skill_dir: (skill_dir / "references" / "playbooks" / "api.md").unlink(),
            (),
            False,
        ),
        (
            "tracking required remains a fact",
            lambda skill_dir: (skill_dir / "templates" / "workflow-state.json").unlink(),
            (),
            False,
        ),
    ]
    failures = 0
    for name, mutate, extra, should_pass in cases:
        if not run_case(name, mutate, extra, should_pass):
            failures += 1
    if failures:
        print(f"check-skill-static tests failed with {failures} issue(s).", file=sys.stderr)
        return 1
    print("check-skill-static tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
