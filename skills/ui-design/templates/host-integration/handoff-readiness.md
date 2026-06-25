# Handoff & export readiness

> Output artifact for the `fixed-canvas` / `bundling-export` routes. Run before
> shipping an artifact out of the host (standalone HTML, project zip, or format
> export).

## Target

- **Bundling level:** ☐ Standalone HTML ☐ Project download ☐ Format export (`PPTX | PDF | image`)
- **Destination:** `<email/upload | engineering handoff | stakeholder edits | archival>`

## Before capture / export

- ☐ Host chrome hidden — tweaks panel, dev overlays, edit handles dropped (`hideSelectors`)
- ☐ Transforms reset — fixed-canvas content renders at native size (`noscale`)
- ☐ Real fonts — `@font-face` used; web-only fonts / styled emoji substituted for PPTX
- ☐ Transient markers absent (`data-cc-id`, `data-dm-ref`)

## Standalone HTML

- ☐ All CSS / JS / images / fonts inline; opens offline
- ☐ `<template id="__bundler_thumbnail">` present (small iconographic SVG, ~30% padding)
- ☐ Network-dependent features degrade gracefully (placeholder, not a broken call)

## Project download

- ☐ Unbundled source: HTML entry + linked JS/JSX/CSS + asset subfolders
- ☐ `README.md` describes contents, dependencies, and how to extend
- ☐ Designer-mode machinery and `__edit_mode_*` scaffolding excluded (unless requested)
- ☐ Scraps / drafts / screenshots excluded

## Format export specifics

- ☐ PDF — `@page` rule yields one slide per page for fixed-canvas decks
- ☐ PPTX editable — shapes/text/layout survive; complex filters/gradients/motion will not
- ☐ PPTX screenshot — chosen only when fidelity matters more than editable text
- ☐ Speaker notes carried to presenter pane / opposite page if present

## Versioning

- ☐ Delivered via copy (history preserved): `index.html` current, `index v2.html` for prior majors

## Notes

- `<anything the recipient needs to know — degraded features, manual steps, host dependencies>`
