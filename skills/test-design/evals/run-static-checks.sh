#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"
skill_json="$skill_dir/skill.json"
intent_router="$skill_dir/references/intent-router.csv"
layer_dir="$skill_dir/references/layers"

SKILL_NAME="test-design"
INTENTS=(author strategize prune)

failures=0
fail() { printf 'FAIL %s\n' "$1" >&2; failures=$((failures + 1)); }
check_file() { [[ -f "$1" ]] || fail "missing file: $1"; }
check_pattern() {
  local label="$1" pattern="$2" path="$3"
  grep -Eq -- "$pattern" "$path" || fail "$label: pattern not found in $path"
}

# ----- File presence (design is lean: no severity/score/tracking) -----
check_file "$skill_md"
check_file "$skill_json"
check_file "$intent_router"
for i in "${INTENTS[@]}"; do check_file "$skill_dir/references/intents/$i.csv"; done
check_file "$skill_dir/references/core/personas.md"
check_file "$skill_dir/references/core/failure-modes.md"
check_file "$skill_dir/templates/author-design.md"
check_file "$skill_dir/templates/strategy-doc.md"
check_file "$skill_dir/templates/prune-plan.md"

# ----- Discover layer references + valid markers -----
all_surfaces=""
if [[ -d "$layer_dir" ]]; then
  for lf in "$layer_dir"/*.md; do
    [[ -e "$lf" ]] || continue
    all_surfaces+="$(basename "$lf" .md) "
  done
fi
valid_surfaces=" "; for s in $all_surfaces; do valid_surfaces+="$s "; done
valid_markers=" all "
if [[ -f "$intent_router" ]]; then
  while IFS=, read -r intent _; do
    [[ "$intent" == "intent" || -z "$intent" ]] && continue
    valid_markers+="${intent}-intent "
  done < "$intent_router"
fi

# ----- skill.json contract -----
validate_skill_json_contract "$repo_root" "$skill_json" "$SKILL_NAME"

# ----- SKILL.md cleanliness + word bound -----
author_stoplist=" Foundation Council Parliament Committee Group Working contributors "
if [[ -f "$skill_md" && -f "$skill_json" ]]; then
  while IFS= read -r author; do
    [[ -n "$author" ]] || continue
    last="${author##* }"
    if [[ "$author_stoplist" == *" $last "* ]] || [[ "$author" == "$last" ]]; then
      grep -qF -- "$author" "$skill_md" && fail "SKILL.md leaks source author: $author"
    else
      grep -qw -- "$last" "$skill_md" && fail "SKILL.md leaks source author last name: $last"
    fi
  done < <(jq -r '.inspired_by[].author' "$skill_json")
  while IFS= read -r title; do
    [[ -n "$title" ]] || continue
    grep -qF -- "$title" "$skill_md" && fail "SKILL.md leaks source title: $title"
  done < <(jq -r '.inspired_by[].name' "$skill_json")
  wc=$(wc -w < "$skill_md")
  (( wc < 800 )) || fail "SKILL.md word count $wc exceeds 800 (runtime-only bound)"
fi

# ----- SKILL.md structural gates -----
if [[ -f "$skill_md" ]]; then
  check_pattern 'frontmatter name' "^name:[[:space:]]*$SKILL_NAME$" "$skill_md"
  check_pattern 'frontmatter license' '^license:' "$skill_md"
  check_pattern 'intent-router routing' 'intent-router\.csv' "$skill_md"
  check_pattern 'good-shaped artifact' 'good-shaped artifact' "$skill_md"
  check_pattern 'routes critique elsewhere' 'test-critique' "$skill_md"
fi

# ----- Template shape gates -----
check_pattern 'author-design has test outline' '^## Test outline' "$skill_dir/templates/author-design.md"
check_pattern 'author-design has heuristics applied' '^## Heuristics applied' "$skill_dir/templates/author-design.md"
check_pattern 'strategy-doc has layer investments' '^## Layer investments' "$skill_dir/templates/strategy-doc.md"
check_pattern 'prune-plan has deletion candidates' '^## Deletion candidates' "$skill_dir/templates/prune-plan.md"

# ----- Intent router structure (design = author, strategize, prune) -----
if [[ -f "$intent_router" ]]; then
  rows=$(grep -cE '^(author|strategize|prune),' "$intent_router")
  (( rows == 3 )) || fail "intent-router.csv: expected 3 data rows, got $rows"
  for i in "${INTENTS[@]}"; do check_pattern "$i intent" "^$i," "$intent_router"; done
  for bad in review triage; do
    grep -Eq "^$bad," "$intent_router" && fail "intent-router.csv: '$bad' belongs in test-critique, not test-design"
  done
fi

# ----- Layer-reference structure gates (shared layers, via symlink) -----
[[ -z "$all_surfaces" ]] && fail "no layer references found in $layer_dir"
for surface in $all_surfaces; do
  lf="$layer_dir/$surface.md"
  for section in '^## Scope' '^## Grounding' '^## Good signals' \
                 '^## Common failures' '^## Heuristics' \
                 '^## Quick diagnostic' '^## Cross-references'; do
    grep -Eq -- "$section" "$lf" || fail "$surface.md missing section ${section#^## }"
  done
  awk '/^## Heuristics/{f=1;next} /^## /{f=0} f && /\((review|triage|author|strategize|prune)/{found=1} END{ if(!found) exit 1 }' \
    "$lf" || fail "$surface.md: Heuristics has no intent tags"
  wc=$(wc -w < "$lf")
  (( wc < 400 || wc > 1500 )) && fail "$surface.md word count $wc outside 400-1500"
done

# ----- Registry integrity (CSV -> file) -----
for intent in "${INTENTS[@]}"; do
  csv="$skill_dir/references/intents/$intent.csv"
  [[ -f "$csv" ]] || { fail "missing intent CSV: $csv"; continue; }
  while IFS='|' read -r pb refs; do
    IFS=';' read -ra parts <<< "$pb"
    for p in "${parts[@]}"; do [[ -f "$skill_dir/$p" ]] || fail "$intent.csv references missing layer: $p"; done
    IFS=';' read -ra rparts <<< "$refs"
    for r in "${rparts[@]}"; do [[ -f "$skill_dir/$r" ]] || fail "$intent.csv references missing core_ref: $r"; done
  done < <(python3 - "$csv" <<'PYEOF'
import csv, sys
with open(sys.argv[1], newline='') as f:
    rows = [r for r in f if r.strip() and not r.lstrip().startswith('#')]
import io
for row in csv.DictReader(io.StringIO(''.join(rows))):
    print(f"{row.get('playbook','').strip()}|{row.get('core_refs','').strip()}")
PYEOF
)
done

# ----- Orphan layer-reference check (file -> CSV) -----
for surface in $all_surfaces; do
  lf_path="references/layers/${surface}.md"
  ref_count=0
  for intent in "${INTENTS[@]}"; do
    csv="$skill_dir/references/intents/$intent.csv"
    [[ -f "$csv" ]] && grep -qF -- "$lf_path" "$csv" && ref_count=$((ref_count + 1))
  done
  (( ref_count > 0 )) || fail "layer reference $surface.md is not referenced by any intent CSV (orphan)"
done

# ----- skill.json playbooks-field gate -----
if [[ -f "$skill_json" ]]; then
  while IFS= read -r p; do
    [[ "$valid_surfaces" == *" $p "* || "$valid_markers" == *" $p "* ]] && continue
    fail "skill.json inspired_by.playbooks has unknown value: $p"
  done < <(jq -r '.inspired_by[].playbooks[]' "$skill_json")
fi

# ----- trigger-evals contract -----
validate_trigger_evals_contract "$repo_root" "$skill_dir/evals/trigger-evals.json" "$SKILL_NAME"

if (( failures > 0 )); then
  printf '\n%s static eval failed with %d issue(s).\n' "$SKILL_NAME" "$failures" >&2
  exit 1
fi
printf '%s static eval passed.\n' "$SKILL_NAME"
