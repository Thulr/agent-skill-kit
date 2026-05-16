# Test Quality Score Rubric (0–10)

A composite score for a test (or test suite) based on four dimensions, each rated 0–2.5:

| Dimension | What it measures | 0 | 2.5 |
|---|---|---|---|
| **Clarity** | Can a cold reader describe intent in 10 seconds? | Indecipherable; cryptic name; scrambled AAA | Name describes behavior; setup/act/assert visually separated; magic values named |
| **Coverage** | Does it catch the bugs that ship in this code class? | Happy path only; no boundaries, no error paths | Bug-shape thinking applied; boundaries and likely failure modes covered |
| **Cost** | Runtime, infrastructure, maintenance burden vs signal | Slow, flaky, requires manual cleanup | Fast, deterministic, self-cleaning |
| **Robustness** | Survives legitimate SUT refactors | Couples to internals; asserts on call counts/order | Asserts behavior at a stable boundary; refactor-safe |

Sum to 10. Round to integer.

## Bands

- **9–10**: exemplar; use as a teaching example
- **7–8**: solid; ship as-is
- **5–6**: viable but improvable; cite top finding
- **3–4**: rework needed; multiple sev ≥ 2 findings
- **0–2**: rewrite or delete; usually a sev-4 false-pass present

## Anti-pattern: averaging

Do **not** report a suite-level average score. Average scores hide the dangerous tail. Report the distribution and call out the bottom-decile tests by name.
