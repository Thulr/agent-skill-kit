#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"

python3 "$repo_root/scripts/check-skill-static.py" \
  --repo-root "$repo_root" \
  --skill-dir "$skill_dir" \
  --skill docs-audit \
  --shape two-layer-audit \
  --intents audit,debug \
  --tracking none \
  --playbook-intent-tag-regex '\((audit|design|debug|measure)' \
  --forbid-intent design \
  --forbid-intent measure \
  --require-file references/core/severity-rubric.md \
  --require-file references/core/score-rubric.md \
  --require-file references/core/personas.md \
  --require-file references/core/audience-matrix.md \
  --require-file templates/audit-report.md \
  --require-file templates/debug-runbook.md \
  --forbid-file references/trackable-findings.md \
  --forbid-file templates/findings-ledger.md \
  --forbid-file templates/workflow-state.json \
  --calibration-report templates/audit-report.md \
  --require-pattern 'intent-router routing::SKILL.md::intent-router\.csv' \
  --require-pattern 'bare activation::SKILL.md::show a compact menu' \
  --require-pattern 'subagent dispatch section::SKILL.md::^## Subagent dispatch' \
  --require-pattern 'four lenses::SKILL.md::four lenses' \
  --require-pattern 'routes design elsewhere::SKILL.md::docs-design' \
  --require-pattern 'report has Later/as-it-grows bucket::templates/audit-report.md::as it grows' \
  --forbid-pattern 'no tracking surface::SKILL.md::(trackable-findings|findings-ledger|workflow-state|tracking state)'
