#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/../../../scripts/static-check-lib.sh"
repo_root="$(repo_root_from "$script_dir")"
skill_dir="${1:-$(cd "$script_dir/.." && pwd)}"

python3 "$repo_root/scripts/check-skill-static.py" \
  --repo-root "$repo_root" \
  --skill-dir "$skill_dir" \
  --skill writing-design \
  --shape two-layer-design \
  --intents structure,draft,persuade \
  --tracking none \
  --playbook-intent-tag-regex '\((structure|draft|persuade)' \
  --forbid-intent revise \
  --forbid-intent copyedit \
  --forbid-intent diagnose \
  --require-file references/core/structure-rubric.md \
  --require-file references/core/audience-frame.md \
  --require-file references/core/draft-discipline.md \
  --require-file references/core/clarity-rubric.md \
  --require-file references/core/voice-guard.md \
  --require-file references/core/persuasion-rubric.md \
  --require-file references/core/narrative-honesty-guard.md \
  --require-file references/subagent-dispatch.md \
  --require-file references/modes.md \
  --require-file templates/outline-plan.md \
  --require-file templates/draft-scaffold.md \
  --require-file templates/persuasion-plan.md \
  --require-pattern 'intent-router routing::SKILL.md::intent-router\.csv' \
  --require-pattern 'bare activation::SKILL.md::show a compact menu' \
  --require-pattern 'routes critique to sibling::SKILL.md::writing-audit' \
  --require-pattern 'outline-plan has outline section::templates/outline-plan.md::^## Outline' \
  --require-pattern 'draft-scaffold has rough first pass::templates/draft-scaffold.md::^## Rough first pass' \
  --require-pattern 'persuasion-plan has ABT spine::templates/persuasion-plan.md::^## ABT spine' \
  --require-pattern 'persuasion-plan has honesty check::templates/persuasion-plan.md::^## Honesty check'
