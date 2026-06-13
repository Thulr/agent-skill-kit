#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"

python3 "$repo_root/scripts/check-skill-static.py" \
  --repo-root "$repo_root" \
  --skill-dir "$skill_dir" \
  --skill dx-audit \
  --shape two-layer-audit \
  --intents audit,debug,edge-pass \
  --tracking required \
  --word-max 800 \
  --playbook-word-min 400 \
  --playbook-word-max 1500 \
  --playbook-intent-tag-regex '\((audit|design|debug)' \
  --forbid-intent design \
  --require-file references/core/severity-rubric.md \
  --require-file references/core/score-rubric.md \
  --require-file references/core/personas.md \
  --require-file references/trackable-findings.md \
  --require-file templates/audit-report.md \
  --require-file templates/audit-report-multi.md \
  --require-file templates/debug-runbook.md \
  --require-file templates/edge-checklist.md \
  --require-file templates/findings-ledger.md \
  --require-file templates/workflow-state.json \
  --tracking-report templates/audit-report.md \
  --tracking-report templates/audit-report-multi.md \
  --tracking-report templates/edge-checklist.md \
  --tracking-intent audit \
  --tracking-intent edge-pass \
  --calibration-report templates/audit-report.md \
  --calibration-report templates/audit-report-multi.md \
  --require-pattern 'intent-router routing::SKILL.md::intent-router\.csv' \
  --require-pattern 'bare activation::SKILL.md::show the intent menu' \
  --require-pattern 'subagent dispatch section::SKILL.md::^## Subagent dispatch' \
  --require-pattern 'three lenses::SKILL.md::three lenses' \
  --require-pattern 'trackable findings reference::SKILL.md::trackable-findings\.md' \
  --require-pattern 'audit report forbids mere offer::templates/audit-report.md::offer or inline tracking' \
  --require-pattern 'audit report preserves fallback path::templates/audit-report.md::audit-artifacts/dx-audit-' \
  --require-pattern 'report has Later/as-it-grows bucket::templates/audit-report.md::as it grows' \
  --require-pattern 'cli.md H1 title::references/playbooks/cli.md::^# CLI Playbook'
