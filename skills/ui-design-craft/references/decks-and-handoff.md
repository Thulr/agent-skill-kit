# Decks and Handoff

## Deck System

Before slide one, define the system:

- 16:9 at 1920x1080 unless the brief says otherwise.
- Four type values max: title, body, caption, eyebrow.
- Title floor around 48-56px; body floor 24px.
- Two backgrounds, three text levels, one accent.
- A consistent grid, margins, section-starter style, and image treatment.

A deck needs rhythm: a small kit of recurring layouts plus section starters
every 4-6 content slides. Too many unique layouts read chaotic; one layout
repeated reads exhausting.

## Slide Layout Kit

Common layouts: title, section starter, title plus body, title plus bullets,
title plus image, full-bleed image, two-column, stat slide, quote slide, and
closing. Pick the layout that fits the content, not the next template in a
sequence.

## Imagery and Charts

Commit to an image strategy. Real photography generally beats generated
illustration when the audience needs to inspect reality. Use one chart per
slide when possible. Make the title state the takeaway, annotate data directly,
and avoid importing colors outside the deck system.

## Speaker Notes

Use notes only when the deck is presented live or narrated. Notes should be
script-like full sentences, one string per slide in order, with empty strings
for slides without notes. When slides move, notes move with them. On active
slide change, post `slideIndexChanged` to keep the host panel synchronized.

## Fixed Canvas Scaling

For decks and video-like artifacts, use a viewport-filling stage that centers
a fixed-size canvas. The canvas scales with `transform: scale()`; controls live
outside the scaled canvas so they remain tappable. Provide a `noscale` escape
hatch for export capture and a print stylesheet with `@page` matching the
canvas size.

## Bundling Levels

- **Standalone HTML:** one self-contained file with CSS, JS, images, and fonts
  inlined. Include a small `__bundler_thumbnail` template for first-load
  preview.
- **Project download:** source folder with entry HTML, CSS/JS/JSX, assets, and
  README for engineering or another team.
- **Format export:** PDF, PPTX, or images. Editable PPTX wins when the user
  needs to revise in PowerPoint; screenshot PPTX wins only for visual effects
  that cannot be represented natively.

## Handoff Rules

Hide tweaks panels, dev overlays, and host chrome before capture. Reset scaled
transforms for export. Include tokens, component states, known limitations, and
version notes. Handoff should be runnable, not just readable.
