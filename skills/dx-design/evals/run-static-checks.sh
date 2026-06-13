#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"

python3 "$repo_root/scripts/check-skill-static.py" \
  --repo-root "$repo_root" \
  --skill-dir "$skill_dir" \
  --skill dx-design \
  --shape two-layer-design \
  --intents design \
  --tracking none \
  --playbook-intent-tag-regex '\((audit|design|debug)' \
  --forbid-intent audit \
  --forbid-intent debug \
  --forbid-intent edge-pass \
  --require-file references/core/personas.md \
  --require-file templates/design-doc.md \
  --require-pattern 'intent-router routing::SKILL.md::intent-router\.csv' \
  --require-pattern 'good-shaped pattern::SKILL.md::good-shaped pattern' \
  --require-pattern 'routes critique elsewhere::SKILL.md::dx-audit' \
  --require-pattern 'design-doc has good-shaped pattern::templates/design-doc.md::^## Good-shaped pattern' \
  --require-pattern 'design-doc has acceptance criteria::templates/design-doc.md::^## Acceptance criteria'
