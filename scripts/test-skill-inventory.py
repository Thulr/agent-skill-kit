#!/usr/bin/env python3
"""Fixture tests for scripts/skill_inventory.py."""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from skill_inventory import SkillInventory


def write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def skill(root: Path, rel: str, *, internal: bool = False, static_check: bool = True) -> None:
    metadata = "\nmetadata:\n  internal: true" if internal else ""
    write(
        root / rel / "SKILL.md",
        f"---\nname: {Path(rel).name}\ndescription: fixture\nlicense: MIT{metadata}\n---\n",
    )
    if static_check:
        write(root / rel / "evals" / "run-static-checks.sh", "#!/usr/bin/env bash\n")


def build_repo(root: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    write(root / ".gitignore", ".agents/skills/local-*\n")
    skill(root, "skills/alpha")
    skill(root, "skills/example-minimal", internal=True)
    skill(root, "skills/.experimental/exp")
    write(root / "skills/.experimental/.gitkeep")
    write(root / "skills/_shared/modes.md", "# shared\n")
    skill(root, ".agents/skills/reviewer")
    skill(root, ".agents/skills/local-clutter")


def names(paths: list[Path]) -> list[str]:
    return [path.name for path in paths]


def assert_equal(label: str, actual, expected) -> bool:
    if actual == expected:
        print(f"OK   {label}")
        return True
    print(f"FAIL {label}: expected {expected!r}, got {actual!r}", file=sys.stderr)
    return False


def main() -> int:
    failures = 0
    with tempfile.TemporaryDirectory(prefix="skill-inventory-") as tmp:
        root = Path(tmp).resolve()
        build_repo(root)
        inventory = SkillInventory(root)

        checks = [
            (
                "product lane excludes _shared and experimental",
                names(inventory.product_lane_skill_dirs()),
                ["alpha", "example-minimal"],
            ),
            (
                "catalog excludes internal templates",
                names(inventory.catalog_skill_dirs()),
                ["alpha"],
            ),
            (
                "experimental lane dirs are explicit",
                names(inventory.experimental_skill_dirs()),
                ["exp"],
            ),
            (
                "experimental lane entries ignore .gitkeep",
                names(inventory.experimental_lane_entries()),
                ["exp"],
            ),
            (
                "repo-local lane excludes gitignored clutter",
                names(inventory.repo_local_skill_dirs()),
                ["reviewer"],
            ),
            (
                "release dirs include product plus reserved lane",
                names(inventory.release_skill_dirs()),
                ["exp", "alpha", "example-minimal"],
            ),
            (
                "static check scripts span all install lanes",
                sorted(str(path.relative_to(root)) for path in inventory.static_check_scripts()),
                [
                    ".agents/skills/reviewer/evals/run-static-checks.sh",
                    "skills/.experimental/exp/evals/run-static-checks.sh",
                    "skills/alpha/evals/run-static-checks.sh",
                    "skills/example-minimal/evals/run-static-checks.sh",
                ],
            ),
        ]
        for label, actual, expected in checks:
            if not assert_equal(label, actual, expected):
                failures += 1

    if failures:
        print(f"skill-inventory tests failed with {failures} issue(s).", file=sys.stderr)
        return 1
    print("skill-inventory tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
