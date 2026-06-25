---
name: agent-ux
description: "Use for AGENT UX — the interaction surface an AI agent acts THROUGH as end user (UI, app, computer-use target). DO — make surfaces agent-perceivable/targetable/actionable. REVIEW — audit for machine-readable state, deterministic actions, agency/approval. DESIGN — shape state, handles, gates, dual paths. Triggers: 'can agent use this UI', 'make app agent-operable', 'should agent confirm action"
license: MIT
---

# Agent UX

The interaction surface an **AI agent acts through as an end user** — a product UI, app, or
computer-use target it perceives, chooses an action on, and acts on, often on a human's behalf.
The agent-actor analog of human UX. Provenance lives in `skill.json`; this file is runtime
routing only.

**Produces:** a `change-plan.md` (DO), an `audit-report.md` plus a findings-ledger +
workflow-state when tracked (REVIEW), or a `design-doc.md` / `refactor-runbook.md` /
`explanation.md` (DESIGN).

## Boundaries

Do NOT use for human-only product UX or visual design (use ux-audit / ui-design), docs an agent reads (use agent-docs), the SDK/tool schema or token-exchange mechanism (use agent-dx), or operating the agent loop (use agent-ops).

## Core principle

**An agent can act only on what it can perceive, can act safely only on what it can target
deterministically, and must not act past its authority.** Expose state in structure, not pixels;
target by stable handle, not coordinates; gate the irreversible action in-path.

## Activation

- **Bare invocation** (`"use agent-ux"`, `"start"`): show a compact menu: mode choice (guided / autopilot / grill me?) and numbered intents from the router. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with intent and surface inferable: skip to step 3.
- **Ambiguous invocation**: ask one — e.g., *"Are you auditing a UI, a computer-use target, or an approval flow?"* or *"Is this about machine-readable state or action handles?"*

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`; match to `do`, `review`, or `design`.
   Ambiguous → ask once.
2. **Pick surface.** Load `references/intents/<intent>.csv`; match one or more of
   `machine-readable-state`, `deterministic-actions`, `approval-and-agency`, `audience-conflicts`
   — or `all` for a REVIEW fan-out. Ambiguous → ask once with the menu.
3. **Load grounded context.** Load only the chosen row's `playbook` plus its `core_refs`. Do not
   load other playbooks (REVIEW's `all` fan-out row carries none — each surface agent loads its own).
4. **Identify the target persona** from `references/core/personas.md`.
5. **Then calibrate to project scale** (REVIEW / DESIGN) per `references/calibration.md`: below
   Load-bearing, narrow scope, collapse same-mechanism gaps into one systemic finding, and split
   **Now** vs **Later (as it grows)**. The tier feeds emission, never severity.
6. **Dispatch lenses in parallel** (REVIEW default when permitted): one surface per agent for
   `all`; otherwise the three lenses below. Sequential fallback if no delegation primitive.
7. **Apply the playbook.** Use the heuristics tagged for the intent. For REVIEW, score each
   surface 0–10 (`references/core/score-rubric.md`); synthesize lens findings, preserving
   disagreements as open questions. Apply severity and stable `AGENT-UX-<surface>-NNN` IDs
   (`references/core/severity-rubric.md`): `AGENT-UX-STATE`, `AGENT-UX-ACT`, `AGENT-UX-APPR`,
   `AGENT-UX-AUD`.
8. **Emit.** DO → `templates/change-plan.md`. REVIEW → `templates/audit-report.md`. DESIGN →
   `templates/design-doc.md` (shape), `templates/refactor-runbook.md` (sequence a hardening), or
   `templates/explanation.md` (explain a principle).
9. **Create, resume, or close tracking state** (REVIEW). For an audit with 7+ findings, any
   severity 3–4, or a save/track/closeout request, load `references/trackable-findings.md`. If
   the request names an existing ledger, workflow-state, PR, or `AGENT-UX-*` ID, read
   saved state first; update statuses only after each verification rule passes. Otherwise write
   the ledger at `docs/audits/agent-ux-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and
   workflow state at `docs/audits/agent-ux-workflow-state-<YYYY-MM-DD>-<scope-slug>.json` (fall
   back to `audit-artifacts/agent-ux-...` if `docs/audits/` is unwritable). Report both paths;
   keep roadmaps, issues, and non-tracking edits opt-in.

> **Wrong direction?** If the user says this isn't what they meant, go back to Understand (step 1) — do not patch in the wrong direction. Restate the corrected understanding and re-plan.

## Modes

Guided Draft (default), Autopilot, Grill Me — see `references/modes.md`. Offer at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the intent, surface(s), persona, playbook(s) applied, and grounding sources
from `skill.json`; REVIEW adds severity + verification per finding and the project tier. **Name
the agent affordance you are deliberately NOT adding (YAGNI), not only what you are.**

## Subagent dispatch

Default for REVIEW when delegation is permitted; skip tiny work. Spawn three lenses in parallel
— **perceive** (machine-readable state, no human-only affordances, observable results),
**act-and-authority** (stable handles, idempotency/retry-safety, in-path gating, on-behalf
consent), and **reconcile** (human-vs-agent trade-off, dual visible+machine path, no hidden
criticals) — per `references/subagent-dispatch.md`, then synthesize, ordering by severity.

## Reference map

- `references/intent-router.csv` + `references/intents/<intent>.csv` — the two routing layers.
- `references/playbooks/<surface>.md` — the four agent-as-user surfaces.
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/core/{severity-rubric,score-rubric,personas,glossary}.md` — scales, audience, terms.
- `references/{calibration,trackable-findings,modes}.md` — shared (symlinks).
- `templates/*.md` — change-plan, audit-report, design-doc, refactor-runbook, explanation.
- `evals/`, `skill.json` — gates and provenance.
