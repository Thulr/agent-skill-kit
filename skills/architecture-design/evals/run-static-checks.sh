#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"

python3 "$repo_root/scripts/check-skill-static.py" \
  --repo-root "$repo_root" \
  --skill-dir "$skill_dir" \
  --skill architecture-design \
  --shape two-layer-design \
  --intents design,refactor,explain \
  --tracking none \
  --playbook-intent-tag-regex '\((audit|design|refactor|explain)' \
  --forbid-intent audit \
  --require-file references/core/personas.md \
  --require-file references/core/glossary.md \
  --require-file templates/design-doc.md \
  --require-file templates/refactor-runbook.md \
  --require-file templates/explanation.md \
  --require-pattern 'intent-router routing::SKILL.md::intent-router\.csv' \
  --require-pattern 'good-shaped pattern::SKILL.md::good-shaped pattern' \
  --require-pattern 'routes critique elsewhere::SKILL.md::architecture-audit' \
  --require-pattern 'design-doc has acceptance criteria::templates/design-doc.md::^## Acceptance criteria' \
  --require-pattern 'design-doc has grounding sources::templates/design-doc.md::^## Grounding sources applied' \
  --require-pattern 'refactor-runbook has step sequence::templates/refactor-runbook.md::^## Step sequence' \
  --require-pattern 'refactor-runbook has verification::templates/refactor-runbook.md::^## Verification' \
  --require-pattern 'explanation has what-it-is-not::templates/explanation.md::^## What it is not' \
  --require-pattern 'explanation has verification::templates/explanation.md::^## Verification'
