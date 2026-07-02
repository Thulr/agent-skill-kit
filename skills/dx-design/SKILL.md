---
name: dx-design
description: "Design a new developer-experience surface - API, SDK, CLI, error envelope, setup flow, auth model, or plugin contract. Triggers: 'design a new API/SDK/CLI', 'what should we get right up front', 'shape the public surface'. Do NOT use to audit or debug an existing surface — use dx-audit."
license: MIT
---

# DX Design

Developer-experience design for any surface a developer will install, call,
extend, or maintain — applied *before* the code exists, so the public shape is
right the first time. Provenance lives in `skill.json`; this file is runtime
routing only.

**Produces:** a `design-doc.md` — a concrete good-shaped pattern (paste-ready
snippet, type signature, schema, or example interaction), the heuristics it
satisfies, the anti-patterns it avoids, and testable acceptance criteria.

## Boundaries

Do NOT use to AUDIT or debug an existing surface (use dx-audit), to design the documentation system itself (use docs-design), for end-user visual UI (use ui-design), for AI/Agent SDK/tool/error/telemetry surface design an agent consumes (use agent-dx), or for AGENTS.md and agent-readable docs (use agent-docs).

## Core principle

**Design the paved path before it sets.** The cheapest time to fix a DX problem
is before the contract ships — every observable behavior of an interface
eventually gets depended on, so name the good-shaped pattern concretely rather
than describing principles abstractly.

## Activation

- **Bare invocation** (`"use dx-design"`, `"design a DX surface"`, `"start"`): show a compact menu: mode choice (guided / autopilot / grill me?) and numbered intents from the router. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with the surface inferable: skip to step 2.
- **Concrete invocation with ambiguous surface**: ask one — e.g., *"Are you designing an API, CLI, SDK, or error envelope?"* or *"Is the primary surface the setup flow or the auth model?"*

## Workflow

1. **Confirm intent = design.** This skill is single-intent (`design`). If the
   ask is actually to audit, debug, or risk-scan an *existing* surface, route to
   `dx-audit` instead.
2. **Pick surface.** Load `references/intents/design.csv`. Match the prompt to
   one surface (or a small set). Ambiguous → ask once with the CSV menu.
3. **Load grounded context.** Load only the chosen row's playbook
   `references/playbooks/<surface>.md` plus its `core_refs` (the persona list,
   and the first-impressions checklist for the README surface). Do not load
   other playbooks.
4. **Identify the target developer persona** from `references/core/personas.md`
   — the design is *for* a specific developer and task.
5. **Name the good-shaped pattern.** Apply the playbook heuristics tagged for
   `design`. Produce the concrete shape — not abstract advice. For a wide design
   space, optionally dispatch parallel design sketches (first-time integrator vs
   maintainer lens) and synthesize the strongest.
6. **Emit output.** Write `templates/design-doc.md`: goal + target developer,
   the good-shaped pattern, heuristics applied, anti-patterns avoided, testable
   acceptance criteria, edge cases handled, open trade-offs, out-of-scope.

> **Wrong direction?** If the user says this is not what they meant, go back to step 1 (Confirm intent) - do not patch in the wrong direction. Restate the corrected understanding and re-plan.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every design doc names the target developer persona, the playbook(s) applied,
the concrete good-shaped pattern, the grounding sources from
`skill.json.inspired_by`, and acceptance criteria checkable by reading the
artifact or running a command.

## Reference map

- `references/intent-router.csv` — single-intent router (`design`).
- `references/intents/design.csv` — surface router for design.
- `references/playbooks/<surface>.md` — surface playbooks (shared with dx-audit).
- `references/core/personas.md` — target developer persona list.
- `references/first-impressions-checklist.md` — use its 10 items as README design
  acceptance criteria; its audit-report scoring contract applies only in dx-audit.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `templates/design-doc.md` — the design output shape.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
