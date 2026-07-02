---
name: research
description: "Use for source-grounded research — REPORT (open-ended topic primer/lit review) or OPPORTUNITY (validate named product/business/market/feature with FADR memo). Triggers: 'research X', 'primer on X', 'validate whether building X is a good opportunity', 'should we build X'"
license: MIT
---

# Research

Source-grounded research, routed by decision-frame. Pick the frame first; each
frame carries its own workflow. Provenance lives in `skill.json`; this file is
runtime routing only.

**Produces (report):** `research-report-<YYYY-MM-DD>-<topic-slug>.md`.
**Produces (opportunity):** intent-specific artifact (`scope-plan` /
`investigation-brief` / `cross-area-brief` / `fadr-memo`) plus area artifacts,
with optional tracking ledger + workflow-state.

## Boundaries

Do NOT use to review an existing artifact like a prompt, plan, or spec (use
the matching red-team or review skill), to compare a fixed set of
already-named options (use tradeoff-analysis), or to ideate candidates from
scratch.

## Core principle

**Keep the line between what is known and what is asserted visible.** In the
report frame, every load-bearing claim is cited or marked as inference. In the
opportunity frame, every branch ends in a decision (Facts / Assumptions /
Decisions / Risks), not a note. Research that hides that line — or that ends
without a citation or a next test — is a content brief, not research.

## Activation

- **Bare invocation** (`"research"`, `"start"`): show a compact menu: mode choice (guided / autopilot / grill me?) and numbered intents from the router. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with the frame inferable from the prompt: skip to
  step 2.
- **Ambiguous invocation**: ask one — e.g., *"Is this an open-ended topic report or a named opportunity to validate?"* or *"What is the one-sentence topic or opportunity statement?"*

## Workflow

1. **Pick frame.** Load [`references/frame-router.csv`](./references/frame-router.csv).
   Match the prompt to `report` or `opportunity`. A request with a decision
   attached ("should we build / enter / invest", go/no-go, market sizing for a
   named idea) is `opportunity`; an open-ended "what's known about X" with no
   decision is `report`. Ambiguous → ask once.
2. **Load the frame workflow.** Load
   [`references/<frame>/workflow.md`](./references/) and follow it end to end —
   it carries that frame's depth/intent routing, search or fan-out strategy,
   output template, confidence/severity rubrics, and tracking rules. Load only
   the chosen frame's files.

> **Wrong direction?** If the user says this isn't what they meant, go back to step 1 (Pick frame) — do not patch in the wrong direction. Restate the corrected understanding and re-plan.

## Modes

Guided Draft (default), Autopilot, Grill Me — see the frame's `modes.md`
([`references/report/modes.md`](./references/report/modes.md) /
[`references/opportunity/core/modes.md`](./references/opportunity/core/modes.md),
report's symlinked from `skills/_shared/modes.md`; the opportunity frame
carries a frame-specialized fork). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Reference map

- [`references/frame-router.csv`](./references/frame-router.csv) — top-level
  router (frame → frame directory).
- [`references/report/workflow.md`](./references/report/workflow.md) — the
  report frame: depth modes (`brief` / `survey` / `deep-dive`), search
  strategy, source triage, confidence, report template.
- [`references/opportunity/workflow.md`](./references/opportunity/workflow.md) —
  the opportunity frame: intent × area routing, sub-agent fan-out, FADR
  decision gate, 14 area artifacts, tracking.
- `templates/report/`, `templates/opportunity/` — the artifacts each frame emits.
- `evals/{activation-cases.md,run-static-checks.sh,trigger-evals.json}` — gates.
- `skill.json` — provenance, grounding sources, version, status.
