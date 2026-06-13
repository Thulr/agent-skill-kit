#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"

python3 "$repo_root/scripts/check-skill-static.py" \
  --repo-root "$repo_root" \
  --skill-dir "$skill_dir" \
  --skill writing-audit \
  --shape two-layer-audit \
  --intents revise,copyedit,diagnose \
  --tracking none \
  --playbook-intent-tag-regex '\((revise|copyedit|diagnose)' \
  --forbid-intent structure \
  --forbid-intent draft \
  --forbid-intent persuade \
  --require-file references/core/clarity-rubric.md \
  --require-file references/core/severity-rubric.md \
  --require-file references/core/voice-guard.md \
  --require-file references/core/mechanics-rubric.md \
  --require-file references/core/structure-rubric.md \
  --require-file references/core/persuasion-rubric.md \
  --require-file references/core/score-rubric.md \
  --require-file references/core/narrative-honesty-guard.md \
  --require-file references/core/audience-frame.md \
  --require-file references/subagent-dispatch.md \
  --require-file references/modes.md \
  --require-file templates/revision-report.md \
  --require-file templates/copyedit-report.md \
  --require-file templates/diagnosis-report.md \
  --calibration-report templates/revision-report.md \
  --calibration-report templates/copyedit-report.md \
  --calibration-report templates/diagnosis-report.md \
  --require-pattern 'intent-router routing::SKILL.md::intent-router\.csv' \
  --require-pattern 'bare activation::SKILL.md::show the intent menu' \
  --require-pattern 'applies severity rubric::SKILL.md::severity-rubric' \
  --require-pattern 'routes creation to sibling::SKILL.md::writing-design' \
  --require-pattern 'revision-report has findings::templates/revision-report.md::^## Findings' \
  --require-pattern 'copyedit-report has findings::templates/copyedit-report.md::^## Findings' \
  --require-pattern 'diagnosis-report has findings::templates/diagnosis-report.md::^## Findings' \
  --require-pattern 'diagnosis-report has score::templates/diagnosis-report.md::^## Score' \
  --require-pattern 'revision-report has Later/as-it-grows bucket::templates/revision-report.md::as it grows' \
  --require-pattern 'copyedit-report has Later/as-it-grows bucket::templates/copyedit-report.md::as it grows' \
  --require-pattern 'diagnosis-report has Later/as-it-grows bucket::templates/diagnosis-report.md::as it grows'
