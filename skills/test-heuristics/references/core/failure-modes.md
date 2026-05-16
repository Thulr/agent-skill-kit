# Test Failure Modes

The six modes by which a test can fail to do its job. Every layer playbook tags its heuristics with the mode(s) the heuristic prevents; the static check verifies that the union of all playbooks covers all six modes.

These are *test* failure modes, not *bug* failure modes — the failure of the test itself to be useful.

## 1. false-pass

The test passes regardless of whether the bug is present.

Symptoms:
- Tautological assertion (`assert(value == value)`, `assert(mock.called_with(arg) == arg)`)
- Over-mocked: every collaborator stubbed; nothing real exercised
- Asserts on side-channel state (logs, call counts) when the real behavior is the return value
- Snapshot rubber-stamped without diff review
- Mutation testing leaves many surviving mutants

Why it's the worst mode: a false-pass test gives confidence without providing evidence. Sev-4 by default.

## 2. brittleness

The test fails on a *legitimate* refactor of the SUT — one that didn't change observable behavior.

Symptoms:
- Asserts on internal method names, call order, or call counts when those aren't the contract
- Mocks at the wrong seam (mocks concrete dependency instead of abstraction)
- Tests private methods directly
- E2E selectors keyed on CSS class names or DOM structure rather than semantic role/text

Cost: discourages refactoring. Tests become a liability.

## 3. flakiness

The test passes and fails non-deterministically on the same code.

Symptoms:
- Time-dependent (`sleep`, real `Date.now()`, timezone-sensitive without freezing)
- Order-dependent (shared mutable state across tests)
- Resource-dependent (race on a port, file, or DB row)
- Network-dependent (calls a real external service)
- Concurrency without explicit synchronization

Cost: erodes signal. Once a suite is flaky, real failures get retried away.

## 4. gap

The bug shape exists, but no test catches it.

Symptoms:
- Happy-path bias — only successful inputs tested
- No boundary cases (empty, single, max, off-by-one)
- No error paths exercised
- No failure injection (the dependency never throws)
- No exploration of the oracles (see oracles.md)

Cost: bugs ship. The test suite confidently approves a broken release.

## 5. cost

The test consumes more time, infra, or maintenance than its bug-catching warrants.

Symptoms:
- Slow unit test (>10ms generally; >100ms always investigated)
- E2E test that exercises the same logic 10 unit tests already cover
- Long-running snapshot maintenance churn
- Mutation testing run against the whole repo on every PR

Cost: slows the feedback loop, which is the most valuable property of a test suite.

## 6. confusion

The test's intent is illegible. When it fails, the reader cannot tell what was supposed to happen.

Symptoms:
- Test name describes structure, not behavior (`test_function_2`)
- Setup, act, and assert sections visually scrambled
- Magic literals without named constants
- Asserts that don't match the test name
- Failure messages that show only "expected X, got Y" with no semantic context

Cost: every red light becomes an investigation. The on-call (persona 2) cannot triage.

## Tag format

Heuristics in layer playbooks tag the mode(s) they prevent:

```
- **Mock at the seam, not the type** *(review, author)* *(brittleness, false-pass)*
```

## Cross-references

- `severity-rubric.md` — false-pass and gap findings tend to be sev-3+; cost and confusion typically sev-1–2
- `oracles.md` — gap findings are surfaced by oracle-driven exploration
- `personas.md` — confusion findings are best surfaced by persona 2 (on-call); brittleness by persona 5 (refactorer)
