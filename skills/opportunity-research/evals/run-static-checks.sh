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
check_file "$skill_dir/references/intents/scope.csv"
check_file "$skill_dir/references/intents/investigate.csv"
check_file "$skill_dir/references/intents/synthesize.csv"
check_file "$skill_dir/references/intents/decide.csv"
check_file "$skill_dir/references/core/severity-rubric.md"
check_file "$skill_dir/references/core/confidence-rubric.md"
check_file "$skill_dir/references/core/fadr-framework.md"
check_file "$skill_dir/references/core/personas.md"
check_file "$skill_dir/references/core/decision-gates.md"
check_file "$skill_dir/references/core/modes.md"
check_file "$skill_dir/references/subagent-dispatch.md"
check_file "$skill_dir/references/starter-scenarios.csv"
check_file "$skill_dir/references/trackable-findings.md"
check_file "$skill_dir/templates/scope-plan.md"
check_file "$skill_dir/templates/investigation-brief.md"
check_file "$skill_dir/templates/cross-area-brief.md"
check_file "$skill_dir/templates/fadr-memo.md"
check_file "$skill_dir/templates/findings-ledger.md"
check_file "$skill_dir/templates/workflow-state.json"
# Artifact templates use specific filenames (e.g., market-sizing.md, not market.md).
for artifact in market-sizing icp-and-jtbd competitor-map domain-glossary technical-feasibility data-inventory operating-model unit-economics legal-register channel-plan gtm-plan stakeholder-map risk-register trend-horizon; do
  check_file "$skill_dir/templates/artifacts/${artifact}.md"
done

check_file "$skill_dir/evals/activation-cases.md"
check_file "$skill_dir/evals/trigger-evals.json"

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

validate_skill_json_contract "$repo_root" "$skill_json" "opportunity-research"

# ----- SKILL.md cleanliness (no leaking source author names) -----

author_stoplist=" Foundation Council Parliament Committee Group Working contributors Parliament Stripe Atlas Reforge "

if [[ -f "$skill_md" ]] && [[ -f "$skill_json" ]]; then
  while IFS= read -r author; do
    [[ -n "$author" ]] || continue
    last="${author##* }"
    if [[ "$author_stoplist" == *" $last "* ]] || [[ "$author" == "$last" ]]; then
      if grep -qF -- "$author" "$skill_md"; then
        fail "SKILL.md leaks source author: $author (from inspired_by)"
      fi
    else
      # Fixed-string + word-boundary regex via -P (PCRE) to avoid regex-meta
      # false positives from author last-tokens like "al." matching "all".
      if grep -qP -- "\\b\\Q$last\\E\\b" "$skill_md" 2>/dev/null; then
        fail "SKILL.md leaks source author last name: $last (from inspired_by)"
      fi
    fi
  done < <(jq -r '.inspired_by[].author' "$skill_json")
fi

# ----- SKILL.md frontmatter + word-count gate -----

if [[ -f "$skill_md" ]]; then
  head -1 "$skill_md" | grep -q '^---$' || fail "SKILL.md missing YAML frontmatter delimiter"
  grep -Eq '^name: opportunity-research$' "$skill_md" || fail "SKILL.md frontmatter must include: name: opportunity-research"
  grep -Eq '^description:' "$skill_md" || fail "SKILL.md frontmatter must include: description:"
  grep -Eq '^license:' "$skill_md" || fail "SKILL.md frontmatter must include: license:"
  desc_len=$(awk -F'description: ' '/^description:/{print length($2); found=1; exit} END {if (!found) print 0}' "$skill_md")
  (( desc_len <= 1024 )) || fail "SKILL.md description length $desc_len exceeds 1024"

  # Routing-only bound; same as dx-heuristics.
  wc=$(wc -w < "$skill_md")
  (( wc < 1200 )) || fail "SKILL.md word count $wc exceeds 1200 (runtime-only bound)"
fi

# ----- Playbook structural sections (canonical) -----

required_sections=("## Scope" "## Grounding" "## Good signals" "## Common failures" "## Heuristics" "## Quick diagnostic" "## Cross-references")
for pb in "$playbook_dir"/*.md; do
  [[ -f "$pb" ]] || continue
  for section in "${required_sections[@]}"; do
    if ! grep -qF -- "$section" "$pb"; then
      fail "playbook $(basename "$pb"): missing canonical section '$section'"
    fi
  done
done

# ----- Registry integrity (CSV → file) -----
# Each intent CSV references playbooks + core_refs (+ artifact_template for
# investigate, output_template for synthesize/decide). Verify every referenced
# file resolves on disk.

check_csv_refs() {
  local csv="$1"
  [[ -f "$csv" ]] || { fail "missing intent CSV: $csv"; return; }
  while IFS='|' read -r pb refs art; do
    for col in "$pb" "$refs" "$art"; do
      [[ -z "$col" ]] && continue
      IFS=';' read -ra parts <<< "$col"
      for p in "${parts[@]}"; do
        [[ -z "$p" ]] && continue
        full="$skill_dir/$p"
        [[ -f "$full" ]] || fail "$(basename "$csv") references missing file: $p"
      done
    done
  done < <(python3 - "$csv" <<'PYEOF'
import csv, sys
with open(sys.argv[1], newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pb = (row.get('playbook') or '').strip()
        refs = (row.get('core_refs') or '').strip()
        art = (row.get('artifact_template') or row.get('output_template') or '').strip()
        print(f"{pb}|{refs}|{art}")
PYEOF
)
}

for intent in scope investigate synthesize decide; do
  check_csv_refs "$skill_dir/references/intents/$intent.csv"
done

# ----- Orphan-playbook check (file → CSV) -----

for surface in $all_surfaces; do
  pb_path="references/playbooks/${surface}.md"
  ref_count=0
  for intent in scope investigate synthesize decide; do
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

# ----- trigger-evals.json schema gate -----

trigger_evals="$skill_dir/evals/trigger-evals.json"
validate_trigger_evals_contract "$repo_root" "$trigger_evals" "opportunity-research"

# ----- Result -----

if (( failures > 0 )); then
  printf '\nopportunity-research static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'opportunity-research static eval passed.\n'
