# test-critique Eval Cases

Activation + behavioral cases for `test-critique` — critiquing an existing test
suite (review / triage). Authoring, strategizing, or pruning tests is
`test-design`; cases that route to design appear here as **negatives**.

## Static verification

```bash
bash skills/test-critique/evals/run-static-checks.sh
```

Verifies file presence, skill.json shape, SKILL.md source-author cleanliness,
CSV registry integrity, layer-reference structure/word-count, and intent-router
shape (exactly review / triage).

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic test-critique prompts; asks at most one blocker
question when scope is missing; does not inspect files/networks or write from a
vague invocation; routes `intent-router.csv` → `intents/<intent>.csv` → one
layer reference; names a target persona; emits the intent's template shape.

---

## Case 1 — Bare activation menu
**Prompt:** `Use test-critique.`
**Expected:** loads `intent-router.csv`; shows the review / triage menu; waits.
**Fail if:** inspects files, runs commands, or invents a review.

## Case 2 — Concrete unit review
**Prompt:** a unit test file + "review these tests for quality."
**Expected:** routes (review, unit); loads `layers/unit.md` + core_refs; names target persona; scores 0–10; findings table with severity 0–4, fix, verification; `review-report.md` shape.
**Fail if:** loads multiple layer references; rewrites tests without severity; omits verification.

## Case 3 — Tracked review artifacts
**Prompt:** `Review our whole unit suite and save the findings so we can close them out later.`
**Expected:** routes (review, unit); stable `TEST-<layer>-NNN` IDs; creates both `docs/audits/test-critique-findings-ledger-…md` and `…workflow-state-…json` (or the `audit-artifacts/test-critique-…` fallback); reports both paths.
**Fail if:** only offers to track, or emits the ledger inline without saving.

## Case 4 — Closeout from saved state
**Prompt:** `Verify whether TEST-unit-002 is fixed in this PR using docs/audits/test-critique-workflow-state-2026-05-20-unit.json.`
**Expected:** loads `trackable-findings.md` then the saved state; reruns that finding's verification rule; updates status only if it passes.
**Fail if:** marks it closed because the PR merged; ignores saved state; invents a new ledger.

## Case 5 — Flaky-test triage
**Prompt:** `These integration tests pass locally but fail 1 in 5 runs in CI. Triage before we bump retries.`
**Expected:** routes (triage, integration); loads `layers/integration.md`; reproducer + ranked hypotheses before naming a fix; `triage-runbook.md` shape with prevention.
**Fail if:** patches by adding retries without ranking causes; omits verification.

## Case 6 — Ambiguous private-system request
**Prompt:** `Take a look at our tests and tell me what to fix.`
**Expected:** asks one blocker question (which intent / which layer); does not inspect first.

## Case 7 — False-pass smell
**Prompt:** `This test passes even when I comment out the function it's supposed to test.`
**Expected:** recognizes a false-pass triage; ranks hypotheses (asserts nothing meaningful, wrong SUT, over-mocked); `triage-runbook.md` shape.
**Fail if:** declares the test fine because it's green.

## Case 8 — Load discipline
**Prompt:** a snapshot test snippet + "review this."
**Expected:** loads only `intent-router.csv`, `intents/review.csv`, `layers/snapshot.md`, the row's core_refs. Does NOT load other layer references.

---

# Negative cases — should not trigger (or should defer)

## N1 — Author new tests
**Prompt:** `Write the tests for our new payment-flow feature — which layers and what oracle?`
**Expected:** recognizes this is **authoring**, not critique; defers to `test-design`.
**Fail if:** produces severity findings for tests that do not exist yet.

## N2 — Prune the suite
**Prompt:** `Our e2e suite takes 45 minutes — which tests should we delete?`
**Expected:** recognizes a **prune** ask; defers to `test-design`.

## N3 — Strategize the portfolio
**Prompt:** `Quarterly test-pyramid review — where do we invest next quarter?`
**Expected:** recognizes a **strategize** ask; defers to `test-design`.

## N4 — Production performance debugging
**Prompt:** `Our reporting query is slow in production at 2pm. Trace what's causing it.`
**Expected:** recognizes operational/runtime perf, not test-suite quality; defers (perf-critique).

## N5 — DX surface review
**Prompt:** `Our CLI --help is dense — review the help layout for developer experience.`
**Expected:** recognizes a DX surface, not a test suite; defers (dx-critique).

## N6 — Concept explanation
**Prompt:** `Explain how property-based testing and shrinking work for a one-pager.`
**Expected:** recognizes educational content; defers.

## N7 — Internal code refactor
**Prompt:** `Refactor this function to use early returns instead of nested ifs.`
**Expected:** recognizes internal refactoring, not test critique; declines.
