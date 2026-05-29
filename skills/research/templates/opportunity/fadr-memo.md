# F/A/D/R Memo — <opportunity-slug>

> Output of the `decide` intent. The forward-committed decision with
> kill criteria, review trigger, and the top-3 assumptions converted
> into next tests with owners + deadlines. **One memo per decision
> point;** if the opportunity is revisited later, a new memo links
> back to this one in the workflow-state.

## Opportunity statement

<one-line statement>

## Decision

**<GO | CONDITIONAL-GO | NO-GO | PIVOT | DEFER>**

> Conditional-Go is used when the call is yes IF the named L-confidence
> assumptions promote to M / H via the next tests. Defer is used when
> the evidence-by-date is named.

## One-paragraph summary

<3–5 sentences linking the top-3 facts / assumptions / risks to the
decision. Must name what is being decided, what is being ruled out,
and what would reverse it.>

## What this decision rules out

- <alternative considered and rejected, with the F/A/D/R citation
  that ruled it out>
- …

## Go-conditions evaluated (from `core/decision-gates.md`)

| Condition | Pass / Fail | Evidence (F/A/D/R) |
|---|---|---|
| Market quality ≥ Medium | <pass/fail> | <citation> |
| Customer pain high + revealed | <pass/fail> | <citation> |
| Differentiation survives do-nothing | <pass/fail> | <citation> |
| LTV/CAC > 3 + payback < 18mo (base) | <pass/fail> | <citation> |
| No unresolved severity-4 risk | <pass/fail> | <citation> |

## No-Go triggers checked

| Trigger | Fire / No-fire | Evidence |
|---|---|---|
| Unmitigated severity-4 risk | <fire/no> | <citation> |
| Market fails five-forces | <fire/no> | <citation> |
| Customer pain stated-only, no test | <fire/no> | <citation> |
| Unit economics need unbounded improvement | <fire/no> | <citation> |
| Legal / regulatory makes mechanic illegal | <fire/no> | <citation> |

## Facts (top-3 cross-area)

- **F-1** (H, from <area>): <fact>
- **F-2** (H, from <area>): <fact>
- **F-3** (M, from <area>): <fact>

## Assumptions (top-3, ranked by leverage)

Each has a falsifiable test, success threshold, owner, deadline.

| ID | Assumption | Leverage | Test | Threshold | Owner | Deadline | Current confidence |
|---|---|---|---|---|---|---|---|
| A-1 | <…> | high | <…> | <…> | <…> | <…> | <L/M/H> |
| A-2 | <…> | high | <…> | <…> | <…> | <…> | <L/M/H> |
| A-3 | <…> | med | <…> | <…> | <…> | <…> | <L/M/H> |

## Decisions (forward commitments)

Each is a change the research forces — not a vibe.

- **D-1:** <decision: e.g., target enterprise beachhead, not SMB>.
  Reason: <…>. Rules out: <…>.
- **D-2:** <decision>. Reason: <…>. Rules out: <…>.
- **D-3:** <decision>. Reason: <…>. Rules out: <…>.

## Risks (top-3) + kill criteria

| ID | Risk | Category | Severity | Likelihood | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| R-1 | <…> | <…> | 4 | <L/M/H> | <…> | <…> | <kill-criterion/mitigated/open> |
| R-2 | <…> | <…> | 3 | <L/M/H> | <…> | <…> | <…> |
| R-3 | <…> | <…> | <0–4> | <L/M/H> | <…> | <…> | <…> |

### Kill criteria (forward-committed)

Observable, time-bounded, asymmetric, pre-committed. **At least one
witness named per criterion.**

- **KC-1:** If <observable> by <date>, we stop. Witness: <name>.
  Reason: <which severity-4 risk this maps to>.
- **KC-2:** If <observable> by <date>, we stop. Witness: <name>.
- **KC-3:** If <observable> by <date>, we stop. Witness: <name>.

### Review trigger

What observable event would reopen this decision (regardless of kill
criteria):

- <event: new entrant / regulatory change / failed assumption-test /
  new revealed evidence>

## Next tests (operational bridge)

The three highest-leverage assumptions above become operational tests
this week / month.

- **Test A-1:** <description>. Owner: <…>. Deadline: <date>. Success
  threshold: <…>. Failure consequence: <kill / pivot / re-investigate>.
- **Test A-2:** <…>
- **Test A-3:** <…>

## Source documents

- `<path to cross-area brief>` — synthesizer output
- `<path to area artifacts>` — investigation outputs
- `<path to scope plan>` — scope decision

## Disclaimers

This memo summarizes opportunity research; it is **not** legal advice,
**not** audited financial figures, and **not** investment advice.
Legal and financial commitments require professional review.

## Signed off by

- <name, role, date>
- <name (witness on kill criteria), date>
