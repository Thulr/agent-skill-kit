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

One trope may be intentional. Three means restart or commit to a stronger
non-generic direction.

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

- **S0:** taste note; optional.
- **S1:** polish issue visible to careful reviewers.
- **S2:** quality issue most users will notice.
- **S3:** task, brand, accessibility, or export problem that blocks approval.
- **S4:** legal/IP, privacy, destructive, or seriously misleading output.

## Anti-Slop Pass

Before final handoff, list what was intentionally committed to: material,
type, accent, density, component vocabulary, content style, imagery strategy,
and motion intensity. If those commitments are missing or contradictory, fix
the design before adding more detail.

## Boundary

This skill can flag accessibility risk, focus gaps, contrast problems, and
motion concerns. For a formal WCAG-oriented audit, hand off to
`ux-accessibility-heuristics` after the visual direction is stable.
