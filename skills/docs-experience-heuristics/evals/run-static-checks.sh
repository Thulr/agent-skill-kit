#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"
skill_json="$skill_dir/skill.json"
intent_router="$skill_dir/references/intent-router.csv"
playbook_dir="$skill_dir/references/playbooks"

failures=0

fail() {
  printf 'FAIL %s\n' "$1" >&2
  failures=$((failures + 1))
}

check_file() {
  [[ -f "$1" ]] || fail "missing file: $1"
}

check_pattern() {
  local label="$1" pattern="$2" path="$3"
  grep -Eq -- "$pattern" "$path" || fail "$label: pattern not found in $path"
}

# ----- File presence -----

check_file "$skill_md"
check_file "$skill_json"
check_file "$intent_router"
check_file "$skill_dir/references/intents/audit.csv"
check_file "$skill_dir/references/intents/design.csv"
check_file "$skill_dir/references/intents/debug.csv"
check_file "$skill_dir/references/intents/measure.csv"
check_file "$skill_dir/references/core/severity-rubric.md"
check_file "$skill_dir/references/core/score-rubric.md"
check_file "$skill_dir/references/core/personas.md"
check_file "$skill_dir/references/core/audience-matrix.md"
check_file "$skill_dir/references/subagent-dispatch.md"
check_file "$skill_dir/references/starter-scenarios.csv"
check_file "$skill_dir/templates/audit-report.md"
check_file "$skill_dir/templates/design-doc.md"
check_file "$skill_dir/templates/debug-runbook.md"
check_file "$skill_dir/templates/measurement-plan.md"

# ----- skill.json gates -----

validate_skill_json_contract "$repo_root" "$skill_json" "docs-experience-heuristics"

# ----- SKILL.md cleanliness (source-safety) -----

author_stoplist=" Foundation Council Parliament Committee Group Working contributors Initiative Consortium Anthropic Stripe Cloudflare "

if [[ -f "$skill_md" && -f "$skill_json" ]]; then
  while IFS= read -r author; do
    [[ -n "$author" ]] || continue
    last="${author##* }"
    if [[ "$author_stoplist" == *" $last "* ]] || [[ "$author" == "$last" ]]; then
      if grep -qF -- "$author" "$skill_md"; then
        fail "SKILL.md leaks source author: $author (from inspired_by)"
      fi
    else
      if grep -qw -- "$last" "$skill_md"; then
        fail "SKILL.md leaks source author last name: $last (from inspired_by)"
      fi
    fi
  done < <(jq -r '.inspired_by[].author' "$skill_json")
  while IFS= read -r title; do
    [[ -n "$title" ]] || continue
    if grep -qF -- "$title" "$skill_md"; then
      fail "SKILL.md leaks source title: $title (from inspired_by)"
    fi
  done < <(jq -r '.inspired_by[].name' "$skill_json")
  wc=$(wc -w < "$skill_md")
  (( wc < 800 )) || fail "SKILL.md word count $wc exceeds 800 (runtime-only bound)"
fi

# ----- SKILL.md structural gates -----

if [[ -f "$skill_md" ]]; then
  check_pattern 'frontmatter name' '^name:[[:space:]]*docs-experience-heuristics$' "$skill_md"
  check_pattern 'frontmatter license' '^license:' "$skill_md"
  check_pattern 'intent-router routing' 'intent-router\.csv' "$skill_md"
  check_pattern 'bare activation' 'show the intent menu' "$skill_md"
  check_pattern 'subagent dispatch section' '^## Subagent dispatch' "$skill_md"
  check_pattern 'four lenses' 'four lenses' "$skill_md"
  check_pattern 'audience conflict rule' 'audience-conflicts\.md' "$skill_md"
fi

# ----- Registry, playbook, template, and inspired_by integrity -----

if ! python3 - "$skill_dir" <<'PYEOF'
import csv
import json
import re
import sys
from pathlib import Path

skill_dir = Path(sys.argv[1])
failures = []

required_sections = [
    "## Scope",
    "## Grounding",
    "## Good signals",
    "## Common failures",
    "## Heuristics",
    "## Quick diagnostic",
    "## Cross-references",
]
expected_intents = {"audit", "design", "debug", "measure"}

