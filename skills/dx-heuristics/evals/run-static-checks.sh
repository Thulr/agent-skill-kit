#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(git -C "$script_dir" rev-parse --show-toplevel)"
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
check_file "$skill_dir/references/intents/edge-pass.csv"
check_file "$skill_dir/references/core/severity-rubric.md"
check_file "$skill_dir/references/core/score-rubric.md"
check_file "$skill_dir/references/core/personas.md"
check_file "$skill_dir/templates/audit-report.md"
check_file "$skill_dir/templates/design-doc.md"
check_file "$skill_dir/templates/debug-runbook.md"
check_file "$skill_dir/templates/edge-checklist.md"

# ----- Discover playbooks (source of truth) -----
# Auto-deriving from the playbook directory means adding a new surface is
# just: drop a playbook file + add CSV rows. No script edits.

all_surfaces=""
if [[ -d "$playbook_dir" ]]; then
  for pb in "$playbook_dir"/*.md; do
    [[ -f "$pb" ]] || continue
    all_surfaces+="$(basename "$pb" .md) "
  done
fi

valid_surfaces=" "
for s in $all_surfaces; do
  valid_surfaces+="$s "
done

# Derive intent markers (intent + "-intent" suffix, plus "all") from the router
valid_markers=" all "
if [[ -f "$intent_router" ]]; then
  while IFS=, read -r intent _; do
    [[ "$intent" == "intent" ]] && continue
    [[ -z "$intent" ]] && continue
    valid_markers+="${intent}-intent "
  done < "$intent_router"
fi

# ----- skill.json gates -----
# Shape is enforced by the canonical schema (schemas/skill.schema.json +
# scripts/validate-against-schema.py). Per-skill assertions stay here.

if [[ -f "$skill_json" ]]; then
  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/skill.schema.json" "$skill_json" \
    || fail "skill.json: schema validation failed (schemas/skill.schema.json)"
  name=$(jq -r '.name' "$skill_json")
  [[ "$name" == "dx-heuristics" ]] || fail "skill.json: name must be dx-heuristics, got $name"
fi

# ----- SKILL.md cleanliness (source-safety) -----
# Last-name tokens too generic to use alone as a leak-detection key. When the
# author's last token is one of these (or the author is a single word, e.g.
# an org name), match the full author string instead of just the last token.

author_stoplist=" Foundation Council Parliament Committee Group Working contributors "

if [[ -f "$skill_md" ]] && [[ -f "$skill_json" ]]; then
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
  check_pattern 'frontmatter name' '^name:[[:space:]]*dx-heuristics$' "$skill_md"
  check_pattern 'frontmatter license' '^license:' "$skill_md"
  check_pattern 'intent-router routing' 'intent-router\.csv' "$skill_md"
  check_pattern 'bare activation' 'show the intent menu' "$skill_md"
  check_pattern 'subagent dispatch section' '^## Subagent dispatch' "$skill_md"
  check_pattern 'three lenses' 'three lenses' "$skill_md"
fi

# ----- Intent router structure -----

if [[ -f "$intent_router" ]]; then
  rows=$(grep -cE '^(audit|design|debug|edge-pass),' "$intent_router")
  (( rows == 4 )) || fail "intent-router.csv: expected 4 data rows, got $rows"
  check_pattern 'audit intent' '^audit,' "$intent_router"
  check_pattern 'design intent' '^design,' "$intent_router"
  check_pattern 'debug intent' '^debug,' "$intent_router"
  check_pattern 'edge-pass intent' '^edge-pass,' "$intent_router"
fi

# ----- Playbook structure gates (every playbook on disk) -----

if [[ -z "$all_surfaces" ]]; then
  fail "no playbooks found in $playbook_dir"
fi

for surface in $all_surfaces; do
  pb="$playbook_dir/$surface.md"
  for section in '^## Scope' '^## Grounding' '^## Good signals' \
                 '^## Common failures' '^## Heuristics' \
                 '^## Quick diagnostic' '^## Cross-references'; do
    grep -Eq -- "$section" "$pb" || fail "$surface.md missing section ${section#^## }"
  done
  awk '
    /^## Heuristics/{f=1;next}
    /^## /{f=0}
    f && /\((audit|design|debug)/{found=1}
    END{ if(!found) exit 1 }
  ' "$pb" || fail "$surface.md: # Heuristics has no intent tags like (audit), (design), or (debug)"
  wc=$(wc -w < "$pb")
  if (( wc < 400 || wc > 1500 )); then
    fail "$surface.md word count $wc outside 400-1500"
  fi
done

# H1 title sanity for cli.md (regression guard for the canonical example)
cli_pb="$playbook_dir/cli.md"
if [[ -f "$cli_pb" ]]; then
  check_pattern 'cli.md H1 title' '^# CLI Playbook' "$cli_pb"
fi

# ----- Registry integrity (CSV → file) -----

for intent in audit design debug edge-pass; do
  csv="$skill_dir/references/intents/$intent.csv"
  [[ -f "$csv" ]] || { fail "missing intent CSV: $csv"; continue; }
  while IFS='|' read -r pb refs; do
    IFS=';' read -ra parts <<< "$pb"
    for p in "${parts[@]}"; do
      full="$skill_dir/$p"
      [[ -f "$full" ]] || fail "$intent.csv references missing playbook: $p"
    done
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

# ----- Orphan-playbook check (file → CSV) -----
# Every playbook on disk must be referenced by at least one intent CSV.
# Catches "I created a new playbook file but forgot to wire it in."

for surface in $all_surfaces; do
  pb_path="references/playbooks/${surface}.md"
  ref_count=0
  for intent in audit design debug edge-pass; do
    csv="$skill_dir/references/intents/$intent.csv"
    [[ -f "$csv" ]] || continue
    if grep -qF -- "$pb_path" "$csv"; then
      ref_count=$((ref_count + 1))
    fi
  done
  (( ref_count > 0 )) || fail "playbook $surface.md is not referenced by any intent CSV (orphan)"
done

# ----- skill.json playbooks-field gate -----

if [[ -f "$skill_json" ]]; then
  while IFS= read -r p; do
    if [[ "$valid_surfaces" == *" $p "* ]] || [[ "$valid_markers" == *" $p "* ]]; then
      continue
    fi
    fail "skill.json inspired_by.playbooks has unknown value: $p"
  done < <(jq -r '.inspired_by[].playbooks[]' "$skill_json")
fi

# ----- trigger-evals.json schema gate -----
# Shape is enforced by the canonical schema (schemas/trigger-evals.schema.json +
# scripts/validate-against-schema.py). Per-skill 'skill' field stays here.

trigger_evals="$skill_dir/evals/trigger-evals.json"
if [[ -f "$trigger_evals" ]]; then
  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/trigger-evals.schema.json" "$trigger_evals" \
    || fail "trigger-evals.json: schema validation failed (schemas/trigger-evals.schema.json)"
  skill_in_trigger=$(jq -r '.skill' "$trigger_evals")
  [[ "$skill_in_trigger" == "dx-heuristics" ]] \
    || fail "trigger-evals.json: 'skill' must be dx-heuristics, got $skill_in_trigger"
fi

# ----- Result -----

if (( failures > 0 )); then
  printf '\ndx-heuristics static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'dx-heuristics static eval passed.\n'
