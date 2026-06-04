---
name: dx-design
description: Use to DESIGN or shape a new developer-experience surface from scratch — an API, SDK, CLI, developer-doc IA, error envelope, setup/first-run flow, auth model, migration/deprecation path, plugin or extension contract, package/publish scheme, logging/config design, changelog convention, or telemetry/consent contract. Triggers on "design a new API/SDK/CLI", "what should we get right up front", "shape the public surface before we write code", "what should our error envelope look like". Emits a design doc with a concrete good-shaped pattern and acceptance criteria. Do NOT use to AUDIT or debug an existing surface (use dx-audit), to design the documentation system itself — mode taxonomy, source-of-truth, retrieval, and cross-audience help (use docs-design), for end-user visual UI (use ui-design), or for AI-agent-facing surfaces / AI/Agent SDK design (use agent-experience).
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

## Core principle

**Design the paved path before it sets.** The cheapest time to fix a DX problem
is before the contract ships — every observable behavior of an interface
eventually gets depended on, so name the good-shaped pattern concretely rather
than describing principles abstractly.

## Activation

- **Bare invocation** (`"use dx-design"`, `"design a DX surface"`, `"start"`):
  load `references/starter-scenarios.csv` and `references/intent-router.csv`,
  show the surface menu, offer the mode choice. Wait. No file inspection, no
  network calls, no writes.
- **Concrete invocation** with the surface inferable: skip to step 2.
- **Concrete invocation with ambiguous surface**: ask one blocker question
  naming the candidate surfaces; do not inspect private systems first.

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
- `references/first-impressions-checklist.md` — first-impressions items (README design).
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `templates/design-doc.md` — the design output shape.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
