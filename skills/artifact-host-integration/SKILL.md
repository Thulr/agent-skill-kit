---
name: artifact-host-integration
description: Use to IMPLEMENT or wire the contract between a portable HTML artifact and its hosting/editing shell — the postMessage handshake for a live tweaks panel, the EDITMODE persistence block, fixed-canvas (1920×1080) scaling and print/export, speaker-notes slide sync, comment/scene anchors (data-comment-anchor, data-screen-label) and mentioned-element resolution, direct-edit-ready markup, and standalone bundling / PPTX / PDF handoff. For agents emitting host-cooperative artifacts and engineers building the host side. Triggers on "wire up the tweaks panel", "persist edits back to the artifact source", "sync speaker notes to slides", "make this direct-edit ready", "scale a 1920x1080 deck to the viewport", "bundle this to standalone HTML", "resolve which element the user commented on". Do NOT use for visual / UI craft or preparing a design for handoff — layout, type, color, components, motion, anti-slop, handoff briefs (use ui-design); not for general API / SDK / CLI design (use dx-design).
license: MIT
---

# Artifact–Host Integration

Wire the contract between a portable HTML artifact and the editing/preview shell
("host") that runs it. The artifact stays a plain HTML document; the host wraps
it in an iframe with editing chrome; the two talk over `postMessage`, and edits
persist by the host rewriting marked regions of the source on disk. Provenance
lives in `skill.json`; this file is runtime routing only.

**Produces:** the integration code/markup for one or more host contracts (tweak
panel, fixed-canvas scaling, speaker notes, comment/scene anchors, direct-edit
markup, bundling/export) plus an `integration-checklist.md` recording what was
wired and what was deliberately left out.

## Core principle

**Portable by default, integrated by opt-in.** Every protocol here is opt-in: an
artifact that never posts a host message simply doesn't get that affordance and
still works as a standalone page. Never let host wiring break the
strip-it-and-it's-just-HTML invariant. Two conventions are load-bearing
throughout: host-protocol messages use a `type` starting with `__`, and
persisted regions sit between `/* IDENTIFIER-BEGIN */ … /* IDENTIFIER-END */`
comment fences that the host rewrites in place.

## Activation

- **Bare invocation** (`"use artifact-host-integration"`, `"host integration"`,
  `"start"`): load `references/intent-router.csv`, show the intent menu, and
  wait. No file inspection, network calls, or writes.
- **Concrete invocation** with the contract inferable: proceed in Guided Draft
  unless the user asks for Autopilot or Grill Me.
- **Ambiguous invocation**: ask one blocker question naming the candidate
  contracts before editing.

## Workflow

1. **Route.** Load `references/intent-router.csv`; pick one or more contracts:
   `architecture`, `tweak-panel`, `fixed-canvas`, `speaker-notes`,
   `mentioned-elements`, `direct-edit`, `bundling-export`.
2. **Load details.** Read only the routed rows' `detail_files` (always including
   `references/architecture.md` for the conventions) plus the mapped templates.
3. **Ground the work.** Inspect the artifact's current markup, any existing host
   markers (`/*EDITMODE-*/`, `__om-edit-overrides`, `data-comment-anchor`,
   `data-screen-label`), and what the host actually supports. Don't invent
   anchors or message types the host doesn't own.
4. **Implement.** Wire the contract exactly as the playbook specifies — message
   order, marker shape, and attribute names are protocol, not style. Register
   listeners before posting availability; keep persisted blocks valid and
   singular.
5. **Verify.** Run the contract's checks: edit-mode toggle round-trip, reload
   persistence, slide-index sync, anchor survival across restructure, and a
   standalone-bundle smoke test where relevant.
6. **Hand off.** Use `templates/integration-checklist.md` (and
   `templates/handoff-readiness.md` for export) to record contracts wired,
   invariants preserved, and any opt-out left in place.

## Modes

Guided Draft (default), Autopilot, Grill Me — shared contract in
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the contracts wired, the exact message types / markers /
attributes touched, the portability opt-out preserved, the verification run, and
anything the host must do on its side. This skill implements the artifact↔host
*contract*; it does not do visual or UX craft — route layout, type, color,
component, motion, and anti-slop work to `ui-design`, and general API / SDK / CLI
design to `dx-design`.

## Reference map

- `references/intent-router.csv` — one-layer contract router.
- `references/architecture.md` — postMessage + marker + `data-` conventions and
  the portability invariant (shared by every route).
- `references/tweak-panel.md` — live edit-mode handshake + EDITMODE persistence
  block.
- `references/fixed-canvas.md` — stage/canvas scaling, `noscale` export hook,
  print-to-PDF.
- `references/speaker-notes.md` — per-slide notes JSON + `slideIndexChanged`
  sync.
- `references/mentioned-elements.md` — `data-screen-label`,
  `data-comment-anchor`, transient markers, mentioned-element resolution.
- `references/direct-edit.md` — canonical/static markup, flex+gap spacing,
  edit-overrides block.
- `references/bundling-export.md` — standalone HTML, thumbnail, project download,
  PPTX / PDF / image export.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `templates/integration-checklist.md`, `templates/handoff-readiness.md` —
  conformance + export outputs.
- `evals/*` — activation, trigger, and static checks.
