# Fixed-canvas scaling

Slide decks, video-style content, and other fixed-aspect artifacts render at
authored dimensions (typically 1920×1080) while fitting any viewport.

## The setup

Two elements: a **stage** that fills the viewport and letterboxes, and a
**canvas** at fixed authored size, scaled to fit.

```css
.stage {
  width: 100vw; height: 100vh;
  background: #000;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.canvas {
  width: 1920px; height: 1080px;
  transform-origin: center center; /* transform: scale(...) set by JS */
}
```

```js
function fit() {
  const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
  canvas.style.transform = `scale(${scale})`;
}
window.addEventListener('resize', fit);
fit();
```

Content authors at 1920×1080; the viewport letterboxes; nothing inside the
canvas needs to know about the host viewport.

## Controls *outside* the scaled canvas

Put prev/next buttons and scrub controls in the **stage**, not the **canvas**,
so they stay usable size on a small viewport. A 48×48 button inside the canvas
shrinks with it — to maybe 10px — and becomes un-tappable.

```html
<div class="stage">
  <div class="canvas"><!-- slides authored at 1920×1080 --></div>
  <div class="controls"><button>←</button> <button>→</button></div>
</div>
```

## The export hook

Export pipelines need native-size rendering. Provide an escape hatch the host
toggles before/after capture:

```js
canvas.setAttribute('noscale', ''); // host posts before capture; removes after
```
```css
.canvas[noscale] { transform: none !important; width: 1920px !important; height: 1080px !important; }
```

## Print to PDF

With one `@page` rule the canvas prints cleanly — one slide per page:

```css
@page { size: 1920px 1080px; margin: 0; }
@media print {
  .stage { display: block; }
  .canvas { width: 1920px; height: 1080px; transform: none; page-break-after: always; }
}
```

For a multi-slide deck, render one `.canvas` per slide during print; the browser
produces one page each.

## Multi-slide variant

```css
.canvas section { display: none; }
.canvas section[data-active] { display: block; }
```
```js
function goToSlide(i) {
  document.querySelectorAll('.canvas section').forEach((s, j) => s.toggleAttribute('data-active', i === j));
  window.parent.postMessage({ slideIndexChanged: i }, '*'); // keeps host speaker notes in sync
}
```

## Why not `zoom` or vw/vh?

`zoom` is non-standard with subtle event/font/layout differences; `transform:
scale()` is portable. `vw/vh` sizing tempts but breaks print/export tools (which
expect fixed-pixel content) and misaligns with pixel-sized library components.
Pick one model and commit.

## Common bugs

- **Black bars with no offscreen content** — the canvas got `position: absolute`
  and lost centered flow; keep the stage a flex centerer.
- **Off-by-one positioning** — `transform-origin: top left` instead of
  `center center` offsets everything.
- **Tap targets too small** — controls are inside the canvas; move them to the
  stage.
- **Resize lag** — throttle only if the recompute is heavy; a plain `scale()`
  needs none.
