# artifact-host-integration Eval Cases

Activation + behavioral cases for `artifact-host-integration` — implementing the
contract between a portable HTML artifact and its hosting/editing shell
(postMessage handshakes, on-disk persistence markers, fixed-canvas scaling,
speaker-notes sync, comment/scene anchors, direct-edit markup, bundling/export).
Visual/UI craft is `ui-design`; general API/SDK/CLI design is `dx-design`. Those
appear here as **negatives**.

## Static verification

```bash
bash skills/artifact-host-integration/evals/run-static-checks.sh
```

Verifies file presence, skill.json + trigger-evals contracts (name ==
artifact-host-integration), `status: published`, the one-layer intent-router
well-formedness (7 contracts, every `detail_files`/`templates` entry resolves,
no orphan references), SKILL.md source-author cleanliness, and the SKILL.md
word-count bound (<900).

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic artifact↔host wiring prompts; on a bare
invocation shows the intent menu and waits (no file inspection, network, or
writes); routes `intent-router.csv` → one or more of the 7 contracts → the row's
`detail_files` and `templates`; grounds in the artifact's existing markup and the
host's actual capabilities before wiring; preserves the portability invariant;
and emits an `integration-checklist.md`.

---

## Case 1 — Bare activation menu
**Prompt:** `Use artifact-host-integration.`
**Expected:** loads `intent-router.csv`; shows the contract menu; offers the mode choice; waits.
**Fail if:** inspects files, runs commands, or starts wiring.

## Case 2 — Tweak panel
**Prompt:** `Wire up the tweaks panel so the user can change the primary color live and persist it.`
**Expected:** routes `tweak-panel`; registers the `message` listener before posting `__edit_mode_available`; adds exactly one valid-JSON `/*EDITMODE-BEGIN*/…/*EDITMODE-END*/` block; posts `__edit_mode_set_keys` on change.
**Fail if:** announces availability before the listener exists, or exposes a raw CSS-variable dump.

## Case 3 — Fixed-canvas scaling
**Prompt:** `Scale this 1920x1080 deck to the viewport and let it print to PDF.`
**Expected:** routes `fixed-canvas`; stage/canvas with `transform: scale()` and `center center` origin; controls in the stage; `noscale` + `@page` for export/print.

## Case 4 — Speaker notes
**Prompt:** `Add speaker notes that follow the active slide in the host panel.`
**Expected:** routes `speaker-notes`; `<script type="application/json" id="speaker-notes">` array aligned by position; posts `{ slideIndexChanged }` on initial render and every navigation.

## Case 5 — Mentioned elements
**Prompt:** `The user commented on a button — which element in source did they mean?`
**Expected:** routes `mentioned-elements`; reads the `react:`/`dom:`/`id:` lines; edits only when they resolve unambiguously; otherwise probes the live DOM or asks.
**Fail if:** guesses-and-edits an ambiguous shared component.

## Case 6 — Direct edit
**Prompt:** `Make these headings direct-edit ready so edits persist.`
**Expected:** routes `direct-edit`; canonical static markup, flex+gap spacing; preserves the `__om-edit-overrides` block.

## Case 7 — Bundling / export
**Prompt:** `Bundle this to one standalone HTML file and export the deck to PPTX.`
**Expected:** routes `bundling-export`; inlines assets; adds `__bundler_thumbnail`; hides host chrome and resets transforms before capture; notes editable-vs-screenshot PPTX trade-off.

## Case 8 — Load discipline
**Prompt:** `Add speaker notes to this deck.` (clear `speaker-notes`)
**Expected:** loads `intent-router.csv`, then only the `speaker-notes` row's `detail_files` (+ `architecture.md`) + templates. Does NOT load the tweak-panel/bundling playbooks.

---

# Negative cases — should not trigger (or should defer)

## N1 — Visual polish
**Prompt:** `Make this dashboard look less like a generic AI template.`
**Expected:** recognizes visual craft; defers to `ui-design`.
**Fail if:** starts wiring host protocol for a look-and-feel request.

## N2 — New screen from scratch
**Prompt:** `Design a new analytics dashboard screen.`
**Expected:** defers to `ui-design` (visual production, not integration).

## N3 — Motion
**Prompt:** `Add atmospheric motion to this hero.`
**Expected:** defers to `ui-design` (`motion-scene`).

## N4 — Developer API design
**Prompt:** `Design the error envelope and pagination for our REST API.`
**Expected:** developer-facing surface; defers to `dx-design`.

## N5 — Accessibility audit
**Prompt:** `Run a WCAG 2.2 audit of our checkout — findings only.`
**Expected:** defers to `ux-audit`.

## N6 — Architecture refactor
**Prompt:** `Refactor this service into clean architecture layers.`
**Expected:** recognizes a code-architecture task; declines.

---

# Edge cases

- Bare `host integration` invocation shows modes and contracts, then waits.
- **Boundary with `ui-design`:** a request to *visually design or polish* an
  artifact is `ui-design`; a request to *wire or implement* its host contract is
  this skill. "Polish the visual design of this prototype" defers to `ui-design`.
- If the target host doesn't support a contract, skip it and document the
  portability assumption — the artifact must still work as standalone HTML.
- Never author or persist transient runtime markers (`data-cc-id`,
  `data-dm-ref`); never invent `data-comment-anchor` values the host owns.
