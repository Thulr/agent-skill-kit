# Bundling & handoff

Packaging an artifact for life *outside* its authoring host — shareable links,
offline files, presentations taken elsewhere.

## Three bundling levels

| Level | Outcome | Use when |
|---|---|---|
| Standalone HTML | One self-contained `.html` | The user wants to email or upload it |
| Project download | Folder of HTML + assets + source | Handoff to engineering or another team |
| Format export | PPTX, PDF, image | The destination isn't a browser |

## Standalone HTML

All CSS, JS, images, and fonts inlined into one file that works online or
offline. The bundler reads the entry HTML, walks every linked stylesheet,
script, image, font, video, and inline `url(...)`, inlines each (text as
content, binary as base64 data URLs), and writes one output file.

### The thumbnail requirement

Single-file bundles can take a moment to unpack on first load. Provide a splash
placeholder the bundler finds by id, so the user sees something immediately:

```html
<template id="__bundler_thumbnail">
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="100" height="100" fill="#0B0D0E"/>
    <text x="50" y="55" text-anchor="middle" font-family="sans-serif"
          font-size="36" font-weight="700" fill="#D7B46A">N</text>
  </svg>
</template>
```

Use a small iconographic SVG (glyph or 1–2 brand letters), ~30% padding per
side. Without it, first load is a blank screen.

### Limitations

Standalone bundles can't reach the network — cross-origin fetches, authenticated
API calls, and un-inlined CDN libraries all fail offline. If the artifact
depends on a runtime API (e.g. a chat completion), that capability disappears;
show a placeholder and degrade gracefully.

## Project download

For engineering handoff, ship the *unbundled* source as a zip — HTML + linked
CSS + JSX + assets, original structure preserved. The recipient can open
`index.html`, drop it on a static host, or wire it into a build.

- **Include:** the HTML entry, all referenced JS/JSX/CSS, asset subfolders
  (`assets/`, `images/`, `fonts/`), and a `README.md` describing what's here,
  dependencies, and how to extend it.
- **Exclude:** the tweaks panel + persistence machinery (unless the team wants
  designer mode), the host-message scaffolding (`__edit_mode_*`, etc.), and
  scraps/drafts/screenshots.

## Format exports

- **PDF** — any HTML; print-to-PDF via browser or host. Fixed-canvas decks get
  clean one-slide-per-page output from the `@page` rule (see `fixed-canvas.md`).
- **PPTX, editable** — deck artifact; host emits native PowerPoint shapes + text
  + images. Text and layout survive; real CSS filters, complex gradients, and
  custom motion don't.
- **PPTX, screenshot** — host captures a full-bleed PNG per slide; embeds as
  image-only slides. Fidelity over editability; text becomes an image.
- **Single image** — host screenshot of any state; thumbnails, social previews,
  docs.

## Conventions for export-friendly artifacts

- **Hide host chrome before capture.** Tweaks panels, dev overlays, and edit
  handles are designer affordances, not deliverable surface. The host passes
  `hideSelectors` for elements to drop before capture.
- **Reset transforms before capture.** Fixed-canvas content renders at native
  size; the host sets a `noscale` attribute and the artifact's CSS unsets its
  scale transform when present (see `fixed-canvas.md`).
- **Use real fonts.** `@font-face` fonts work in exports; CSS-styled emoji and
  web-only fonts may not render in PPTX — substitute or fall back to plain text.

## Versioning for handoff

Mark versions with copy operations (preserve history; don't overwrite in place):
`index.html` is current, `index v2.html` / `index v3.html` for prior major
iterations. Convention, not protocol — but it makes the package
self-documenting.
