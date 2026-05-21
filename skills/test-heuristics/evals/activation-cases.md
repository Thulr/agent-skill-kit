# Test Heuristics Eval Cases

These evals check activation, routing, ambiguity handling, load discipline, and
output shape for `test-heuristics`. Static structure is checked by
`evals/run-static-checks.sh`; these behavioral cases are reviewed from session
logs.

## Positive cases

### Case 1: Bare activation menu

**Prompt:** `Use test-heuristics.`

**Expected:** Loads `references/activity-router.csv`, shows the activity menu
(`triage` / `review` / `author` / `strategize` / `prune`), and waits. No file
inspection, commands, network calls, or writes.

### Case 2: Unit review

**Prompt:** `Review my unit tests for false-pass risk.`

**Expected:** Routes to `review/unit`, loads `references/layers/unit.md` plus
the row's core refs, names a target persona, scores 0-10, tags findings with
failure modes, and uses `templates/review-report.md`.

### Case 3: Flaky test triage

**Prompt:** `This e2e test keeps flaking in CI, help me triage it.`

**Expected:** Routes to `triage/e2e-ui`, ranks hypotheses before fixes, names
repro steps, likely failure modes, and prevention. Uses
`templates/triage-runbook.md`.

### Case 4: Test authoring

**Prompt:** `I'm about to write a property-based test for invoice totals; what
shape should it have?`

**Expected:** Routes to `author/property-based`, asks or infers purpose, names
generator/property/shrinking concerns, and uses `templates/author-design.md`.

### Case 5: Cross-layer strategy

**Prompt:** `What should I test at unit vs integration vs e2e for this payment
flow?`

**Expected:** Routes to `strategize/all`, performs a single integrative pass,
loads the cross-layer row's playbooks, and uses `templates/strategy-doc.md`.

### Case 6: Prune review with tracking

**Prompt:** `Review all test layers and save a ledger so we can track closeout.`

**Expected:** Routes to `review/all`, assigns stable `TEST-<layer>-NNN`
finding IDs, saves both
`test-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and
`test-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`, and reports
both paths without creating roadmaps or issues unless explicitly confirmed.

### Case 7: Snapshot review

**Prompt:** `Audit snapshot tests that keep changing after harmless CSS edits.`

**Expected:** Routes to `review/snapshot`, flags brittleness and false-pass
risk, names update discipline, and includes verification.

### Case 8: Contract test review

**Prompt:** `Improve my contract tests so provider changes stop surprising
consumers.`

**Expected:** Routes to `review/contract`, looks for versioned/brokered
contracts, provider verification, consumer relevance, and CI evidence.

### Case 9: Performance test triage

**Prompt:** `Our performance test is noisy and fails on random CI runs.`

**Expected:** Routes to `triage/performance`, ranks environment variance,
measurement setup, thresholds, and workload stability before fixes.

### Case 10: Closeout verification

**Prompt:** `Verify whether TEST-UNIT-004 is fixed using the saved
workflow-state JSON.`

**Expected:** Routes to closeout, reads saved state first, reruns the finding's
verification rule, and updates status only when evidence passes. A merged PR or
closed issue is evidence to inspect, not proof that a finding is closed.

## Negative cases

- `Review my CLI design.` -> `dx-heuristics`, not this skill.
- `Set up jest in my repo.` -> tooling/setup; closer to `dx-heuristics`.
- `Deploy this code to staging.` -> not a test-quality task.
- `Explain how to use pytest fixtures.` -> general programming education unless
  the user asks for test-quality review.
- `Audit our checkout page for WCAG.` -> `ux-accessibility-heuristics`.

## Boundary cases

- `Fix this failing test.` -> ask whether the test is wrong or the system under
  test is wrong. If unsure, default to triage.
- `Improve my tests.` -> ask which layer and improvement target: clarity,
  coverage, cost, or robustness.
- `Review my testing.` -> ask which layer; offer `all`.
- `Write a unit test for this function.` -> plain implementation unless the
  user adds a quality intent such as robust, well-designed, or review.

## Tracking and closeout cases

- A review or prune output with 7+ findings/candidates must save both
  skill-prefixed tracking artifacts, report both paths, and not merely offer
  to create them.
- Tracking artifacts use `docs/audits/` by default and
  `audit-artifacts/test-heuristics-...` when the target is not a writable repo.
- Roadmaps, GitHub issues, and non-tracking project-file edits require explicit
  user confirmation.
- Closeout resumes from the saved workflow-state JSON/ledger; a merged PR or
  closed issue is evidence to inspect, not proof that a finding is closed.

## Load discipline

For a clear `review/unit` prompt, the skill should load
`activity-router.csv`, `activities/review.csv`, `layers/unit.md`, and the
row's core refs only. It may load the review template. It should not load every
layer playbook "for context."
