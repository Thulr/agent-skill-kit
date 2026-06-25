# Anti-Slop Review

## Single Test

If the design could have come from a generic AI SaaS template, it is not done.
Specificity is the goal: a reviewer should infer the product's audience,
domain, and intent from the visual system and content choices.

## Visual Tropes to Avoid

- Purple-blue gradients as the main identity.
- Animated gradient meshes, floating blobs, or random particles with no
  content role.
- Frosted glass cards over gradients.
- Big blurred glows behind heroes.
- Gradient-border cards and tilted stacked cards.
- Neumorphic surfaces everywhere.
- Mixed icon families or emoji used as section markers.
- Corporate line-art people, generic decorative icons, and fake mascot art.
- Four-stat hero grids, fake logo rows, repeated three-column feature grids,
  and FAQ sections used to pad thin content.
- Aggressive gradient backgrounds with no content purpose.
- Glassmorphism applied by default to every surface.
- Left-border accent callout cards used as a crutch for hierarchy.
- Fake dashboards filled with arbitrary numbers.
- Stock-photo hero sections with overlaid text.
- Oversized rounded rectangles as a substitute for visual hierarchy.
- Rainbow palettes with no semantic logic.
- Decorative SVG illustrations pretending to be product imagery.

One trope may be intentional. Three means restart or commit to a stronger
non-generic direction.

## Posture Tropes to Avoid

- **Minimal is not automatically good.** Stripping everything down without
  intention leaves an artifact that feels unfinished, not designed.
- **Dense is not automatically cluttered.** A tool UI with dense, precise
  layout communicates capability. Choose density deliberately.
- **The first idea is usually generic.** The layout, component, or color
  scheme that comes to mind fastest is also the one every AI model produces.
  Iterate past the first pass.

## Copy Tropes to Avoid

Cut cheerleading, hedging, and marketing filler from product UI:

- "Let's get started"
- "Awesome"
- "Your AI assistant is ready"
- "Click here"
- "Discover the power"
- "Unlock"
- "Supercharge"
- "Something went wrong" with no recovery path
- Vague labels like "Insights", "Growth", "Scale", "Optimize" with no real
  content backing them up

Use direct product language instead: "Open", "Save", "Connect runtime",
"Could not reach the runtime", "Drop a markdown file to start".

## Review Lenses

Run at least three lenses:

- **Visual craft:** type scale, spacing, alignment, contrast, palette, radius,
  icon family, and state polish.
- **User task:** can the primary user see the next correct action, recover,
  and understand status without explanation?
- **Implementation/handoff:** can the artifact be edited, shipped, exported,
  and maintained without fragile assumptions?

## Severity

- **0:** taste note; optional.
- **1:** polish issue visible to careful reviewers.
- **2:** quality issue most users will notice.
- **3:** task, brand, accessibility, or export problem that blocks approval.
- **4:** excludes users (keyboard-inoperable or content not perceivable),
  legal/IP, privacy, destructive, or seriously misleading output.

## Anti-Slop Pass

Before final handoff, list what was intentionally committed to: material,
type, accent, density, component vocabulary, content style, imagery strategy,
and motion intensity. If those commitments are missing or contradictory, fix
the design before adding more detail.

## Boundary

This skill can flag accessibility risk, focus gaps, contrast problems, and
motion concerns. For a formal WCAG-oriented audit, hand off to the
`ux-audit` skill after the visual direction is stable.
