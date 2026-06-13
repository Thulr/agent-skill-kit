#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"

python3 "$repo_root/scripts/check-skill-static.py" \
  --repo-root "$repo_root" \
  --skill-dir "$skill_dir" \
  --skill docs-design \
  --shape two-layer-design \
  --intents design,measure \
  --tracking none \
  --playbook-intent-tag-regex '\((audit|design|debug|measure)' \
  --forbid-intent audit \
  --forbid-intent debug \
  --require-file references/core/severity-rubric.md \
  --require-file references/core/score-rubric.md \
  --require-file references/core/personas.md \
  --require-file references/core/audience-matrix.md \
  --require-file templates/design-doc.md \
  --require-file templates/measurement-plan.md \
  --require-pattern 'intent-router routing::SKILL.md::intent-router\.csv' \
  --require-pattern 'proposed structure::SKILL.md::proposed structure' \
  --require-pattern 'routes critique elsewhere::SKILL.md::docs-audit' \
  --require-pattern 'design-doc has proposed structure::templates/design-doc.md::^## Proposed structure' \
  --require-pattern 'design-doc has acceptance criteria::templates/design-doc.md::^## Acceptance criteria' \
  --require-pattern 'measurement-plan has metrics::templates/measurement-plan.md::^## Metrics' \
  --require-pattern 'measurement-plan has gates and evals::templates/measurement-plan.md::^## Gates and evals'
