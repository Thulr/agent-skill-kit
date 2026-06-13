#!/usr/bin/env python3
"""Run every per-skill static-check adapter from the shared skill inventory."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from skill_inventory import SkillInventory


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    inventory = SkillInventory(ROOT)
    scripts = inventory.static_check_scripts()
    if not scripts:
        print("OK:   no skill static-check scripts found")
        return 0

    failed = False
    github_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    for script in scripts:
        rel = script.relative_to(ROOT).as_posix()
        if github_actions:
            print(f"::group::{rel}")
        else:
            print(f"running {rel}")
        proc = subprocess.run(["bash", str(script)], cwd=ROOT)
        if proc.returncode != 0:
            failed = True
        if github_actions:
            print("::endgroup::")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
