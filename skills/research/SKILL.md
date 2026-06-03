---
name: research
description: Use for source-grounded research in one of two decision-frames. REPORT — open-ended research on a topic with no decision attached (primer, literature review, state of the art), e.g. 'research X for me', 'what's known about X', 'deep dive on X'. OPPORTUNITY — validate a named product, business, market, or feature opportunity across 14 areas (market, customer, competitive, technical, financial, legal, and more) ending in a Facts/Assumptions/Decisions/Risks go, no-go, or pivot memo. Triggers on 'research X', 'give me a primer on X', 'validate whether building X is a good opportunity', 'should we build X'. Do NOT use to review an existing artifact like a prompt, plan, or spec (use a dedicated red-team or review skill), to compare a fixed set of already-named options, or to ideate candidates from scratch.
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

## Core principle

**Keep the line between what is known and what is asserted visible.** In the
report frame, every load-bearing claim is cited or marked as inference. In the
opportunity frame, every branch ends in a decision (Facts / Assumptions /
Decisions / Risks), not a note. Research that hides that line — or that ends
without a citation or a next test — is a content brief, not research.

## Activation

- **Bare invocation** (`"research"`, `"start"`): ask which frame fits in one
  question — open-ended topic report, or validating a named opportunity toward
  a decision — then offer the mode choice. Wait. No file inspection, no network
  calls, no writes.
- **Concrete invocation** with the frame inferable from the prompt: skip to
  step 2.
- **Object missing** (`"research this"` / `"do research"` with no topic or
  opportunity stated): ask for the one-sentence topic or opportunity statement
  before routing. A topic too broad returns noise; an opportunity with no scope
  fans out into disconnected dumps — both are named failure modes.

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

## Modes

Guided Draft (default), Autopilot, Grill Me — see the frame's `modes.md`
([`references/report/modes.md`](./references/report/modes.md) /
[`references/opportunity/core/modes.md`](./references/opportunity/core/modes.md),
both sourced from `skills/_shared/modes.md`). Offer the mode at bare
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
