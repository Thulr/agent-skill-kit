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

SKILL_NAME="dx-design"
INTENTS=(design)

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
check_file "$skill_dir/references/intents/design.csv"
check_file "$skill_dir/references/core/personas.md"
check_file "$skill_dir/templates/design-doc.md"

# ----- Discover playbooks + valid markers -----
all_surfaces=""
if [[ -d "$playbook_dir" ]]; then
  for pb in "$playbook_dir"/*.md; do
    [[ -e "$pb" ]] || continue
    all_surfaces+="$(basename "$pb" .md) "
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
  check_pattern 'good-shaped pattern' 'good-shaped pattern' "$skill_md"
  check_pattern 'routes critique elsewhere' 'dx-critique' "$skill_md"
fi

# ----- design-doc template shape -----
check_pattern 'design-doc has good-shaped pattern' '^## Good-shaped pattern' "$skill_dir/templates/design-doc.md"
check_pattern 'design-doc has acceptance criteria' '^## Acceptance criteria' "$skill_dir/templates/design-doc.md"

# ----- Intent router structure (design only) -----
if [[ -f "$intent_router" ]]; then
  rows=$(grep -cE '^design,' "$intent_router")
  (( rows == 1 )) || fail "intent-router.csv: expected 1 design row, got $rows"
  for bad in audit debug edge-pass; do
    grep -Eq "^$bad," "$intent_router" && fail "intent-router.csv: '$bad' belongs in dx-critique, not dx-design"
  done
fi

# ----- Playbook structure gates (shared playbooks, via symlink) -----
[[ -z "$all_surfaces" ]] && fail "no playbooks found in $playbook_dir"
for surface in $all_surfaces; do
  pb="$playbook_dir/$surface.md"
  for section in '^## Scope' '^## Grounding' '^## Good signals' \
                 '^## Common failures' '^## Heuristics' \
                 '^## Quick diagnostic' '^## Cross-references'; do
    grep -Eq -- "$section" "$pb" || fail "$surface.md missing section ${section#^## }"
  done
  awk '/^## Heuristics/{f=1;next} /^## /{f=0} f && /\((audit|design|debug)/{found=1} END{ if(!found) exit 1 }' \
    "$pb" || fail "$surface.md: Heuristics has no intent tags"
  wc=$(wc -w < "$pb")
  (( wc < 400 || wc > 1500 )) && fail "$surface.md word count $wc outside 400-1500"
done

# ----- Registry integrity (CSV -> file) -----
for intent in "${INTENTS[@]}"; do
  csv="$skill_dir/references/intents/$intent.csv"
  [[ -f "$csv" ]] || { fail "missing intent CSV: $csv"; continue; }
  while IFS='|' read -r pb refs; do
    IFS=';' read -ra parts <<< "$pb"
    for p in "${parts[@]}"; do [[ -f "$skill_dir/$p" ]] || fail "$intent.csv references missing playbook: $p"; done
    IFS=';' read -ra rparts <<< "$refs"
    for r in "${rparts[@]}"; do [[ -f "$skill_dir/$r" ]] || fail "$intent.csv references missing core_ref: $r"; done
  done < <(python3 - "$csv" <<'PYEOF'
import csv, sys
with open(sys.argv[1], newline='') as f:
    for row in csv.DictReader(f):
        print(f"{row.get('playbook','').strip()}|{row.get('core_refs','').strip()}")
PYEOF
)
done

# ----- Orphan-playbook check -----
for surface in $all_surfaces; do
  pb_path="references/playbooks/${surface}.md"
  grep -qF -- "$pb_path" "$skill_dir/references/intents/design.csv" \
    || fail "playbook $surface.md is not referenced by design.csv (orphan)"
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
