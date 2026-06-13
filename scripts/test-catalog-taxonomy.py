#!/usr/bin/env python3
"""Fixture tests for scripts/catalog_taxonomy.py."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from catalog_taxonomy import CatalogTaxonomy


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def write_json(path: Path, data: dict) -> None:
    write(path, json.dumps(data, indent=2) + "\n")


def skill(root: Path, name: str, family: str, function: str) -> None:
    write(root / "skills" / name / "SKILL.md", f"---\nname: {name}\nlicense: MIT\n---\n")
    write_json(
        root / "skills" / name / "skill.json",
        {
            "name": name,
            "status": "published",
            "description": "Fixture.",
            "license": "MIT",
            "maintainers": ["@owner"],
            "inspired_by": [
                {
                    "name": "Source",
                    "author": "Author",
                    "kind": "book",
                    "contribution": "Fixture.",
                    "playbooks": ["all"],
                }
            ],
            "metadata": {
                "family": family,
                "function": function,
                "catalog_summary": "Fixture summary.",
            },
        },
    )


def build_repo(root: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    skill(root, "writing-audit", "heuristics", "audit")
    skill(root, "writing-design", "heuristics", "design")
    write(root / "skills" / "_shared" / "writing" / "core" / "rubric.md", "# Rubric\n")
    write(root / "skills" / ".experimental" / ".gitkeep", "")
    write_json(
        root / "catalog" / "catalog.json",
        {
            "pick_a_skill": {
                "intro": "Pick.",
                "primary": {
                    "columns": ["Surface", "Audit", "Design"],
                    "rows": [
                        {
                            "surface": "Writing",
                            "critique": "`writing-audit`",
                            "design": "`writing-design`",
                        }
                    ],
                },
                "secondary": {"lead": "Other.", "columns": ["Need", "Skill"], "rows": []},
                "unsure": [],
            },
            "catalog": {
                "lead_in": "Catalog.",
                "families": [
                    {"id": "heuristics", "title": "Heuristics", "intro": []},
                    {"id": "research", "title": "Research", "intro": []},
                    {"id": "ax", "title": "AX", "intro": []},
                    {"id": "discovery", "title": "Discovery", "intro": []},
                ],
            },
        },
    )
    # Add one skill in each non-heuristic family so the family coverage check is
    # isolated from the writing-pair checks.
    for name, family in (
        ("research", "research"),
        ("agent-experience", "ax"),
        ("product-discovery", "discovery"),
    ):
        skill(root, name, family, "singleton")
    write(root / "docs" / "architecture" / "README.md", "Domains: `writing`.\n")


def run_case(name: str, mutate=None, should_pass: bool = True) -> bool:
    with tempfile.TemporaryDirectory(prefix="catalog-taxonomy-") as tmp:
        root = Path(tmp).resolve()
        build_repo(root)
        if mutate:
            mutate(root)
        failures = CatalogTaxonomy(root).validate()
    passed = not failures
    if passed == should_pass:
        print(f"OK   {name}")
        return True
    print(f"FAIL {name}: expected pass={should_pass}, failures={failures}", file=sys.stderr)
    return False


def main() -> int:
    cases = [
        ("valid taxonomy", None, True),
        (
            "architecture doc must name pair domain",
            lambda root: write(root / "docs" / "architecture" / "README.md", "Domains: `dx`.\n"),
            False,
        ),
        (
            "pair requires shared substrate",
            lambda root: (root / "skills" / "_shared" / "writing" / "core" / "rubric.md").unlink(),
            False,
        ),
    ]
    failures = 0
    for name, mutate, should_pass in cases:
        if not run_case(name, mutate, should_pass):
            failures += 1
    if failures:
        print(f"catalog taxonomy tests failed with {failures} issue(s).", file=sys.stderr)
        return 1
    print("catalog taxonomy tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
