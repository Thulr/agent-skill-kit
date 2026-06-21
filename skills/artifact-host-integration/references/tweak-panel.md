# Tweak panel

A small in-artifact UI where the user changes exposed values live. The host
surfaces it on a toolbar toggle; changes persist to disk. Designer-side only —
never shipped to end users.

## The handshake

1. Register a `window` `message` listener that handles:
   - `{ type: '__activate_edit_mode' }` → show the panel
   - `{ type: '__deactivate_edit_mode' }` → hide it
2. *Only after* the listener is live, announce availability:
   ```js
   window.parent.postMessage({ type: '__edit_mode_available' }, HOST_ORIGIN);
   ```
3. If the panel has its own close button, post on close so host chrome stays in
   lockstep:
   ```js
   window.parent.postMessage({ type: '__edit_mode_dismissed' }, HOST_ORIGIN);
   ```

**Order matters.** Announce availability before the listener exists and the
toggle appears but does nothing (see `architecture.md`).

## Persistence — the EDITMODE block

Place exactly one valid-JSON object between sentinel comments, inside an inline
`<script>` so the host treats it as source, not content:

```js
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "primaryColor": "#D97757",
  "fontSize": 16,
  "darkMode": false
}/*EDITMODE-END*/;
```

Constraints: valid JSON only (double-quoted keys/strings, no trailing commas);
**exactly one** block in the canonical HTML file; inside an inline `<script>`.

## Pushing changes

On a tweak change, post a partial edit; the host reads the canonical file,
parses the EDITMODE JSON, merges the included keys, and writes it back:

```js
window.parent.postMessage({
  type: '__edit_mode_set_keys',
  edits: { fontSize: 18, primaryColor: '#2A6FDB' }
}, HOST_ORIGIN);
```

Partial updates are fine — only included keys merge.

## The read path

On reload the artifact reads merged defaults from its own source:

```js
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{ ... }/*EDITMODE-END*/;
const [tweaks, setTweaks] = useState(TWEAK_DEFAULTS);
// or a useTweaks(TWEAK_DEFAULTS) hook whose setter posts __edit_mode_set_keys
```

The hook is client-side state; persistence happens via the postMessage inside
the setter. Reload reads new defaults from disk; the round trip is complete.

## From-scratch skeleton

```html
<script>
// Pin HOST_ORIGIN to the editor's origin (see architecture.md -> Origin security).
// '*' / no origin check is only safe for a purely local file:// preview.
const HOST_ORIGIN = "https://your-host.example";

window.addEventListener('message', (e) => {
  if (e.origin !== HOST_ORIGIN) return;            // drop messages from untrusted origins
  if (e.data?.type === '__activate_edit_mode')   showPanel();
  if (e.data?.type === '__deactivate_edit_mode') hidePanel();
});
window.parent.postMessage({ type: '__edit_mode_available' }, HOST_ORIGIN);

function setTweak(key, value) {
  // ...apply to local state...
  window.parent.postMessage({ type: '__edit_mode_set_keys', edits: { [key]: value } }, HOST_ORIGIN);
}
</script>
```

If the host ships a reusable `TweaksPanel` + `useTweaks` helper, prefer it.

## Failure modes

| Symptom | Likely cause |
|---|---|
| Toolbar toggle never appears | Listener registered *after* the available message, or message blocked by sandbox |
| Toggle appears but does nothing | Listener throws on the activate message |
| Changes don't persist across reload | EDITMODE block missing, malformed JSON, or not inside an inline `<script>` |
| Persisted state contains `[object …]` | `setTweak(state)` called with the whole object instead of key + value |

## What to expose, what to hide

Expose: variation axes under active exploration; curated palette swatches (3–5,
not a free color picker); a handful of layout/density/copy switches;
step-jumping in multi-step flows. Hide: every CSS variable, free-form
spacing/margin sliders, animation-timing knobs. Twelve well-named controls beat
sixty raw ones.
