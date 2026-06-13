#!/usr/bin/env python3
"""Validate routing CSV structure and executable routing graphs."""
from __future__ import annotations

import sys
from pathlib import Path

from routing_graph import build_routing_graph
from skill_inventory import SkillInventory


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    inventory = SkillInventory(ROOT)
    checked = 0
    failures: list[str] = []
    for skill_dir in inventory.all_skill_dirs():
        graph = build_routing_graph(skill_dir)
        if not graph.csvs:
            continue
        for doc in graph.csvs:
            print(f"OK:   {doc.path.relative_to(ROOT)}")
            checked += 1
        for failure in graph.failures:
            failures.append(f"{skill_dir.relative_to(ROOT)}: {failure}")
    if checked == 0:
        print("OK:   no routing CSVs found to check")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        print("\nRouting-CSV checks FAILED.", file=sys.stderr)
        return 1
    print(f"All routing-CSV checks passed ({checked} CSV(s) verified).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
