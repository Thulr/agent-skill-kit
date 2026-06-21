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
registry="$skill_dir/references/use-case-registry.csv"

failures=0
fail() { printf 'FAIL %s\n' "$1" >&2; failures=$((failures + 1)); }
check_file() { [[ -f "$1" ]] || fail "missing file: ${1#"$skill_dir"/}"; }

# ----- Required artifacts (repo contract) -----
check_file "$skill_md"
check_file "$skill_json"
check_file "$trigger_evals"
check_file "$activation_cases"

# ----- Skill-specific surfaces: registry, playbooks, scripts, templates -----
check_file "$registry"
for ref in cli-contract.md review-changes-playbook.md delegation-playbook.md output-rubric.md; do
  check_file "$skill_dir/references/$ref"
done
for s in cursor-review-changes.sh cursor-ask.sh cursor-doctor-check.sh; do
  check_file "$skill_dir/scripts/$s"
  [[ -x "$skill_dir/scripts/$s" ]] || fail "script not executable: scripts/$s"
done
for t in review-prompt.md delegation-prompt.md; do
  check_file "$skill_dir/templates/$t"
done

# ----- SKILL.md frontmatter + word-count gate -----
if [[ -f "$skill_md" ]]; then
  head -1 "$skill_md" | grep -q '^---$' || fail "SKILL.md missing YAML frontmatter delimiter (---)"
  grep -Eq '^name: cursor-cli$' "$skill_md" || fail "SKILL.md frontmatter must include: name: cursor-cli"
  grep -Eq '^description:' "$skill_md" || fail "SKILL.md frontmatter must include: description:"
  grep -Eq '^license:' "$skill_md" || fail "SKILL.md frontmatter must include: license:"
  wc=$(wc -w < "$skill_md")
  (( wc < 1200 )) || fail "SKILL.md word count $wc exceeds 1200 (runtime-only bound)"
fi

# ----- Every registry script/detail/template path resolves on disk -----
while IFS= read -r missing; do
  [[ -n "$missing" ]] && fail "use-case-registry.csv points at missing path: $missing"
done < <(python3 - "$skill_dir" "$registry" <<'PYEOF'
import csv, os, sys
skill, reg = sys.argv[1], sys.argv[2]
with open(reg, newline="") as fh:
    for row in csv.DictReader(fh):
        for col in ("detail_files", "artifact_templates", "script"):
            for tok in (row.get(col) or "").split(";"):
                tok = tok.strip()
                if tok and not os.path.exists(os.path.join(skill, tok)):
                    print(tok)
PYEOF
)

# ----- Safety defaults: scripts must keep the read-only guard. cursor-agent -p
#       defaults to full tool access, so the wrappers must default to --mode plan
#       and must not hardcode --force / --yolo / --sandbox disabled. -----
if grep -rqE '\-\-force|\-\-yolo|\-\-sandbox[[:space:]]+disabled' "$skill_dir/scripts"; then
  fail "scripts must not hardcode a Cursor read-only bypass (--force / --yolo / --sandbox disabled)"
fi
grep -q 'CURSOR_CLI_MODE:-plan' "$skill_dir/scripts/cursor-review-changes.sh" \
  || fail "cursor-review-changes.sh must default --mode to plan (read-only)"

# ----- Scripts are hermetic in --dry-run (no cursor-agent binary, no network) -----
run_dry() {
  local label="$1"; shift
  "$@" >/dev/null 2>&1 || fail "$label: --dry-run did not exit cleanly"
}
run_dry "cursor-ask.sh" bash "$skill_dir/scripts/cursor-ask.sh" --dry-run "Review the API boundary in this repository."
run_dry "cursor-doctor-check.sh" bash "$skill_dir/scripts/cursor-doctor-check.sh" --dry-run

# Review-changes needs a git repo; guard so the gate still passes outside one.
if git -C "$skill_dir" rev-parse --show-toplevel >/dev/null 2>&1; then
  review_out="$(bash "$skill_dir/scripts/cursor-review-changes.sh" --dry-run 2>&1 || true)"
  grep -q 'cursor-agent -p --mode plan' <<<"$review_out" \
    || fail "cursor-review-changes.sh --dry-run must build a read-only 'cursor-agent -p --mode plan' command"
else
  echo "note: skipping cursor-review-changes.sh --dry-run (not inside a git repo)"
fi

# ----- Shared JSON contracts (schema + name match) -----
validate_skill_json_contract "$repo_root" "$skill_json" "cursor-cli"
validate_trigger_evals_contract "$repo_root" "$trigger_evals" "cursor-cli"

if (( failures > 0 )); then
  exit 1
fi
echo "cursor-cli static eval passed."
