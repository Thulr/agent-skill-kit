# Activation Cases

Behavioral cases the skill should respond to (positive) or stay silent on (negative). Used in manual review and as seeds for `trigger-evals.json`.

## Positive — should activate

- "review my unit tests for false-pass risk" → review × unit
- "this test keeps flaking, help me triage" → triage (asks for layer)
- "I'm about to write a test for the new payment flow, what's the right shape?" → author (asks for layer)
- "audit my snapshot tests" → review × snapshot
- "we have 4000 unit tests; which can we delete?" → prune × unit
- "should I test this with property-based or example-based?" → strategize
- "where in the test pyramid does this go?" → strategize
- "my e2e suite is 80% flaky" → triage × e2e-ui (or review)
- "use test-heuristics" → bare invocation; show activity menu
- "test review on `path/to/users_test.py`" → review × unit (inferred from file)
- "review all test layers and save a ledger so we can track closeout" → review × all; creates `test-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and `test-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`

## Negative — should NOT activate (these belong to other skills)

- "set up jest in my repo" → tooling/setup; closer to dx-heuristics' `setup` playbook.
- "explain how mocking works in pytest" → general programming question; no quality review needed.
- "deploy this code to staging" → not testing.
- "review my CLI design" → dx-heuristics, not test-heuristics.

## Boundary cases — ambiguous

- "fix this failing test" → could be triage (the test is wrong) or could be a SUT bug. Ask: "is the test wrong or is the code wrong?" If unsure, default to triage flow.
- "improve my tests" → ask: which layer, and what improvement (clarity / coverage / cost)?
- "review my testing" → ask: which layer? offer `all` as an option.
- "write a unit test for this function" with no quality concern → the model can usually handle a plain implementation request alone. Activate only if the user adds a quality intent ("good", "robust", "well-designed", "review the test after").

## Lens-specific cases

- A test asserts `mock.payment_gateway.charge.call_count == 1` → refactor adversary should flag this as brittleness/false-pass.
- A test name `test_user_2` exists → intent reader should flag this as confusion.
- A unit test only has happy-path inputs → bug-shape hunter should flag this as gap.

## Artifact/state regression cases

- A review or prune output with 7+ findings/candidates must save both
  skill-prefixed tracking artifacts, report both paths, and not merely offer
  to create them.
- Tracking artifacts use `docs/audits/` by default and
  `audit-artifacts/test-heuristics-...` when the target is not a writable repo.
- Roadmaps, GitHub issues, and non-tracking project-file edits require explicit
  user confirmation.
