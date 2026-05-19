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
check_file "$skill_dir/references/intents/refactor.csv"
check_file "$skill_dir/references/intents/explain.csv"
check_file "$skill_dir/references/core/severity-rubric.md"
check_file "$skill_dir/references/core/score-rubric.md"
check_file "$skill_dir/references/core/personas.md"
check_file "$skill_dir/references/core/glossary.md"
check_file "$skill_dir/references/trackable-findings.md"
check_file "$skill_dir/references/subagent-dispatch.md"
check_file "$skill_dir/templates/audit-report.md"
check_file "$skill_dir/templates/audit-report-multi.md"
check_file "$skill_dir/templates/design-doc.md"
check_file "$skill_dir/templates/refactor-runbook.md"
check_file "$skill_dir/templates/explanation.md"
check_file "$skill_dir/templates/findings-ledger.md"
check_file "$skill_dir/templates/roadmap.md"
check_file "$skill_dir/templates/github-issue.md"
check_file "$skill_dir/templates/workflow-state.json"
check_file "$skill_dir/evals/activation-cases.md"

# Skill-specific: glossary must be non-empty (terminology overload is the
# highest-likelihood reader-derailment risk in this domain).
if [[ -f "$skill_dir/references/core/glossary.md" ]]; then
  glossary_words=$(wc -w < "$skill_dir/references/core/glossary.md")
  (( glossary_words > 50 )) || fail "glossary.md must be > 50 words (got $glossary_words)"
fi

# ----- Discover playbooks (source of truth) -----

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

# Intent markers: <intent>-intent + "all"
valid_markers=" all "
if [[ -f "$intent_router" ]]; then
  while IFS=, read -r intent _; do
    [[ "$intent" == "intent" ]] && continue
    [[ -z "$intent" ]] && continue
    valid_markers+="${intent}-intent "
  done < "$intent_router"
fi

# ----- skill.json gates -----

if [[ -f "$skill_json" ]]; then
  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/skill.schema.json" "$skill_json" \
    || fail "skill.json: schema validation failed (schemas/skill.schema.json)"
  name=$(jq -r '.name' "$skill_json")
  [[ "$name" == "clean-architecture" ]] || fail "skill.json: name must be clean-architecture, got $name"
fi

# ----- SKILL.md source-safety (citations live in skill.json, not SKILL.md) -----

author_stoplist=" Foundation Council Parliament Committee Group Working contributors Facebook "

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
  check_pattern 'frontmatter name' '^name:[[:space:]]*clean-architecture$' "$skill_md"
  check_pattern 'frontmatter license' '^license:' "$skill_md"
  check_pattern 'intent-router routing' 'intent-router\.csv' "$skill_md"
  check_pattern 'bare activation' 'show the intent menu' "$skill_md"
  check_pattern 'subagent dispatch section' '^## Subagent dispatch' "$skill_md"
  check_pattern 'three lenses' 'three lenses' "$skill_md"
  check_pattern 'trackable findings reference' 'trackable-findings\.md' "$skill_md"
fi

# ----- Intent router structure -----

if [[ -f "$intent_router" ]]; then
  rows=$(grep -cE '^(audit|design|refactor|explain),' "$intent_router")
  (( rows == 4 )) || fail "intent-router.csv: expected 4 data rows, got $rows"
  check_pattern 'audit intent' '^audit,' "$intent_router"
  check_pattern 'design intent' '^design,' "$intent_router"
  check_pattern 'refactor intent' '^refactor,' "$intent_router"
  check_pattern 'explain intent' '^explain,' "$intent_router"
fi

# ----- Playbook structural gates -----

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
    f && /\((audit|design|refactor|explain)/{found=1}
    END{ if(!found) exit 1 }
  ' "$pb" || fail "$surface.md: ## Heuristics has no intent tags like (audit), (design), (refactor), or (explain)"
  wc=$(wc -w < "$pb")
  if (( wc < 400 || wc > 1500 )); then
    fail "$surface.md word count $wc outside 400-1500"
  fi
done

# ----- Audit-only `all`-fanout invariant (skill-specific) -----

for intent in design refactor explain; do
  csv="$skill_dir/references/intents/$intent.csv"
  [[ -f "$csv" ]] || continue
  if grep -qE '^all,' "$csv"; then
    fail "$intent.csv contains an 'all' row; only audit.csv may declare all-fanout"
  fi
done

audit_csv="$skill_dir/references/intents/audit.csv"
if [[ -f "$audit_csv" ]]; then
  grep -qE '^all,' "$audit_csv" || fail "audit.csv missing required 'all' row for fan-out intent"
fi

# ----- CSV → file registry integrity -----

for intent in audit design refactor explain; do
  csv="$skill_dir/references/intents/$intent.csv"
  [[ -f "$csv" ]] || { fail "missing intent CSV: $csv"; continue; }
  while IFS='|' read -r pb refs; do
    [[ -z "$pb" && -z "$refs" ]] && continue
    IFS=';' read -ra parts <<< "$pb"
    for p in "${parts[@]}"; do
      [[ -z "$p" ]] && continue
      full="$skill_dir/$p"
      [[ -f "$full" ]] || fail "$intent.csv references missing playbook: $p"
    done
    IFS=';' read -ra rparts <<< "$refs"
    for r in "${rparts[@]}"; do
      [[ -z "$r" ]] && continue
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

for surface in $all_surfaces; do
  pb_path="references/playbooks/${surface}.md"
  ref_count=0
  for intent in audit design refactor explain; do
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
  done < <(jq -r '.inspired_by[].playbooks[]?' "$skill_json")
fi

# ----- trigger-evals.json gate -----
# trigger-evals.json is required: presence + schema + skill-name match.

trigger_evals="$skill_dir/evals/trigger-evals.json"
check_file "$trigger_evals"
if [[ -f "$trigger_evals" ]]; then
  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/trigger-evals.schema.json" "$trigger_evals" \
    || fail "trigger-evals.json: schema validation failed (schemas/trigger-evals.schema.json)"
  skill_in_trigger=$(jq -r '.skill' "$trigger_evals")
  [[ "$skill_in_trigger" == "clean-architecture" ]] \
    || fail "trigger-evals.json: 'skill' must be clean-architecture, got $skill_in_trigger"
fi

# ----- Result -----

if (( failures > 0 )); then
  printf '\nclean-architecture static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'clean-architecture static eval passed.\n'
