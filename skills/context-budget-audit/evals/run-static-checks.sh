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
audit_py="$skill_dir/scripts/audit_context_budget.py"

failures=0
fail() { printf 'FAIL %s\n' "$1" >&2; failures=$((failures + 1)); }
check_file() { [[ -f "$1" ]] || fail "missing file: ${1#"$skill_dir"/}"; }

# ----- Required artifacts (repo contract) -----
check_file "$skill_md"
check_file "$skill_json"
check_file "$trigger_evals"
check_file "$activation_cases"

# ----- Skill-specific surfaces -----
check_file "$registry"
check_file "$skill_dir/references/audit-framework.md"
check_file "$skill_dir/references/recommendation-rubric.md"
check_file "$audit_py"
check_file "$skill_dir/evals/context-budget-audit-eval-suite.json"

# ----- SKILL.md frontmatter + word-count gate -----
# Cap raised to 1500 (vs the 1200 default): this is a deliberately operational
# skill — kind model, evidence/privacy rules, a gated act-on-named-items flow,
# stop conditions, and an output contract all carry runtime weight. Splitting it
# to hit 1200 would be the unenforced-cap restructuring anti-pattern
# (docs/reflection-log/2026-05-28-restructure-split-justified-by-unenforced-cap.md).
if [[ -f "$skill_md" ]]; then
  head -1 "$skill_md" | grep -q '^---$' || fail "SKILL.md missing YAML frontmatter delimiter (---)"
  grep -Eq '^name: context-budget-audit$' "$skill_md" || fail "SKILL.md frontmatter must include: name: context-budget-audit"
  grep -Eq '^description:' "$skill_md" || fail "SKILL.md frontmatter must include: description:"
  grep -Eq '^license:' "$skill_md" || fail "SKILL.md frontmatter must include: license:"
  wc=$(wc -w < "$skill_md")
  (( wc < 1500 )) || fail "SKILL.md word count $wc exceeds 1500 (raised operational bound)"
fi

# ----- Every registry detail/template/script path resolves on disk -----
while IFS= read -r missing; do
  [[ -n "$missing" ]] && fail "use-case-registry.csv points at missing path: $missing"
done < <(python3 - "$skill_dir" "$registry" <<'PYEOF'
import csv, os, shlex, sys
skill, reg = sys.argv[1], sys.argv[2]
with open(reg, newline="") as fh:
    for row in csv.DictReader(fh):
        for col in ("detail_files", "artifact_templates"):
            for tok in (row.get(col) or "").split(";"):
                tok = tok.strip()
                if tok and not os.path.exists(os.path.join(skill, tok)):
                    print(tok)
        script = (row.get("script") or "").strip()
        if script:
            tok = shlex.split(script)[0]
            if not os.path.exists(os.path.join(skill, tok)):
                print(tok)
PYEOF
)

# ----- The audit engine is read-only, stdlib-only, and hermetic (ported from the
#       skill's own eval suite; all runs use a throwaway --home, never the real ~). -----
python3 "$audit_py" --help >/dev/null 2>&1 || fail "audit_context_budget.py --help failed (script may not import)"

# Empty home → valid JSON, expected schema, zero items.
empty_home="$(mktemp -d)"
if ! python3 "$audit_py" --home "$empty_home" --repo-root "$repo_root" --json --no-write 2>/dev/null \
    | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['schema']=='context-budget-audit.v1', d.get('schema'); assert d['items']==[], d['items']"; then
  fail "empty-home audit did not emit schema 'context-budget-audit.v1' with empty items"
fi

# --only filter restricts kinds; the frontmatter parser reads YAML block scalars.
demo_home="$(mktemp -d)"
mkdir -p "$demo_home/.claude/skills/demo"
printf -- '---\nname: demo\ndescription: >\n  line one of a long description\n  line two of the same description\n---\nbody\n' \
  > "$demo_home/.claude/skills/demo/SKILL.md"
if ! python3 "$audit_py" --home "$demo_home" --repo-root "$repo_root" --only skill --json --no-write 2>/dev/null \
    | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['kinds']==['skill'], d['kinds']; demo=[i for i in d['items'] if i['name']=='demo'][0]; assert demo['est_tokens']>5, demo"; then
  fail "kinds filter / block-scalar token-estimate check failed"
fi

# --no-write writes no artifact files into cwd.
out_dir="$(mktemp -d)"
( cd "$out_dir" && python3 "$audit_py" --home "$empty_home" --repo-root "$repo_root" --no-write >/dev/null 2>&1 ) || true
[[ -z "$(ls -A "$out_dir")" ]] || fail "--no-write run wrote files into the working directory"

# ----- Shared JSON contracts (schema + name match) -----
validate_skill_json_contract "$repo_root" "$skill_json" "context-budget-audit"
validate_trigger_evals_contract "$repo_root" "$trigger_evals" "context-budget-audit"

if (( failures > 0 )); then
  exit 1
fi
echo "context-budget-audit static eval passed."
