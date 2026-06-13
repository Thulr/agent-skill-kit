#!/usr/bin/env python3
"""Check that skills consume `skills/_shared/**` through relative symlinks."""
from __future__ import annotations

import sys
from pathlib import Path

from skill_inventory import SkillInventory


ROOT = Path(__file__).resolve().parents[1]
SHARED_DIR = ROOT / "skills" / "_shared"


def fail(failures: list[str], message: str) -> None:
    failures.append(message)
    print(f"FAIL: {message}", file=sys.stderr)


def check_shared_symlink(
    candidate: Path,
    expected_basename: str,
    checked: set[Path],
    failures: list[str],
) -> None:
    if candidate in checked:
        return
    checked.add(candidate)
    rel = candidate.relative_to(ROOT).as_posix()
    if not candidate.is_symlink():
        fail(
            failures,
            f"{rel} exists as a regular file but a shared file is its canonical source",
        )
        return
    if not candidate.exists():
        fail(failures, f"{rel} is a symlink to {candidate.readlink()!s} which does not resolve")
        return
    target = candidate.readlink()
    if target.is_absolute():
        fail(failures, f"{rel} is an absolute symlink ({target}) — must be relative")
        return
    resolved = candidate.resolve()
    if not resolved.is_relative_to(SHARED_DIR.resolve()):
        fail(failures, f"{rel} resolves to {resolved} which is outside skills/_shared/")
        return
    if resolved.name != expected_basename:
        fail(
            failures,
            f"{rel} points at {resolved.relative_to(ROOT)} but basename does not match {expected_basename}",
        )
        return
    print(f"OK:   {rel} -> {target}")


def main() -> int:
    if not SHARED_DIR.is_dir():
        print("OK:   no skills/_shared/ yet — nothing to check")
        return 0
    shared_files = sorted(path for path in SHARED_DIR.rglob("*") if path.is_file())
    if not shared_files:
        print("OK:   skills/_shared/ exists but contains no shared files yet")
        return 0

    top_level_shared_md = sorted(path for path in SHARED_DIR.glob("*.md") if path.is_file())
    inventory = SkillInventory(ROOT)
    checked: set[Path] = set()
    failures: list[str] = []

    for skill_dir in inventory.all_skill_dirs():
        if not (skill_dir / "SKILL.md").is_file():
            continue
        refs_dir = skill_dir / "references"
        if refs_dir.is_dir():
            for shared_file in top_level_shared_md:
                candidate = refs_dir / shared_file.name
                if candidate.exists() or candidate.is_symlink():
                    check_shared_symlink(candidate, shared_file.name, checked, failures)
        for symlink in sorted(path for path in skill_dir.rglob("*") if path.is_symlink()):
            resolved = symlink.resolve()
            if resolved.is_relative_to(SHARED_DIR.resolve()):
                check_shared_symlink(symlink, resolved.name, checked, failures)

    if not checked:
        print(
            "OK:   no skill currently references any shared file "
            f"(consider why skills/_shared/ has {len(shared_files)} file(s) but no consumers)"
        )
    if failures:
        print("\nShared-content checks FAILED.", file=sys.stderr)
        return 1
    print(f"All shared-content checks passed ({len(checked)} symlink(s) verified).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
