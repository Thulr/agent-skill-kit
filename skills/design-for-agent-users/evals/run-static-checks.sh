#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"
skill_json="$skill_dir/skill.json"
trigger_evals="$skill_dir/evals/trigger-evals.json"
activation_cases="$skill_dir/evals/activation-cases.md"
router="$skill_dir/references/ax-router.csv"

failures=0
fail() { printf 'FAIL %s\n' "$1" >&2; failures=$((failures + 1)); }
check_file() { [[ -f "$1" ]] || fail "missing file: ${1#$skill_dir/}"; }

# ----- Required artifacts -----
check_file "$skill_md"
check_file "$skill_json"
check_file "$trigger_evals"
check_file "$activation_cases"
check_file "$router"

# ----- AX umbrella playbooks + AX core refs + template -----
for f in \
  references/playbooks/ax-docs.md \
  references/playbooks/ai-sdk.md \
  references/playbooks/agent.md \
  references/playbooks/audience-conflicts.md \
  references/core/severity-rubric.md \
  references/core/audience-matrix.md \
  references/empirical-warnings-w1.md \
  templates/ax-review-report.md; do
  check_file "$skill_dir/$f"
done

# ----- ax-router.csv header (well-formedness gated separately by check-routing-csv.sh) -----
[[ -f "$router" ]] && { head -1 "$router" | grep -q "," || fail "ax-router.csv missing header"; }

# ----- SKILL.md frontmatter + word-count gate -----
if [[ -f "$skill_md" ]]; then
  head -1 "$skill_md" | grep -q '^---$' || fail "SKILL.md missing YAML frontmatter delimiter (---)"
  grep -Eq '^name: design-for-agent-users$' "$skill_md" || fail "SKILL.md frontmatter must include: name: design-for-agent-users"
  grep -Eq '^description:' "$skill_md" || fail "SKILL.md frontmatter must include: description:"
  grep -Eq '^license:' "$skill_md" || fail "SKILL.md frontmatter must include: license:"
  wc=$(wc -w < "$skill_md")
  (( wc < 1200 )) || fail "SKILL.md word count $wc exceeds 1200 (runtime-only bound; detail belongs in references/)"
fi

# ----- Shared content is single-sourced via relative symlinks into _shared/ -----
for s in empirical-warnings.md lenses.md modes.md agent-friendly-architecture.md trackable-findings.md; do
  [[ -L "$skill_dir/references/$s" ]] || fail "references/$s must be a relative symlink into ../../_shared/"
done

# ----- Shared JSON contracts -----
validate_skill_json_contract "$repo_root" "$skill_json" "design-for-agent-users"
validate_trigger_evals_contract "$repo_root" "$trigger_evals" "design-for-agent-users"

if (( failures > 0 )); then
  exit 1
fi
echo "design-for-agent-users static eval passed."
