# Severity Rubric

Apply this 0–4 scale to every test-quality finding.

| Severity | Label | Definition | Examples |
|---|---|---|---|
| 0 | Note | Style preference; no behavior or signal impact | Inconsistent test naming convention within a file |
| 1 | Minor | Mild friction or noise; doesn't hide bugs or break suites | Magic literal without a named constant; redundant setup |
| 2 | Moderate | Hurts diagnosability or modest cost on the suite | Test name doesn't describe the behavior; 200ms unit test |
| 3 | Serious | Brittleness, flakiness, or coverage gap likely to allow a real bug or block work | Couples to private impl; intermittent failure once a week; missing the canonical error path |
| 4 | Critical | False-pass that lets a real bug ship to prod; or a flake severe enough to gate the build | Test that passes regardless of SUT behavior; snapshot rubber-stamped on every PR; flaky test in the merge gate |

## Guidance

- Apply severity to the **finding**, not to the test as a whole.
- A 4 demands an immediate action item; a 3 demands a tracked one.
- A test with a severity-4 finding scores ≤2 on the score-rubric regardless of other strengths.
- Severities are not additive: two sev-2 findings don't make a sev-3 finding.
