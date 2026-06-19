# Approval and Agency Playbook

## Scope

The approval and authority surface as agent-agency design: when an AI agent acts through a product on a human's behalf, the consent, confirmation, and authority-scoping UX *is* the agency design. This playbook covers the mechanical-vs-judgment split (routine reversible actions the agent takes unprompted; irreversible, destructive, or authority-crossing actions surfaced for human confirmation in the action path), on-behalf visibility ("an agent is acting on your account"), scoped and revocable consent as product UX, and confirmation proportional to consequence.

- **In:** confirmation gates on the action path, the mechanical-vs-judgment classifier, on-behalf-of presence indicators, scoped/revocable consent UI, consequence-proportional friction, agent action audit trail visible to the human principal.
- **Out:** the SDK token-exchange or OAuth-scope *mechanism* and machine-readable scope grants (see `agent-dx`); the agent's own internal approval loop and autonomy policy (see `agent-ops`); human-only consent flows where no agent acts (see `ux-audit` / `ui-design`); how the agent *perceives* the confirmation prompt (see sibling `machine-readable-state`).
- **Intents this surface answers:** do, review, design.

## Grounding

- An agent acting on a human's behalf is an authority delegation; the product is the principal's only window into what the delegate is about to do. Borrow least-privilege and scoped-grant practice from OAuth consent screens and the object-capability model: consent is for a named action set, not blanket account control.
- Computer-use is stochastic — a model may fire an action it did not intend or repeat one after a timeout. The confirmation gate on irreversible actions is the safety backstop, the same role a "Type DELETE to confirm" destructive-action pattern plays for humans, scaled to a delegate that acts at machine speed.
- Accessibility practice (WCAG 3.3.4, Error Prevention for legal/financial/data actions) already requires reversible, checked, or confirmed submissions for high-consequence actions. The agent case generalizes it: the consequence, not the actor, sets the friction.
- Consent and on-behalf status are load-bearing facts; per the no-hidden-criticals rule they must live in text/structure and on the action path, never only in a hover, toast, color, or fine-print footer that neither the human principal nor the acting agent reliably reads.

## Good signals

- Actions are classified mechanical-vs-judgment by consequence: routine reversible ones (read, draft, sort, label) the agent completes unprompted; irreversible/destructive/authority-crossing ones (payments, deletions, permission grants, external sends) route to a human confirmation step.
- The confirmation gate sits *in the action path* and names the specific consequence and the affected object ("Send $480 to Acme — irreversible") as text, so both the human and the agent perceive it.
- When an agent is acting, the product shows it explicitly ("Assistant is acting on your account") as a persistent, machine-readable presence indicator, not a one-time transient banner.
- Consent is scoped to a named action set and is revocable from an obvious place; revoking it stops the agent mid-delegation without account-level lockout.
- Confirmation friction scales with consequence: reversible actions are frictionless, costly/irreversible ones require an explicit affirmative, and authority-crossing ones name who is being granted what.
- An agent-visible audit trail records what the agent did, when, and under whose authority, observable in state so the human principal (and an eval) can reconstruct the delegated session.

## Common failures

- A single autonomy switch (agent on / agent off) replaces per-action judgment, so the agent either over-asks on trivial actions or silently executes a payment the human never saw.
- The confirmation lives only in a toast or hover — the consequence text vanishes before the human reads it and never exists as state the agent can branch on.
- The agent's presence is invisible: the human cannot tell an action was taken by a delegate, so an erroneous external send looks like their own.
- Consent is blanket and irrevocable: granting "let the assistant help" hands over full account authority with no scoped action list and no off-ramp.
- Friction is flat — a destructive bulk-delete has the same one-click affordance as marking a message read, so the consequence is invisible until after it fires.
- A retryable action (re-submit after timeout) has no idempotency guard or "already happened" signal, so a re-fired payment double-charges; the approval UX never surfaced that the action was singular.
- The authority boundary is buried in fine print: the scope an agent is granted is described in a linked policy, not at the consent moment, so neither principal nor agent treats it as load-bearing.

## Heuristics

- **(design, review) Split by mechanical-vs-judgment, not agent-vs-human.** Classify each action by consequence: routine reversible actions the agent completes; irreversible, destructive, or authority-crossing actions (payments, deletions, permission grants, external sends) surface for human confirmation. The actor is not the axis — the reversibility and authority cost are.
- **(design, do) Put the gate on the action path, as text.** The confirmation for a high-consequence action sits inline in the flow that triggers it and names the specific consequence and affected object as text/structure — never only in a hover, toast, color, icon, or fine-print footer that the human misses and the agent cannot perceive.
- **(design, review) Scale friction to consequence.** Reversible actions stay frictionless; costly or irreversible ones require an explicit affirmative; authority-crossing ones name the grantee and scope. A flat affordance hides the consequence until it has already fired.
- **(design, do) Make on-behalf-of presence visible and persistent.** When an agent acts, the product shows "an agent is acting on your account" as a durable, machine-readable indicator, so a delegated action is never mistaken for a first-party one — by the human or by a second agent observing the surface.
- **(design, review) Scope consent and keep it revocable.** Borrow OAuth/object-capability practice: consent grants a named action set, not blanket control, and the human can revoke it from an obvious place; revocation halts the delegation without locking the whole account.
- **(design, do) Guard retry-safe so confirmation isn't bypassed by a re-fire.** Because computer-use repeats actions, a confirmed irreversible action must be idempotent or guarded and expose an "already happened" signal in state — re-submitting a confirmed payment must not double-charge.
- **(review) Audit the delegated session.** Verify the product records and shows what the agent did, when, and under whose authority, observable in state — so the principal can reconstruct the session and an eval can replay the approval path.
- **(review) Test the no-hidden-criticals rule against the consent surface.** Confirm every load-bearing fact — irreversibility, auth scope, grantee, retry-safety — exists in text/structure on the action path, not only in prose, hover, or color outside it.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are actions split mechanical-vs-judgment by consequence, not one autonomy toggle? | Agent over-asks or silently fires high-consequence actions | Classify actions; gate irreversible/authority-crossing ones |
| Does the confirmation sit in the action path as text naming the consequence? | Human misses it; agent can't perceive it | Move the gate inline; render consequence as text/structure |
| Does friction scale with consequence? | Destructive actions feel as cheap as safe ones | Add affirmative confirmation proportional to cost |
| Is on-behalf-of status visible and persistent? | Delegated actions look first-party | Add a durable, machine-readable agent-presence indicator |
| Is consent scoped to a named action set and revocable? | Blanket, irrevocable authority is granted | Scope the grant; add an obvious revoke control |
| Is a confirmed irreversible action idempotent / guarded against re-fire? | A repeated action double-charges or double-posts | Add idempotency key + an "already happened" state signal |

## Cross-references

- `machine-readable-state` — how the agent perceives the confirmation prompt, presence indicator, and "already happened" signal as state.
- `deterministic-actions` — targeting the confirm control by stable handle and the idempotency/retry-safety mechanics this surface depends on.
- `audience-conflicts` — the human-vs-agent tension when a confirmation that reassures a human adds a step the agent must navigate; one source, many renderings.
- → `agent-dx` for the SDK token-exchange / OAuth-scope *mechanism* behind scoped consent (this surface owns the product consent UX, not the wire mechanism).
- → `agent-ops` for the agent's internal approval loop and autonomy policy.
- → `ux-audit` / `ui-design` for human-only consent flows where no agent acts.
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` — REVIEW scales; finding IDs `AGENT-UX-APPR-NNN`.
- `references/intents/{do,review,design}.csv` row `approval-and-agency` — the entry points.