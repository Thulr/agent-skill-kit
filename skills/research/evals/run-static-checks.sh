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

# ----- Frame router + per-frame workflows (the merge contract) -----
check_file "$skill_dir/references/frame-router.csv"
check_file "$skill_dir/references/report/workflow.md"
check_file "$skill_dir/references/opportunity/workflow.md"

# ----- Report frame surfaces (formerly topic-research) -----
for f in search-strategy.md source-triage.md confidence-rubric.md modes.md; do
  check_file "$skill_dir/references/report/$f"
done
check_file "$skill_dir/templates/report/research-report.md"

# ----- Opportunity frame surfaces (formerly opportunity-research) -----
check_file "$skill_dir/references/opportunity/intent-router.csv"
for intent in scope investigate synthesize decide; do
  check_file "$skill_dir/references/opportunity/intents/$intent.csv"
done
for core in severity-rubric.md confidence-rubric.md fadr-framework.md personas.md decision-gates.md modes.md; do
  check_file "$skill_dir/references/opportunity/core/$core"
done
check_file "$skill_dir/references/opportunity/subagent-dispatch.md"
check_file "$skill_dir/references/opportunity/trackable-findings.md"
check_file "$skill_dir/references/opportunity/starter-scenarios.csv"
for t in scope-plan investigation-brief cross-area-brief fadr-memo; do
  check_file "$skill_dir/templates/opportunity/$t.md"
done
# 14 area artifacts must all survive the move
artifact_count=$(find "$skill_dir/templates/opportunity/artifacts" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
(( artifact_count == 14 )) || fail "expected 14 opportunity area artifacts, found $artifact_count"

# ----- Opportunity routing integrity (every CSV path token must resolve) -----
# The opportunity sub-tree was relocated under references/opportunity/ +
# templates/opportunity/ during the research merge; its router/intents CSVs
# once carried pre-move paths (references/intents/*, templates/*) that resolved
# to nothing. This validates every references//templates/ token in the
# intent-router and its intent CSVs (registry_file, default_template, playbook,
# core_refs, artifact_template, output_template) against the skill on disk.
while IFS= read -r missing; do
  [[ -n "$missing" ]] && fail "opportunity routing CSV points at missing path: $missing"
done < <(python3 - "$skill_dir" <<'PYEOF'
import csv, os, re, sys, glob
skill = sys.argv[1]
pathlike = re.compile(r'^(references|templates)/[A-Za-z0-9_./-]+\.(csv|md)$')
csvs = [os.path.join(skill, 'references/opportunity/intent-router.csv')] + \
       sorted(glob.glob(os.path.join(skill, 'references/opportunity/intents/*.csv')))
for p in csvs:
    if not os.path.exists(p):
        continue
    with open(p, newline='') as fh:
        for row in csv.DictReader(fh):
            for v in row.values():
                if not v:
                    continue
                for tok in v.split(';'):
                    tok = tok.strip()
                    if pathlike.match(tok) and not os.path.exists(os.path.join(skill, tok)):
                        print(tok)
PYEOF
)

# ----- SKILL.md frontmatter + word-count gate -----
if [[ -f "$skill_md" ]]; then
  head -1 "$skill_md" | grep -q '^---$' || fail "SKILL.md missing YAML frontmatter delimiter (---)"
  grep -Eq '^name: research$' "$skill_md" || fail "SKILL.md frontmatter must include: name: research"
  grep -Eq '^description:' "$skill_md" || fail "SKILL.md frontmatter must include: description:"
  grep -Eq '^license:' "$skill_md" || fail "SKILL.md frontmatter must include: license:"
  # Thin frame-router body (detail lives in references/<frame>/workflow.md).
  wc=$(wc -w < "$skill_md")
  (( wc < 1200 )) || fail "SKILL.md word count $wc exceeds 1200 (runtime-only bound; per-frame detail belongs in references/<frame>/workflow.md)"
fi

# ----- Shared JSON contracts -----
validate_skill_json_contract "$repo_root" "$skill_json" "research"
validate_trigger_evals_contract "$repo_root" "$trigger_evals" "research"

if (( failures > 0 )); then
  exit 1
fi
echo "research static eval passed."
