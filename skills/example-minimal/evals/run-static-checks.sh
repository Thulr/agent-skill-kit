#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(git -C "$script_dir" rev-parse --show-toplevel)"
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

  # Parity with other skills' word-count bound (see dx-heuristics/test-heuristics).
  wc=$(wc -w < "$skill_md")
  (( wc < 800 )) || fail "SKILL.md word count $wc exceeds 800 (runtime-only bound)"
fi

# ----- skill.json gates -----
# Shape is enforced by the canonical schema (schemas/skill.schema.json +
# scripts/validate-against-schema.py). Per-skill assertions stay here.
if [[ -f "$skill_json" ]]; then
  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/skill.schema.json" "$skill_json" \
    || fail "skill.json: schema validation failed (schemas/skill.schema.json)"
  name=$(jq -r '.name' "$skill_json")
  [[ "$name" == "example-minimal" ]] || fail "skill.json: name must be example-minimal, got $name"
fi

# ----- trigger-evals.json schema gate -----
# Shape is enforced by the canonical schema (schemas/trigger-evals.schema.json +
# scripts/validate-against-schema.py). Per-skill 'skill' field stays here.
if [[ -f "$trigger_evals" ]]; then
  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/trigger-evals.schema.json" "$trigger_evals" \
    || fail "trigger-evals.json: schema validation failed (schemas/trigger-evals.schema.json)"
  skill_in_trigger=$(jq -r '.skill' "$trigger_evals")
  [[ "$skill_in_trigger" == "example-minimal" ]] \
    || fail "trigger-evals.json: 'skill' must be example-minimal, got $skill_in_trigger"
fi

if (( failures > 0 )); then
  exit 1
fi

echo "example-minimal static eval passed."
