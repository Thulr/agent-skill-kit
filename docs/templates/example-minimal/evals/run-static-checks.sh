#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Walk upward to the repo root (mirrors static-check-lib.sh repo_root_from,
# which is unavailable until sourced) so this script keeps working when the
# template is copied into any lane (skills/<name>/, .agents/skills/<name>/).
lib_root="$script_dir"
while [[ "$lib_root" != "/" && ! -f "$lib_root/scripts/static-check-lib.sh" ]]; do
  lib_root="$(dirname "$lib_root")"
done
if [[ ! -f "$lib_root/scripts/static-check-lib.sh" ]]; then
  echo "FAIL: scripts/static-check-lib.sh not found in any parent of $script_dir — run this from a checkout of agent-skill-kit." >&2
  exit 1
fi
source "$lib_root/scripts/static-check-lib.sh"
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

  # Parity with other skills' word-count bound.
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
