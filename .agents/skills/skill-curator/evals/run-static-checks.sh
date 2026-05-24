#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"
registry="$skill_dir/references/intent-router.csv"

failures=0

fail() {
  printf 'FAIL %s\n' "$1" >&2
  failures=$((failures + 1))
}

check_file() {
  [[ -f "$1" || -L "$1" ]] || fail "missing file: $1"
}

check_pattern() {
  local label="$1" pattern="$2" path="$3"
  grep -Eq -- "$pattern" "$path" || fail "$label: pattern not found in $path"
}

check_file "$skill_md"
check_file "$registry"
check_file "$skill_dir/references/research-dossier-playbook.md"
check_file "$skill_dir/references/pack-placement-rubric.md"
check_file "$skill_dir/references/depth-rubric.md"
check_file "$skill_dir/references/draft-skill-playbook.md"
check_file "$skill_dir/references/shapes/flat.md"
check_file "$skill_dir/references/shapes/single-layer.md"
check_file "$skill_dir/references/shapes/two-level.md"
check_file "$skill_dir/references/validation-rubrics/flat.md"
check_file "$skill_dir/references/validation-rubrics/single-layer.md"
check_file "$skill_dir/references/validation-rubrics/two-level.md"
check_file "$skill_dir/templates/intake-brief.md"
check_file "$skill_dir/templates/source-dossier.md"
check_file "$skill_dir/templates/candidate-plan.md"
check_file "$skill_dir/templates/playbook-skeletons/flat.md"
check_file "$skill_dir/templates/playbook-skeletons/single-layer.md"
check_file "$skill_dir/templates/playbook-skeletons/two-level.md"
check_file "$skill_dir/templates/activation-cases-skeleton.md"
check_file "$skill_dir/evals/activation-cases.md"

check_pattern 'frontmatter name' '^name:[[:space:]]*skill-curator$' "$skill_md"
check_pattern 'registry routing' 'intent-router\.csv' "$skill_md"
check_pattern 'published status contract' 'status` to `published`' "$skill_md"
check_pattern 'repo tag maturity contract' 'repository tag' "$skill_md"
check_pattern 'five-phase workflow named' 'five (named )?phases' "$skill_md"
check_pattern 'phase 1 intake' 'Phase 1 . Intake' "$skill_md"
check_pattern 'phase 5 validate' 'Phase 5 . Validate' "$skill_md"
check_pattern 'hard gate language' '(hard phase gate|hard user-confirmation|hard gates between)' "$skill_md"

check_pattern 'flat route renamed' '^create-flat,' "$registry"
check_pattern 'single-layer route renamed' '^create-single-layer,' "$registry"
check_pattern 'two-level route renamed' '^create-two-level,' "$registry"

check_pattern 'flat evals required' 'Required in this repo' "$skill_dir/references/shapes/flat.md"
check_pattern 'single-layer trigger evals required' 'trigger-evals\.json' "$skill_dir/references/shapes/single-layer.md"
check_pattern 'single-layer static checks required' 'Every public skill in this repo has `evals/run-static-checks\.sh`' "$skill_dir/references/shapes/single-layer.md"
check_pattern 'playbook published status' '"status": "published"' "$skill_dir/references/draft-skill-playbook.md"
check_pattern 'quality bar published status' 'skill\.json\.status` is `published`' "$skill_dir/references/draft-skill-playbook.md"

check_pattern 'intake brief audience slot' '## Audience' "$skill_dir/templates/intake-brief.md"
check_pattern 'intake brief success slot' '## Success criteria' "$skill_dir/templates/intake-brief.md"
check_pattern 'dossier confidence rules' 'Confidence rules' "$skill_dir/templates/source-dossier.md"
check_pattern 'dossier paraphrase audit' '## Paraphrase Audit' "$skill_dir/templates/source-dossier.md"
check_pattern 'dossier critical takes' '## Critical / Dissenting Takes' "$skill_dir/templates/source-dossier.md"
check_pattern 'candidate plan anti-pattern check' 'Anti-pattern self-check' "$skill_dir/templates/candidate-plan.md"
check_pattern 'candidate plan grounding map' 'grounding_map' "$skill_dir/templates/candidate-plan.md"
check_pattern 'flat skeleton headings' '## When to use' "$skill_dir/templates/playbook-skeletons/flat.md"
check_pattern 'single-layer skeleton heuristics' '## Heuristics' "$skill_dir/templates/playbook-skeletons/single-layer.md"
check_pattern 'two-level skeleton sections' '## Quick diagnostic' "$skill_dir/templates/playbook-skeletons/two-level.md"
check_pattern 'activation skeleton negative' 'sibling skill' "$skill_dir/templates/activation-cases-skeleton.md"

python3 - "$skill_dir" "$registry" <<'PYEOF' || fail "registry references missing files"
import csv
import sys
from pathlib import Path

skill_dir = Path(sys.argv[1])
registry = Path(sys.argv[2])
ok = True

with registry.open(newline="") as f:
    for row in csv.DictReader(f):
        for column in ("detail_file", "templates"):
            for rel in filter(None, (p.strip() for p in row.get(column, "").split(";"))):
                path = skill_dir / rel
                if column == "detail_file" and not path.exists():
                    path = skill_dir / "references" / rel
                if not path.is_file():
                    print(f"missing {column}: {rel}", file=sys.stderr)
                    ok = False

sys.exit(0 if ok else 1)
PYEOF

if (( failures > 0 )); then
  printf '\nskill-curator static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'skill-curator static eval passed.\n'
