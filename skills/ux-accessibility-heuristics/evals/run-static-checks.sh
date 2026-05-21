#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(git -C "$script_dir" rev-parse --show-toplevel)"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"
skill_json="$skill_dir/skill.json"
registry="$skill_dir/references/use-case-registry.csv"
playbook_dir="$skill_dir/references/playbooks"

failures=0

fail() {
  printf 'FAIL %s\n' "$1" >&2
  failures=$((failures + 1))
}

check_file() {
  [[ -f "$1" || -L "$1" ]] || fail "missing file: $1"
}

check_pattern() {
  local label="$1" pattern="$2" path="$3"
  grep -Eq -- "$pattern" "$path" || fail "$label: pattern not found in $path"
}

check_file "$skill_md"
check_file "$skill_json"
check_file "$registry"
check_file "$skill_dir/references/core/severity-rubric.md"
check_file "$skill_dir/references/trackable-findings.md"
check_file "$skill_dir/templates/audit-report.md"
check_file "$skill_dir/templates/findings-ledger.md"
check_file "$skill_dir/templates/workflow-state.json"
check_file "$skill_dir/evals/activation-cases.md"
check_file "$skill_dir/evals/trigger-evals.json"

if [[ -f "$skill_json" ]]; then
  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/skill.schema.json" "$skill_json" \
    || fail "skill.json: schema validation failed"
  name=$(jq -r '.name' "$skill_json")
  [[ "$name" == "ux-accessibility-heuristics" ]] || fail "skill.json name mismatch: $name"
  status=$(jq -r '.status' "$skill_json")
  [[ "$status" == "published" ]] || fail "skill.json status must be published, got $status"
fi

if [[ -f "$skill_md" ]]; then
  check_pattern 'frontmatter name' '^name:[[:space:]]*ux-accessibility-heuristics$' "$skill_md"
  check_pattern 'frontmatter license' '^license:' "$skill_md"
  check_pattern 'bare activation' 'use-case menu' "$skill_md"
  check_pattern 'registry routing' 'use-case-registry\.csv' "$skill_md"
  check_pattern 'tracking state' 'Create tracking state' "$skill_md"
  wc=$(wc -w < "$skill_md")
  (( wc < 800 )) || fail "SKILL.md word count $wc exceeds 800"
fi

if [[ -f "$registry" ]]; then
  rows=$(grep -cE '^(usability-audit|accessibility-audit|form-review|navigation-review|error-recovery),' "$registry")
  (( rows == 5 )) || fail "use-case-registry.csv: expected 5 data rows, got $rows"
  while IFS='|' read -r details templates; do
    IFS=';' read -ra dparts <<< "$details"
    for p in "${dparts[@]}"; do
      [[ -z "$p" ]] && continue
      [[ -f "$skill_dir/$p" || -L "$skill_dir/$p" ]] || fail "registry references missing detail file: $p"
    done
    IFS=';' read -ra tparts <<< "$templates"
    for p in "${tparts[@]}"; do
      [[ -z "$p" ]] && continue
      [[ -f "$skill_dir/$p" || -L "$skill_dir/$p" ]] || fail "registry references missing template: $p"
    done
  done < <(python3 - "$registry" <<'PYEOF'
import csv, sys
with open(sys.argv[1], newline='') as f:
    for row in csv.DictReader(f):
        print(f"{row.get('detail_files','').strip()}|{row.get('templates','').strip()}")
PYEOF
)
fi

for pb in "$playbook_dir"/*.md; do
  [[ -f "$pb" ]] || continue
  for section in '^## Scope' '^## Grounding' '^## Good signals' '^## Common failures' '^## Heuristics' '^## Quick diagnostic' '^## Cross-references'; do
    grep -Eq -- "$section" "$pb" || fail "$(basename "$pb") missing section ${section#^## }"
  done
  wc=$(wc -w < "$pb")
  if (( wc < 250 || wc > 1200 )); then
    fail "$(basename "$pb") word count $wc outside 250-1200"
  fi
done

if [[ -f "$skill_json" ]]; then
  valid=" usability-audit accessibility-audit form-review navigation-review error-recovery "
  while IFS= read -r p; do
    [[ -z "$p" ]] && continue
    [[ "$valid" == *" $p "* ]] || fail "skill.json inspired_by.playbooks has unknown value: $p"
  done < <(jq -r '.inspired_by[].playbooks[]?' "$skill_json")
fi

if [[ -f "$skill_dir/evals/trigger-evals.json" ]]; then
  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/trigger-evals.schema.json" "$skill_dir/evals/trigger-evals.json" \
    || fail "trigger-evals.json: schema validation failed"
  trigger_skill=$(jq -r '.skill' "$skill_dir/evals/trigger-evals.json")
  [[ "$trigger_skill" == "ux-accessibility-heuristics" ]] || fail "trigger-evals.json skill mismatch: $trigger_skill"
fi

if (( failures > 0 )); then
  printf '\nux-accessibility-heuristics static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'ux-accessibility-heuristics static eval passed.\n'
