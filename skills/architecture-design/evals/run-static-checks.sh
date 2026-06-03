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

SKILL_NAME="architecture-design"
INTENTS=(design refactor explain)

failures=0
fail() { printf 'FAIL %s\n' "$1" >&2; failures=$((failures + 1)); }
check_file() { [[ -f "$1" ]] || fail "missing file: $1"; }
check_pattern() {
  local label="$1" pattern="$2" path="$3"
  grep -Eq -- "$pattern" "$path" || fail "$label: pattern not found in $path"
}

# ----- File presence (design is lean: no score/tracking) -----
check_file "$skill_md"
check_file "$skill_json"
check_file "$intent_router"
for i in "${INTENTS[@]}"; do check_file "$skill_dir/references/intents/$i.csv"; done
check_file "$skill_dir/references/core/personas.md"
check_file "$skill_dir/references/core/glossary.md"
check_file "$skill_dir/templates/design-doc.md"
check_file "$skill_dir/templates/refactor-runbook.md"
check_file "$skill_dir/templates/explanation.md"

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
  check_pattern 'routes critique elsewhere' 'architecture-audit' "$skill_md"
fi

# ----- design-doc template shape -----
check_pattern 'design-doc has acceptance criteria' '^## Acceptance criteria' "$skill_dir/templates/design-doc.md"
check_pattern 'design-doc has grounding sources' '^## Grounding sources applied' "$skill_dir/templates/design-doc.md"
# ----- refactor-runbook template shape -----
check_pattern 'refactor-runbook has step sequence' '^## Step sequence' "$skill_dir/templates/refactor-runbook.md"
check_pattern 'refactor-runbook has verification' '^## Verification' "$skill_dir/templates/refactor-runbook.md"
# ----- explanation template shape -----
check_pattern 'explanation has what-it-is-not' '^## What it is not' "$skill_dir/templates/explanation.md"
check_pattern 'explanation has verification' '^## Verification' "$skill_dir/templates/explanation.md"

# ----- Intent router structure (design / refactor / explain; no audit) -----
if [[ -f "$intent_router" ]]; then
  rows=$(grep -cE '^(design|refactor|explain),' "$intent_router")
  (( rows == 3 )) || fail "intent-router.csv: expected 3 data rows, got $rows"
  for i in "${INTENTS[@]}"; do check_pattern "$i intent" "^$i," "$intent_router"; done
  grep -Eq '^audit,' "$intent_router" && fail "intent-router.csv: 'audit' belongs in architecture-audit, not architecture-design"
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
  awk '/^## Heuristics/{f=1;next} /^## /{f=0} f && /\((audit|design|refactor|explain)/{found=1} END{ if(!found) exit 1 }' \
    "$pb" || fail "$surface.md: Heuristics has no intent tags"
  wc=$(wc -w < "$pb")
  (( wc < 400 || wc > 1500 )) && fail "$surface.md word count $wc outside 400-1500"
done

# ----- Registry integrity (CSV -> file) -----
for intent in "${INTENTS[@]}"; do
  csv="$skill_dir/references/intents/$intent.csv"
  [[ -f "$csv" ]] || { fail "missing intent CSV: $csv"; continue; }
  while IFS='|' read -r pb refs; do
    if [[ -n "$pb" ]]; then
      IFS=';' read -ra parts <<< "$pb"
      for p in "${parts[@]}"; do [[ -z "$p" ]] || [[ -f "$skill_dir/$p" ]] || fail "$intent.csv references missing playbook: $p"; done
    fi
    if [[ -n "$refs" ]]; then
      IFS=';' read -ra rparts <<< "$refs"
      for r in "${rparts[@]}"; do [[ -z "$r" ]] || [[ -f "$skill_dir/$r" ]] || fail "$intent.csv references missing core_ref: $r"; done
    fi
  done < <(python3 - "$csv" <<'PYEOF'
import csv, sys
with open(sys.argv[1], newline='') as f:
    for row in csv.DictReader(f):
        print(f"{row.get('playbook','').strip()}|{row.get('core_refs','').strip()}")
PYEOF
)
done

# ----- Orphan-playbook check (file -> CSV; any intent references it) -----
for surface in $all_surfaces; do
  pb_path="references/playbooks/${surface}.md"
  ref_count=0
  for intent in "${INTENTS[@]}"; do
    csv="$skill_dir/references/intents/$intent.csv"
    [[ -f "$csv" ]] && grep -qF -- "$pb_path" "$csv" && ref_count=$((ref_count + 1))
  done
  (( ref_count > 0 )) || fail "playbook $surface.md is not referenced by any intent CSV (orphan)"
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
