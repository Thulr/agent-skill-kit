#!/usr/bin/env bash
set -euo pipefail

skill_dir="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"
skill_json="$skill_dir/skill.json"
intent_router="$skill_dir/references/intent-router.csv"

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
check_file "$skill_dir/references/intents/edge-pass.csv"
check_file "$skill_dir/references/core/severity-rubric.md"
check_file "$skill_dir/references/core/score-rubric.md"
check_file "$skill_dir/references/core/personas.md"
check_file "$skill_dir/templates/audit-report.md"
check_file "$skill_dir/templates/design-doc.md"
check_file "$skill_dir/templates/debug-runbook.md"
check_file "$skill_dir/templates/edge-checklist.md"

# ----- skill.json gates -----

if [[ -f "$skill_json" ]]; then
  jq . "$skill_json" > /dev/null 2>&1 || fail "skill.json: invalid JSON"
  name=$(jq -r '.name' "$skill_json")
  [[ "$name" == "dx-heuristics" ]] || fail "skill.json: name must be dx-heuristics, got $name"
  status=$(jq -r '.status' "$skill_json")
  case "$status" in
    draft|reviewed|published) ;;
    *) fail "skill.json: status must be draft/reviewed/published, got $status" ;;
  esac
  count=$(jq '.inspired_by | length' "$skill_json")
  (( count > 0 )) || fail "skill.json: inspired_by must be non-empty"
  missing=$(jq -r '.inspired_by | map(select(.name == null or .author == null or .kind == null or .contribution == null)) | length' "$skill_json")
  (( missing == 0 )) || fail "skill.json: $missing inspired_by entry/entries missing required fields"
fi

# ----- SKILL.md cleanliness (source-safety) -----

if [[ -f "$skill_md" ]] && [[ -f "$skill_json" ]]; then
  while IFS= read -r author; do
    last="${author##* }"
    if grep -q "$last" "$skill_md"; then
      fail "SKILL.md leaks source author: $last (from inspired_by)"
    fi
  done < <(jq -r '.inspired_by[].author' "$skill_json")
  while IFS= read -r title; do
    if grep -qF "$title" "$skill_md"; then
      fail "SKILL.md leaks source title: $title (from inspired_by)"
    fi
  done < <(jq -r '.inspired_by[].name' "$skill_json")
  wc=$(wc -w < "$skill_md")
  (( wc < 800 )) || fail "SKILL.md word count $wc exceeds 800 (runtime-only bound)"
fi

# ----- SKILL.md structural gates -----

if [[ -f "$skill_md" ]]; then
  check_pattern 'frontmatter name' '^name:[[:space:]]*dx-heuristics$' "$skill_md"
  check_pattern 'frontmatter license' '^license:' "$skill_md"
  check_pattern 'intent-router routing' 'intent-router\.csv' "$skill_md"
  check_pattern 'bare activation' 'show the intent menu' "$skill_md"
fi

# ----- Intent router structure -----

if [[ -f "$intent_router" ]]; then
  # Robust row count: count data rows by intent prefixes (ignores trailing newline issues)
  rows=$(grep -cE '^(audit|design|debug|edge-pass),' "$intent_router")
  (( rows == 4 )) || fail "intent-router.csv: expected 4 data rows, got $rows"
  check_pattern 'audit intent' '^audit,' "$intent_router"
  check_pattern 'design intent' '^design,' "$intent_router"
  check_pattern 'debug intent' '^debug,' "$intent_router"
  check_pattern 'edge-pass intent' '^edge-pass,' "$intent_router"
fi

# ----- cli playbook gates (vertical slice) -----

cli_pb="$skill_dir/references/playbooks/cli.md"
if [[ -f "$cli_pb" ]]; then
  for section in '^# CLI Playbook' '^## Scope' '^## Grounding' \
                 '^## Good signals' '^## Common failures' '^## Heuristics' \
                 '^## Quick diagnostic' '^## Cross-references'; do
    check_pattern "cli.md section ${section#^## }" "$section" "$cli_pb"
  done
  wc=$(wc -w < "$cli_pb")
  (( wc >= 400 && wc <= 1500 )) || fail "cli.md word count $wc outside 400-1500"
else
  fail "missing file: $cli_pb"
fi

# ----- All playbook gates -----

playbook_dir="$skill_dir/references/playbooks"
expected_playbooks=(api sdk cli docs errors setup inner-loop contributor auth migration plugin ide perf telemetry)

for surface in "${expected_playbooks[@]}"; do
  pb="$playbook_dir/$surface.md"
  if [[ ! -f "$pb" ]]; then
    fail "missing playbook: $pb"
    continue
  fi
  for section in '^## Scope' '^## Grounding' '^## Good signals' \
                 '^## Common failures' '^## Heuristics' \
                 '^## Quick diagnostic' '^## Cross-references'; do
    grep -Eq -- "$section" "$pb" || fail "$surface.md missing section ${section#^## }"
  done
  # Heuristics section must tag at least one intent
  awk -v surface="$surface" '
    /^## Heuristics/{f=1;next}
    /^## /{f=0}
    f && /\((audit|design|debug)/{found=1}
    END{ if(!found) exit 1 }
  ' "$pb" || fail "$surface.md: # Heuristics has no intent tags like (audit), (design), or (debug)"
  # Word count
  wc=$(wc -w < "$pb")
  if (( wc < 400 || wc > 1500 )); then
    fail "$surface.md word count $wc outside 400-1500"
  fi
done

# ----- Registry integrity -----

for intent in audit design debug edge-pass; do
  csv="$skill_dir/references/intents/$intent.csv"
  [[ -f "$csv" ]] || { fail "missing intent CSV: $csv"; continue; }
  # Use Python csv module to correctly handle quoted fields with embedded commas
  while IFS='|' read -r pb refs; do
    # Check playbook column (semicolon-separated paths)
    IFS=';' read -ra parts <<< "$pb"
    for p in "${parts[@]}"; do
      full="$skill_dir/$p"
      [[ -f "$full" ]] || fail "$intent.csv references missing playbook: $p"
    done
    # Check core_refs column (semicolon-separated paths)
    IFS=';' read -ra rparts <<< "$refs"
    for r in "${rparts[@]}"; do
      full="$skill_dir/$r"
      [[ -f "$full" ]] || fail "$intent.csv references missing core_ref: $r"
    done
  done < <(python3 - "$csv" <<'PYEOF'
import csv, sys
with open(sys.argv[1], newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pb = row.get('playbook', '').strip()
        refs = row.get('core_refs', '').strip()
        print(f"{pb}|{refs}")
PYEOF
)
done

# ----- skill.json playbooks-field gate -----

if [[ -f "$skill_json" ]]; then
  valid_markers=" audit-intent design-intent debug-intent edge-pass-intent all "
  valid_surfaces=" api sdk cli docs errors setup inner-loop contributor auth migration plugin ide perf telemetry "
  while IFS= read -r p; do
    if [[ "$valid_surfaces" == *" $p "* ]] || [[ "$valid_markers" == *" $p "* ]]; then
      continue
    fi
    fail "skill.json inspired_by.playbooks has unknown value: $p"
  done < <(jq -r '.inspired_by[].playbooks[]' "$skill_json")
fi

# ----- Result -----

if (( failures > 0 )); then
  printf '\ndx-heuristics static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'dx-heuristics static eval passed.\n'
