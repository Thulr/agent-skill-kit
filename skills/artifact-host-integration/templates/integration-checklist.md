# Artifact–host integration checklist

> Output artifact for `artifact-host-integration`. Record which host contracts
> were wired, the exact protocol surface touched, and the portability opt-out
> preserved. Copy into the target repo or paste into the handoff message.

## Summary

- **Artifact:** `<path/to/index.html>`
- **Host contracts wired:** `<architecture | tweak-panel | fixed-canvas | speaker-notes | mentioned-elements | direct-edit | bundling-export>`
- **Portability invariant preserved:** ☐ yes — strip host messages and it's still a working HTML page

## Conventions (architecture)

- ☐ Host-protocol messages use a `__`-prefixed `type`; app messages do not
- ☐ Persisted regions sit in exactly one `/* IDENTIFIER-BEGIN */ … /* IDENTIFIER-END */` block per identifier
- ☐ Host-inspected attributes use stable `data-` prefixes; transient markers (`data-cc-id`, `data-dm-ref`) are not authored or persisted
- ☐ Every `message` listener is registered **before** its `__..._available` post

## Per-contract

### Tweak panel
- ☐ Listener handles `__activate_edit_mode` / `__deactivate_edit_mode`
- ☐ `__edit_mode_available` posted after listener is live; `__edit_mode_dismissed` on self-close
- ☐ Exactly one valid-JSON `/*EDITMODE-BEGIN*/…/*EDITMODE-END*/` block inside an inline `<script>`
- ☐ Changes post `__edit_mode_set_keys` with partial `edits`
- ☐ Only curated axes exposed (no raw CSS-variable dump)

### Fixed canvas
- ☐ Stage (viewport) + canvas (authored size) with `transform: scale()` and `center center` origin
- ☐ Controls live in the stage, not the scaled canvas
- ☐ `noscale` export hook unsets the transform; `@page` print rule present if PDF matters

### Speaker notes
- ☐ `<script type="application/json" id="speaker-notes">` array, one entry per slide (positions aligned)
- ☐ `{ slideIndexChanged: i }` posted on initial render **and** every navigation

### Mentioned elements
- ☐ `data-screen-label` on top-level scenes (1-indexed, matches visible counter)
- ☐ `data-comment-anchor` values preserved through edits; moved with the semantic-equivalent element on restructure

### Direct edit
- ☐ Editable content is canonical, static markup (not JS arrays / template literals)
- ☐ Sibling spacing uses flex/grid `gap`, not per-child margin
- ☐ `<style id="__om-edit-overrides">` block preserved on rewrite

### Bundling / export
- ☐ `<template id="__bundler_thumbnail">` present for standalone bundles
- ☐ Host chrome dropped via `hideSelectors`; transforms reset before capture
- ☐ Network-dependent features degrade gracefully offline

## Verification run

| Check | Result |
|---|---|
| Edit-mode toggle round-trip | ☐ |
| Reload persistence (EDITMODE / direct edit) | ☐ |
| Slide-index → notes sync (incl. initial) | ☐ |
| Comment anchor survives a restructure | ☐ |
| Standalone bundle opens offline | ☐ |

## Left out on purpose

- `<contract or affordance intentionally not wired, and why>`

## Host-side requirements

- `<anything the host must do: surface a toggle, write the EDITMODE block, pass hideSelectors, etc.>`
