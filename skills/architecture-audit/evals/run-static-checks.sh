#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"

python3 "$repo_root/scripts/check-skill-static.py" \
  --repo-root "$repo_root" \
  --skill-dir "$skill_dir" \
  --skill architecture-audit \
  --shape two-layer-audit \
  --intents audit \
  --tracking required \
  --playbook-intent-tag-regex '\((audit|design|refactor|explain)' \
  --forbid-intent design \
  --forbid-intent refactor \
  --forbid-intent explain \
  --require-file references/core/severity-rubric.md \
  --require-file references/core/score-rubric.md \
  --require-file references/core/personas.md \
  --require-file references/core/glossary.md \
  --require-file references/audit-mechanics.md \
  --require-file references/trackable-findings.md \
  --require-file templates/audit-report.md \
  --require-file templates/audit-report-multi.md \
  --require-file templates/findings-ledger.md \
  --require-file templates/workflow-state.json \
  --tracking-report templates/audit-report.md \
  --tracking-report templates/audit-report-multi.md \
  --calibration-report templates/audit-report.md \
  --calibration-report templates/audit-report-multi.md \
  --require-pattern 'intent-router routing::SKILL.md::intent-router\.csv' \
  --require-pattern 'bare activation::SKILL.md::show the intent menu' \
  --require-pattern 'subagent dispatch section::SKILL.md::^## Subagent dispatch' \
  --require-pattern 'three lenses::SKILL.md::three lenses' \
  --require-pattern 'trackable findings reference::SKILL.md::trackable-findings\.md' \
  --require-pattern 'routes design elsewhere::SKILL.md::architecture-design' \
  --require-pattern 'CA- finding-ID namespace preserved::SKILL.md::CA-' \
  --require-pattern 'audit report forbids mere offer::templates/audit-report.md::offer or inline tracking' \
  --require-pattern 'audit report preserves fallback path::templates/audit-report.md::audit-artifacts/architecture-audit-' \
  --require-pattern 'report has Later/as-it-grows bucket::templates/audit-report.md::as it grows'
