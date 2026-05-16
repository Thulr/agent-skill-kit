---
name: clean-architecture
description: Audit, design, refactor toward, or explain clean-architecture concerns — dependency rule, layered/hexagonal/onion boundaries, DDD tactical and strategic patterns, cross-cutting concerns. Use for architecture review, layer-violation audits, bounded-context design, anemic-domain detection, refactor sequencing toward ports and adapters, or explaining principles like the dependency rule, aggregate vs entity, or anti-corruption layers. Opinionated terrain; surfaces school disagreements explicitly. Language-agnostic, full-stack-friendly (frontend grounding is thinner than backend).
license: MIT
---

# Clean Architecture

Architecture review, design, refactor, and explanation grounded in the
clean-architecture family of approaches. Provenance and source citations
live in `skill.json`; this file is runtime routing only.

## Core principle

**Direction of dependencies is the load-bearing invariant.** Inner, more
abstract code never depends on outer, more concrete code. Whether the
diagram is layered, hexagonal, onion, or concentric, the rule is the
same: if an inward arrow exists, the architecture leaks.

## Activation

- **Bare invocation** (`"use clean-architecture"`, `"architecture review"`,
  `"start"`): load `references/intent-router.csv`, show the intent menu,
  wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with both intent and surface inferable: skip to
  step 3 of the workflow.
- **Concrete invocation with ambiguous scope**: ask one blocker question
  identifying intent or surface; do not inspect private systems first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt
   to one of: `audit`, `design`, `refactor`, `explain`. Ambiguous → ask
   once.
2. **Pick surface.** Load the intent's CSV from
   `references/intents/<intent>.csv`. Match the prompt to one or more
   surfaces, or `all` (audit only) for multi-surface fan-out. Ambiguous →
   ask once with the CSV menu, adding `all` as an option for audit intent.
3. **Load grounded context.** Load only the files listed in the chosen
   CSV row: one playbook from `references/playbooks/<surface>.md` plus the
   `core_refs` listed. Do not load other playbooks. Skip this step when
   surface = `all` — each spawned surface agent loads its own playbook
   in step 5.
4. **Identify the target developer persona** from
   `references/core/personas.md`. Load `references/core/glossary.md`
   to disambiguate terminology before applying the playbook. For
   surface = `all`, do this at synthesis only; spawned surface agents
   load their own copies.
5. **Spawn sub-agents in parallel (default for `audit`; see Subagent dispatch below for other intents).** Single-surface:
   delegate one lens per agent — dependency-auditor, boundary-designer,
   refactor-pragmatist. Audit + `all`: delegate one surface per agent;
   each runs the three lenses sequentially inside itself. See
   `references/subagent-dispatch.md`; fall back to sequential execution
   only if the host has no delegation primitive.
6. **Apply the playbook.** Use the playbook's heuristics tagged for this
   intent. For `audit`, score the surface 0–10 using
   `references/core/score-rubric.md`; for `design`, name the good-shaped
   pattern; for `refactor`, sequence steps with safety nets; for
   `explain`, ground the explanation in the playbook's `## Grounding` section. If
   sub-agents ran, synthesize their findings here.
7. **Apply severity** from `references/core/severity-rubric.md` (0–4) to
   every finding or risk.
8. **Emit output.** Audit → `templates/audit-report.md` (or
   `templates/audit-report-multi.md` for surface = `all`). Design →
   `templates/design-doc.md`. Refactor → `templates/refactor-runbook.md`.
   Explain → `templates/explanation.md`.

## Modes

- **Guided Draft (default):** one optionized question at a time, 3–4
  likely choices plus a freeform path.
- **Autopilot:** proceed from available context; state assumptions when
  the task is clear and low-risk.
- **Grill Me:** open-ended questions, one at a time, when audience,
  constraints, or trade-offs materially change the result.

## Output requirements

Every output includes:

- Target developer persona.
- Playbook(s) applied.
- Intent-specific load-bearing section: findings (audit), acceptance
  criteria (design), sequenced steps (refactor), explanation (explain).
- Verification — how to prove the change worked.

## Subagent dispatch

Independent perspectives catch issues a single pass misses. **Default for
`audit`.** Preferred for `design` when comparing trade-offs. Optional for
`refactor` when ranking sequencing. Skip for tiny explanations,
deterministic checks, or tasks needing secrets / live production.

Spawn three sub-agents — one per lens: **dependency-auditor**,
**boundary-designer**, **refactor-pragmatist** — in parallel. Some hosts
do not auto-dispatch; instruct explicitly ("spawn three agents" /
"delegate in parallel"). Load `references/subagent-dispatch.md` for the
per-lens prompts, dispatch template, and synthesis step. The three lenses
each produce findings; synthesis deduplicates, preserves disagreements as
open questions, and emits the template-shaped output.

Fall back to running the three lenses sequentially only when the host has
no delegation primitive — switching lens between passes matters more than
the parallelism.

## Reference map

- `references/intent-router.csv` — level-1 router (intent).
- `references/intents/<intent>.csv` — level-2 router (surface) per intent.
- `references/playbooks/<surface>.md` — surface-specific playbooks.
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/core/{severity,score}-rubric.md` — shared 0–4 and 0–10
  scales.
- `references/core/personas.md` — target developer persona list.
- `references/core/glossary.md` — disambiguates "boundary" vs "bounded
  context" vs "layer" vs "module" vs "context" before playbook content.
- `templates/*.md` — four intent-specific output templates plus the
  audit-multi template for surface = `all`.
- `evals/activation-cases.md` — activation cases (positive, negative, edge).
- `evals/run-static-checks.sh` — structural and schema gates run in CI.
- `evals/trigger-evals.json` — queries for description-optimization.
- `skill.json` — provenance, grounding sources, version, status.
