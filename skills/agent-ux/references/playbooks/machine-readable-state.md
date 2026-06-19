# Machine-Readable State Playbook

## Scope

How an AI agent *perceives* a product surface it acts through: the current
state, the actions available, and the result of each action, exposed as
structure an assistive-tech-style consumer can read — accessibility tree,
ARIA roles/labels/states, semantic HTML, and text — rather than pixels,
color, spatial layout, or animation. An agent reads the surface the way a
screen reader does, then chooses an action; if a load-bearing fact lives only
in a tooltip, hover, icon, color, UI ordering, or animation, the agent (and
the screen-reader user) is blind to it.

- **In:** state and status as text/roles, named and enumerable actions,
  action results observable in persisted state, the human-only-affordance
  anti-pattern, "what am I in / what can I do" answerable from structure.
- **Out:** how an agent *targets* and *retries* a control (see
  `deterministic-actions`); when an action needs human sign-off (see
  `approval-and-agency`); the human-vs-agent trade-off framing itself (see
  `audience-conflicts`); docs the agent reads, not acts through (agent-docs);
  the SDK/tool schema it calls (agent-dx).
- **Intents this surface answers:** do, review, design.

## Grounding

- An agent perceives structure, not rendering. The accessibility tree — roles,
  accessible names, states, and properties (the same surface ARIA and
  semantic HTML expose to screen readers) — is the machine-readable contract;
  a pixel buffer is not.
- WCAG principles set the operational floor: information and relationships
  conveyed through presentation should be programmatically determinable
  (1.3.1 Info and Relationships) and not rely on color or other sensory
  characteristics alone (1.4.1 Use of Color, 1.3.3 Sensory Characteristics).
  If state is encoded only visually, it is not perceivable to a non-visual
  consumer.
- Computer-use agents act on observed state and re-observe to confirm; a result
  that exists only as a transient toast or an animation is gone before the
  agent re-reads, so success must persist in queryable state.
- One source, many renderings: the same fact should drive both the human pixel
  and the machine-readable role/text, never a forked visual-only path.

## Good signals

- Every load-bearing piece of state (selected, disabled, loading, error,
  expanded, "3 of 5 saved") is exposed via a role/state/`aria-*`/text node,
  not by color, position, or icon alone.
- Available actions are present as named, enumerable elements (buttons/links
  with accessible names, or a documented action list) — discoverable without
  guessing coordinates.
- Disabled or unavailable actions say *why* in text (a label, `aria-disabled`
  plus a reason, helper text), not merely a greyed-out pixel.
- Action results land in persisted, re-readable state: a status region, an
  updated row, a value the agent can poll — confirmable on re-observation.
- Status messages use a live region (`role="status"` is a built-in polite
  live region; or apply `aria-live="polite"` to another element) so a result
  persists and is capturable, not a 2-second visual flash.
- Validation errors are tied to their input programmatically
  (`aria-describedby`, inline text) so the agent knows *which* field failed.
- The page answers "what state am I in" from one read of the tree: headings,
  landmarks, current step, and selection are all in structure.
- Dynamic content updates the tree (the DOM/accessibility node changes), not
  only a canvas repaint or CSS class the tree never sees.

## Common failures

- State carried only by color (red = error), icon (a checkmark glyph), or
  position — no role, label, or text equivalent. Invisible to agent and
  screen reader alike (the human-only-affordance anti-pattern).
- A rule or constraint that lives only in a tooltip or hover card: the agent
  never hovers, so the constraint may as well not exist.
- Success shown only as a toast that disappears; the agent re-reads and sees
  no evidence the action took, then retries or reports failure.
- Controls rendered on a `<canvas>`, a custom `<div>` with no role, or an
  image with no text alternative — present to the eye, absent from the tree.
- Disabled buttons with no reason: the agent cannot tell "not yet" from "never"
  and cannot recover.
- Loading/progress shown only as a spinner animation; the agent cannot
  distinguish "still working" from "stuck."
- Order or grouping conveying meaning ("the first one is the default") with no
  text/role marking which is which.
- A forked "accessible version" or text-only mode that drifts out of sync with
  the real UI, so the machine path lies about current state.

## Heuristics

- **(do, review, design) Put load-bearing state in the tree.** Every fact an
  actor must know — selection, disabled-ness, errors, counts, current step —
  exists as a role, state, `aria-*`, or text node. Color/icon/position may
  *reinforce* it but must never be the *only* carrier.
- **(review, design) Kill human-only affordances.** Any control or rule that
  lives solely in a tooltip, hover, icon, color, UI ordering, or animation
  with no text/role/schema equivalent is a defect: invisible to agents and
  screen-reader users. Give it a programmatic equivalent or move it inline.
- **(design, do) Make results observable in persisted state, not a toast.**
  After an action, the outcome must be re-readable on the next observation —
  an updated value, a status region, a row that now exists. Transient toasts
  may *also* fire, but cannot be the only evidence.
- **(design, review) Announce status through a live region.** Use
  `role="status"` / `aria-live` for async results and validation so the
  outcome is captured by the tree, not lost to a visual flash.
- **(do, review) Enumerate actions by name.** Available actions are present as
  named, discoverable elements (accessible name, documented action id), so an
  agent can answer "what can I do here" without inferring from layout.
- **(design, review) Say why an action is unavailable.** A disabled control
  carries its reason in text/state ("Save is disabled until email is valid"),
  distinguishing temporary from permanent so the agent can recover.
- **(design) Drive both renderings from one source.** The same state object
  feeds the human pixel and the machine-readable role/text. Avoid a forked
  agent-only surface that drifts; keep the human affordance *and* the
  structured path. (When that tension is real, route it to
  `audience-conflicts`.)
- **(do, review) Re-observe to confirm, and design for it.** Treat a write as
  unconfirmed until state reflects it; the surface must expose enough state
  for that re-read to succeed deterministically.
- **(design) Update the tree when content changes.** Dynamic updates must mutate
  accessible structure (DOM/accessibility node), not only repaint a canvas or
  toggle a CSS class the tree never surfaces.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is every load-bearing state in a role/state/text node? | State is visual-only; the agent is blind to it | Add a programmatic carrier; AGENT-UX-STATE-001 |
| Can you list available actions from the tree alone? | Actions are inferred from layout/pixels | Give each a role + accessible name; AGENT-UX-STATE-002 |
| Does any rule/control live only in hover/tooltip/icon/color? | Human-only affordance — invisible to agents | Provide a text/role equivalent inline; AGENT-UX-STATE-003 |
| Is an action's result re-readable after it happens? | Result was a transient toast only | Persist outcome in queryable state; AGENT-UX-STATE-004 |
| Do disabled controls state why? | Agent can't tell "not yet" from "never" | Add a reason in text/state; AGENT-UX-STATE-005 |
| Are async status/errors in a live region? | Result lost to a visual flash | Use `role="status"`/`aria-live`; AGENT-UX-STATE-006 |

## Cross-references

- `deterministic-actions` — how the agent *targets and retries* the named
  controls this surface exposes.
- `approval-and-agency` — when an observable action requires human confirmation
  before it runs.
- `audience-conflicts` — resolving a visual-human vs structured-agent tension
  on the same surface.
- → `ux-audit` for the human-only accessibility pass (WCAG/screen reader);
  → `agent-docs` for what the agent *reads*; → `agent-dx` for the tool/SDK
  schema it *calls*.
- Finding IDs `AGENT-UX-STATE-NNN`.
- `references/intents/{do,review,design}.csv` row `machine-readable-state` — the entry points.
