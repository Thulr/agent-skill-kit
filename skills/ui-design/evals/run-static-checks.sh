#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"
skill_json="$skill_dir/skill.json"
router="$skill_dir/references/intent-router.csv"

SKILL_NAME="ui-design"
INTENTS=(product-ui design-system prototype deck motion-scene host-handoff quality-review)

failures=0
fail() { printf 'FAIL %s\n' "$1" >&2; failures=$((failures + 1)); }
check_file() { [[ -f "$1" || -L "$1" ]] || fail "missing file: $1"; }
check_pattern() {
  local label="$1" pattern="$2" path="$3"
  grep -Eq -- "$pattern" "$path" || fail "$label: pattern not found in $path"
}

# ----- File presence -----
check_file "$skill_md"
check_file "$skill_json"
check_file "$router"
check_file "$skill_dir/references/starter-scenarios.csv"
check_file "$skill_dir/references/modes.md"
check_file "$skill_dir/templates/design-brief.md"
check_file "$skill_dir/templates/ui-plan.md"
check_file "$skill_dir/templates/review-report.md"
check_file "$skill_dir/templates/design-system-spec.md"
check_file "$skill_dir/templates/prototype-handoff.md"
check_file "$skill_dir/templates/deck-plan.md"
check_file "$skill_dir/templates/workflow-state.json"
check_file "$skill_dir/evals/activation-cases.md"
check_file "$skill_dir/evals/trigger-evals.json"

# ----- skill.json contract -----
validate_skill_json_contract "$repo_root" "$skill_json" "$SKILL_NAME"
if [[ -f "$skill_json" ]]; then
  status=$(jq -r '.status' "$skill_json")
  [[ "$status" == "published" ]] || fail "skill.json status must be published, got $status"
fi

# ----- SKILL.md cleanliness + word bound -----
author_stoplist=" Foundation Council Parliament Committee Group Working contributors notes team Initiative "
if [[ -f "$skill_md" && -f "$skill_json" ]]; then
  while IFS= read -r author; do
    [[ -n "$author" ]] || continue
    last="${author##* }"
    if [[ "$author_stoplist" == *" $last "* ]] || [[ "$author" == "$last" ]]; then
      grep -qF -- "$author" "$skill_md" && fail "SKILL.md leaks source author: $author"
    else
      grep -qw -- "$last" "$skill_md" && fail "SKILL.md leaks source author last name: $last"
    fi
  done < <(jq -r '.inspired_by[].author' "$skill_json")
  while IFS= read -r title; do
    [[ -n "$title" ]] || continue
    grep -qF -- "$title" "$skill_md" && fail "SKILL.md leaks source title: $title"
  done < <(jq -r '.inspired_by[].name' "$skill_json")
  wc=$(wc -w < "$skill_md")
  (( wc < 800 )) || fail "SKILL.md word count $wc exceeds 800 (runtime-only bound)"
fi

# ----- SKILL.md structural gates -----
if [[ -f "$skill_md" ]]; then
  check_pattern 'frontmatter name' "^name:[[:space:]]*$SKILL_NAME$" "$skill_md"
  check_pattern 'frontmatter license' '^license:' "$skill_md"
  check_pattern 'bare activation menu' 'show the intent menu' "$skill_md"
  check_pattern 'router routing' 'intent-router\.csv' "$skill_md"
  check_pattern 'mode support' '^## Modes' "$skill_md"
  check_pattern 'subagent dispatch' '^## Subagent dispatch' "$skill_md"
  check_pattern 'routes audits elsewhere' 'ux-audit' "$skill_md"
  check_pattern 'routes dev surfaces elsewhere' 'dx-design' "$skill_md"
fi

# ----- One-layer intent-router well-formedness -----
if [[ -f "$router" ]]; then
  rows=$(grep -cE '^(product-ui|design-system|prototype|deck|motion-scene|host-handoff|quality-review),' "$router")
  (( rows == 7 )) || fail "intent-router.csv: expected 7 data rows, got $rows"

  # Every detail_files / templates entry resolves to a real file.
  python3 - "$skill_dir" "$router" <<'PYEOF' || fail "router references missing files"
import csv, sys
from pathlib import Path
skill_dir = Path(sys.argv[1]); router = Path(sys.argv[2]); ok = True
with router.open(newline="") as f:
    for row in csv.DictReader(f):
        for column in ("detail_files", "templates"):
            for rel in filter(None, (p.strip() for p in row.get(column, "").split(";"))):
                if not (skill_dir / rel).is_file():
                    print(f"missing {column}: {rel}", file=sys.stderr); ok = False
sys.exit(0 if ok else 1)
PYEOF

  # No orphan reference .md files (every references/*.md reachable from router).
  python3 - "$skill_dir" "$router" <<'PYEOF' || fail "reference file not reachable from router"
import csv, sys
from pathlib import Path
skill_dir = Path(sys.argv[1]); router = Path(sys.argv[2]); referenced = set()
with router.open(newline="") as f:
    for row in csv.DictReader(f):
        for rel in filter(None, (p.strip() for p in row.get("detail_files", "").split(";"))):
            referenced.add(rel)
ok = True
for path in (skill_dir / "references").glob("*.md"):
    rel = path.relative_to(skill_dir).as_posix()
    if rel not in referenced:
        print(f"orphan reference: {rel}", file=sys.stderr); ok = False
sys.exit(0 if ok else 1)
PYEOF
fi

# ----- skill.json playbooks-field gate (values map to the 7 intents) -----
if [[ -f "$skill_json" ]]; then
  valid=" "; for i in "${INTENTS[@]}"; do valid+="$i "; done
  while IFS= read -r p; do
    [[ -z "$p" ]] && continue
    [[ "$valid" == *" $p "* ]] || fail "skill.json inspired_by.playbooks has unknown value: $p"
  done < <(jq -r '.inspired_by[].playbooks[]?' "$skill_json")
fi

# ----- Tracking artifact validity -----
jq empty "$skill_dir/templates/workflow-state.json" || fail "workflow-state.json is invalid JSON"

# ----- trigger-evals contract -----
validate_trigger_evals_contract "$repo_root" "$skill_dir/evals/trigger-evals.json" "$SKILL_NAME"

if (( failures > 0 )); then
  printf '\n%s static eval failed with %d issue(s).\n' "$SKILL_NAME" "$failures" >&2
  exit 1
fi
printf '%s static eval passed.\n' "$SKILL_NAME"
