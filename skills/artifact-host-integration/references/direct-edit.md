# Direct edit & edit overrides

Users edit rendered content directly — click a heading and retype, drag to
reposition, change a color via an inspector — and the edits round-trip back to
source. These patterns make that work.

## Write canonical HTML

Direct edit relies on the host reading the rendered DOM and the source agreeing
on what's there. Non-canonical tags often *render* fine but defeat the
DOM-to-source mapping, so the edit happens visually but never persists.

- **Close every non-void element explicitly** — `<p>…</p>`, not a bare `<p>`.
- **Double-quote every attribute** — `class="foo"`, never `class=foo`.
- **Don't self-close non-void elements** — `<div></div>`, not `<div/>`.
- **Lowercase tag and attribute names.**

## Prefer static markup for editable content

Headings, paragraphs, labels, button text — write as static HTML, not values in
a JS array or component prop:

```html
<!-- Edit-friendly: click and retype -->
<h2>Choose who reads your notebook.</h2>
<p>A runtime reads your files and produces tokens.</p>

<!-- Not edit-friendly: every change must go through chat -->
<script type="text/babel">
  const COPY = { title: 'Choose who reads your notebook.', body: 'A runtime reads your files…' };
</script>
```

Reach for generated markup only when behavior needs it — widgets, charts,
animations, conditional renders.

## Spacing: flex/grid + gap over margin

```html
<!-- Edit-friendly -->
<div style="display:flex; flex-direction:column; gap:12px;">
  <header>…</header><main>…</main><footer>…</footer>
</div>
<!-- Fragile under edit: reorder/duplicate/delete breaks per-child margins -->
<header style="margin-bottom:12px">…</header><main style="margin-bottom:12px">…</main>
```

When the user reorders, duplicates, or deletes children, flex+gap keeps spacing
right automatically. Same logic for rows of buttons, chips, cards, nav items —
any sibling group. Reserve inline flow for sentences with the occasional inline
element.

## The edit-overrides block

When the user makes a *style* change via direct manipulation, the host persists
it in a marked style block (usually at document end) without rewriting the
artifact's main styles:

```html
<style id="__om-edit-overrides">
  [data-comment-anchor="cc-abc123"] { color: #2A6FDB !important; font-size: 18px !important; }
</style>
```

- `id="__om-edit-overrides"` — host-recognized id.
- Rules use `!important` to win over the artifact's own styles.
- Each rule targets a stable selector (a `data-comment-anchor` or other
  deterministic attribute).

## Editing an element that has an override

1. **If the override expresses the user's intent**, keep it (they set the
   heading navy; you're changing the text, not the color).
2. **If the override conflicts** with the new style, edit or remove the rule —
   an inline-style or class change alone won't beat the `!important`.

When in doubt, ask. Silent removal of user overrides is more destructive than
asking. Never strip the edit-overrides block on a rewrite — those rules are the
user's manual tuning.

## Preserving comment anchors through restructure

Carry the anchor onto the *semantically equivalent* element in the new
structure:

```html
<!-- Before -->            <!-- After (button moved into a shared component) -->
<footer>                    <footer>
  <button data-comment-anchor="cc-abc">Get started</button>
                              <PrimaryCta data-comment-anchor="cc-abc">Get started</PrimaryCta>
</footer>                   </footer>
```

If deleting the element entirely, drop the anchor — but warn the comment will
lose its pin.

## Testing direct-edit-readiness

Load in the host, click a heading, retype, save, reload. If the new text
persists, the markup is ready. If not, find the heading in source and verify
it's static markup with a canonical tag pair — not in a JS array, template
literal, or JSX expression.
