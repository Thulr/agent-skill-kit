---
name: ui-design
description: Use to PRODUCE or polish user-facing visual UI — design a product screen or dashboard, author a design system with tokens and components, build an interactive prototype, make a slide deck, add motion or atmospheric effects, prepare a design for handoff, or run an anti-slop visual self-review. Triggers on "make this UI look better", "design a dashboard", "build a frontend mockup", "prototype this flow", "author a design system", "make a deck", "add motion", "prepare handoff", "review visual craft". Emits a runnable or viewable visual artifact plus a design brief. Do NOT use to AUDIT an existing interface's usability or accessibility with no new visual design (use ux-audit); do NOT use for developer-facing API/SDK/CLI surfaces (use dx-design); do NOT use for the artifact-host integration contract (use artifact-host-integration).
license: MIT
---

# UI Design

Generative visual UI design: produce and polish interface artifacts that feel
grounded, specific, usable, and visibly intentional. Provenance lives in
`skill.json`; this file is runtime routing only.

**Produces:** a runnable / viewable visual artifact (product screen, prototype,
design-system page, deck, motion scene, or handoff bundle) plus a design brief.
Long runs persist `templates/workflow-state.json` (mode, format, viewport set,
design-system choices).

## Core principle

**Context before craft, show early, iterate small.** Read the product, system,
code, screenshots, and source before inventing visuals. Put a runnable artifact
in front of the user as soon as it can communicate direction.

## Activation

- **Bare invocation** (`"use ui-design"`, `"UI designer"`, `"start"`):
  load `references/starter-scenarios.csv` and `references/intent-router.csv`,
  then show the intent menu with the named starter scenarios on top (each
  pre-routes intent + mode) and offer the full mode choice. Wait. No file
  inspection, network calls, or writes.
- **Concrete invocation** with intent inferable: proceed in Guided Draft unless
  the user requests Autopilot or Grill Me.
- **Ambiguous concrete invocation**: ask one blocker question about audience,
  format, design system, or variation axis before editing.

## Modes

Three shared modes — Guided Draft (default), Autopilot, Grill Me — set
depth-vs-speed up front. Canonical contract in
[`references/modes.md`](./references/modes.md). UI-design specifics:

- **Guided Draft (default):** ask one optionized question round only when the
  answer changes format, audience, design-system binding, or variation count;
  then design, show early, verify, and state assumptions.
- **Autopilot:** proceed from available context; make conservative calls; stop
  only for missing assets, legal/IP risk, destructive edits, or
  credential-bound tooling.
- **Grill Me:** use open questions one at a time to lock audience, system,
  content, interaction, motion, and handoff decisions before drafting.

## Workflow

1. **Route.** Load `references/intent-router.csv`; pick one or more of:
   `product-ui`, `design-system`, `prototype`, `deck`, `motion-scene`,
   `host-handoff`, `quality-review`.
2. **Load details.** Load only the router row's `detail_files` and mapped
   templates. If multiple rows apply, prefer the smallest set that covers the
   deliverable.
3. **Ground the work.** Inspect the brief, product vocabulary, design system,
   tokens, existing components, assets, screenshots, and relevant files. If no
   system exists, use `references/brief-and-format.md` and state the chosen
   aesthetic commitments.
4. **Ask or decide.** Ask one focused question round when blocked. If the user
   says "decide for me", decide and record the call in the artifact or plan.
5. **Plan.** Use `templates/design-brief.md` plus the intent template to name
   audience, format, constraints, direction, variation axes, and checks.
6. **Show early.** Start with layout skeleton, type/color direction, and honest
   placeholders. Surface the artifact as soon as it runs.
7. **Build.** Compose layout, typography, color, content, components, motion,
   and host protocol support in that order. Avoid silent design-system
   invention.
8. **Verify (self-polish).** Check load, console, responsive viewports,
   hover/focus/press, overflow, reduced motion, editability, export needs, and
   the anti-slop pass; the `quality-review` intent runs this as its own route.
9. **Hand off.** Summarize files changed, decisions, verification, remaining
   risks, and any prepared host/export instructions.

## Operational memory

For recurring work, use explicit workflow artifacts first:
`templates/workflow-state.json` copied into the target repo or an approved
host-provided memory surface. Store only non-secret run defaults: mode, output
format, artifact paths, viewport set, accepted design-system choices. Never
store private user facts or identity data.

## Subagent dispatch

Use subagents only when the host/session permits and independent critique helps:
one visual-craft reviewer, one user-task reviewer, one implementation/handoff
reviewer. If subagents are unavailable, run the same three lenses sequentially
using `references/subagent-dispatch.md`.

## Output requirements

Every output names the user/audience, chosen format, design-system binding or
from-scratch commitments, files/artifacts produced, verification performed, and
the anti-slop checks applied. Visual artifacts must be runnable or viewable, not
merely described.

## Reference map

- `references/intent-router.csv` — one-layer intent router (`intent` →
  `detail_files` + `templates`).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/*.md` — routed craft, workflow, host, and review playbooks.
- `templates/*.md` — repeatable brief, plan, system, deck, prototype, and
  review outputs.
- `templates/workflow-state.json` — resumable state for long runs.
- `evals/*` — activation, scenario, and static checks.
