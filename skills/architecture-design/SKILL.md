---
name: architecture-design
description: Use to DESIGN, refactor toward, or EXPLAIN a target clean architecture — set the dependency-rule invariant for new work, shape layer/port/adapter boundaries, model entities/aggregates/value objects, carve a bounded context, sequence a safe refactor toward ports and adapters, or explain a principle like the dependency rule or aggregate vs entity. Triggers on "design the boundaries for this new service", "refactor toward ports and adapters", "plan a strangler-fig extraction", "how should we split this bounded context", "explain the dependency rule against our code". Do NOT use to AUDIT and score an existing codebase for violations (use architecture-audit), for developer-facing API/SDK/CLI surfaces (use dx-design), or for product UX / forms / navigation / accessibility (use ux-audit or ui-design).
license: MIT
---

# Architecture Design

Clean-architecture design, refactor sequencing, and explanation — applied to
new work, to a planned move from a tangled state toward cleaner boundaries, or
to teaching a principle against the actual code. Provenance lives in
`skill.json`; this file is runtime routing only.

**Produces:** a `design-doc.md` (target shape + acceptance criteria), a
`refactor-runbook.md` (reversible step sequence), or an `explanation.md`
(grounded concept walkthrough), depending on intent.

## Core principle

**Decide the dependency direction before code sets.** Source-code dependencies
point inward, toward more abstract code; the cheapest time to place a seam
correctly is before anything depends on it crossing the wrong way. Name the
good-shaped pattern concretely — a layer diagram, a port signature, an aggregate
boundary — rather than restating principles abstractly.

## Activation

- **Bare invocation** (`"use architecture-design"`, `"design the architecture"`,
  `"start"`): load `references/starter-scenarios.csv` and
  `references/intent-router.csv`, show the intent menu, offer the mode choice.
  Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with intent and surface inferable: skip to step 3.
- **Concrete invocation with ambiguous scope**: ask one blocker question
  naming the candidate intent or surface; do not inspect private systems first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to one
   of: `design` (target shape for new work), `refactor` (sequenced safe path),
   `explain` (grounded concept walkthrough). Ambiguous → ask once. (Auditing an
   *existing* surface for violations is `architecture-audit` instead.)
2. **Pick surface.** Load the intent's CSV from
   `references/intents/<intent>.csv`. Match to one surface (or a small set):
   `dependency-rule`, `boundaries`, `domain-model`, `bounded-context`,
   `cross-cutting`. Ambiguous → ask once with the CSV menu.
3. **Load grounded context.** Load only the chosen row's playbook
   `references/playbooks/<surface>.md` plus its `core_refs`. Do not load other
   playbooks.
4. **Identify the target persona** from `references/core/personas.md` — the
   output is *for* a specific reader and decision.
5. **Name the good-shaped pattern.** Apply the playbook heuristics tagged for
   the intent (`design`, `refactor`, or `explain`). Produce the concrete shape —
   a layer/port diagram, a parallel-change step sequence, or a worked example —
   not abstract advice. For a wide design space, optionally dispatch parallel
   lenses (dependency-auditor / boundary-designer) and synthesize the strongest.
6. **Emit output.** Design → `templates/design-doc.md`. Refactor →
   `templates/refactor-runbook.md`. Explain → `templates/explanation.md`.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the target persona, the playbook(s) applied, the concrete
good-shaped pattern (or step sequence / worked example), the grounding sources
from `skill.json.inspired_by`, and acceptance criteria checkable by reading the
artifact or running a command. Surface school disagreements explicitly rather
than flattening them. For audit/scoring of an existing codebase, route to
`architecture-audit`.

## Reference map

- `references/intent-router.csv` — intent router (`design` / `refactor` / `explain`).
- `references/intents/<intent>.csv` — surface router per intent.
- `references/playbooks/<surface>.md` — surface playbooks (shared with architecture-audit).
- `references/core/{personas,glossary}.md` — target persona list and terms.
- `references/core/severity-rubric.md` — used by `refactor` to weigh what to fix first.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `templates/{design-doc,refactor-runbook,explanation}.md` — the output shapes.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
