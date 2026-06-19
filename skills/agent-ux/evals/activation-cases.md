# Activation cases — agent-ux

Natural-language behavioral cases for the **interaction surface an AI agent acts through as an end
user**. Each negative names the sibling skill it disambiguates from. The agent should activate on
realistic agent-as-user prompts, ask at most one blocker question, and route to `<intent>/<surface>`
— deferring human-only UX to `ux-audit` / `ui-design`.

## Positive

### P1 — Machine-readable state
**Prompt:** `Our computer-use agent can't tell our app's state — status is just a colored badge.`
**Expected:** activates; intent `do`, surface `machine-readable-state`; expose state via role/text,
not color/icon alone.

### P2 — Deterministic targeting
**Prompt:** `Our agent clicks the wrong control — we target by pixel coordinates. Review targeting.`
**Expected:** activates; intent `review`, surface `deterministic-actions`; stable semantic handles
over coordinates/brittle XPath.

### P3 — Approval for a destructive action
**Prompt:** `Can the agent fire "delete account" on its own, or does it need confirmation?`
**Expected:** activates; intent `design`, surface `approval-and-agency`; mechanical-vs-judgment, gate
the irreversible action in-path.

### P4 — Human-vs-agent conflict
**Prompt:** `Our UI is great for humans but the agent can't see rules buried in tooltips — resolve it.`
**Expected:** activates; intent `design`, surface `audience-conflicts`; name the trade-off + dual path.

### P5 — Idempotent action
**Prompt:** `An agent retried checkout and double-charged — make the action retry-safe.`
**Expected:** activates; intent `do`, surface `deterministic-actions`; idempotency/guarded retry.

### P6 — Full agent-UX review (fan-out)
**Prompt:** `Make our web app agent-operable — full review and score.`
**Expected:** activates; intent `review`, surface `all`; fans out with `AGENT-UX-*` finding IDs.

## Negative

### N1 — Human visual design
**Prompt:** `Redesign our marketing homepage to convert better for human visitors.`
**Expected:** does not activate; defers to `ui-design` / `ux-audit` (human-only UX).

### N2 — Human accessibility audit
**Prompt:** `Run a WCAG accessibility audit for human users with disabilities.`
**Expected:** does not activate; defers to `ux-audit` (human accessibility; agent-ux *reuses* the
accessibility tree as a machine surface but is not a human-a11y audit).

### N3 — Agent-readable docs
**Prompt:** `Curate our llms.txt and AGENTS.md so an agent can read our docs.`
**Expected:** does not activate; defers to `agent-docs` (docs an agent reads, not a surface it acts
through).

### N4 — SDK schema / token exchange
**Prompt:** `Design the typed tool schema and token-exchange for our Agent SDK.`
**Expected:** does not activate; defers to `agent-dx` (the SDK/tool mechanism; agent-ux owns the
product consent UX, not the token-exchange mechanism).

### N5 — Operating the loop
**Prompt:** `Set up a trace-and-eval loop to watch our agent's quality in production.`
**Expected:** does not activate; defers to `agent-ops`.

### N6 — Human checkout flow
**Prompt:** `Review our human checkout flow for friction and drop-off.`
**Expected:** does not activate; defers to `ux-audit`.

## Edge / boundary

### E1 — Accessibility tree already present
**Prompt:** `We expose a good accessibility tree for screen readers — does that make us agent-operable?`
**Expected:** activates; intent `review`, surface `machine-readable-state`; the a11y tree is a strong
start (perception) but agent-ux also needs deterministic actions, retry-safety, and authority gating.

### E2 — On-behalf consent: agent-ux vs agent-dx
**Prompt:** `An agent acts on a user's behalf — is the consent UX ours or the SDK's token-exchange?`
**Expected:** activates; intent `design`, surface `approval-and-agency`; agent-ux owns the product
consent/visibility UX; the token-exchange *mechanism* is `agent-dx`.
