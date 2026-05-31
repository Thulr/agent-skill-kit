# Visual Craft

## Typography

Use a type system, not individual font guesses:

- One sans for UI chrome.
- Optional serif for editorial or long-form reading.
- One mono for code, paths, IDs, and structured metadata.

Define a small scale with jobs, for example display, title, heading, body,
caption, chip, and eyebrow. Body text should usually sit at 13-16px in UI and
24px+ in 1920x1080 slides. Use `text-wrap: pretty` for prose and
`text-wrap: balance` for headings when supported. Body letter spacing is `0`;
tracked uppercase belongs only to small eyebrows.

## Color

Use semantic roles, not decorative preference: canvas, surface, border,
primary text, muted text, primary action, focus, success, warning, error, and
info. Dark mode usually needs borders and top-edge highlights more than
shadows. Light mode needs restrained near-black text and cool light borders.

One accent is often stronger than many. If every heading, card, icon, and dot
uses accent color, nothing is accented.

## Spacing and Density

Use a scale such as 4 / 8 / 12 / 16 / 24 / 32 / 48, or the product's own
scale. Prefer flex/grid with `gap` over child margins so direct edit,
reordering, and deletion do not break spacing.

Density communicates product type:

- Dense: 32-36px rows, 8/12/16px padding, working tools.
- Comfortable: 48px rows, 16/24px padding, consumer or reading surfaces.
- Airy: 32/48px section gaps, marketing or premium narrative surfaces.

## Layout

Hierarchy lives mostly in size, then weight, then contrast. If the design
needs more levers, remove elements. Constrain long text to 60-80 characters.
Use negative space intentionally; do not fill sparse areas with filler copy.

Use `grid-template-columns: minmax(0, 1fr)` and set `min-width: 0` on shrinking
children. For truncation, the triplet is `overflow: hidden`,
`text-overflow: ellipsis`, and `white-space: nowrap`.

## CSS Hygiene

Prefer modern primitives: grid, flex, `gap`, `aspect-ratio`, `clamp()`,
`:has()`, `color-mix(in oklch, ...)`, and targeted `@supports` only when a
fallback is necessary. Write canonical HTML: explicit closing tags, lowercase
elements, double-quoted attributes, no self-closing non-void elements.

## Interaction States

- Hover: one subtle band lighter or border stronger.
- Focus: visible ring or inset treatment with strong contrast.
- Press: decisive color/border response, no celebratory scale bounce.
- Disabled: muted text, unchanged layout, `not-allowed` only when a pointer
  exists.

Icon systems should be singular: one family, one stroke/fill model, sizes such
as 16/18/20/24, and `currentColor` inheritance.
