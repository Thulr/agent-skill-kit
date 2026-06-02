#!/usr/bin/env python3
"""Generate the README "Pick a skill" + "Catalog" sections from a single source.

Source of truth:
  - each published skill.json's `metadata.{family,function,catalog_order,catalog_summary}`
  - catalog/catalog.json (family-level prose + the routing matrix)

The two README sections live between sentinel markers and are *generated*, never
hand-edited. This is the same anti-drift discipline as the instruction-surface
and shared-content symlink checks (W8): one source, mechanically enforced.

Usage:
  python3 scripts/build-catalog.py            # --check (default): fail if README is stale
  python3 scripts/build-catalog.py --check    #   same
  python3 scripts/build-catalog.py --write     # regenerate the marked sections in README

Run by `just check` and CI in --check mode.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CATALOG = ROOT / "catalog" / "catalog.json"

FAMILIES = ("heuristics", "research", "ax")
FUNCTIONS = ("critique", "design", "singleton")
REQUIRED_META = ("family", "function", "catalog_summary")

INTERNAL_RE = re.compile(
    r"(?m)^metadata:\s*\n(?:^[ \t]+[^\n]*\n)*^[ \t]+internal:\s*true\s*$"
)
BACKTICK_RE = re.compile(r"`([^`]+)`")


def fail(failures: list[str], message: str) -> None:
    failures.append(message)
    print(f"FAIL {message}", file=sys.stderr)


def is_internal(skill_dir: Path) -> bool:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False
    return bool(INTERNAL_RE.search(skill_md.read_text()))


def _git_ignored(paths: list[Path]) -> set[Path]:
    """Subset of `paths` that git ignores (local clutter is not a release
    artifact). No-op on a clean CI checkout. Mirrors check-release-contract.py."""
    if not paths:
        return set()
    by_str = {str(p): p for p in paths}
    try:
        proc = subprocess.run(
            ["git", "check-ignore", "--stdin"],
            cwd=ROOT, text=True, capture_output=True, input="\n".join(by_str),
        )
    except OSError:
        return set()
    if proc.returncode not in (0, 1):
        return set()
    return {by_str[line] for line in proc.stdout.splitlines() if line in by_str}


def public_skills(failures: list[str]) -> dict[str, dict]:
    """name -> metadata dict, for every published (non-internal) skill in the
    skills/ lane. The catalog covers this lane only; .agents/ is repo-local
    tooling and skills/.experimental/ is reserved-empty."""
    dirs = [
        p for p in (ROOT / "skills").iterdir()
        if p.is_dir() and p.name not in {"_shared", ".experimental"}
    ]
    ignored = _git_ignored(dirs)
    skills: dict[str, dict] = {}
    for d in sorted(p for p in dirs if p not in ignored):
        if is_internal(d):
            continue
        manifest = d / "skill.json"
        if not manifest.exists():
            fail(failures, f"{d.name}: missing skill.json")
            continue
        data = json.loads(manifest.read_text())
        meta = data.get("metadata", {})
        name = data.get("name", d.name)
        for key in REQUIRED_META:
            if not meta.get(key):
                fail(failures, f"{name}: skill.json metadata.{key} is required "
                               f"for the catalog but is missing/empty")
        if meta.get("family") and meta["family"] not in FAMILIES:
            fail(failures, f"{name}: metadata.family {meta['family']!r} not one "
                           f"of {FAMILIES}")
        if meta.get("function") and meta["function"] not in FUNCTIONS:
            fail(failures, f"{name}: metadata.function {meta['function']!r} not "
                           f"one of {FUNCTIONS}")
        skills[name] = meta
    return skills


def sort_key(item: tuple[str, dict]):
    name, meta = item
    return (meta.get("catalog_order", 10**6), name)


def render_bullet(name: str, meta: dict) -> str:
    fn = meta.get("function")
    summary = meta.get("catalog_summary", "")
    tag = f" *({fn})*" if fn in ("critique", "design") else ""
    return f"- **`{name}`**{tag} — {summary}"


def render_table(columns: list[str], rows: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return out


def render_pick_a_skill(cat: dict) -> str:
    p = cat["pick_a_skill"]
    lines = ["## Pick a skill", "", p["intro"], ""]
    primary = p["primary"]
    lines += render_table(primary["columns"],
                          [[r["surface"], r["critique"], r["design"]]
                           for r in primary["rows"]])
    sec = p["secondary"]
    lines += ["", sec["lead"], ""]
    lines += render_table(sec["columns"],
                          [[r["need"], r["skill"]] for r in sec["rows"]])
    lines += [""] + p["unsure"]
    return "\n".join(lines)


def render_catalog(cat: dict, skills: dict[str, dict]) -> str:
    c = cat["catalog"]
    lines = ["## Catalog", "", c["lead_in"]]
    for fam in c["families"]:
        lines += ["", f"### {fam['title']}"]
        if fam.get("intro"):
            lines += [""] + fam["intro"]
        members = sorted(
            ((n, m) for n, m in skills.items() if m.get("family") == fam["id"]),
            key=sort_key,
        )
        if members:
            lines.append("")
            lines += [render_bullet(n, m) for n, m in members]
    return "\n".join(lines)


def matrix_skill_refs(cat: dict) -> set[str]:
    refs: set[str] = set()
    p = cat["pick_a_skill"]
    cells = []
    for r in p["primary"]["rows"]:
        cells += [r["critique"], r["design"]]
    for r in p["secondary"]["rows"]:
        cells.append(r["skill"])
    for cell in cells:
        refs.update(BACKTICK_RE.findall(cell))
    return refs


def replace_block(text: str, marker: str, body: str, failures: list[str]) -> str:
    begin = f"<!-- BEGIN GENERATED: {marker} (scripts/build-catalog.py) -->"
    end = f"<!-- END GENERATED: {marker} -->"
    pattern = re.compile(
        re.escape(begin) + r"\n.*?\n" + re.escape(end), re.DOTALL
    )
    if not pattern.search(text):
        fail(failures, f"README.md is missing the '{marker}' generated markers "
                       f"({begin} ... {end})")
        return text
    return pattern.sub(begin + "\n" + body + "\n" + end, text)


def extract_block(text: str, marker: str) -> str | None:
    begin = f"<!-- BEGIN GENERATED: {marker} (scripts/build-catalog.py) -->"
    end = f"<!-- END GENERATED: {marker} -->"
    m = re.search(re.escape(begin) + r"\n(.*?)\n" + re.escape(end), text, re.DOTALL)
    return m.group(1) if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="fail if README is stale (default)")
    g.add_argument("--write", action="store_true", help="regenerate the README sections")
    args = ap.parse_args()
    write = args.write

    failures: list[str] = []
    cat = json.loads(CATALOG.read_text())
    skills = public_skills(failures)

    # cross-check: every skill named in the routing matrix exists
    known = set(skills)
    for ref in sorted(matrix_skill_refs(cat)):
        if ref not in known:
            fail(failures, f"catalog/catalog.json matrix references unknown skill "
                           f"`{ref}` (not a published skill)")
    # cross-check: every catalog family has at least one skill
    for fam in cat["catalog"]["families"]:
        if not any(m.get("family") == fam["id"] for m in skills.values()):
            fail(failures, f"catalog family {fam['id']!r} has no skills")

    if failures:
        print(f"\nbuild-catalog: {len(failures)} validation failure(s).", file=sys.stderr)
        return 1

    pick = render_pick_a_skill(cat)
    catalog = render_catalog(cat, skills)

    text = README.read_text()
    new_text = replace_block(text, "pick-a-skill", pick, failures)
    new_text = replace_block(new_text, "catalog", catalog, failures)
    if failures:
        return 1

    if write:
        if new_text != text:
            README.write_text(new_text)
            print("build-catalog: README.md regenerated.")
        else:
            print("build-catalog: README.md already up to date.")
        return 0

    # --check (default)
    stale = []
    for marker, body in (("pick-a-skill", pick), ("catalog", catalog)):
        current = extract_block(text, marker)
        if current != body:
            stale.append(marker)
    if stale:
        print(f"FAIL build-catalog: README sections out of date: {', '.join(stale)}",
              file=sys.stderr)
        print("      fix: python3 scripts/build-catalog.py --write", file=sys.stderr)
        return 1
    print(f"OK:   README catalog is in sync with skill.json + catalog/catalog.json "
          f"({len(skills)} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
