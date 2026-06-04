# End-to-End / UI Test Playbook

## Scope

Tests that drive the system through its real UI (or a top-level API surface) end to end, exercising the full stack. Slow, expensive, and the source of most flakiness. Routes to `integration.md` when the real cross-boundary behavior can be tested below the UI. Routes to `contract.md` for service-to-service verification that doesn't need the UI.

## Grounding

- **Lisa Crispin & Janet Gregory — *Agile Testing: A Practical Guide for Testers and Agile Teams*** — the agile testing quadrants and the framing of UI tests as the apex of the pyramid: high-value, expensive, and over-relied-upon when the layers below are weak.
- **Ham Vocke — "The Practical Test Pyramid"** — concrete framing for why UI tests should be few and well-chosen, and the "ice-cream cone" anti-pattern when teams invert the pyramid.
- **Page Object Model and Screenplay Pattern** (Selenium / Cypress / Playwright community) — abstracting the UI behind a stable API so tests assert on intent rather than DOM structure.

## Good signals

- A small number (often <50) of e2e tests covering the canonical user journeys (login, search, primary purchase / submit / checkout flow).
- Selectors keyed on semantic role + accessible name, not on CSS class or DOM structure.
- Waits are explicit and tied to app state (network idle, element visible, attribute set), never `sleep(N)`.
- Hermetic from external services: third-party network calls are recorded/replayed or stubbed at the network boundary.
- When a test fails, the artifacts (screenshot, DOM snapshot, console log, network log, video) are captured automatically and attached to the CI run.
- Flakes go to a quarantine bucket with a deadline (e.g., 7 days), not silently retried forever.
- Test assertions are not retried — only infrastructure (page-load, element-render) is.

## Common failures

- Fifty e2e tests that exhaustively cover combinations the unit suite already tests — slow, brittle, no extra signal.
- Selectors keyed on `.btn-primary > span` or `xpath=//div[3]/...` — the test breaks on every UI restyling.
- `sleep(5)` between actions to "let the page settle" — flakes when the network is slow or fast.
- Tests that hit the real third-party API in CI — vendor outage takes the build red.
- Test assertions wrapped in retries (`retryUntilTrue(() => assert(...))`) — passes once it eventually becomes true, masks real bugs.
- Failure produces a stack trace and nothing else — no screenshot, no DOM, no network log; the on-call has nothing to work with.
- A flaky test runs forever on auto-retry-3-times until it passes — quarantine never happens, signal stays eroded.

## Heuristics

- **Minimum journey, not full clickthrough** *(audit, author, strategize)* *(cost, brittleness)* — pick the few flows that prove end-to-end (login → search → checkout). E2E is not the place to exhaustively test combinations; that's what the unit and integration layers are for.
- **Semantic selectors** *(audit, author)* *(brittleness)* — query by accessibility role + accessible name (`getByRole('button', { name: 'Submit' })`), not by CSS class, ID, or DOM structure. Semantic selectors survive UI restyling and improve accessibility as a side effect.
- **Wait for state, not for time** *(audit)* *(flakiness)* — explicit waits on signals (network idle, element visible, attribute set). Never `sleep(N)`. The wait library should expose intention-revealing primitives, not generic timers.
- **Hermetic from external services** *(audit, author)* *(flakiness, cost)* — record/replay (VCR / Polly / network mock) or test doubles at the network boundary. Don't call real third parties from CI; their availability is not your responsibility to monitor through your test suite.
- **Retry the infrastructure, never the assertion** *(audit)* *(false-pass)* — page-load may be retried; element-find may be retried; the truthiness of the assertion is never retried. An assertion that "becomes true on the third try" is a false-pass waiting to ship.
- **Failure artifacts captured by default** *(audit, author)* *(confusion)* — screenshot, DOM snapshot, console log, network log, and ideally video on every failure. Without these, the test is undebuggable in CI.
- **Quarantine before delete** *(audit, prune)* *(flakiness)* — flaky tests move to a tagged quarantine bucket with a deadline (e.g., 7 days), with an owner. After the deadline, deflake or delete. Auto-retry without quarantine is signal erosion.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is this a journey or a combination? | Cost vs signal | Move combinatorial coverage to the unit/integration layer |
| Are selectors semantic? | Brittle on every UI change | Refactor to role + accessible name |
| Are waits state-based? | Flaky on slow / fast networks | Replace `sleep` with explicit-wait primitives |
| Is the test hermetic? | Vendor outages take you down | Record/replay or stub at the network boundary |
| Are assertions retried? | False-pass risk | Retry only infrastructure, never assertion truthiness |
| Are failure artifacts captured? | Undebuggable in CI | Add screenshot + DOM + console + network capture on failure |
| Are flakes quarantined with a deadline? | Signal erodes; nothing gets fixed | Add a quarantine tag and a 7-day owner |

## Cross-references

- → `integration.md` when the cross-boundary behavior can be verified below the UI
- → `contract.md` for service-to-service contracts that don't need the UI
- → `core/failure-modes.md` — flakiness and cost dominate at this layer
- → `core/personas.md` — persona 3 (suite operator) cares most: e2e suites are the largest line item in the test budget
