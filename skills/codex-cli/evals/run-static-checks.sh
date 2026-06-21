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
for ref in cli-contract.md review-changes-playbook.md delegation-playbook.md doctor-playbook.md output-rubric.md; do
  check_file "$skill_dir/references/$ref"
done
for s in codex-review-changes.sh codex-ask.sh codex-cross-project-reflect.sh codex-doctor-check.sh; do
  check_file "$skill_dir/scripts/$s"
  [[ -x "$skill_dir/scripts/$s" ]] || fail "script not executable: scripts/$s"
done
for t in review-prompt.md delegation-prompt.md cross-project-reflection-prompt.md; do
  check_file "$skill_dir/templates/$t"
done

# ----- SKILL.md frontmatter + word-count gate -----
if [[ -f "$skill_md" ]]; then
  head -1 "$skill_md" | grep -q '^---$' || fail "SKILL.md missing YAML frontmatter delimiter (---)"
  grep -Eq '^name: codex-cli$' "$skill_md" || fail "SKILL.md frontmatter must include: name: codex-cli"
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

# ----- Safety defaults: scripts must never wire in a Codex bypass, and must
#       default the delegated sandbox to read-only (the cli-contract invariant). -----
if grep -rqE 'dangerously-bypass' "$skill_dir/scripts"; then
  fail "scripts must not hardcode a Codex approval/sandbox bypass (dangerously-bypass-*)"
fi
grep -q 'CODEX_CLI_SANDBOX:-read-only' "$skill_dir/scripts/codex-ask.sh" \
  || fail "codex-ask.sh must default --sandbox to read-only"

# ----- Scripts are hermetic in --dry-run (no Codex binary, no network) -----
run_dry() {
  local label="$1"; shift
  "$@" >/dev/null 2>&1 || fail "$label: --dry-run did not exit cleanly"
}
run_dry "codex-doctor-check.sh" bash "$skill_dir/scripts/codex-doctor-check.sh" --dry-run
run_dry "codex-ask.sh" bash "$skill_dir/scripts/codex-ask.sh" --dry-run "Review the API boundary in this repository."

# Cross-project reflection must target a neutral dir and skip the git-repo check —
# never silently audit the launching repository.
reflect_out="$(bash "$skill_dir/scripts/codex-cross-project-reflect.sh" --dry-run --since 'last 30 days' 2>&1 || true)"
grep -q -- '--skip-git-repo-check' <<<"$reflect_out" \
  || fail "cross-project-reflect --dry-run must pass --skip-git-repo-check"
grep -q -- '--cd' <<<"$reflect_out" \
  || fail "cross-project-reflect --dry-run must set a neutral --cd directory"

# Review-changes needs a git repo; guard so the gate still passes outside one.
if git -C "$skill_dir" rev-parse --show-toplevel >/dev/null 2>&1; then
  review_out="$(bash "$skill_dir/scripts/codex-review-changes.sh" --dry-run 2>&1 || true)"
  grep -q 'codex review --uncommitted' <<<"$review_out" \
    || fail "review-changes uncommitted --dry-run must build 'codex review --uncommitted'"
  # codex 0.141 rejects a [PROMPT] with every scope flag, so the command must NOT
  # carry the '-- -' stdin sentinel (regression guard for the live-found bug).
  if grep -q -- '-- -' <<<"$review_out"; then
    fail "codex review must not pass a [PROMPT]/'-- -' (codex rejects it with --uncommitted/--base/--commit)"
  fi
else
  echo "note: skipping codex-review-changes.sh --dry-run (not inside a git repo)"
fi

# ----- Shared JSON contracts (schema + name match) -----
validate_skill_json_contract "$repo_root" "$skill_json" "codex-cli"
validate_trigger_evals_contract "$repo_root" "$trigger_evals" "codex-cli"

if (( failures > 0 )); then
  exit 1
fi
echo "codex-cli static eval passed."
