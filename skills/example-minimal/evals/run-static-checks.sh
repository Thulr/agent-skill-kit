#!/usr/bin/env bash
set -euo pipefail

skill_dir="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
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
if [[ -f "$skill_md" ]]; then
  head -1 "$skill_md" | grep -q '^---$' || fail "SKILL.md missing YAML frontmatter delimiter (---)"
  grep -Eq '^name: example-minimal$' "$skill_md" || fail "SKILL.md frontmatter must include: name: example-minimal"
  grep -Eq '^description:' "$skill_md" || fail "SKILL.md frontmatter must include: description:"
  grep -Eq '^license:' "$skill_md" || fail "SKILL.md frontmatter must include: license:"
fi

# ----- skill.json gates -----
if [[ -f "$skill_json" ]]; then
  jq . "$skill_json" > /dev/null 2>&1 || fail "skill.json: invalid JSON"
  name=$(jq -r '.name' "$skill_json")
  [[ "$name" == "example-minimal" ]] || fail "skill.json: name must be example-minimal, got $name"

  status=$(jq -r '.status' "$skill_json")
  case "$status" in
    draft|reviewed|published) ;;
    *) fail "skill.json: status must be draft/reviewed/published, got $status" ;;
  esac

  python3 - "$skill_json" <<'PYEOF' || fail "skill.json: maintainers must be resolvable GitHub handles (@user or @org/team)"
import json, re, sys
path = sys.argv[1]
with open(path) as f:
  data = json.load(f)
maintainers = data.get("maintainers")
if not isinstance(maintainers, list) or not maintainers:
  raise SystemExit("skill.json: maintainers must be a non-empty list")
pat = re.compile(r"^@[A-Za-z0-9-]+(?:/[A-Za-z0-9-]+)?$")
for m in maintainers:
  if not isinstance(m, str) or not pat.match(m):
    raise SystemExit(f"skill.json: invalid maintainer handle: {m!r}")
PYEOF

  count=$(jq '.inspired_by | length' "$skill_json")
  (( count > 0 )) || fail "skill.json: inspired_by must be non-empty"
  missing=$(jq -r '.inspired_by | map(select(.name == null or .author == null or .kind == null or .contribution == null)) | length' "$skill_json")
  (( missing == 0 )) || fail "skill.json: $missing inspired_by entry/entries missing required fields"
fi

# ----- trigger-evals.json schema gate -----
# Canonical schema (see AGENTS.md §Canonical trigger-evals.json schema).
if [[ -f "$trigger_evals" ]]; then
  python3 - "$trigger_evals" "example-minimal" <<'PYEOF' || fail "trigger-evals.json schema check failed"
import json, sys
path, expected_skill = sys.argv[1], sys.argv[2]
try:
  with open(path) as f:
    data = json.load(f)
except json.JSONDecodeError as e:
  print(f"trigger-evals.json: invalid JSON ({e})", file=sys.stderr); sys.exit(1)
if not isinstance(data, dict):
  print("trigger-evals.json: top-level must be object", file=sys.stderr); sys.exit(1)
if data.get("skill") != expected_skill:
  print(f"trigger-evals.json: 'skill' must be {expected_skill!r}, got {data.get('skill')!r}", file=sys.stderr); sys.exit(1)
version = data.get("version")
if not isinstance(version, str) or not version.strip():
  print("trigger-evals.json: 'version' must be a non-empty string (canonical schema)", file=sys.stderr); sys.exit(1)
queries = data.get("queries")
if not isinstance(queries, list) or not queries:
  print("trigger-evals.json: 'queries' must be a non-empty list", file=sys.stderr); sys.exit(1)
errors = 0
for i, q in enumerate(queries):
  if not isinstance(q, dict):
    print(f"trigger-evals.json[{i}]: must be object", file=sys.stderr); errors += 1; continue
  if not isinstance(q.get("query"), str) or not q["query"].strip():
    print(f"trigger-evals.json[{i}]: 'query' must be non-empty string", file=sys.stderr); errors += 1
  if not isinstance(q.get("should_activate"), bool):
    print(f"trigger-evals.json[{i}]: 'should_activate' must be bool", file=sys.stderr); errors += 1
  er = q.get("expected_route")
  if er is not None and not isinstance(er, str):
    print(f"trigger-evals.json[{i}]: 'expected_route' must be string or null", file=sys.stderr); errors += 1
  cat = q.get("category")
  if cat is not None and cat not in ("positive", "negative", "edge"):
    print(f"trigger-evals.json[{i}]: 'category' must be positive|negative|edge or null", file=sys.stderr); errors += 1
sys.exit(1 if errors else 0)
PYEOF
fi

if (( failures > 0 )); then
  exit 1
fi

echo "example-minimal static eval passed."