router = skill_dir / "references" / "intent-router.csv"
try:
    router_rows = list(csv.DictReader(router.open(newline="")))
except Exception as exc:
    failures.append(f"intent-router.csv could not be read: {exc}")
    router_rows = []

intents = {row.get("intent", "") for row in router_rows}
if intents != expected_intents:
    failures.append(f"intent-router.csv intents must be {sorted(expected_intents)}, got {sorted(intents)}")

referenced_playbooks = set()
valid_surfaces = set()

for row in router_rows:
    intent = (row.get("intent") or "").strip()
    registry = skill_dir / (row.get("registry_file") or "")
    template = skill_dir / (row.get("default_template") or "")
    if not registry.is_file():
        failures.append(f"intent {intent} references missing registry: {registry}")
        continue
    if not template.is_file():
        failures.append(f"intent {intent} references missing template: {template}")
    rows = list(csv.DictReader(registry.open(newline="")))
    if len(rows) < 3:
        failures.append(f"{registry.relative_to(skill_dir)} has only {len(rows)} rows; need >=3")
    signatures = set()
    for r in rows:
        surface = (r.get("surface") or "").strip()
        if not surface:
            failures.append(f"{registry.relative_to(skill_dir)} has row without surface")
        valid_surfaces.add(surface)
        signature = tuple(sorted((r.get(k) or "") for k in ("playbook", "core_refs")))
        signatures.add(signature)
        for piece in (r.get("playbook") or "").split(";"):
            piece = piece.strip()
            if not piece:
                continue
            path = skill_dir / piece
            if not path.is_file():
                failures.append(f"{registry.relative_to(skill_dir)} references missing playbook: {piece}")
            else:
                referenced_playbooks.add(path.stem)
        for piece in (r.get("core_refs") or "").split(";"):
            piece = piece.strip()
            if piece and not (skill_dir / piece).is_file():
                failures.append(f"{registry.relative_to(skill_dir)} references missing core_ref: {piece}")
    if len(rows) > 1 and len(signatures) == 1:
        failures.append(f"{registry.relative_to(skill_dir)} rows load identical playbook/core_refs signatures")

pb_dir = skill_dir / "references" / "playbooks"
playbooks_on_disk = {p.stem for p in pb_dir.glob("*.md")}
if not playbooks_on_disk:
    failures.append("no playbooks found")

for pb in sorted(pb_dir.glob("*.md")):
    text = pb.read_text()
    for section in required_sections:
        if section not in text:
            failures.append(f"{pb.name} missing section {section}")
    words = len(text.split())
    if words < 400 or words > 1500:
        failures.append(f"{pb.name} word count {words} outside 400-1500")
    m = re.search(r"## Heuristics\n(.*?)(?:\n## |\Z)", text, re.S)
    if not m or not re.search(r"\((audit|design|debug|measure)", m.group(1)):
        failures.append(f"{pb.name}: heuristics lack intent tags")

for orphan in sorted(playbooks_on_disk - referenced_playbooks):
    failures.append(f"playbook {orphan}.md is not referenced by any intent CSV")

valid_slugs = playbooks_on_disk | expected_intents | {f"{i}-intent" for i in expected_intents} | {"all"}
try:
    data = json.loads((skill_dir / "skill.json").read_text())
    for idx, entry in enumerate(data.get("inspired_by", [])):
        for slug in entry.get("playbooks", []):
            if slug not in valid_slugs:
                failures.append(f"skill.json inspired_by[{idx}].playbooks has unknown value: {slug}")
except Exception as exc:
    failures.append(f"skill.json inspired_by slug check failed: {exc}")

for failure in failures:
    print(f"FAIL {failure}", file=sys.stderr)

sys.exit(1 if failures else 0)
PYEOF
then
  fail "registry/playbook/template integrity failed"
fi

# ----- trigger-evals.json schema gate -----

trigger_evals="$skill_dir/evals/trigger-evals.json"
validate_trigger_evals_contract "$repo_root" "$trigger_evals" "docs-experience-heuristics"

# ----- Result -----

if (( failures > 0 )); then
  printf '\ndocs-experience-heuristics static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'docs-experience-heuristics static eval passed.\n'
