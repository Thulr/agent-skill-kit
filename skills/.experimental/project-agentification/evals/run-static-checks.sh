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
if [ -f references/layer-router.csv ]; then
  # Column 4 expected to be the playbook path (relative to references/)
  tail -n +2 references/layer-router.csv | awk -F',' '{print $4}' | while read -r path; do
    [ -z "$path" ] && continue
    if [ -f "references/$path" ]; then
      ok "playbook present: references/$path"
    else
      err "playbook missing: references/$path"
    fi
  done
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

if [ "$fail" -ne 0 ]; then
  echo
  echo "Static checks FAILED."
  exit 1
fi

echo
echo "All static checks passed."
