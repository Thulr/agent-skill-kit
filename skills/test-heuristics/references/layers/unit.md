# Unit Test Playbook

## Scope

Tests of a single function, class, or module in isolation, with no I/O. Routes to `integration.md` when collaborators are real. Routes to `property-based.md` when generating inputs. Routes to `mutation.md` when assessing assertion strength.

## Grounding

- **Gerard Meszaros — *xUnit Test Patterns: Refactoring Test Code*** — the canonical smell catalog and the test-fixture / object-mother / test-data-builder vocabulary used throughout this playbook.
- **Michael Feathers — *Working Effectively with Legacy Code*** — characterization tests, seams, the test-as-pin-down technique for untestable code.
- **Kent Beck — *Test-Driven Development By Example*** — the spec-purpose framing and the red/green/refactor cadence.
- **Vladimir Khorikov — *Unit Testing: Principles, Practices, and Patterns*** — the four-quadrant test-value model: protection-against-regressions × resistance-to-refactoring × fast-feedback × maintainability.

## Good signals

- The test name is a sentence describing behavior: `withdraw_rejects_when_balance_below_amount`.
- Arrange / Act / Assert is visually separated by blank lines; or each is one short call.
- Each test has one Act and one logical Assert; multiple physical asserts only when verifying one observable outcome.
- Magic literals are named: `BALANCE_AT_LIMIT`, not `100`.
- Test runs in <10ms; no I/O, no `sleep`, no real clock.
- Tests pass when run in any order, individually or together.
- Mocks are at abstract seams (interfaces / ports), not at concrete dependencies (a specific HTTP client).

## Common failures

- Test names like `test_withdraw_2`, `test_withdraw_works` — describe nothing.
- Asserting on `mock.callCount` or `mock.callOrder` when those are not the actual contract.
- Mocking the SUT's collaborators so thoroughly that nothing real is exercised — the test passes regardless of SUT behavior.
- Long shared `setUp` that's used by 20 tests, half of which only need a fraction.
- Sleeps or real-time clocks → flaky in CI.
- Asserting on private methods directly via reflection or visibility hacks.
- Single test asserting five unrelated things — when it fails, you don't know which thing broke.

## Heuristics

- **AAA visibility** *(review, author)* *(confusion)* — Arrange / Act / Assert visually separable in the test body. Good: blank lines, comments, or one-line each. Bad: 30 lines of intermixed setup and assertions.
- **Behavior-named tests** *(review, author)* *(confusion, brittleness)* — test name describes the behavior under test, not the function name and not the test number. Renaming the SUT method should not require renaming the test.
- **One behavior per test** *(review, author)* *(confusion)* — each test exercises one logical behavior. Multiple assertions are fine when they verify facets of one outcome; multiple unrelated assertions are not.
- **Mock at the seam, not the type** *(review, author)* *(brittleness, false-pass)* — mocks belong at architectural seams (an abstraction the SUT depends on by interface), not at concrete library types. Mocking a concrete HTTP client couples the test to that library; mocking the `PaymentGateway` port doesn't.
- **No assertions on implementation** *(review)* *(brittleness, false-pass)* — do not assert on call counts, call order, or internal state unless the contract really is "X is called Y times in Z order." Asserting on side-channels turns the test into an implementation lock.
- **Magic literals named** *(review, author)* *(confusion)* — every meaningful literal gets a constant or local with an intent-bearing name.
- **Fast-by-default** *(review, prune)* *(cost)* — unit tests target <10ms. >100ms gets investigated; usually means real I/O has crept in. If genuinely needed, move to integration layer.
- **Independent** *(review)* *(flakiness)* — tests run in any order, individually or together. No shared mutable state via globals or class attributes.
- **Characterization for legacy code** *(author)* *(gap, false-pass)* — when pinning behavior of code you cannot easily change, write tests that capture *current* behavior even if it seems wrong; they protect the refactor.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does the test name describe behavior? | Reader can't tell intent | Rename to `<subject>_<expected_outcome>_<condition>` |
| Is AAA visually separable? | Cognitive load on reader | Add blank lines or extract helpers |
| Does the test exercise real SUT behavior? | False-pass risk | Reduce mocking; mock only at architectural seams |
| Does it run in <10ms? | Suite slows; flake risk grows | Strip I/O; consider moving to integration |
| Does it run in any order? | Flakiness | Remove shared mutable state |
| Could a legitimate refactor break it for the wrong reason? | Brittleness | Stop asserting on internal call counts/order |

## Cross-references

- → `integration.md` when the test exercises real collaborators
- → `property-based.md` when generating inputs is the right approach
- → `mutation.md` to assess whether the assertions actually catch bugs
- → `core/failure-modes.md` — false-pass and brittleness are the two modes most common in unit tests
- → `core/personas.md` — persona 4 (test skeptic) is the right lens for false-pass risk in unit tests
