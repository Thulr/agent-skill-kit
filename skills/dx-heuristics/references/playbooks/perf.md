# Performance Playbook

## Scope

Install time, cold start, build and test latency, CLI command response time,
IDE responsiveness, and doc-site load. Routes to `inner-loop.md` for
edit-run-test cycle performance and `setup.md` for install and first-run
performance.

## Grounding

- **Brendan Gregg — *Systems Performance*** — the USE method (utilization,
  saturation, errors) as a systematic checklist for diagnosing resource
  bottlenecks; the principle that profiling must precede optimization; a
  methodology for working from symptoms to root causes without guessing.
- **Jakob Nielsen — response-time research (1993)** — three human-perception
  thresholds: 0.1 s feels instantaneous, 1 s preserves the user's train of
  thought, 10 s is the boundary beyond which attention is lost and a progress
  indicator is mandatory.
- **Martin Kleppmann — *Designing Data-Intensive Applications*** — latency
  framing: median (p50) hides the tail experience; p99 represents the worst
  regular user; head-of-line blocking means a single slow operation can stall
  unrelated requests behind it.

## Good signals

- Latency budgets are documented per operation (e.g., install < 60 s, smoke
  test < 30 s, CLI cold start < 500 ms, doc-site first contentful paint < 2 s).
- Tail percentiles (p95, p99) are tracked and reported alongside median.
- Docs include a "how to profile a slow run" section; the knowledge is written
  down, not tribal.
- A benchmark suite runs in CI; regressions above a defined threshold block
  merge.
- Cold-start path is bounded — CLI or SDK initialization completes in a
  documented, enforced time limit.
- Bundle size and install footprint have a documented ceiling; growth requires
  explicit review.
- User-perceived latency is tracked separately from backend wall-clock
  time — spinner presence and interaction feedback are part of the budget.

## Common failures

- Cold-start latency is unbounded; CLI takes several seconds before printing
  anything.
- Install pulls hundreds of megabytes of transitive dependencies without
  review or size gate.
- Build performance degrades silently as the project grows; no one notices
  until it's painful.
- Only averages are reported; tail latency is hidden, and the slowest users
  are invisible.
- No latency budget means no accountability; performance slips one merged PR
  at a time.
- Slow tests are treated as normal; "just wait for CI" becomes the team
  culture.
- User-perceived latency is ignored — a 3 s operation shows no spinner, no
  progress feedback, no acknowledgment that anything is happening.

## Heuristics

- **Named latency budgets** *(design, audit)* — every user-facing operation
  has a documented target latency. Without a budget, there is no definition of
  "too slow" and no trigger to investigate.
- **Tail-percentile reporting** *(audit, design)* — p95, p99, and max are
  tracked alongside median. Averages obscure the experience of the users who
  hit the slow path most often.
- **Profiling docs** *(design, audit)* — there is a written "how to profile a
  slow run" page; the approach is not locked in one engineer's head. Include
  the tool, the flag, and an example command.
- **Perf CI gates** *(design)* — benchmarks run in CI; merges that exceed the
  regression threshold are blocked, not just flagged. Silent regressions
  compound.
- **Bundle and dep size discipline** *(audit, design)* — install footprint and
  bundle size are measured in CI; growth above a watermark requires deliberate
  sign-off, not passive accumulation.
- **User-perceived latency budget** *(design, audit)* — interactions that
  complete in under 0.1 s feel instant; anything over 1 s needs a progress
  signal; anything over 10 s needs a status update or the user assumes it
  failed.
- **Cold-start bound** *(audit, design)* — CLI and SDK initialization time is
  documented, measured, and enforced. A startup that varies from 200 ms to 4 s
  depending on environment is a latency bug.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are latency budgets documented? | Drift goes unnoticed | Define and publish budgets per operation |
| Are tail percentiles tracked? | Averages lie | Add p95 / p99 reporting to metrics |
| Is there a profiling doc? | Tribal knowledge | Write a "how to profile" page with example commands |
| Do benchmarks run in CI? | Silent regressions | Add a benchmark suite with a regression threshold |
| Is bundle / install size monitored? | Bloat creeps in | Add a size check with a documented ceiling |
| Is cold start bounded? | Variable startup surprises | Profile initialization; document and cap the limit |

## Cross-references

- → `inner-loop.md` for build and test latency.
- → `setup.md` for install and first-run performance.
