#!/usr/bin/env bash
# Static checks for the project-agentification skill.
# Exits non-zero on any failure.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../../scripts/static-check-lib.sh"
REPO_ROOT="$(repo_root_from "$SCRIPT_DIR")"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SKILL_DIR"

fail=0
note() { printf '  • %s\n' "$1"; }
err()  { printf '  ✗ %s\n' "$1" >&2; fail=1; }
ok()   { printf '  ✓ %s\n' "$1"; }

echo "Checking project-agentification skill at: $SKILL_DIR"

# 1. skill.json conforms to canonical schema and matches the directory.
validate_skill_json_contract "$REPO_ROOT" skill.json "project-agentification"

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
for csv in references/intent-router.csv references/surface-router.csv; do
  if [ -f "$csv" ]; then
    head -1 "$csv" | grep -q "," && ok "CSV has header: $csv" || err "CSV missing header: $csv"
  else
    err "CSV missing: $csv"
  fi
done

# 5. Every playbook referenced in surface-router.csv exists
# Use python csv module to parse properly (handles quoted comma-containing values)
if [ -f references/surface-router.csv ]; then
  while IFS= read -r path; do
    [ -z "$path" ] && continue
    if [ -f "references/$path" ]; then
      ok "playbook present: references/$path"
    else
      err "playbook missing: references/$path"
    fi
  done < <(python3 -c "
import csv
with open('references/surface-router.csv') as f:
    for row in csv.DictReader(f):
        print(row['playbook'])
")
fi

# 5b. Playbook progressive-disclosure discipline.
# These playbooks are allowed to be larger than DX/test playbooks because each
# surface carries cross-harness implementation tables, empirical warnings,
# examples, and scaffold-template pointers. They are still bounded: every
# playbook must use the same navigable section shape and stay under the
# explicit 3200-word ceiling (the largest current exception is gates.md).
if [ -d references/playbooks ]; then
  for pb in references/playbooks/*.md; do
    [ -f "$pb" ] || continue
    for section in '^## What it is' '^## Why it matters for agents' '^## Heuristics by intent' '^## Sources'; do
      if grep -Eq "$section" "$pb"; then
        :
      else
        err "$(basename "$pb") missing section ${section#^## }"
      fi
    done
    words="$(wc -w < "$pb" | tr -d ' ')"
    if [ "$words" -lt 900 ] || [ "$words" -gt 3200 ]; then
      err "$(basename "$pb") word count $words outside 900-3200 progressive-disclosure bound"
    else
      ok "playbook bounded: $(basename "$pb") ($words words)"
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

# 7c. Default tracking behavior for assessment findings
if grep -q "Create tracking state" SKILL.md; then
  ok "SKILL.md creates tracking state by default"
else
  err "SKILL.md must create tracking state by default for trackable assess outputs"
fi
if grep -q "project-agentification-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md" SKILL.md &&
   grep -q "project-agentification-workflow-state-<YYYY-MM-DD>-<scope-slug>.json" SKILL.md; then
  ok "SKILL.md uses skill-prefixed tracking filenames"
else
  err "SKILL.md missing project-agentification-prefixed ledger/workflow-state paths"
fi
if grep -q "audit-artifacts/project-agentification-" SKILL.md; then
  ok "SKILL.md preserves tracking fallback path"
else
  err "SKILL.md missing audit-artifacts/project-agentification fallback path"
fi
if grep -q "^## Findings ledger" templates/assess-report.md &&
   grep -q "do not merely offer" templates/assess-report.md &&
   grep -q "audit-artifacts/project-agentification-" templates/assess-report.md; then
  ok "assess report requires saved ledger/workflow-state artifacts"
else
  err "templates/assess-report.md must require saved tracking artifacts with fallback"
fi

# 7d. CI runner trust playbook
if grep -q '^control,ci-runners,' references/surface-router.csv &&
   [ -f references/playbooks/ci-runners.md ] &&
   grep -q 'self-hosted runners' references/playbooks/ci-runners.md &&
   grep -q 'required-check parity' references/playbooks/ci-runners.md; then
  ok "ci-runners surface is routed and covers runner trust"
else
  err "ci-runners playbook must be routed and cover self-hosted runner trust + required-check parity"
fi

# 8. Activation eval present
if [ -f evals/activation-cases.md ]; then
  ok "evals/activation-cases.md present"
else
  err "evals/activation-cases.md missing"
fi

# 9. evals/trigger-evals.json conforms to schema and matches the skill.
validate_trigger_evals_contract "$REPO_ROOT" evals/trigger-evals.json "project-agentification"

if [ "$fail" -ne 0 ]; then
  echo
  echo "Static checks FAILED."
  exit 1
fi

echo
echo "All static checks passed."
