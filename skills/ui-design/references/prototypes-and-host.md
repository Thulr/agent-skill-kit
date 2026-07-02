# Prototypes and Host Integration

## Prototype or Mockup

Use a mockup when the user reviews layout, hierarchy, visual direction, or
static content. Use a prototype when interaction matters: onboarding, forms,
branching, state changes, latency, error handling, or pacing.

A prototype must be believable, not complete. Mock the interactions under
review, stub backend wiring, and use realistic but honest data.

## Variations as Tweaks

If the user wants comparisons, prefer one artifact with curated tweaks over
many copied files. Expose legitimate design axes: palette, density, flow
variant, copy, step, or a key layout choice. Do not expose every CSS variable,
spacing value, or animation timing.

Tweak controls should be discrete: toggle, radio, select, slider, curated
swatches, number, or text. Free-form controls are a last resort.

## Host Tweak Protocol

For hosts that support designer-mode panels:

- Register the `message` listener before posting availability.
- Listen for `__activate_edit_mode` and `__deactivate_edit_mode`.
- Post `__edit_mode_available` after the listener is live.
- Persist changes by posting `__edit_mode_set_keys` with partial edits.
- Store defaults in exactly one valid JSON block between
  `/*EDITMODE-BEGIN*/` and `/*EDITMODE-END*/` inside an inline script.

If the panel has a close button, post `__edit_mode_dismissed` so host chrome
stays synchronized.

## Direct Edit Readiness

Write editable content as static markup. Headings, paragraphs, labels, and
button text should not be buried inside arrays or template literals unless the
behavior requires it. Use canonical HTML and flex/grid `gap` for sibling
spacing so source mapping and direct manipulation remain stable.

Keep host-owned anchors:

- `data-screen-label` on top-level scenes, slides, or screens.
- `data-comment-anchor` only when the host stamps a commented element.
- Never invent, duplicate, or strip anchors during a rewrite.

If a user style override exists in an edit-overrides block, preserve it unless
it conflicts with the new design direction. Ask before removing intent-bearing
overrides.

## Mentioned Elements

When the host provides a mentioned-element block, use the React path, DOM
selector, and transient id together. If they point to one source location, edit
it. If repeated components make the target ambiguous, inspect the live DOM or
ask; do not guess.

## Prototype Checks

Verify click paths, keyboard path, reload persistence, tweak persistence,
direct-edit text persistence, and that host-only panels or overlays are hidden
before capture/export.

## Full host protocol

This page is the designer's slice — enough to emit a host-cooperative artifact.
For the complete integration *contract* (exact `postMessage` types, the EDITMODE
persistence block, fixed-canvas scaling, speaker-notes sync, comment/scene
anchor resolution, direct-edit overrides, and bundling/export), use this
skill's host-integration route (`references/host-integration/`).
