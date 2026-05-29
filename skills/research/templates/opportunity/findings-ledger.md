# opportunity-research findings ledger — <opportunity-slug> — <YYYY-MM-DD>

Workflow-state at: `<path to workflow-state.json>`

## Opportunity

- Statement: <one-line>
- Stage: <pre-idea / idea / validation / build / launch / scale>
- Lead: <name>
- Areas in scope: <list>

## Decision gate

- Status: <pending / Go / Conditional-Go / No-Go / Pivot / Defer>
- Last review: <date>
- Review trigger: <event>
- Kill criteria (active): <list>

## Findings

Each finding gets a stable ID `OR-<area>-NNN`. Re-discovered findings
update existing IDs; do not allocate new ones.

| ID | Area | Severity | Confidence | F/A/D/R | Claim (one line) | Evidence / artifact | Mitigation / next test | Owner | Status | Last review |
|---|---|---|---|---|---|---|---|---|---|---|
| OR-market-001 | market | 2 | H | Fact | <…> | <link> | <…> | <…> | resolved | <date> |
| OR-customer-001 | customer | 3 | M | Assumption | <…> | <link> | <test> | <…> | in-progress | <date> |
| OR-risk-001 | risk | 4 | M | Risk | <…> | <link> | <kill criterion> | <…> | kill-criterion | <date> |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Top-3 facts (cross-area)

- <fact, area, source>
- <fact, area, source>
- <fact, area, source>

## Top-3 assumptions (ranked by leverage)

- <A-1: assumption, leverage, test, deadline, owner>
- <A-2: …>
- <A-3: …>

## Top-3 risks (severity × likelihood)

- <R-1: severity 4, kill criterion candidate, mitigation, owner>
- <R-2: severity 3, mitigation, owner>
- <R-3: severity 3, mitigation, owner>

## Open contradictions (preserved, not averaged)

- <claim, area-A view, area-B view, resolving test>

## Cross-area coupling (severity upgrades)

- <coupled risks, independent severities, coupled severity, reason>

## Next tests

- <test 1, owner, deadline, success threshold>
- <test 2, owner, deadline, success threshold>
- <test 3, owner, deadline, success threshold>

## Activity log

| Date | Action | By | Notes |
|---|---|---|---|
| <YYYY-MM-DD> | <e.g., investigation: market> | <name> | <link to artifact> |
| <…> | <…> | <…> | <…> |

## Closeout summary (only when status moves to Go / No-Go / Pivot)

- Decision: <…>
- Top-3 facts that drove the call: <…>
- Assumptions tested + outcomes: <…>
- Kill criteria active: <…>
- Review trigger: <…>
- Closed by: <name>, <date>
