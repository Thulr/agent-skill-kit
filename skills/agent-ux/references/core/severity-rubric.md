# Severity rubric (0–4)

Apply to every finding in a REVIEW, every risk in a DESIGN, and every step in a hardening
runbook. Agent-UX severity weighs what an agent acting through the surface does wrong — at
machine speed, often on a human's behalf — when it cannot perceive, cannot target reliably, or
acts past its authority.

| Level | Label | Meaning |
|------:|-------|---------|
| 4 | **Critical** | An irreversible/authority-crossing action (payment, deletion, permission grant, external send) fires with no in-path confirmation; a non-idempotent financial/destructive action an agent will retry double-executes. Block the action surface. |
| 3 | **High** | A load-bearing control or rule lives only in a human-only affordance (tooltip/color/icon/animation) an agent cannot perceive; controls are targetable only by coordinates/brittle XPath so actions break on layout change; an agent acts on a user's behalf with no on-behalf visibility or scoped consent. Large but tractable fix. |
| 2 | **Medium** | Action results are not observable in state (only a transient toast); a human-vs-agent trade-off is made without naming who is harmed; forked human/agent surfaces drift; a non-destructive action is not idempotent. Fix this cycle. |
| 1 | **Low** | A control with a weak accessible name, a slightly fragile selector off the core path, a missing dual-path on a non-load-bearing hint. Queue for cleanup if it accumulates. |
| 0 | **Note** | An observation worth recording, not a defect — e.g. "this surface is human-only by design; agents are routed to an API." |

## How to pick a level

1. **Action consequence.** Irreversible/authority-crossing and unguarded (4), wrong/failed action
   or unperceivable control (3), unobservable result or unnamed trade-off (2), friction (1)?
2. **On-behalf risk.** An agent acting for a user without visible, scoped, revocable consent rates
   higher — the human bears the consequence.
3. **Retry safety.** A stochastic agent will repeat or mis-fire actions; non-idempotent
   destructive/financial actions escalate toward 4.

## Calibration anchors

- "A payment/delete/permission-grant fires with no in-path confirmation" → **4**.
- "A retryable financial/destructive action is not idempotent; a retry double-executes" → **4**.
- "A load-bearing control lives only in a tooltip/color/icon an agent cannot perceive" → **3**.
- "Controls are targetable only by pixel coordinates or brittle XPath" → **3**.
- "An agent acts on a user's behalf with no on-behalf visibility or scoped consent" → **3**.
- "Action results show only as a transient toast, not in observable state" → **2**.
- "A human-vs-agent trade-off is chosen without naming who is harmed" → **2**.
- "A non-destructive action is not idempotent" → **2**.
- "Forked human/agent surfaces drift" → **2**.

## Cross-surface comparison

Scores and severities are comparable only within one REVIEW run, using the same persona and
project tier. Do not benchmark across teams or across time without recalibrating against these
anchors.
