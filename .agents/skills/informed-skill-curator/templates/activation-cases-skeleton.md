# <Skill Name> Activation Cases

Saved at `skills/<skill-name>/evals/activation-cases.md`. This is the
canonical pattern. Curator must seed this file as part of scaffolding;
the validation rubric checks counts and shape.

## Positive

The skill should activate and route correctly. **Minimum 3** for flat
and single-layer skills, **10+** for two-level. Each line names the
prompt and the expected route / intent / surface / template.

- "<natural-language prompt>" -> routes to `<intent>` (and `<surface>` for two-level), loads `<playbook>`, emits `<template>`.
- "<prompt>" -> ...
- "<prompt>" -> ...

## Negative

Near-miss prompts that share keywords but should **not** trigger this
skill. Each negative case **must name the sibling skill** it would
correctly route to — this catches "weak activation/eval coverage"
where negatives are too generic to discriminate.

**Minimum 3** for flat and single-layer, **8+** for two-level.

- "<prompt>" -> use `<sibling-skill>` instead, because <reason this skill is the wrong match>.
- "<prompt>" -> use `<sibling-skill>` instead, because <reason>.
- "<prompt>" -> use `<sibling-skill>` instead, because <reason>.

## Boundary / edge

Cases on the edge of activation — the skill may or may not be right
depending on context. State the boundary explicitly.

**Minimum 1** for any published skill.

- "<prompt>" -> activates only if <condition>; otherwise prefer `<other-skill>`.

## Notes

- Cover the dominant phrasings users will actually try — not just the
  phrasings from `description`.
- Include at least one negative per neighbor skill identified in the
  intake brief's "Comparable existing skills" section.
- Re-read this file after writing trigger-evals.json to confirm the
  two artifacts say the same thing.
