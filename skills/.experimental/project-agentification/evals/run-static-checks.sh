#!/usr/bin/env bash
# Static checks for the project-agentification skill.
# Exits non-zero on any failure.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

fail=0
note() { printf '  • %s\n' "$1"; }
err()  { printf '  ✗ %s\n' "$1" >&2; fail=1; }
ok()   { printf '  ✓ %s\n' "$1"; }

echo "Checking project-agentification skill at: $SKILL_DIR"

# 1. skill.json parses
if python3 -c "import json,sys; json.load(open('skill.json'))" 2>/dev/null; then
  ok "skill.json is valid JSON"
else
  err "skill.json failed to parse"
fi

# 1b. skill.json identity fields are resolvable (AGENTS.md Rule 4)
if python3 - <<'PY' 2>/dev/null; then
import json, re
data = json.load(open("skill.json"))
assert data.get("name") == "project-agentification"
status = data.get("status")
assert status in {"draft", "reviewed", "published"}
maintainers = data.get("maintainers")
assert isinstance(maintainers, list) and maintainers
pat = re.compile(r"^@[A-Za-z0-9-]+(?:/[A-Za-z0-9-]+)?$")
for m in maintainers:
  assert isinstance(m, str) and pat.match(m), m
PY
  ok "skill.json identity fields are valid (status + maintainers)"
else
  err "skill.json identity fields invalid (status must be draft/reviewed/published; maintainers must be @handles)"
fi

# 2. SKILL.md has frontmatter
if [ -f SKILL.md ] && head -1 SKILL.md | grep -q '^---$'; then
  ok "SKILL.md has frontmatter"
else
  err "SKILL.md missing or missing frontmatter"
fi

# 3. Required directories
for d in references references/playbooks references/core templates evals; do
  if [ -d "$d" ]; then
    ok "directory exists: $d"
  else
    err "missing directory: $d"
  fi
done

# 4. CSV routers exist and have headers
for csv in references/intent-router.csv references/layer-router.csv; do
  if [ -f "$csv" ]; then
    head -1 "$csv" | grep -q "," && ok "CSV has header: $csv" || err "CSV missing header: $csv"
  else
    err "CSV missing: $csv"
  fi
done

# 5. Every playbook referenced in layer-router.csv exists
# Use python csv module to parse properly (handles quoted comma-containing values)
if [ -f references/layer-router.csv ]; then
  while IFS= read -r path; do
    [ -z "$path" ] && continue
    if [ -f "references/$path" ]; then
      ok "playbook present: references/$path"
    else
      err "playbook missing: references/$path"
    fi
  done < <(python3 -c "
import csv
with open('references/layer-router.csv') as f:
    for row in csv.DictReader(f):
        print(row['playbook'])
")
fi

# 6. Templates exist
for t in assess-report harden-recommendation scaffold-bundle diagnose-runbook; do
  if [ -f "templates/$t.md" ]; then
    ok "template present: templates/$t.md"
  else
    err "template missing: templates/$t.md"
  fi
done

# 7. Core rubrics + warnings
for f in references/core/maturity-rubric.md references/core/severity-rubric.md references/empirical-warnings.md references/lenses.md; do
  if [ -f "$f" ]; then
    ok "present: $f"
  else
    err "missing: $f"
  fi
done

# 8. Activation eval present
if [ -f evals/activation-cases.md ]; then
  ok "evals/activation-cases.md present"
else
  err "evals/activation-cases.md missing"
fi

# 9. trigger-evals.json schema (canonical shape — see AGENTS.md §Canonical
#    trigger-evals.json schema). Schema changes migrate all skills in the same
#    PR (Rule 2 in AGENTS.md).
if [ -f evals/trigger-evals.json ]; then
  if python3 - evals/trigger-evals.json "project-agentification" <<'PYEOF' >&2; then
import json, sys
path, expected_skill = sys.argv[1], sys.argv[2]
try:
    with open(path) as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"trigger-evals.json: invalid JSON ({e})"); sys.exit(1)
if not isinstance(data, dict):
    print("trigger-evals.json: top-level must be object"); sys.exit(1)
if data.get("skill") != expected_skill:
    print(f"trigger-evals.json: 'skill' must be {expected_skill!r}, got {data.get('skill')!r}"); sys.exit(1)
version = data.get("version")
if not isinstance(version, str) or not version.strip():
    print("trigger-evals.json: 'version' must be a non-empty string (canonical schema, AGENTS.md §Canonical trigger-evals.json schema)"); sys.exit(1)
queries = data.get("queries")
if not isinstance(queries, list) or not queries:
    print("trigger-evals.json: 'queries' must be a non-empty list"); sys.exit(1)
errors = 0
for i, q in enumerate(queries):
    if not isinstance(q, dict):
        print(f"trigger-evals.json[{i}]: must be object"); errors += 1; continue
    if not isinstance(q.get("query"), str) or not q["query"].strip():
        print(f"trigger-evals.json[{i}]: 'query' must be non-empty string"); errors += 1
    if not isinstance(q.get("should_activate"), bool):
        print(f"trigger-evals.json[{i}]: 'should_activate' must be bool"); errors += 1
    er = q.get("expected_route")
    if er is not None and not isinstance(er, str):
        print(f"trigger-evals.json[{i}]: 'expected_route' must be string or null"); errors += 1
    cat = q.get("category")
    if cat is not None and cat not in ("positive", "negative", "edge"):
        print(f"trigger-evals.json[{i}]: 'category' must be positive|negative|edge or null"); errors += 1
if errors > 0:
    sys.exit(1)
PYEOF
    ok "trigger-evals.json schema valid"
  else
    err "trigger-evals.json schema check failed"
  fi
else
  err "evals/trigger-evals.json missing"
fi

if [ "$fail" -ne 0 ]; then
  echo
  echo "Static checks FAILED."
  exit 1
fi

echo
echo "All static checks passed."
