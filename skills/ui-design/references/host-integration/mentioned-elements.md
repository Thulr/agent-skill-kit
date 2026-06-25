# Mentioned elements

When the user clicks, comments on, or drags an element in the rendered artifact,
the host tells the author *which element* they meant. These are the attributes
and the resolution process.

## Two persistent attributes

### `data-screen-label` — high-level scenes

Put it on top-level scenes (slides, screens, major regions) so the host can
describe context: "the user commented on slide 5."

```html
<section data-screen-label="01 Welcome">…</section>
<section data-screen-label="02 Runtime">…</section>
```

Conventions: **1-indexed** for sequential content ("01", not "00"); **match the
visible counter** (footer "5/12" → label "05 …"); **title-case** the descriptive
part ("02 Meet your cast").

### `data-comment-anchor` — pinned references

When a user comments on an element, the host stamps it
`data-comment-anchor="<id>"`, pinning the comment. The author preserves it
through edits:

- **Don't invent anchor values** — the host owns the namespace; you preserve.
- **Don't duplicate an anchor** across siblings — one anchor, one element.
- **Move the anchor with the element** — on restructure, carry it onto the
  *semantic equivalent* in the new structure.
- **Drop it only when deleting** that element entirely (and warn the user the
  pinned comment loses its anchor).

## Transient runtime markers

While the user is actively commenting/editing, the host stamps the hovered
element with a transient attribute: `data-cc-id="cc-N"` (comment/edit modes),
`data-dm-ref="N"` (design mode). They exist only while host UI is active — don't
author them, don't preserve them across edits. You see them only when the host
*describes* a touched element back to you.

## The `<mentioned-element>` block

The host attaches a structured description to its message:

```
<mentioned-element>
react: OnboardingApp > OnboardingModal > FooterBtns > button.cta
dom: section[data-screen-label="04 Tour"] > footer > button
id: data-cc-id="cc-3"
</mentioned-element>
```

- **`react:`** — component path (when fibers are available); highest fidelity.
- **`dom:`** — CSS selector ancestry; always present.
- **`id:`** — the transient runtime marker.

## Resolution

When all three lines point unambiguously to one source location, edit it. When
they don't — the same component renders many times, or the selector is
ambiguous — probe the live DOM to disambiguate. **Do not guess-and-edit.**

If a shared component (`FooterBtns`) is used by multiple screens, the
`data-screen-label` line tells you which instance the user means; decide whether
to change all screens or scope to that one, and ask if unclear.

## Density

Stamp `data-screen-label` on top-level scenes; let the host add
`data-comment-anchor` as the user comments. Don't pre-stamp every button, text
node, or chip — these resolve *referenced* elements, not a universal index.
