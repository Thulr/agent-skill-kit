#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"

python3 "$repo_root/scripts/check-skill-static.py" \
  --repo-root "$repo_root" \
  --skill-dir "$skill_dir" \
  --skill perf-design \
  --shape two-layer-design \
  --intents design,optimize,strategize \
  --tracking none \
  --playbook-intent-tag-regex '\((audit|design|diagnose|optimize|strategize)' \
  --forbid-intent audit \
  --forbid-intent diagnose \
  --require-file references/core/personas.md \
  --require-file templates/design-doc.md \
  --require-file templates/optimize-plan.md \
  --require-file templates/strategy-doc.md \
  --require-pattern 'intent-router routing::SKILL.md::intent-router\.csv' \
  --require-pattern 'good-shaped pattern::SKILL.md::good-shaped pattern' \
  --require-pattern 'routes critique elsewhere::SKILL.md::perf-audit' \
  --require-pattern 'design-doc has good-shaped pattern::templates/design-doc.md::^## Good-shaped pattern' \
  --require-pattern 'design-doc has acceptance criteria::templates/design-doc.md::^## Acceptance criteria' \
  --require-pattern 'optimize-plan is profile-first::templates/optimize-plan.md::^## Profile' \
  --require-pattern 'optimize-plan has verification gate::templates/optimize-plan.md::^## Verification' \
  --require-pattern 'strategy-doc has adoption sequence::templates/strategy-doc.md::^## Adoption sequence'
