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

fail() {
  printf 'FAIL %s\n' "$1" >&2
  failures=$((failures + 1))
}

check_file() {
  [[ -f "$1" ]] || fail "missing file: $1"
}

check_file "$skill_md"
check_file "$skill_json"
check_file "$trigger_evals"
check_file "$activation_cases"

# ----- SKILL.md frontmatter gate -----
# `metadata.internal: true` is load-bearing here: it is the only thing keeping
# example-minimal hidden from `npx skills add . --list`. If it disappears, the
# template starts showing up as an installable skill.
if [[ -f "$skill_md" ]]; then
  head -1 "$skill_md" | grep -q '^---$' || fail "SKILL.md missing YAML frontmatter delimiter (---)"
  grep -Eq '^name: example-minimal$' "$skill_md" || fail "SKILL.md frontmatter must include: name: example-minimal"
  grep -Eq '^description:' "$skill_md" || fail "SKILL.md frontmatter must include: description:"
  grep -Eq '^license:' "$skill_md" || fail "SKILL.md frontmatter must include: license:"
  grep -Eq '^metadata:[[:space:]]*$' "$skill_md" \
    || fail "SKILL.md frontmatter must include: metadata: (with internal: true)"
  grep -Eq '^[[:space:]]+internal:[[:space:]]*true[[:space:]]*$' "$skill_md" \
    || fail "SKILL.md frontmatter must include: metadata.internal: true (keeps example-minimal hidden from npx skills add . --list)"

  # Parity with other skills' word-count bound (see review-heuristics).
  wc=$(wc -w < "$skill_md")
  (( wc < 1200 )) || fail "SKILL.md word count $wc exceeds 1200 (runtime-only bound)"
fi

# ----- Shared JSON gates -----
validate_skill_json_contract "$repo_root" "$skill_json" "example-minimal"
validate_trigger_evals_contract "$repo_root" "$trigger_evals" "example-minimal"

if (( failures > 0 )); then
  exit 1
fi

echo "example-minimal static eval passed."
