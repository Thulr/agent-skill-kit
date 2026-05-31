# Performance Test Playbook

## Scope

Tests that measure speed, throughput, or resource use under load — micro-benchmarks, load tests (k6/Gatling/Locust), profiling-driven regression tests. Routes to `unit.md` for functional correctness. Routes to `integration.md` when the perf test exercises real I/O. Distinct from "is it fast enough" gut-checks — performance tests are tied to SLOs.

## Grounding

- **Brendan Gregg — *Systems Performance: Enterprise and the Cloud*** — the USE method (utilization / saturation / errors), the discipline of profiling before optimizing, methodologies for diagnosing performance problems.
- **Jakob Nielsen — "Response Times: The 3 Important Limits"** — the 0.1s / 1s / 10s thresholds for user-perceived latency: instant feel, train-of-thought, attention loss. Anchors the human-perceptible thresholds in perf SLOs.
- **k6 / Gatling / Locust documentation** — practical patterns for workload modeling, ramp-up profiles, percentile reporting, distributed load generation.

## Good signals

- Every perf test has explicit thresholds, expressed as percentiles (p50, p99, p999) — not "should be fast."
- Thresholds are tied to a user-facing SLO or an SLA commitment, not pulled from thin air.
- The test runs in a stable environment with warmup and multiple runs; reports statistical significance.
- The workload represents the real production shape (mostly small payloads with a long tail), not synthetic uniform distributions.
- The metric chosen matches the failure mode that matters (latency tail for user-perceived; throughput for capacity planning; saturation for headroom).
- Failures flag the *delta from baseline*, not absolute numbers — absolute thresholds in CI are flake generators.
- When the test fails, the trace / flame graph / profile is captured automatically. The on-call doesn't have to reproduce to diagnose.

## Common failures

- Threshold-free perf test: "make sure it runs in a reasonable time" — passes everything, signals nothing.
- Thresholds set in CI based on the CI runner's variable performance — flakes constantly.
- Absolute thresholds (`< 50ms p99`) in CI on shared infra — passes on Monday, fails on Friday when the runner is busy.
- Synthetic uniform workload — measures the wrong thing; production has a heavy long tail.
- Reports only mean / average latency — the tail (where users notice) is invisible.
- Test fails with "expected <50ms, got 76ms" — no profile, no trace, no flame graph; the on-call has to reproduce locally to diagnose.
- Perf test runs on every PR with no warmup — high false-positive rate, ignored within a week.

## Heuristics

- **Explicit thresholds** *(review, author)* *(confusion)* — p50 / p99 / p999 bounds, not "should be fast." A perf test without thresholds is documentation, not a test.
- **Tied to SLO** *(strategize)* *(gap)* — perf gates enforce something a user or SLA cares about. Otherwise the test is theatre — and worse, it diverts attention from the perf problems that do matter.
- **Stable environment** *(review)* *(flakiness)* — known infra, warmup runs, multiple measurement runs, statistical significance. CI runners are the worst place for *absolute* perf tests; relative regression detection works better there.
- **Workload represents real shape** *(review, author)* *(gap)* — production-shaped distribution (mostly small payloads with a long tail), not synthetic uniform distributions. The real bugs live in the tail.
- **Captures the failure mode that matters** *(review)* *(gap)* — saturation? latency tail? throughput? Use the USE method (utilization / saturation / errors) to choose what to measure. The wrong metric measured perfectly is still the wrong test.
- **Regression-detected, not absolute** *(review, strategize)* *(brittleness)* — flag the *delta from baseline*, not absolute numbers. Absolute thresholds in CI are flake generators because the runner's load varies. Baseline-relative thresholds (e.g., "no more than 10% slower than last week's median") are stable.
- **Profiling artifacts captured** *(review, triage)* *(confusion)* — when a perf test fails, the trace, flame graph, or profile is captured automatically. Without it, the failure is undebuggable; the on-call has to reproduce locally to find anything.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are thresholds explicit (and percentile-based)? | Signals nothing | Add p50 / p99 / p999 thresholds |
| Are thresholds tied to a real SLO? | Test is theatre | Anchor thresholds in a user-facing or SLA commitment |
| Is the environment stable, with warmup? | Constant flake | Move to dedicated infra; add warmup; report stat-sig |
| Does the workload match production shape? | Misses the real bugs in the tail | Model the workload from production traffic |
| Is the metric the one that matters? | Wrong-target measurement | Apply USE method to choose what to measure |
| Are thresholds baseline-relative? | Absolute thresholds flake | Switch to delta-from-baseline detection |
| Are profiling artifacts captured on failure? | Undebuggable in CI | Auto-capture trace / flame graph / profile on failure |

## Cross-references

- → `unit.md` for functional correctness
- → `integration.md` when the perf test exercises real I/O collaborators
- → `core/failure-modes.md` — gap (wrong metric or wrong workload) and flakiness (unstable environment) are the dominant modes
- → `core/personas.md` — persona 3 (suite operator) tunes the budget; persona 2 (on-call) needs the artifacts when it fails
