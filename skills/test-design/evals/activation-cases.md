# test-design Eval Cases

Activation + behavioral cases for `test-design` — producing test-suite artifacts
(author / strategize / prune). Reviewing or triaging *existing* tests is
`test-audit`; those appear here as **negatives**.

## Static verification

```bash
bash skills/test-design/evals/run-static-checks.sh
```

Verifies file presence, skill.json shape, SKILL.md source-author cleanliness,
the template shapes, CSV registry integrity, layer-reference structure/word-count,
and that the intent-router is author / strategize / prune only.

## Behavioral protocol

Run each case in a fresh session with only this skill loaded. Passing means the
agent: activates for realistic design prompts; asks at most one blocker question
when intent or layer is missing; does not inspect files/networks or write from a
vague invocation; routes `intent-router.csv` → `intents/<intent>.csv` → one layer
reference; names a target persona; emits the intent's template shape with a
concrete good-shaped artifact.

---

## Case 1 — Bare activation menu
**Prompt:** `Use test-design.`
**Expected:** loads `intent-router.csv` + `starter-scenarios.csv`; shows the author / strategize / prune menu; waits.
**Fail if:** inspects files, runs commands, or invents a design.

## Case 2 — Author a unit test
**Prompt:** `Help me author a unit test for this discount-calculation function.`
**Expected:** routes (author, unit); loads `layers/unit.md`; `author-design.md` shape — behavior, AAA test outline, heuristics applied, failure modes prevented, verification.
**Fail if:** uses a review template / severity findings for an authoring task; omits the test outline.

## Case 3 — Cross-layer strategy
**Prompt:** `Where should we invest next quarter across unit/integration/e2e? Shape the suite as a portfolio.`
**Expected:** routes (strategize, all); names the suite-operator persona; `strategy-doc.md` shape — purpose-by-purpose coverage and layer investments with rationale; cites pyramid/trophy grounding.
**Fail if:** reviews individual tests instead of recommending investments.

## Case 4 — Prune plan
**Prompt:** `Our e2e suite takes 45 minutes — which tests do we delete and which do we keep?`
**Expected:** routes (prune, e2e-ui); loads `layers/e2e-ui.md`; `prune-plan.md` shape — deletion and quarantine candidates with a reason and the failure mode of keeping each.
**Fail if:** issues blanket cuts without rationale; treats it as a review with severity findings.

## Case 5 — Intent ambiguity
**Prompt:** `Help me with our tests.`
**Expected:** recognizes a design ask but asks for the intent/layer; offers the `intent-router.csv` menu; does not inspect first.

## Case 6 — Load discipline
**Prompt:** `Design a property-based test for our serializer round-trip.` (clear (author, property-based))
**Expected:** loads `intent-router.csv`, `intents/author.csv`, `layers/property-based.md`, the row's core_refs. Does NOT load other layer references.

---

# Negative cases — should not trigger (or should defer)

## N1 — Review an existing suite
**Prompt:** `We inherited ~5000 unit tests and nobody trusts them — review the suite and tell me which actually catch bugs.`
**Expected:** recognizes this is **critique** of an existing suite; defers to `test-audit`.
**Fail if:** produces an authoring outline for a suite that already exists.

## N2 — Triage a failing/flaky test
**Prompt:** `These integration tests fail 1 in 5 runs in CI — what's wrong?`
**Expected:** defers to `test-audit` (triage).

## N3 — DX surface design
**Prompt:** `Design how our CLI reads config — file vs env vs flag precedence.`
**Expected:** recognizes a DX surface, not a test suite; defers (dx-design).

## N4 — Production performance work
**Prompt:** `Our reporting query is slow at 2pm — design a fix.`
**Expected:** recognizes operational/runtime perf, not test design; defers (perf-design).

## N5 — End-user UI design
**Prompt:** `Design a lower-friction consumer signup flow.`
**Expected:** recognizes end-user audience; defers (ui-design / ux-audit).

## N6 — Internal refactor
**Prompt:** `Refactor this function to use early returns.`
**Expected:** recognizes internal refactoring, not test design; declines.
