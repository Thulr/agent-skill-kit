#!/usr/bin/env bash
# Static checks for the project-agentification skill.
# Exits non-zero on any failure.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SKILL_DIR"

fail=0
note() { printf '  • %s\n' "$1"; }
err()  { printf '  ✗ %s\n' "$1" >&2; fail=1; }
ok()   { printf '  ✓ %s\n' "$1"; }

echo "Checking project-agentification skill at: $SKILL_DIR"

# 1. skill.json conforms to canonical schema (schemas/skill.schema.json)
#    Shape (name presence/type, status enum, maintainer handle pattern, inspired_by
#    required fields) lives in the schema. Per-skill name match is asserted below.
if python3 "$REPO_ROOT/scripts/validate-against-schema.py" \
     "$REPO_ROOT/schemas/skill.schema.json" skill.json; then
  ok "skill.json conforms to schemas/skill.schema.json"
else
  err "skill.json schema validation failed (see above)"
fi

# 1b. skill name matches the directory
actual_name="$(python3 -c "import json; print(json.load(open('skill.json'))['name'])")"
if [ "$actual_name" = "project-agentification" ]; then
  ok "skill.json name == project-agentification"
else
  err "skill.json name is $actual_name, expected project-agentification"
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
for f in references/core/maturity-rubric.md references/core/severity-rubric.md references/empirical-warnings.md references/lenses.md references/trackable-findings.md; do
  if [ -f "$f" ]; then
    ok "present: $f"
  else
    err "missing: $f"
  fi
done

# 7b. Shared tracking artifacts
for f in templates/findings-ledger.md templates/roadmap.md templates/github-issue.md templates/workflow-state.json; do
  if [ -f "$f" ]; then
    ok "tracking artifact present: $f"
  else
    err "tracking artifact missing: $f"
  fi
done

# 8. Activation eval present
if [ -f evals/activation-cases.md ]; then
  ok "evals/activation-cases.md present"
else
  err "evals/activation-cases.md missing"
fi

# 9. evals/trigger-evals.json conforms to schemas/trigger-evals.schema.json.
#    Per-skill 'skill' field is asserted below.
if [ -f evals/trigger-evals.json ]; then
  if python3 "$REPO_ROOT/scripts/validate-against-schema.py" \
       "$REPO_ROOT/schemas/trigger-evals.schema.json" evals/trigger-evals.json; then
    ok "trigger-evals.json conforms to schemas/trigger-evals.schema.json"
  else
    err "trigger-evals.json schema validation failed (see above)"
  fi
  trigger_skill="$(python3 -c "import json; print(json.load(open('evals/trigger-evals.json'))['skill'])")"
  if [ "$trigger_skill" = "project-agentification" ]; then
    ok "trigger-evals.json 'skill' field == project-agentification"
  else
    err "trigger-evals.json 'skill' is $trigger_skill, expected project-agentification"
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
