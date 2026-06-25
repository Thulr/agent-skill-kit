# Brief and Format

## Question Round

Ask only when the answer changes the design. Cover:

- Starting context: codebase, design system, UI kit, brand references, assets.
- Audience and setting: internal tool, consumer app, live presentation,
  async share, marketing surface, executive review, engineering handoff.
- Output format: HTML mockup, HTML prototype, design canvas, animated HTML,
  slide deck, PDF, PPTX, static asset, or handoff package.
- Variations: count and axis. Visual direction, flow structure, density,
  palette, type, or copy.
- Novelty appetite: conservative, distinctive, or exploratory.
- Tweak surface: which live controls matter, such as palette, density,
  copy, step, or animation.

Provide options plus "decide for me" for most questions. If the user says
decide for me, decide and move on.

## Variation Exploration

When the brief asks for options or the direction is uncertain, default to
three variants that explore different dimensions:

- **Conservative** — closest to existing patterns, lowest risk. Honours the
  existing design system or product conventions. Use when fidelity to what
  exists is the priority.
- **Strong-fit** — best interpretation of the brief. The most direct answer
  to the user's stated needs. Use when the goal is "make it right."
- **Divergent** — more novel, useful for discovering taste boundaries and
  hidden preferences. Changes a load-bearing assumption (layout, density,
  color posture, interaction model). Use when the user says "surprise me"
  or the first direction feels generic.

Variants can explore different dimensions on each axis:

| Axis | What changes |
|---|---|
| Layout | Single column vs multi-panel, sidebar vs top nav, card vs list |
| Hierarchy | What gets primary visual weight, what gets collapsed |
| Type scale | Display-driven vs body-driven, serif vs sans vs mono voice |
| Density | Dense tool UI vs comfortable consumer vs airy narrative |
| Color posture | Light vs dark, saturated vs muted, warm vs cool accent |
| Surface treatment | Flat vs subtle elevation, border vs fill, sharp vs soft radius |
| Motion | Static vs animated, utilitarian vs expressive |
| Interaction model | Click-through vs inline edit, stepped vs freeform |
| Copy structure | Short headline + detail vs narrative lead vs data-first |
| Component shape | Pill buttons vs square, outlined cards vs filled |

Do not create variants that differ only by color swap unless color is the
actual question being decided. Each variant should test a meaningful
hypothesis about the design direction.

When the user picks a direction, **consolidate.** Do not leave the project
as a pile of options. Merge the strongest ideas from each direction into
one coherent artifact, then polish.

## Format Picker

- **HTML mockup:** static in-browser visual review. Use when layout, type,
  hierarchy, and copy are the main questions.
- **HTML prototype:** working slice with state and interaction. Use for flows,
  forms, branching, latency, feedback, or error handling.
- **Design canvas:** multiple artboards in one file. Use for 3-6 directions
  or side-by-side comparisons.
- **Animated HTML:** timeline, scene, or motion-design artifact. Include a
  scrubber for iteration.
- **Slide deck:** fixed-canvas presentation with keyboard navigation,
  print-to-PDF, and optional speaker notes.
- **PDF/PPTX/image:** export formats, not primary design sources unless the
  user specifically needs them.
- **Handoff package:** runnable source, tokens, component notes, edge cases,
  and implementation guidance for engineering.

When unsure, ask format before building. If the user only asks for "a design",
default to HTML mockup. If they ask for "options", default to a design canvas.
If they ask for "the flow", default to prototype.

## From-Scratch Commitments

Without an existing brand, generic is the default risk. Commit explicitly:

- One material: graphite, paper, color-saturated, brutalist mono, or soft
  organic.
- One type voice: serious geometric, editorial serif, humanist sans, or
  code-heavy mono.
- One accent used sparingly for primary action, focus, and emphasis.
- One radius family: sharp, soft, or round.
- One density: dense for tools, comfortable for consumer flows, airy for
  marketing and presentations.

The test: a reviewer should be able to name what kind of product this is from
the interface alone.
