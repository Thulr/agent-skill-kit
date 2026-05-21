# Flat Shape

## When to use

A single procedure, technique, or rubric with no internal branching. One
`SKILL.md` is the whole skill.

Pick this when:

- The skill has 1–2 invocations that share most of their content.
- There's no need for output templates beyond what fits inline.
- Adding routing would be ceremony for its own sake.

## Anatomy

```text
skills/<skill-name>/
  SKILL.md
  skill.json
  (optional) scripts/<helper>.py
  (optional) references/<one-deep-dive>.md
```

Don't add a `templates/` or `evals/` directory until there's a real
artifact or invariant to test.

## SKILL.md outline

- Frontmatter (`name`, `description`)
- One H1
- Overview / core principle (3–5 lines)
- When to use (bullets)
- The procedure (numbered steps OR a single named pattern)
- Output requirements or examples
- (optional) Common mistakes / red flags

Aim for <300 lines / <500 words. If you push past 800 words, escalate to
single-layer.

## skill.json

Match the schema in `skills/dx-heuristics/skill.json`. For a flat skill,
`inspired_by[].playbooks` can be omitted or be a single value, since
there's only one playbook (the SKILL.md itself).

## Evals

Required in this repo. Even flat public skills ship:

- `evals/activation-cases.md`
- `evals/trigger-evals.json`
- `evals/run-static-checks.sh`

Keep them minimal when the trigger is simple, but do not omit them.

## Promotion signals

Promote to single-layer when any of these are true:

- A second clearly-distinct use case appears.
- An output template would be reused enough to deserve its own file.
- Three or more rubrics or vocabularies start to share text.
- `SKILL.md` is creeping past 500 lines.

## Anti-patterns

- **A flat skill with 10 different procedures stuffed into one SKILL.md.**
  Split into single-layer; group by registered use case.
- **A flat skill whose SKILL.md grows past 800 words on one procedure.**
  Move detail into a `references/` file even if the skill stays
  effectively flat.
- **A `templates/` directory in a flat skill with no actual repeatable
  artifact.** Delete it.
