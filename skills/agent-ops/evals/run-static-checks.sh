#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"

python3 "$repo_root/scripts/check-skill-static.py" \
  --repo-root "$repo_root" \
  --skill-dir "$skill_dir" \
  --skill agent-ops \
  --shape two-layer-audit \
  --intents do,review,design \
  --tracking required \
  `# 880 (vs the 800 default): agent-ops is the family FRONT-DOOR, so it carries a` \
  `# runtime "## Front-door — routing out" section the leaf agent skills do not.` \
  --word-max 880 \
  --playbook-word-min 400 \
  --playbook-word-max 1500 \
  --playbook-intent-tag-regex '\((do|review|design)' \
  --require-file references/core/severity-rubric.md \
  --require-file references/core/score-rubric.md \
  --require-file references/core/personas.md \
  --require-file references/core/glossary.md \
  --require-file references/subagent-dispatch.md \
  --require-file references/calibration.md \
  --require-file references/trackable-findings.md \
  --require-file references/modes.md \
  --require-file templates/change-plan.md \
  --require-file templates/audit-report.md \
  --require-file templates/design-doc.md \
  --require-file templates/refactor-runbook.md \
  --require-file templates/explanation.md \
  --require-file templates/findings-ledger.md \
  --require-file templates/workflow-state.json \
  --tracking-report templates/audit-report.md \
  --tracking-intent review \
  --calibration-report templates/audit-report.md \
  --require-pattern 'intent-router routing::SKILL.md::intent-router\.csv' \
  --require-pattern 'bare activation::SKILL.md::show a compact menu' \
  --require-pattern 'subagent dispatch section::SKILL.md::^## Subagent dispatch' \
  --require-pattern 'three lenses::SKILL.md::three lenses' \
  --require-pattern 'front-door section::SKILL.md::^## Routing out' \
  --require-pattern 'trackable findings reference::SKILL.md::trackable-findings\.md' \
  --require-pattern 'audit report forbids mere offer::templates/audit-report.md::offer or inline tracking' \
  --require-pattern 'audit report preserves fallback path::templates/audit-report.md::audit-artifacts/agent-ops-' \
  --require-pattern 'report has Later/as-it-grows bucket::templates/audit-report.md::as it grows' \
  --require-pattern 'observability playbook H1::references/playbooks/observability.md::^# Observability Playbook'
