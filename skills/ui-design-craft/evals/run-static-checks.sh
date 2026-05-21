#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(git -C "$script_dir" rev-parse --show-toplevel)"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"
skill_json="$skill_dir/skill.json"
registry="$skill_dir/references/use-case-registry.csv"

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
check_file "$skill_json"
check_file "$registry"
check_file "$skill_dir/templates/design-brief.md"
check_file "$skill_dir/templates/ui-plan.md"
check_file "$skill_dir/templates/review-report.md"
check_file "$skill_dir/templates/design-system-spec.md"
check_file "$skill_dir/templates/prototype-handoff.md"
check_file "$skill_dir/templates/deck-plan.md"
check_file "$skill_dir/templates/workflow-state.json"
check_file "$skill_dir/evals/activation-cases.md"
check_file "$skill_dir/evals/trigger-evals.json"

if [[ -f "$skill_json" ]]; then
  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/skill.schema.json" "$skill_json" \
    || fail "skill.json: schema validation failed"
  name=$(jq -r '.name' "$skill_json")
  [[ "$name" == "ui-design-craft" ]] || fail "skill.json name mismatch: $name"
  status=$(jq -r '.status' "$skill_json")
  [[ "$status" == "draft" ]] || fail "skill.json status must be draft, got $status"
fi

if [[ -f "$skill_md" ]]; then
  check_pattern 'frontmatter name' '^name:[[:space:]]*ui-design-craft$' "$skill_md"
  check_pattern 'frontmatter license' '^license:' "$skill_md"
  check_pattern 'bare activation' 'show the use-case menu' "$skill_md"
  check_pattern 'registry routing' 'use-case-registry\.csv' "$skill_md"
  check_pattern 'mode support' '^## Modes' "$skill_md"
  check_pattern 'subagent dispatch' '^## Subagent Dispatch' "$skill_md"
  wc=$(wc -w < "$skill_md")
  (( wc < 800 )) || fail "SKILL.md word count $wc exceeds 800"
fi

if [[ -f "$registry" ]]; then
  rows=$(grep -cE '^(product-ui|design-system|prototype|deck|motion-scene|host-handoff|quality-review),' "$registry")
  (( rows == 7 )) || fail "use-case-registry.csv: expected 7 data rows, got $rows"
  python3 - "$skill_dir" "$registry" <<'PYEOF' || fail "registry references missing files"
import csv
import sys
from pathlib import Path

skill_dir = Path(sys.argv[1])
registry = Path(sys.argv[2])
ok = True
with registry.open(newline="") as f:
    for row in csv.DictReader(f):
        for column in ("detail_files", "templates"):
            for rel in filter(None, (p.strip() for p in row.get(column, "").split(";"))):
                if not (skill_dir / rel).is_file():
                    print(f"missing {column}: {rel}", file=sys.stderr)
                    ok = False
sys.exit(0 if ok else 1)
PYEOF

  python3 - "$skill_dir" "$registry" <<'PYEOF' || fail "reference file not reachable from registry"
import csv
import sys
from pathlib import Path

skill_dir = Path(sys.argv[1])
registry = Path(sys.argv[2])
referenced = set()
with registry.open(newline="") as f:
    for row in csv.DictReader(f):
        for rel in filter(None, (p.strip() for p in row.get("detail_files", "").split(";"))):
            referenced.add(rel)

ok = True
for path in (skill_dir / "references").glob("*.md"):
    rel = path.relative_to(skill_dir).as_posix()
    if rel not in referenced:
        print(f"orphan reference: {rel}", file=sys.stderr)
        ok = False
sys.exit(0 if ok else 1)
PYEOF
fi

if [[ -f "$skill_json" ]]; then
  valid=" product-ui design-system prototype deck motion-scene host-handoff quality-review "
  while IFS= read -r p; do
    [[ -z "$p" ]] && continue
    [[ "$valid" == *" $p "* ]] || fail "skill.json inspired_by.playbooks has unknown value: $p"
  done < <(jq -r '.inspired_by[].playbooks[]?' "$skill_json")
fi

jq empty "$skill_dir/templates/workflow-state.json" || fail "workflow-state.json is invalid JSON"

if [[ -f "$skill_dir/evals/trigger-evals.json" ]]; then
  python3 "$repo_root/scripts/validate-against-schema.py" \
    "$repo_root/schemas/trigger-evals.schema.json" "$skill_dir/evals/trigger-evals.json" \
    || fail "trigger-evals.json: schema validation failed"
  trigger_skill=$(jq -r '.skill' "$skill_dir/evals/trigger-evals.json")
  [[ "$trigger_skill" == "ui-design-craft" ]] || fail "trigger-evals.json skill mismatch: $trigger_skill"
fi

if (( failures > 0 )); then
  printf '\nui-design-craft static eval failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'ui-design-craft static eval passed.\n'
