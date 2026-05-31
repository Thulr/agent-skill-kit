---
name: test-design
description: Use to PRODUCE test-suite artifacts — author a new test or test plan for a feature, shape a cross-layer test strategy (what to test at which layer, as a portfolio), or plan which tests to delete (low-value, redundant, characterizing dead code). Covers unit, integration, e2e/UI, exploratory, property-based, contract, snapshot, mutation, and performance tests. Triggers on "write tests for this feature", "what should I test and at which layer", "design our test strategy", "which tests should we delete", "is our test pyramid right". Do NOT use to REVIEW or triage existing tests for smells, flakiness, or false-pass (use test-critique), or for production-system performance/SLOs (use perf-design).
license: MIT
---

# Test Design

Test-suite design for any layer a team relies on — applied *before* writing the
tests (author), when shaping the suite as a portfolio (strategize), or when
deciding what to remove (prune). Provenance lives in `skill.json`; this file is
runtime routing only.

**Produces:** an intent-specific artifact — `author-design.md` (a behavior, a
test outline, the heuristics it satisfies, the failure modes it prevents) /
`strategy-doc.md` (layer-by-layer investment with rationale) / `prune-plan.md`
(deletion and quarantine candidates with reasons).

## Core principle

**Decide what a test is for before you write it.** Spec, regression,
characterization, exploration, and gate are different jobs that want different
layers and oracles — naming the purpose first beats writing a plausible test at
the most familiar layer.

## Activation

- **Bare invocation** (`"use test-design"`, `"design our tests"`, `"start"`):
  load `references/starter-scenarios.csv` and `references/intent-router.csv`,
  then show the intent menu with named starter scenarios on top and offer the
  mode choice. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with both intent and layer inferable: skip to step 3.
- **Concrete invocation with ambiguous scope**: ask one blocker question
  identifying intent or layer; do not inspect private systems first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to
   `author`, `strategize`, or `prune`. Ambiguous → ask once. (Reviewing or
   triaging *existing* tests instead? That is `test-critique`.)
2. **Pick layer.** Load the intent's CSV from `references/intents/<intent>.csv`.
   Match to one layer, or `all` (strategize) for a cross-layer portfolio.
   Ambiguous → ask once with the CSV menu.
3. **Load grounded context.** Load only the chosen CSV row's files: the layer
   reference(s) from `references/layers/<layer>.md` plus its `core_refs`. Do not
   load other layer references.
4. **Identify the target persona** from `references/core/personas.md` — the
   design is *for* a specific reader and task.
5. **Name the good-shaped artifact.** Apply the layer heuristics tagged for the
   intent. For `author`, produce a concrete test outline (behavior, AAA shape,
   oracle), not abstract advice. For `strategize`, recommend layer investments
   purpose-by-purpose. For `prune`, list deletion candidates with a reason and
   the failure mode of keeping each. For a wide design space, optionally dispatch
   parallel sketches and synthesize the strongest.
6. **Emit output.** Author → `templates/author-design.md`. Strategize →
   `templates/strategy-doc.md`. Prune → `templates/prune-plan.md`.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the target persona, the layer reference(s) applied, the
concrete good-shaped artifact, the grounding sources from
`skill.json.inspired_by`, and verification checkable by reading the artifact or
running a command.

## Reference map

- `references/intent-router.csv` — level-1 router (author / strategize / prune).
- `references/intents/<intent>.csv` — level-2 router (layer) per intent.
- `references/layers/<layer>.md` — layer references (shared with test-critique).
- `references/core/{personas,failure-modes,oracles}.md` — personas, failure
  taxonomy, and consistency oracles.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `templates/{author-design,strategy-doc,prune-plan}.md` — the output shapes.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
