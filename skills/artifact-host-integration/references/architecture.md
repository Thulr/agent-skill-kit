# Architecture & conventions

The shared model every other contract builds on. Read this first.

## The model in one paragraph

The artifact is a regular HTML document. The host displays it in an iframe with
editing chrome around it. Communication is via `postMessage` — the artifact
posts state to the host (`window.parent.postMessage(...)`), the host posts
commands back (handled by a `window` `message` listener). Persistence (so
changes survive a reload) is the host rewriting specific marked regions of the
source file on disk. There is no server, no API, and no JS framework
prescribed — just messages and a few marker conventions.

This buys two properties, both of which you must preserve:

- **The artifact stays portable.** Strip out the host messages and it is a
  normal HTML page that opens anywhere.
- **The host stays generic.** It doesn't know what a "slide" or a "tweak" is —
  it routes messages and rewrites marked regions.

## The portability invariant

**Every protocol here is opt-in.** An artifact that never posts
`__edit_mode_available` simply doesn't get a tweaks toggle in the host chrome —
and works perfectly without one. Same for speaker notes, comment anchors,
scaling, and the rest. Pick the integrations the artifact needs; skip the rest;
never let host wiring break the strip-it-and-it's-just-HTML guarantee.

## Three conventions

1. **Messages** use a `type` field starting with `__` to signal host-protocol
   (not application-domain) traffic — e.g. `__activate_edit_mode`,
   `__edit_mode_available`, `__edit_mode_set_keys`. Application messages
   (`{ slideIndexChanged: i }`) carry no `__` prefix.
2. **Markers in source** use `/* IDENTIFIER-BEGIN */ … /* IDENTIFIER-END */`
   comment fences. The host edits only the content between them; everything
   outside stays untouched. There must be exactly one block per identifier in
   the canonical file.
3. **DOM attributes** the host inspects start with `data-` and use a short,
   stable prefix: `data-screen-label` (top-level scenes), `data-comment-anchor`
   (host-stamped pinned references). Transient runtime markers
   (`data-cc-id`, `data-dm-ref`) appear only while host UI is active — never
   author or persist them.

## Direction of each message (quick reference)

| Message | Direction | Meaning |
|---|---|---|
| `__activate_edit_mode` / `__deactivate_edit_mode` | host → artifact | show / hide the tweaks panel |
| `__edit_mode_available` | artifact → host | surface the edit toggle in chrome |
| `__edit_mode_dismissed` | artifact → host | panel self-closed; flip toggle off |
| `__edit_mode_set_keys` | artifact → host | persist `{edits}` into the EDITMODE block |
| `{ slideIndexChanged: i }` | artifact → host | active slide changed; sync notes |

## Order matters

Register the `message` listener **before** posting any `__..._available`
message. Posting availability first races the host's reply: the toggle appears,
the user clicks it, the activate message arrives at a window with no handler,
and the control silently does nothing. This ordering bug recurs across every
handshake — make the listener live first, then announce.
