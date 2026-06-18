#!/usr/bin/env bash
# Static checks for the rules-from-coding-agent-failures skill.
# Exits non-zero on any failure.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../../scripts/static-check-lib.sh"
REPO_ROOT="$(repo_root_from "$SCRIPT_DIR")"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SKILL_DIR"

fail=0
err()  { printf '  ✗ %s\n' "$1" >&2; fail=1; }
ok()   { printf '  ✓ %s\n' "$1"; }

echo "Checking rules-from-coding-agent-failures skill at: $SKILL_DIR"

# 1. skill.json conforms to canonical schema and matches the directory
validate_skill_json_contract "$REPO_ROOT" skill.json "rules-from-coding-agent-failures"

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
for f in references/empirical-warnings.md references/lenses.md references/trackable-findings.md; do
  if [ -L "$f" ]; then
    target=$(readlink "$f")
    case "$target" in
      ../../_shared/*|../../../_shared/*) ok "$f -> $target" ;;
      *) err "$f is a symlink to '$target' — expected relative path into skills/_shared/<file>" ;;
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

# 7. Promotion playbooks
for f in references/playbooks/reflection-log.md references/playbooks/gate-hardening.md; do
  if [ -f "$f" ]; then
    ok "playbook present: $f"
  else
    err "playbook missing: $f"
  fi
done
if grep -q "gate-hardening variant matrix" SKILL.md &&
   grep -q "references/playbooks/gate-hardening.md" SKILL.md; then
  ok "SKILL.md routes promoted gates through gate-hardening"
else
  err "SKILL.md must route hook/CI/static-gate promotion through gate-hardening"
fi
if grep -q "Variant Matrix" references/playbooks/gate-hardening.md &&
   grep -q "CI parity" references/playbooks/gate-hardening.md &&
   grep -q "Shared-Content Requirements" references/playbooks/gate-hardening.md; then
  ok "gate-hardening playbook covers variants, CI parity, and shared-content gates"
else
  err "gate-hardening playbook missing required hardening sections"
fi

# 8. Artifact templates for the reflection-log directory
for f in templates/artifacts/reflection-log/README.md templates/artifacts/reflection-log/_template.md; do
  if [ -f "$f" ]; then
    ok "artifact template present: $f"
  else
    err "artifact template missing: $f"
  fi
done

# 8b. Tracking artifacts for assess-l4l5 findings
for f in templates/findings-ledger.md templates/workflow-state.json; do
  if [ -f "$f" ]; then
    ok "tracking artifact present: $f"
  else
    err "tracking artifact missing: $f"
  fi
done
if grep -q "Create tracking state" SKILL.md &&
   grep -q "rules-from-coding-agent-failures-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md" SKILL.md &&
   grep -q "rules-from-coding-agent-failures-workflow-state-<YYYY-MM-DD>-<scope-slug>.json" SKILL.md; then
  ok "SKILL.md creates skill-prefixed assess-l4l5 tracking state"
else
  err "SKILL.md missing default assess-l4l5 tracking artifact behavior"
fi
if grep -q "audit-artifacts/rules-from-coding-agent-failures-" SKILL.md; then
  ok "SKILL.md preserves tracking fallback path"
else
  err "SKILL.md missing audit-artifacts/rules-from-coding-agent-failures fallback path"
fi

# 9. Activation eval present
if [ -f evals/activation-cases.md ]; then
  ok "evals/activation-cases.md present"
else
  err "evals/activation-cases.md missing"
fi

# 10. evals/trigger-evals.json conforms to schema and matches the skill
validate_trigger_evals_contract "$REPO_ROOT" evals/trigger-evals.json "rules-from-coding-agent-failures"

if [ "$fail" -ne 0 ]; then
  echo
  echo "Static checks FAILED."
  exit 1
fi

echo
echo "All static checks passed."
