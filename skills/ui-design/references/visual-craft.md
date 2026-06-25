# Visual Craft

## Typography

Use the existing type system first. If none exists, choose deliberately based
on the artifact's job:

- **Editorial / long-form:** serif or humanist headline with a restrained sans
  body. Generous leading.
- **Software / productivity:** precise sans with strong numeric treatment.
  Compact but legible.
- **Deck / presentation:** large, clear, high contrast. Body text 24px+ on a
  1920×1080 canvas.
- **Technical / developer-facing:** code-family accent only, not mono
  everywhere.
- **Luxury / minimal:** fewer weights, more spacing discipline.

Define a small scale with jobs, for example display, title, heading, body,
caption, chip, and eyebrow. Body text should usually sit at 13-16px in UI and
24px+ in 1920x1080 slides. Use `text-wrap: pretty` for prose and
`text-wrap: balance` for headings when supported. Body letter spacing is `0`;
tracked uppercase belongs only to small eyebrows.

Avoid overused defaults when a stronger choice fits the artifact.

## Color

Use semantic roles, not decorative preference: canvas, surface, border,
primary text, muted text, primary action, focus, success, warning, error, and
info. Dark mode usually needs borders and top-edge highlights more than
shadows. Light mode needs restrained near-black text and cool light borders.

If no palette exists, define a small system:

- Neutrals, surface, ink, muted text, border, accent, danger/success as needed.
- One primary accent unless the assignment calls for a broader palette.
- Prefer `oklch` for harmonious invented palettes when browser support allows.
- Check contrast for important text and controls.

One accent is often stronger than many. If every heading, card, icon, and dot
uses accent color, nothing is accented. Do not invent lots of colors from
scratch — start with a small set and add only when a semantic need is proven.

## Spacing and Density

Use a scale such as 4 / 8 / 12 / 16 / 24 / 32 / 48, or the product's own
scale. Prefer flex/grid with `gap` over child margins so direct edit,
reordering, and deletion do not break spacing.

Density communicates product type:

- Dense: 32-36px rows, 8/12/16px padding, working tools.
- Comfortable: 48px rows, 16/24px padding, consumer or reading surfaces.
- Airy: 32/48px section gaps, marketing or premium narrative surfaces.

## Layout and Composition

Design with rhythm: scale, whitespace, density, alignment, repetition,
contrast, and interruption. Avoid making every section the same card grid.

Hierarchy lives mostly in size, then weight, then contrast. If the design
needs more levers, remove elements. Constrain long text to 60-80 characters.
Use negative space intentionally; do not fill sparse areas with filler copy.

For product UIs, prioritize speed of comprehension over decoration. The user
should find the action they need on first glance.

For marketing surfaces, make one idea land per section. If a section has no
single job, remove it.

For dashboards, avoid "data slop" — only show data that helps the user decide
or act. Every metric on screen should answer a question the user is likely to
ask.

Use `grid-template-columns: minmax(0, 1fr)` and set `min-width: 0` on shrinking
children. For truncation, the triplet is `overflow: hidden`,
`text-overflow: ellipsis`, and `white-space: nowrap`.

## Motion

Use motion as discipline, not theater.

Good motion:
- Clarifies state changes (what just happened, what to expect next).
- Reduces anxiety during loading (progress, not spinning).
- Shows continuity between surfaces (where an element came from, where it went).
- Gives controls tactility (press feels like press).
- Stays subtle — the user shouldn't notice the animation on its own.

Bad motion:
- Loops without purpose.
- Delays the user from taking the next action.
- Calls attention to itself instead of the content.
- Hides poor hierarchy behind movement.

Respect `prefers-reduced-motion` for non-trivial animation.

## Interaction States

- Hover: one subtle band lighter or border stronger.
- Focus: visible ring or inset treatment with strong contrast.
- Press: decisive color/border response, no celebratory scale bounce.
- Disabled: muted text, unchanged layout, `not-allowed` only when a pointer
  exists.

Icon systems should be singular: one family, one stroke/fill model, sizes such
as 16/18/20/24, and `currentColor` inheritance.

## CSS Hygiene

Prefer modern primitives: grid, flex, `gap`, `aspect-ratio`, `clamp()`,
`:has()`, `color-mix(in oklch, ...)`, and targeted `@supports` only when a
fallback is necessary. Write canonical HTML: explicit closing tags, lowercase
elements, double-quoted attributes, no self-closing non-void elements.

## Images and Icons

Use real supplied imagery when available. If an asset is missing:

- Use a clean placeholder (grey field or subtle pattern, not a photo).
- Use typography, layout, or abstract texture instead of decorative imagery.
- Ask for the real asset when fidelity matters.

Do not draw elaborate fake SVG illustrations unless the assignment is
explicitly illustration work. Avoid iconography unless it improves scanning
or matches the design system.

## Copyright and Reference Models

Do not recreate a company's distinctive UI, proprietary screens, or exact
visual identity unless the user clearly has rights to that source. It is
acceptable to extract general design principles (density without clutter,
command-first interaction, monochrome with one accent). Transform posture
and principles into an original design — do not clone.
