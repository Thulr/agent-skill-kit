# Two-Level Routing Shape

## When to use

The skill's invocation space is genuinely two-dimensional. Each dimension
is orthogonal to the other, and the leaves at their intersection each need
distinct content. The canonical example is `skills/dx-critique/`:

- Dimension 1 (intent): audit / debug / edge-pass
- Dimension 2 (surface): api / sdk / cli / docs / errors / ...
- Each (intent, surface) leaf loads one playbook plus shared rubrics.

Pick this when:

- A single registry would have 30+ rows that factor cleanly into two axes.
- Per-leaf content is substantial (500+ words) and would all bloat
  `SKILL.md` if inlined.
- The two axes share rubrics (severity scale, scoring, personas) that
  belong in one shared place.

**Read `skills/dx-critique/` end-to-end as the canonical example before
scaffolding a two-level skill of your own.** Copying its structure beats
inventing one.

## Anatomy

```text
skills/<skill-name>/
  SKILL.md
  skill.json
  references/
    intent-router.csv           # level 1: intent × default_template
    intents/
      <intent>.csv              # level 2: surface × playbook × core_refs
    playbooks/
      <surface>.md              # one per surface, uniform structure
    core/
      <shared-rubric>.md        # severity / score / personas / etc.
    subagent-dispatch.md        # when the skill recommends multi-lens
                                # review (audits and edge-passes benefit)
  templates/
    <intent>.md                 # one per intent, governs output shape
  evals/
    activation-cases.md         # behavioral cases (positive + negative)
    run-static-checks.sh        # REQUIRED at this depth
    trigger-evals.json          # optional, for description optimization
```

## The two registries

`references/intent-router.csv` columns:

```text
intent,name,when_to_use,registry_file,default_template
```

Each `references/intents/<intent>.csv` columns:

```text
surface,name,when_to_use,playbook,core_refs
```

`playbook` and `core_refs` may be semicolon-separated paths so a single
row can load multiple playbooks (e.g., an edge-pass row that needs both
`setup.md` and `inner-loop.md`).

## Playbook structure

Every `references/playbooks/<surface>.md` should have the same structure
so the static check can validate it uniformly:

- `# <Surface> Playbook` H1
- `## Scope` — what's in / what's out
- `## Grounding` — cited canonical sources
- `## Good signals` — what right looks like
- `## Common failures` — what wrong looks like
- `## Heuristics` — each tagged with one or more intents, e.g.
  `(audit, design)`
- `## Quick diagnostic` — binary questions with named actions
- `## Cross-references` — pointers to related playbooks

Target 400–1500 words per playbook.

## Shared rubrics

Anything used across multiple playbooks goes in `references/core/`:

- **Severity rubric** (0–4 scale is a good default for cross-skill
  alignment).
- **Score rubric** (0–10 if the skill scores anything).
- **Personas** (target audience taxonomy).

This is what makes two-level worth the ceremony — each playbook leans on
the same vocabulary.

## Output templates

One template per intent, in `templates/<intent>.md`. Each template has a
load-bearing section the intent is named for (e.g. findings for audit,
acceptance criteria for design, prevention for debug, re-run trigger for
edge-pass). Use angle-bracket placeholders like `<surface>` or
`<severity>` so the template is clearly a skeleton.

## Subagent dispatch

Two-level skills with audit or edge-pass intents benefit from dispatching
sub-agents per persona/lens, then synthesizing. Put the per-lens
persona prompts, dispatch template, and synthesis instructions in
`references/subagent-dispatch.md`. Reference it from the workflow in
`SKILL.md` so dispatch is the default for relevant intents, with a
sequential-lens fallback when sub-agents are unavailable.

## Static checks

A two-level skill has enough invariants — orphan playbooks, missing
sections, registry rows pointing at nonexistent files — that a static
check script becomes necessary, not optional.

`evals/run-static-checks.sh` should verify (see
`skills/dx-critique/evals/run-static-checks.sh` for a working
implementation):

- All expected files exist (SKILL.md, skill.json, both registry layers,
  every playbook listed by the registries, every template).
- `skill.json` is valid JSON with required fields, `status: "published"`
  for installable skills, and a non-empty `inspired_by`.
- `SKILL.md` is under a word cap (800 is a good default) and contains the
  gates the runtime expects (e.g., `^## Subagent dispatch`).
- Every playbook on disk is referenced by at least one intent CSV
  (file → CSV; orphan check).
- Every playbook referenced by a CSV exists on disk (CSV → file;
  registry integrity).
- Every playbook has the structural sections.
- `skill.json.inspired_by` source author names and titles do not leak
  into `SKILL.md` (provenance lives in `skill.json`, not the runtime
  file).

Auto-derive the playbook list from disk (don't hardcode it) so adding a
new surface is "drop a file + add a CSV row" — no script edits required.

Wire `run-static-checks.sh` into `just check` and a CI job.

## Activation cases

`evals/activation-cases.md` should cover:

- **Positive cases:** the skill activates correctly, picks the right
  intent + surface, names a persona, emits the correct template shape.
- **Negative cases:** near-miss prompts that share keywords but should
  not trigger (e.g., for a DX skill, "audit the marketing site" should
  not route through any DX playbook).

Plan for 10+ positive and 8+ negative when the skill is published.

## Anti-patterns

- **One dimension has only 1–2 values.** Collapse to single-layer; the
  second axis isn't earning its keep.
- **Playbooks that don't follow the uniform structure.** Static check
  catches this; fix the playbook, don't loosen the check.
- **Detail in `SKILL.md` that should be in a playbook.** SKILL.md is
  routing, not content.
- **`skill.json.inspired_by` rendered as a list of strings instead of
  objects.** Loses the per-source grounding metadata that future
  contributors need.
- **Hardcoded surface lists in static-check or registry validation.**
  Auto-derive from disk so a new surface is a two-file change.
