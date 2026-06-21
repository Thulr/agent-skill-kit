# Speaker notes

For narrated decks. The artifact ships per-slide notes; the host renders them in
a side panel that follows the active slide.

## The data

Notes live as a JSON array inside a `<script>` with a known `id`. One string per
slide, in slide order. Empty strings for slides without notes — **positions
matter**; entry N is for slide N.

```html
<script type="application/json" id="speaker-notes">
[
  "Welcome slide — open with the elevator pitch, 30 seconds.",
  "",
  "Architecture overview. Walk the layers, then call out the local-first principle bottom-right.",
  "Stat slide — just say the number out loud."
]
</script>
```

`type="application/json"` keeps the browser from executing it; the host parses
it on load.

## The sync protocol

On every active-slide change, post:

```js
window.parent.postMessage({ slideIndexChanged: i }, HOST_ORIGIN);
```

The artifact **must** post:
- On initial render (so the panel shows slide 0's notes immediately).
- On every navigation — next, prev, keyboard, click, scrub, jump.

Forgetting the initial post is the most common bug: the panel shows nothing
until the first navigation, then catches up.

```js
const notes = JSON.parse(document.querySelector('#speaker-notes').textContent);
function goToSlide(i) {
  document.querySelectorAll('section').forEach((s, j) => s.toggleAttribute('data-active', i === j));
  window.parent.postMessage({ slideIndexChanged: i }, HOST_ORIGIN);
}
goToSlide(0); // post on load
```

## Authoring: scripts, not summaries

A note is a *script* the speaker reads under pressure:
- **Full conversational sentences** — what to actually say.
- **Stage directions in brackets** — "[Pause for laughs]", "[Click to reveal
  chart]", "[If running long, skip the example]".
- **Spell out tongue-twister numbers** — "twelve hundred", not "1,200".
- **No bullet points** — fragments force the speaker to extemporize.

## When *not* to add notes

Self-running decks, decks for unattended sharing, and quick mockups. Default to
**no notes** unless the user asked or the deck's purpose clearly requires them.

## Keeping notes in sync when slides change

Reorder slides → reorder notes by the same shuffle. Insert a slide → insert `""`
at the same index. Delete a slide → delete its entry. Drift is silent: every
slide reads the wrong note and the speaker doesn't notice until they're on
stage.

## Reuse in export

PDF: append the script as a presenter-notes page opposite each slide. PPTX:
attach each note to its slide's notes pane. Most pipelines handle this
automatically when `#speaker-notes` is in the standard format.
