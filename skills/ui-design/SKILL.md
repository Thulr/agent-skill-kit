---
name: ui-design
description: "Use to PRODUCE or polish user-facing visual UI — design a product screen or dashboard, author a design system with tokens and components, build an interactive prototype, make a slide deck, add motion or atmospheric effects, prepare a design for handoff, or run an anti-slop visual self-review. Triggers on make this UI look better, design a dashboard, build a frontend mockup, prototype this flow, author a design system, make a deck, add motion, prepare handoff, review visual craft. Do NOT use for UX/accessibility audit (use ux-audit) or developer-facing surfaces (use dx-design)."
license: MIT
---

# UI Design

Generative visual UI design: produce and polish interface artifacts that feel
grounded, specific, usable, and visibly intentional. Provenance lives in
`skill.json`; this file is runtime routing only.

**Produces:** a runnable/viewable visual artifact (product screen, prototype,
design-system page, deck, or handoff bundle plus a design brief.
Long runs persist `templates/workflow-state.json` (mode, format, viewport,
design-system choices).

## Core principle

**Context before craft, show early, iterate small.** Read the product, system,
code, screenshots, and source before inventing visuals. Put a runnable artifact
in front of the user as soon as it can communicate direction.

## Activation

- **Bare invocation** (`"use ui-design"`, `"UI designer"`, `"start"`):
  show a compact menu: mode choice (guided / autopilot / grill me?) and
  numbered intents from the router. Wait. No file inspection, network
  calls, or writes.
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
   `host-handoff`, `host-integration`, `quality-review`.
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
8. **Verify (self-polish).** Load `references/browser-verification.md` and
   follow its concrete browser-tool checks: navigate to the rendered artifact,
   visually inspect it with the session's vision/screenshot tool, check the console for errors,
   verify responsive viewports, interaction states, and reduced motion. Also
   check editability, export needs, and the anti-slop pass. The `quality-review`
   intent runs this as its own route.
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
One visual-craft reviewer, one user-task reviewer, one implementation/handoff
reviewer. If subagents unavailable, run the three lenses sequentially
using `references/subagent-dispatch.md`.

## Output requirements

Every output names the user/audience, format, design-system binding, files
produced, verification performed, and anti-slop checks. Visual artifacts must
be runnable or viewable, not merely described.

## Reference map

- `references/intent-router.csv` — intent router (`intent` →
  `detail_files` + `templates`). Routes: `product-ui`, `design-system`,
  `prototype`, `deck`, `motion-scene`, `host-handoff`, `host-integration`,
  and `quality-review`.
- `references/host-integration/*.md` — postMessage handshake, EDITMODE
  persistence, fixed-canvas scaling, speaker-notes sync, comment anchors,
  direct-edit markup, bundling/export.
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/*.md` — routed craft, workflow, host, and review playbooks.
- `templates/*.md` — repeatable brief, plan, system, deck, prototype, and
  review outputs.
- `templates/workflow-state.json` — resumable state for long runs.
- `evals/*` — activation, scenario, and static checks.
