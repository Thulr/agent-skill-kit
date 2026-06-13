#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"

python3 "$repo_root/scripts/check-skill-static.py" \
  --repo-root "$repo_root" \
  --skill-dir "$skill_dir" \
  --skill test-audit \
  --shape two-layer-audit \
  --intents audit,triage \
  --tracking required \
  --playbook-intent-tag-regex '\((audit|triage|author|strategize|prune)' \
  --forbid-intent author \
  --forbid-intent strategize \
  --forbid-intent prune \
  --require-file references/core/severity-rubric.md \
  --require-file references/core/score-rubric.md \
  --require-file references/core/personas.md \
  --require-file references/core/failure-modes.md \
  --require-file references/core/oracles.md \
  --require-file references/trackable-findings.md \
  --require-file templates/audit-report.md \
  --require-file templates/audit-report-multi.md \
  --require-file templates/triage-runbook.md \
  --require-file templates/findings-ledger.md \
  --require-file templates/workflow-state.json \
  --tracking-report templates/audit-report.md \
  --tracking-report templates/audit-report-multi.md \
  --tracking-intent audit \
  --calibration-report templates/audit-report.md \
  --calibration-report templates/audit-report-multi.md \
  --require-pattern 'intent-router routing::SKILL.md::intent-router\.csv' \
  --require-pattern 'bare activation::SKILL.md::show the intent menu' \
  --require-pattern 'subagent dispatch section::SKILL.md::^## Subagent dispatch' \
  --require-pattern 'three lenses::SKILL.md::three lenses' \
  --require-pattern 'trackable findings reference::SKILL.md::trackable-findings\.md' \
  --require-pattern 'audit report forbids mere offer::templates/audit-report.md::do not merely' \
  --require-pattern 'audit report preserves fallback path::templates/audit-report.md::audit-artifacts/test-audit-' \
  --require-pattern 'report has Later/as-it-grows bucket::templates/audit-report.md::as it grows'
