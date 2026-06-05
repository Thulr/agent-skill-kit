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

SKILL_NAME="ux-audit"
# One-layer router: intent routes directly to detail files + templates.
INTENTS=(usability-audit accessibility-audit form-review navigation-review error-recovery)

failures=0
fail() { printf 'FAIL %s\n' "$1" >&2; failures=$((failures + 1)); }
# Tracking files are relative symlinks into skills/_shared/; accept files or links.
check_file() { [[ -f "$1" || -L "$1" ]] || fail "missing file: $1"; }
check_pattern() {
  local label="$1" pattern="$2" path="$3"
  grep -Eq -- "$pattern" "$path" || fail "$label: pattern not found in $path"
}

# ----- File presence -----
check_file "$skill_md"
check_file "$skill_json"
check_file "$router"
check_file "$skill_dir/references/starter-scenarios.csv"
check_file "$skill_dir/references/core/severity-rubric.md"
check_file "$skill_dir/references/trackable-findings.md"
check_file "$skill_dir/references/modes.md"
check_file "$skill_dir/templates/audit-report.md"
check_file "$skill_dir/templates/findings-ledger.md"
check_file "$skill_dir/templates/workflow-state.json"
check_file "$skill_dir/evals/activation-cases.md"
check_file "$skill_dir/evals/trigger-evals.json"

# ----- Discover playbooks (file presence side; CSV holds the route vocabulary) -----
all_surfaces=""
if [[ -d "$playbook_dir" ]]; then
  for pb in "$playbook_dir"/*.md; do
    [[ -e "$pb" ]] || continue
    all_surfaces+="$(basename "$pb" .md) "
  done
fi

# ----- skill.json contract -----
validate_skill_json_contract "$repo_root" "$skill_json" "$SKILL_NAME"
if [[ -f "$skill_json" ]]; then
  status=$(jq -r '.status' "$skill_json")
  [[ "$status" == "published" ]] || fail "skill.json status must be published, got $status"
fi

# ----- SKILL.md cleanliness (no source-author/title leak) + word bound -----
author_stoplist=" Foundation Council Parliament Committee Group Working Initiative contributors "
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
  check_pattern 'bare activation' 'intent menu' "$skill_md"
  check_pattern 'trackable findings reference' 'trackable-findings\.md' "$skill_md"
fi

# ----- Tracking behavior gates (ux-audit ships findings-ledger + workflow-state) -----
check_pattern 'creates tracking state by default' 'Create, resume, or close tracking state' "$skill_md"
check_pattern 'ledger filename has skill prefix' "$SKILL_NAME-findings-ledger-<YYYY-MM-DD>-<scope-slug>\.md" "$skill_md"
check_pattern 'workflow-state filename has skill prefix' "$SKILL_NAME-workflow-state-<YYYY-MM-DD>-<scope-slug>\.json" "$skill_md"
check_pattern 'tracking fallback path preserved' "audit-artifacts/$SKILL_NAME-" "$skill_md"
check_pattern 'roadmaps and issues opt-in' 'roadmaps,' "$skill_md"
check_pattern 'closeout resumes saved state' 'saved state first' "$skill_md"
check_pattern 'closeout verifies before status update' 'verification rule' "$skill_md"
check_pattern 'audit report has findings ledger section' '^## Findings ledger' "$skill_dir/templates/audit-report.md"
check_pattern 'audit report forbids mere offer' 'do not merely offer' "$skill_dir/templates/audit-report.md"
check_pattern 'audit report preserves fallback path' "audit-artifacts/$SKILL_NAME-" "$skill_dir/templates/audit-report.md"
check_pattern 'audit report ledger path has skill prefix' "docs/audits/$SKILL_NAME-findings-ledger-<YYYY-MM-DD>-<scope-slug>\.md" "$skill_dir/templates/audit-report.md"
check_pattern 'ledger template has skill field' '^\*\*Skill:\*\*' "$skill_dir/templates/findings-ledger.md"
check_pattern 'ledger template has skill-prefixed markdown path' '<skill-name>-findings-ledger-<YYYY-MM-DD>-<scope-slug>\.md' "$skill_dir/templates/findings-ledger.md"
check_pattern 'workflow-state template has state_file' '"state_file": "docs/audits/<skill-name>-workflow-state-<YYYY-MM-DD>-<scope-slug>\.json"' "$skill_dir/templates/workflow-state.json"

# ----- One-layer intent-router structure -----
if [[ -f "$router" ]]; then
  # Header column vocabulary for a one-layer router.
  check_pattern 'router header columns' '^intent,trigger_examples,detail_files,templates,notes$' "$router"
  rows=$(grep -cE '^(usability-audit|accessibility-audit|form-review|navigation-review|error-recovery),' "$router")
  (( rows == 5 )) || fail "intent-router.csv: expected 5 data rows, got $rows"
  for i in "${INTENTS[@]}"; do check_pattern "$i intent" "^$i," "$router"; done
  # This is a one-layer router: no per-intent surface CSVs should exist.
  [[ -d "$skill_dir/references/intents" ]] && fail "references/intents/ found: ux-audit is a one-layer router (no surface layer)"

  # Registry integrity: every detail_file and template the router names must exist.
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

# ----- Playbook structure gates -----
[[ -z "$all_surfaces" ]] && fail "no playbooks found in $playbook_dir"
for pb in "$playbook_dir"/*.md; do
  [[ -f "$pb" ]] || continue
  for section in '^## Scope' '^## Grounding' '^## Good signals' '^## Common failures' \
                 '^## Heuristics' '^## Quick diagnostic' '^## Cross-references'; do
    grep -Eq -- "$section" "$pb" || fail "$(basename "$pb") missing section ${section#^## }"
  done
  wc=$(wc -w < "$pb")
  (( wc < 250 || wc > 1200 )) && fail "$(basename "$pb") word count $wc outside 250-1200"
done

# ----- Orphan-playbook check (file -> router) -----
for surface in $all_surfaces; do
  pb_path="references/playbooks/${surface}.md"
  [[ -f "$router" ]] && grep -qF -- "$pb_path" "$router" \
    || fail "playbook $surface.md is not referenced by intent-router.csv (orphan)"
done

# ----- skill.json playbooks-field gate (one-layer: values are intent names) -----
if [[ -f "$skill_json" ]]; then
  valid=" "
  for i in "${INTENTS[@]}"; do valid+="$i "; done
  while IFS= read -r p; do
    [[ -z "$p" ]] && continue
    [[ "$valid" == *" $p "* ]] || fail "skill.json inspired_by.playbooks has unknown value: $p"
  done < <(jq -r '.inspired_by[].playbooks[]?' "$skill_json")
fi

# ----- trigger-evals contract -----
validate_trigger_evals_contract "$repo_root" "$skill_dir/evals/trigger-evals.json" "$SKILL_NAME"

# ----- Calibration: project-scale right-sizing -----
check_pattern 'SKILL.md has calibration step' 'calibrate to project scale' "$skill_md"
check_pattern 'report declares project tier' 'Project tier' "$skill_dir/templates/audit-report.md"
check_pattern 'report has Later/as-it-grows bucket' 'as it grows' "$skill_dir/templates/audit-report.md"

if (( failures > 0 )); then
  printf '\n%s static eval failed with %d issue(s).\n' "$SKILL_NAME" "$failures" >&2
  exit 1
fi
printf '%s static eval passed.\n' "$SKILL_NAME"
