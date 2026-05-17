#!/usr/bin/env bash
# Static checks for the evidence-driven-agent-rules skill.
# Exits non-zero on any failure.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SKILL_DIR"

fail=0
err()  { printf '  ✗ %s\n' "$1" >&2; fail=1; }
ok()   { printf '  ✓ %s\n' "$1"; }

echo "Checking evidence-driven-agent-rules skill at: $SKILL_DIR"

# 1. skill.json conforms to canonical schema
if python3 "$REPO_ROOT/scripts/validate-against-schema.py" \
     "$REPO_ROOT/schemas/skill.schema.json" skill.json; then
  ok "skill.json conforms to schemas/skill.schema.json"
else
  err "skill.json schema validation failed (see above)"
fi

# 1b. skill name matches the directory
actual_name="$(python3 -c "import json; print(json.load(open('skill.json'))['name'])")"
if [ "$actual_name" = "evidence-driven-agent-rules" ]; then
  ok "skill.json name == evidence-driven-agent-rules"
else
  err "skill.json name is $actual_name, expected evidence-driven-agent-rules"
fi

# 2. SKILL.md has frontmatter
if [ -f SKILL.md ] && head -1 SKILL.md | grep -q '^---$'; then
  ok "SKILL.md has frontmatter"
else
  err "SKILL.md missing or missing frontmatter"
fi

# 3. Required directories
for d in references references/playbooks references/core templates templates/artifacts/reflection-log evals; do
  if [ -d "$d" ]; then
    ok "directory exists: $d"
  else
    err "missing directory: $d"
  fi
done

# 4. W1 sole-tenant file (this skill owns W1; shared file has W2–W10)
if [ -f references/empirical-warnings-w1.md ]; then
  ok "references/empirical-warnings-w1.md present"
else
  err "references/empirical-warnings-w1.md missing — W1 belongs to this skill"
fi

# 5. Shared symlinks: empirical-warnings.md and lenses.md must be symlinks
#    into skills/_shared/. The repo-level scripts/check-shared-content.sh
#    enforces the structural invariants in detail; here we just assert presence.
for f in references/empirical-warnings.md references/lenses.md; do
  if [ -L "$f" ]; then
    target=$(readlink "$f")
    case "$target" in
      ../../../_shared/*) ok "$f -> $target" ;;
      *) err "$f is a symlink to '$target' — expected ../../../_shared/<file>" ;;
    esac
  elif [ -f "$f" ]; then
    err "$f exists as a regular file — must be a symlink into skills/_shared/ (see scripts/check-shared-content.sh)"
  else
    err "$f missing — should symlink to skills/_shared/$(basename "$f")"
  fi
done

# 6. Level 4–5 maturity rubric extension (this skill's portion)
if [ -f references/core/maturity-rubric.md ]; then
  ok "references/core/maturity-rubric.md present (Levels 4–5 extension)"
else
  err "references/core/maturity-rubric.md missing"
fi

# 7. Reflection-log playbook
if [ -f references/playbooks/reflection-log.md ]; then
  ok "playbook present: references/playbooks/reflection-log.md"
else
  err "playbook missing: references/playbooks/reflection-log.md"
fi

# 8. Artifact templates for the reflection-log directory
for f in templates/artifacts/reflection-log/README.md templates/artifacts/reflection-log/_template.md; do
  if [ -f "$f" ]; then
    ok "artifact template present: $f"
  else
    err "artifact template missing: $f"
  fi
done

# 9. Activation eval present
if [ -f evals/activation-cases.md ]; then
  ok "evals/activation-cases.md present"
else
  err "evals/activation-cases.md missing"
fi

# 10. evals/trigger-evals.json conforms to schema
if [ -f evals/trigger-evals.json ]; then
  if python3 "$REPO_ROOT/scripts/validate-against-schema.py" \
       "$REPO_ROOT/schemas/trigger-evals.schema.json" evals/trigger-evals.json; then
    ok "trigger-evals.json conforms to schemas/trigger-evals.schema.json"
  else
    err "trigger-evals.json schema validation failed (see above)"
  fi
  trigger_skill="$(python3 -c "import json; print(json.load(open('evals/trigger-evals.json'))['skill'])")"
  if [ "$trigger_skill" = "evidence-driven-agent-rules" ]; then
    ok "trigger-evals.json 'skill' field == evidence-driven-agent-rules"
  else
    err "trigger-evals.json 'skill' is $trigger_skill, expected evidence-driven-agent-rules"
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
