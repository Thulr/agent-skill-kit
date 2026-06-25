---
name: test-design
description: "Produce test-suite artifacts - author tests for a feature, shape cross-layer strategy, or plan deletions. Triggers: 'write tests for this feature', 'design our test strategy', 'which tests should we delete'."
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

## Boundaries

Do NOT use to REVIEW or triage existing tests for smells, flakiness, or false-pass (use test-audit).

## Core principle

**Decide what a test is for before you write it.** Spec, regression,
characterization, exploration, and gate are different jobs that want different
layers and oracles — naming the purpose first beats writing a plausible test at
the most familiar layer.

## Activation

- **Bare invocation** (`"use test-design"`, `"design our tests"`, `"start"`): show a compact menu: mode choice (guided / autopilot / grill me?) and numbered intents from the router. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with both intent and layer inferable: skip to step 3.
- **Concrete invocation with ambiguous scope**: ask one — e.g., *"Are you authoring, strategizing, or pruning?"* or *"Which test layer — unit, integration, e2e, or property-based?"*

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to
   `author`, `strategize`, or `prune`. Ambiguous → ask once. (Reviewing or
   triaging *existing* tests instead? That is `test-audit`.)
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

> **Wrong direction?** If the user says this is not what they meant, go back to Understand (step 1) - do not patch in the wrong direction. Restate the corrected understanding and re-plan.

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
- `references/layers/<layer>.md` — layer references (shared with test-audit).
- `references/core/{personas,failure-modes,oracles}.md` — personas, failure
  taxonomy, and consistency oracles.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `templates/{author-design,strategy-doc,prune-plan}.md` — the output shapes.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
