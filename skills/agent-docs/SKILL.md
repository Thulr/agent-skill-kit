---
name: agent-docs
description: "Use for AGENT DOCS — agent-native docs an AI agent reads and acts on (no humans). DO: write/fix AGENTS.md, llms.txt, tool descs, refs, context-budget. REVIEW: audit for findability, chunk survivability, trigger clarity, budget. DESIGN: shape doc contracts. Triggers: audit AGENTS.md, curate llms.txt, wrong tool call, will doc survive chunking."
license: MIT
---

# Agent Docs

The agent-NATIVE documentation an **AI agent reads and acts on** — `AGENTS.md`, `llms.txt`, tool
descriptions, machine-readable reference, and the context budget. Narrowed to artifacts with no
human-docs analog; generic and dual-audience docs stay in `docs-audit` / `docs-design`.
Provenance lives in `skill.json`; this file is runtime routing only.

**Produces:** a `change-plan.md` (DO), an `audit-report.md` plus a findings-ledger +
workflow-state when tracked (REVIEW), or a `design-doc.md` / `refactor-runbook.md` /
`explanation.md` (DESIGN).

## Boundaries

Do NOT use for human or dual-audience docs, README, help, or RAG-for-human-search (use docs-audit / docs-design), the typed tool/SDK schema as code (use agent-dx), scaffolding or enforcing repo hooks/gates (use harden-repo-for-coding-agents), or operating an agent system (use agent-ops).

## Core principle

**Write so an agent can find it, use a chunk of it alone, trigger on it correctly, and not
drown in it.** Curation raises *average* success, not worst-case reliability — mandatory
invariants belong in gates (route to `harden-repo-for-coding-agents`), not ignorable prose.

## Activation

- **Bare invocation** (`"use agent-docs"`, `"start"`): show a compact menu: mode choice (guided / autopilot / grill me?) and numbered intents from the router. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with intent and surface inferable: skip to step 3.
- **Ambiguous invocation**: ask one — e.g., *"Are you auditing AGENTS.md, llms.txt, or tool descriptions?"* or *"Is this about findability or trigger clarity?"*

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`; match to `do`, `review`, or `design`.
   Ambiguous → ask once.
2. **Pick surface.** Load `references/intents/<intent>.csv`; match one or more of `agents-md`,
   `llms-txt`, `tool-descriptions`, `machine-reference`, `context-budget` — or `all` for a REVIEW
   fan-out. Ambiguous → ask once with the menu.
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
   disagreements as open questions. Apply severity and stable `AGENT-DOC-<surface>-NNN` IDs
   (`references/core/severity-rubric.md`): `AGENT-DOC-AGMD`, `AGENT-DOC-LLMS`, `AGENT-DOC-TOOL`,
   `AGENT-DOC-REF`, `AGENT-DOC-CTX`.
8. **Emit.** DO → `templates/change-plan.md`. REVIEW → `templates/audit-report.md`. DESIGN →
   `templates/design-doc.md` (shape), `templates/refactor-runbook.md` (sequence a hardening), or
   `templates/explanation.md` (explain a principle).
9. **Create, resume, or close tracking state** (REVIEW). For an audit with 7+ findings, any
   severity 3–4, or a save/track/closeout request, load `references/trackable-findings.md`. If
   the request names an existing ledger, workflow-state, PR, or `AGENT-DOC-*` ID, read
   saved state first; update statuses only after each verification rule passes. Otherwise write
   the ledger at `docs/audits/agent-docs-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and
   workflow state at `docs/audits/agent-docs-workflow-state-<YYYY-MM-DD>-<scope-slug>.json` (fall
   back to `audit-artifacts/agent-docs-...` if `docs/audits/` is unwritable). Report both paths;
   keep roadmaps, issues, and non-tracking edits opt-in.

> **Wrong direction?** If the user says this isn't what they meant, go back to Understand (step 1) — do not patch in the wrong direction. Restate the corrected understanding and re-plan.

## Modes

Guided Draft (default), Autopilot, Grill Me — see `references/modes.md`. Offer at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the intent, surface(s), persona, playbook(s) applied, and grounding sources
from `skill.json`; REVIEW adds severity + verification per finding and the project tier. **Name
the doc surface you are deliberately NOT adding (YAGNI), not only what you are.**

## Subagent dispatch

Default for REVIEW when delegation is permitted; skip tiny work. Spawn three lenses in parallel
— **retrieval-and-survivability** (curated index, chunk survivability, stable anchors,
placement), **trigger-and-contract** (trigger/tool-description clarity, AGENTS.md curation +
mirror parity + evidence rules), and **budget-and-truth** (load-budget tiers, everything-dump,
single-source/drift, invariants-in-gates, persona/ops boundary) — per
`references/subagent-dispatch.md`, then synthesize, ordering by severity.

## Reference map

- `references/intent-router.csv` + `references/intents/<intent>.csv` — the two routing layers.
- `references/playbooks/<surface>.md` — the five agent-native doc surfaces.
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/core/{severity-rubric,score-rubric,personas,glossary}.md` — scales, audience, terms.
- `references/{calibration,trackable-findings,modes}.md` — shared (symlinks).
- `templates/*.md` — change-plan, audit-report, design-doc, refactor-runbook, explanation.
- `evals/`, `skill.json` — gates and provenance.
