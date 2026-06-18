# Single-Layer (Hub-and-Spoke) Shape

## When to use

The skill has 3–8 distinct intents. Each picks a subset of supporting
references and templates. There's one router (`SKILL.md` + a registry
CSV), and every detail file is loaded only when relevant.

Pick this when:

- Use cases share rubrics, vocabulary, or output templates worth
  centralizing.
- Each leaf needs 200–500 words of dedicated guidance.
- A flat shape's `SKILL.md` would balloon past ~500 lines.

## Anatomy

```text
skills/<skill-name>/
  SKILL.md
  skill.json
  references/
    intent-router.csv     # the single router
    <topic-or-rubric>.md      # one per intent or shared rubric
  templates/
    <artifact-name>.md        # only when the skill emits repeatable
                              # artifacts
  evals/
    activation-cases.md       # behavioral cases (positive + negative)
    trigger-evals.json        # canonical trigger-eval schema
    run-static-checks.sh      # required repo gate
```

## The registry CSV

`references/intent-router.csv` is the source of truth for which detail
files and templates load for each intent. One row per intent:

```text
intent,trigger_examples,detail_file,templates,notes
```

The `detail_file` and `templates` columns may be semicolon-separated lists.

Rules:

- Every row points to existing files.
- Every reference file is reachable from at least one row.
- No row points to every file — that defeats progressive disclosure.

## SKILL.md outline

- Frontmatter (`name`, `description`)
- Overview / core principle
- Operating contract (the non-negotiables)
- Activation handshake (what to ask when invoked bare)
- Modes (optional — Guided Build / Autopilot / Grill Me are common)
- Workflow that consults the registry
- Output requirements
- Reference map (mirrors the registry, plus templates and evals)

Keep `SKILL.md` under ~600 lines / <800 words. The whole point of
single-layer is that detail lives in references, not in the navigator.

## skill.json

Match the schema in `skills/dx-audit/skill.json`. For single-layer
skills, `inspired_by[].playbooks` can name the intent(s) each source
informs, so future agents see the source → intent mapping.

## Static check

Every public skill in this repo has `evals/run-static-checks.sh`.
It verifies:

- All expected files exist.
- `skill.json` is valid JSON with the required fields.
- Every reference path in `intent-router.csv` exists on disk
  (registry → file direction).
- Every `.md` in `references/` is referenced by at least one row
  (file → registry direction; orphan check).
- `SKILL.md` is under its word cap and contains the structural sections
  the runtime expects.

Wire it into `just check`.

## Promotion signals

Promote to two-level when any of these are true:

- The registry needs a second axis (e.g., not just "intent" but
  "intent × audience" or "intent × surface").
- A leaf needs to load 9+ distinct chunks of content depending on
  context.
- One leaf grows past ~1500 words — that's a sign it's actually several
  variants that deserve their own routing layer.
- You find yourself wanting two registry CSVs to express the routing.

## Anti-patterns

- **A registry whose rows all point to the same files.** No real routing
  is happening; collapse to flat.
- **Detail files not referenced by the registry.** Orphans that future
  contributors won't find. Either map them or delete them.
- **Templates with no corresponding intent row.** Same problem; map
  them or delete.
- **`SKILL.md` containing what should be a reference file.** SKILL.md is
  routing, not content. Move it out.
