# Deterministic Actions Playbook

## Scope

How an AI agent **acts through** a product surface reliably and safely. An agent
perceives the surface (covered in machine-readable-state), chooses an action, and
acts — often on a human's behalf and often inside a stochastic computer-use loop
where any single action may misfire, repeat, or land twice. This playbook covers
how the surface lets the agent target controls deterministically, discover what is
actionable, and confirm what happened, so a repeated or mis-fired action stays
safe. The interaction is the unit of design here, not the page.

- In: stable semantic handles for controls (role + accessible name, stable test
  ids, documented actions); discoverable and named actions; idempotency and
  retry-safety so a re-submit does not double-charge or double-post; the surface
  exposing whether an action already happened; explicit, observable action
  outcomes.
- Out: how state is *perceived* before acting (use machine-readable-state); human
  confirmation of irreversible/authority-crossing actions and on-behalf consent
  (use approval-and-agency); cases where the deterministic-handle need conflicts
  with a human-facing design choice (use audience-conflicts); the SDK/tool-schema
  or token-exchange mechanism behind the surface (use the `agent-dx` SKILL); docs
  the agent reads (use the `agent-docs` SKILL); human-only end-user interaction
  (use the `ux-audit` / `ui-design` SKILLs); operating the agent loop itself (use
  the `agent-ops` SKILL).
- Intents this surface answers: **do** (act reliably right now), **review** (audit
  a surface for action determinism and retry-safety), **design** (shape controls
  and outcomes so any agent can act safely).

## Grounding

- An agent targets controls the way assistive tech and test automation do — by a
  control's **role and accessible name** (ARIA / accessibility tree), a **stable
  test id**, or a **documented action** — never by pixel coordinates, fixed
  offsets, or brittle absolute XPath that breaks on any layout change.
- Computer-use is **stochastic**: the same prompt can produce a different action,
  a retried action, or a double-click. Determinism is a property the *surface*
  must provide; the agent cannot guarantee exactly-once on its own.
- An action is only complete when its result is **observable in state** (HTTP
  status, updated record, role/`aria` change, returned id) — not when a transient
  toast flashed or a spinner stopped.
- Safe retry is a server-and-surface contract: idempotency keys, guarded
  resubmission, and a queryable "did this already happen?" signal, mirroring
  idempotent HTTP verbs and payment-grade idempotency-key practice.

## Good signals

- Every load-bearing control has a stable handle: a programmatic role plus a human
  meaningful accessible name, a documented test id, or a named documented action.
- Action names are verbs that state the outcome ("Submit order", "Delete draft"),
  and the full set of currently-available actions is enumerable from structure.
- Re-issuing the same action with the same inputs is a no-op or returns the prior
  result — it does not create a second charge, post, or record.
- The surface answers "did this already happen?" — an idempotency key, a stable
  resource id, or a queryable status — before the agent retries.
- Outcomes are reported as durable, machine-readable state: a status field, an
  updated record, a returned id, or a role/state change in the tree.
- Handles survive a layout, theme, copy, or A/B change; nothing load-bearing is
  addressed only by coordinates or DOM position.
- Disabled, pending, and in-flight states are exposed (`aria-disabled`,
  `aria-busy`, status text) so the agent knows when *not* to act.

## Common failures

- Coordinate / pixel targeting — the agent clicks an (x, y) or a screenshot
  region; a one-row layout shift fires the wrong control or nothing.
- Brittle locator — deep absolute XPath or nth-child selectors that break on any
  re-render, with no role or test-id fallback.
- Anonymous control — an icon-only or unlabeled button with no accessible name, so
  there is no stable, meaningful handle to target.
- Double-charge on retry — a non-idempotent submit that a stochastic re-fire turns
  into two payments, two posts, or two records.
- Toast-only outcome — success lives only in a transient toast or color change; on
  the retry the agent cannot tell the first attempt already succeeded.
- Hidden in-flight state — no pending/disabled signal, so the agent re-clicks a
  still-processing action.
- Undiscoverable action — the only way to invoke something is a human gesture
  (hover-reveal, long-press, drag) with no named, structural equivalent.
- Order-coupled actions — steps that silently require an exact sequence with no
  state to confirm a prior step landed, so a re-fired step corrupts the flow.

## Heuristics

- **(do, design) Target by semantic handle.** Address controls by role +
  accessible name, a stable test id, or a documented action — never by
  coordinates, pixel offsets, or position-dependent XPath.
- **(design) Name the action for its outcome.** Give every actionable control a
  verb-outcome accessible name; keep the available-action set enumerable from
  structure so the agent discovers what it may do without guessing.
- **(do, review) Check "already happened?" before retrying.** Before re-issuing a
  stochastic action, query the idempotency key, resource id, or status; only act
  if state shows it did not land.
- **(design) Make resubmission a no-op.** Guard mutating actions with idempotency
  keys or server-side dedupe so a repeated or mis-fired action does not
  double-charge, double-post, or double-create.
- **(review, design) Observe the outcome in state.** Require a durable,
  machine-readable result — status field, returned id, updated record, or
  role/state change — not a transient toast, spinner, or color as the sole signal.
- **(design, do) Expose in-flight and disabled states.** Surface pending, busy,
  and disabled status (`aria-busy`, `aria-disabled`, status text) so the agent
  knows when an action is unavailable or still running.
- **(review) Stress the surface against re-renders.** Confirm load-bearing handles
  and outcomes survive layout, theme, copy, and A/B variation — anything addressed
  only by coordinate or DOM position is a finding.
- **(do, review) Prefer the smallest safe action that completes the task.** Choose
  the most direct named action over a multi-step gesture chain; fewer mutating
  steps means fewer stochastic retry hazards.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Can every load-bearing control be targeted by role + name, test id, or documented action? | Add a stable semantic handle; stop relying on coordinates/XPath | AGENT-UX-ACT-001 |
| Is the set of currently-available actions discoverable and verb-named from structure? | Name each action for its outcome and expose it in the tree | AGENT-UX-ACT-002 |
| Is re-issuing the same mutating action safe (idempotent or guarded)? | Add an idempotency key or server-side dedupe | AGENT-UX-ACT-003 |
| Can the agent ask "did this already happen?" before retrying? | Expose an idempotency key, resource id, or queryable status | AGENT-UX-ACT-004 |
| Is the action outcome observable in durable state, not just a toast? | Return a status/id/record or change a role/state in the tree | AGENT-UX-ACT-005 |
| Are pending / disabled / in-flight states exposed? | Add `aria-busy` / `aria-disabled` / status text | AGENT-UX-ACT-006 |

## Cross-references

- machine-readable-state — the agent must *perceive* the control and its current
  state before it can target an action here.
- approval-and-agency — irreversible, destructive, or authority-crossing actions
  (payments, deletions, permission grants, external sends) route to human
  confirmation in the action path.
- audience-conflicts — when a stable-handle or observable-outcome need collides
  with a human-facing visual/conversational choice on the same surface.
- `agent-dx` SKILL — the SDK / tool-schema and token-exchange *mechanism* behind
  the surface the agent acts through.
- `agent-ops` SKILL — operating and retrying the agent loop in production.
- finding IDs AGENT-UX-ACT-NNN
- references/intents/{do,review,design}.csv row deterministic-actions
