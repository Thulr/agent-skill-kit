---
name: minimal-modular-code
description: Use to keep code MINIMAL and right-sized for AI coding agents. DO — keep an in-progress change minimal (reuse before adding, subtract, avoid the wrong abstraction, check blast radius). REVIEW — audit existing code or a repo for slop (duplication, dead code, over-engineering) and parallel-readiness (coupling, boundaries, gate coverage), then score it. DESIGN — shape right-sized boundaries and work-partitioning so many agents work in parallel, sequence a safe refactor, or explain a principle. Triggers on 'is this over-engineered', 'reduce the slop', 'audit our coupling/boundaries', 'structure this repo for parallel agents'. Do NOT use to wire enforcement gates/hooks/AGENTS.md (use harden-repo-for-coding-agents), for developer API/SDK/CLI surfaces (use dx-audit / dx-design), for product UX (use ux-audit / ui-design), or to tighten prose (use writing-audit).
license: MIT
---

# Minimal Modular Code

Keep code minimal and right-sized for AI coding agents — anti-slop in the small, modular
boundaries in the large. Provenance lives in `skill.json`; this file is runtime routing only.

**Produces:** a `change-plan.md` (DO), an `audit-report.md` plus a findings-ledger +
workflow-state when tracked (REVIEW), or a `design-doc.md` / `refactor-runbook.md` /
`explanation.md` (DESIGN).

## Core principle

**Invest in interfaces, not implementations; enforce with gates, not prose; delete
scaffolding as models improve.** The scarce resource is accountable review, not code
generation — so the bar for any line, abstraction, or boundary is whether it earns the
attention it will cost. Minimal is not fewest lines or smallest units; it is *nothing left
to take away* — powerful behavior behind a simple interface, reused before rebuilt, legible
to a reader with a finite context window.

## Activation

- **Bare invocation** (`"use minimal-modular-code"`, `"is this over-engineered"`, `"start"`):
  load `references/intent-router.csv`, show the intent menu, offer the mode. Wait. No file
  inspection, network calls, or writes.
- **Concrete invocation** with intent and surface inferable: skip to step 3.
- **Ambiguous scope**: ask one blocker question naming the candidate intent or surface; do
  not inspect private systems first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`; match to `do`, `review`, or
   `design`. Ambiguous → ask once.
2. **Pick surface.** Load `references/intents/<intent>.csv`; match one or more of
   `minimalism`, `legibility`, `boundaries`, `parallel-readiness`, `enforcement` — or `all`
   for a REVIEW fan-out. Ambiguous → ask once with the menu.
3. **Load grounded context.** Load only the chosen row's `playbook` plus its `core_refs`.
   Do not load other playbooks (the `review`/`all` row carries none — each surface agent loads its own; see step 6).
4. **Identify the target persona** from `references/core/personas.md`.
5. **Then calibrate to project scale** (REVIEW / DESIGN) per `references/calibration.md`:
   below Load-bearing, narrow scope, collapse same-mechanism gaps into one systemic finding,
   and split **Now** vs **Later (as it grows)**. The tier feeds emission, never severity.
6. **Dispatch lenses in parallel** (REVIEW default when permitted): one surface per agent for
   `all`; otherwise the three lenses below. Sequential fallback if no delegation primitive.
7. **Apply the playbook.** Use the heuristics tagged for the intent. For REVIEW, score each
   surface 0–10 (`references/core/score-rubric.md`); synthesize lens findings, preserving
   disagreements as open questions. Apply severity and stable `MM-<surface>-NNN` IDs
   (`references/core/severity-rubric.md`): `MM-MIN`, `MM-LEG`, `MM-BND`, `MM-PAR`, `MM-ENF`.
8. **Emit.** DO → `templates/change-plan.md`. REVIEW → `templates/audit-report.md`. DESIGN →
   `templates/design-doc.md` (shape), `templates/refactor-runbook.md` (sequence a refactor),
   or `templates/explanation.md` (explain a principle).
9. **Create, resume, or close tracking state** (REVIEW). For an audit with 7+ findings, any
   severity 3–4, or a save/track/closeout request, load `references/trackable-findings.md`.
   If the request names an existing ledger, workflow-state, PR, or `MM-*` ID, read
   saved state first; update statuses only after each verification rule passes. Otherwise write the
   ledger at `docs/audits/minimal-modular-code-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and workflow state at
   `docs/audits/minimal-modular-code-workflow-state-<YYYY-MM-DD>-<scope-slug>.json` (fall
   back to `audit-artifacts/minimal-modular-code-...` if `docs/audits/` is unwritable). Report
   both paths; keep roadmaps, issues, and non-tracking edits opt-in.

## Modes

Guided Draft (default), Autopilot, Grill Me — see `references/modes.md`. Offer at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the intent, surface(s), persona, playbook(s) applied, and grounding
sources from `skill.json`; REVIEW adds severity + verification per finding and the project
tier. **Name the seams you are deliberately NOT adding (YAGNI), not only the ones you are.**

## Subagent dispatch

Default for REVIEW when delegation is permitted; skip tiny or secret-bound work. Spawn three
lenses in parallel — **slop-hunter** (duplication, dead code, over-abstraction, verbosity),
**coupling-and-boundary** (dependency direction, deep vs shallow modules, blast radius),
**parallel-readiness** (work-partitionability, contract stability, gate coverage) — per
`references/subagent-dispatch.md`, then synthesize, ordering by severity.

## Reference map

- `references/intent-router.csv` + `references/intents/<intent>.csv` — the two routing layers.
- `references/playbooks/<surface>.md` — minimalism, legibility, boundaries, parallel-readiness, enforcement.
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/core/{severity-rubric,score-rubric,personas,glossary}.md` — scales, audience, terms.
- `references/{calibration,trackable-findings,modes}.md` — shared (symlinks).
- `templates/*.md` — change-plan, audit-report, design-doc, refactor-runbook, explanation,
  plus the shared tracking artifacts.
- `evals/`, `skill.json` — gates and provenance.
