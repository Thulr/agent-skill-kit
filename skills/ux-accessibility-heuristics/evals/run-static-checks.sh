#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"
skill_json="$skill_dir/skill.json"
router="$skill_dir/references/intent-router.csv"
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
check_file "$router"
check_file "$skill_dir/references/core/severity-rubric.md"
check_file "$skill_dir/references/trackable-findings.md"
check_file "$skill_dir/templates/audit-report.md"
check_file "$skill_dir/templates/findings-ledger.md"
check_file "$skill_dir/templates/workflow-state.json"
check_file "$skill_dir/evals/activation-cases.md"
check_file "$skill_dir/evals/trigger-evals.json"

validate_skill_json_contract "$repo_root" "$skill_json" "ux-accessibility-heuristics"
if [[ -f "$skill_json" ]]; then
  status=$(jq -r '.status' "$skill_json")
  [[ "$status" == "published" ]] || fail "skill.json status must be published, got $status"
fi

if [[ -f "$skill_md" ]]; then
  check_pattern 'frontmatter name' '^name:[[:space:]]*ux-accessibility-heuristics$' "$skill_md"
  check_pattern 'frontmatter license' '^license:' "$skill_md"
  check_pattern 'bare activation' 'intent menu' "$skill_md"
  check_pattern 'router routing' 'intent-router\.csv' "$skill_md"
  check_pattern 'tracking state' 'Create tracking state' "$skill_md"
  wc=$(wc -w < "$skill_md")
  (( wc < 800 )) || fail "SKILL.md word count $wc exceeds 800"
fi

if [[ -f "$router" ]]; then
  rows=$(grep -cE '^(usability-audit|accessibility-audit|form-review|navigation-review|error-recovery),' "$router")
  (( rows == 5 )) || fail "intent-router.csv: expected 5 data rows, got $rows"
  while IFS='|' read -r details templates; do
    IFS=';' read -ra dparts <<< "$details"
    for p in "${dparts[@]}"; do
      [[ -z "$p" ]] && continue
      [[ -f "$skill_dir/$p" || -L "$skill_dir/$p" ]] || fail "router references missing detail file: $p"
    done
    IFS=';' read -ra tparts <<< "$templates"
    for p in "${tparts[@]}"; do
      [[ -z "$p" ]] && continue
      [[ -f "$skill_dir/$p" || -L "$skill_dir/$p" ]] || fail "router references missing template: $p"
    done
  done < <(python3 - "$router" <<'PYEOF'
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

validate_trigger_evals_contract "$repo_root" "$skill_dir/evals/trigger-evals.json" "ux-accessibility-heuristics"

if (( failures > 0 )); then
  printf '\nux-accessibility-heuristics static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'ux-accessibility-heuristics static eval passed.\n'
