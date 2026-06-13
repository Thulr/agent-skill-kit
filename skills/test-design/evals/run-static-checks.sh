#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"

python3 "$repo_root/scripts/check-skill-static.py" \
  --repo-root "$repo_root" \
  --skill-dir "$skill_dir" \
  --skill test-design \
  --shape two-layer-design \
  --intents author,strategize,prune \
  --tracking none \
  --playbook-intent-tag-regex '\((audit|triage|author|strategize|prune)' \
  --forbid-intent audit \
  --forbid-intent triage \
  --require-file references/core/personas.md \
  --require-file references/core/failure-modes.md \
  --require-file templates/author-design.md \
  --require-file templates/strategy-doc.md \
  --require-file templates/prune-plan.md \
  --require-pattern 'intent-router routing::SKILL.md::intent-router\.csv' \
  --require-pattern 'good-shaped artifact::SKILL.md::good-shaped artifact' \
  --require-pattern 'routes critique elsewhere::SKILL.md::test-audit' \
  --require-pattern 'author-design has test outline::templates/author-design.md::^## Test outline' \
  --require-pattern 'author-design has heuristics applied::templates/author-design.md::^## Heuristics applied' \
  --require-pattern 'strategy-doc has layer investments::templates/strategy-doc.md::^## Layer investments' \
  --require-pattern 'prune-plan has deletion candidates::templates/prune-plan.md::^## Deletion candidates'
