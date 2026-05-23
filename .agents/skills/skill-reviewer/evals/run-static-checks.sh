#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"

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

check_file "$skill_md"
check_file "$skill_dir/references/intent-router.csv"
check_file "$skill_dir/references/review-rubric.md"
check_file "$skill_dir/references/source-safety-review.md"
check_file "$skill_dir/references/contract-drift-review.md"
check_file "$skill_dir/references/trackable-findings.md"
check_file "$skill_dir/templates/review-report.md"
check_file "$skill_dir/templates/findings-ledger.md"
check_file "$skill_dir/templates/workflow-state.json"
check_file "$skill_dir/evals/activation-cases.md"

check_pattern 'frontmatter name' '^name:[[:space:]]*skill-reviewer$' "$skill_md"
check_pattern 'bare activation asks for target' 'ask for the skill path' "$skill_md"
check_pattern 'trackable findings reference' 'trackable-findings\.md' "$skill_md"
check_pattern 'tracking state created by default' 'Create tracking state' "$skill_md"
check_pattern 'ledger filename has skill prefix' 'skill-reviewer-findings-ledger-<YYYY-MM-DD>-<scope-slug>\.md' "$skill_md"
check_pattern 'workflow-state filename has skill prefix' 'skill-reviewer-workflow-state-<YYYY-MM-DD>-<scope-slug>\.json' "$skill_md"
check_pattern 'tracking fallback path is preserved' 'audit-artifacts/skill-reviewer-' "$skill_md"
check_pattern 'review report has findings ledger section' '^## Findings ledger' "$skill_dir/templates/review-report.md"
check_pattern 'review report forbids mere offer' 'offer tracking' "$skill_dir/templates/review-report.md"
check_pattern 'ledger template has skill field' '^\*\*Skill:\*\*' "$skill_dir/templates/findings-ledger.md"
check_pattern 'workflow-state template has state_file' '"state_file": "docs/audits/<skill-name>-workflow-state-<YYYY-MM-DD>-<scope-slug>\.json"' "$skill_dir/templates/workflow-state.json"
check_pattern 'registry maps tracking reference' 'trackable-findings\.md' "$skill_dir/references/intent-router.csv"
check_pattern 'registry maps ledger template' 'templates/findings-ledger\.md' "$skill_dir/references/intent-router.csv"
check_pattern 'registry maps workflow-state template' 'templates/workflow-state\.json' "$skill_dir/references/intent-router.csv"
check_pattern 'registry maps contract drift mode' '^contract-drift-audit,' "$skill_dir/references/intent-router.csv"
check_pattern 'contract drift reference maps CI parity' 'CI parity' "$skill_dir/references/contract-drift-review.md"
check_pattern 'contract drift reference maps symlink integrity' 'Symlink integrity' "$skill_dir/references/contract-drift-review.md"

if (( failures > 0 )); then
  printf '\nskill-reviewer static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'skill-reviewer static eval passed.\n'
