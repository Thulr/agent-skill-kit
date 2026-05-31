#!/usr/bin/env python3
"""Fail the build on broken *relative* links in the repo's navigable docs.

Scope: top-level `*.md` (README, CHANGELOG, CONTRIBUTING, AGENTS, constitution,
SECURITY, THIRD_PARTY) + everything under `docs/`. These are the docs whose
links are meant to resolve *within this repo*, so a rename or move that orphans
a link should fail CI rather than rot silently (the failure mode the catalog's
own `docs` playbook calls out under "Broken-link CI").

Deliberately NOT in scope:
  - Skill content (`skills/**`): SKILL.md and references frequently link to a
    *consuming* repo's paths (e.g. `./docs/reflection-log/`, `./AGENTS.md`),
    which don't exist in this catalog. Skill-internal file integrity is covered
    by the per-skill registry checks + `check-shared-content.sh`.
  - Symlinked docs (`CLAUDE.md`, `.github/copilot-instructions.md` → AGENTS.md):
    checked once via the canonical target, not from the symlink's own dir.
  - `docs/superpowers/` (git-ignored local clutter).

External links (http/https/mailto/tel), pure `#anchors`, and obvious
placeholders (`<...>`, `path/to/...`) are skipped — this gate verifies that
relative paths point at files that exist, not that the wider web is up.

Run by `just check` and CI.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK_RE = re.compile(r"\]\(([^)]+)\)")
REF_RE = re.compile(r"^\s*\[[^\]]+\]:\s+(\S+)", re.MULTILINE)


def in_scope(path: str) -> bool:
    if path.startswith("docs/superpowers/"):
        return False
    if "/" not in path:  # top-level *.md
        return True
    return path.startswith("docs/")


def link_targets(text: str):
    for m in LINK_RE.finditer(text):
        yield m.group(1)
    for m in REF_RE.finditer(text):
        yield m.group(1)


def main() -> int:
    os.chdir(ROOT)
    md_files = subprocess.run(
        ["git", "ls-files", "*.md"], capture_output=True, text=True, check=True
    ).stdout.split()

    broken, checked = [], 0
    for md in md_files:
        if not in_scope(md) or os.path.islink(md):
            continue
        d = os.path.dirname(md)
        with open(md, encoding="utf-8") as fh:
            text = fh.read()
        for raw in link_targets(text):
            tgt = raw.strip()
            if tgt.startswith(("http://", "https://", "mailto:", "tel:", "#", "<")):
                continue
            tgt = tgt.split()[0].split("#")[0]  # drop optional "title" and #anchor
            if not tgt or "<" in tgt or "path/to" in tgt:
                continue
            checked += 1
            base = ROOT if tgt.startswith("/") else os.path.join(ROOT, d)
            resolved = os.path.normpath(os.path.join(base, tgt.lstrip("/")))
            if not os.path.exists(resolved):
                broken.append((md, raw.strip()))

    if broken:
        print(f"FAIL: {len(broken)} broken relative link(s) in repo docs:", file=sys.stderr)
        for md, tgt in broken:
            print(f"  {md} -> {tgt}", file=sys.stderr)
        print("\nFix the path, or — if the target intentionally lives in a "
              "consuming repo — make it a non-relative reference.", file=sys.stderr)
        return 1

    print(f"All doc links resolve ({checked} relative link(s) checked across "
          f"top-level + docs/).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
