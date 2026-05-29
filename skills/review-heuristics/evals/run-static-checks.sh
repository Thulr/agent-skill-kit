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

failures=0
fail() { printf 'FAIL %s\n' "$1" >&2; failures=$((failures + 1)); }
check_file() { [[ -f "$1" ]] || fail "missing file: ${1#$skill_dir/}"; }

# ----- Required artifacts -----
check_file "$skill_md"
check_file "$skill_json"
check_file "$trigger_evals"
check_file "$activation_cases"

# ----- Domain router + shared workflow (the merge contract) -----
check_file "$skill_dir/references/domain-router.csv"
check_file "$skill_dir/references/review-workflow.md"

# ----- Every domain self-contained: intent-router + a templates dir -----
DOMAINS=(dx docs perf test ux ui-craft architecture)
for d in "${DOMAINS[@]}"; do
  check_file "$skill_dir/references/$d/intent-router.csv"
  [[ -d "$skill_dir/templates/$d" ]] || fail "missing templates/$d/ for domain $d"
done

# ----- domain-router.csv lists exactly the seven domain directories -----
router_domains="$(tail -n +2 "$skill_dir/references/domain-router.csv" | cut -d, -f1 | sort | tr '\n' ' ')"
expected_domains="$(printf '%s\n' "${DOMAINS[@]}" | sort | tr '\n' ' ')"
[[ "$router_domains" == "$expected_domains" ]] \
  || fail "domain-router.csv domains [$router_domains] != directories [$expected_domains]"

# ----- SKILL.md frontmatter + word-count gate -----
if [[ -f "$skill_md" ]]; then
  head -1 "$skill_md" | grep -q '^---$' || fail "SKILL.md missing YAML frontmatter delimiter (---)"
  grep -Eq '^name: review-heuristics$' "$skill_md" || fail "SKILL.md frontmatter must include: name: review-heuristics"
  grep -Eq '^description:' "$skill_md" || fail "SKILL.md frontmatter must include: description:"
  grep -Eq '^license:' "$skill_md" || fail "SKILL.md frontmatter must include: license:"
  # Thin domain-router body + a seven-domain description (kept higher than the
  # 800 single-domain bound because the description must carry all seven
  # domains' trigger keywords; per-domain detail lives in references/<domain>/).
  wc=$(wc -w < "$skill_md")
  (( wc < 1100 )) || fail "SKILL.md word count $wc exceeds 1100 (runtime-only bound; per-domain detail belongs in references/<domain>/)"
fi

# ----- Shared JSON contracts -----
validate_skill_json_contract "$repo_root" "$skill_json" "review-heuristics"
validate_trigger_evals_contract "$repo_root" "$trigger_evals" "review-heuristics"

if (( failures > 0 )); then
  exit 1
fi
echo "review-heuristics static eval passed."
