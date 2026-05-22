# Latency Playbook

## Scope

End-to-end response-time distribution for any user-facing or
service-to-service operation. Covers the backend service tier (request
handling, queueing, IO waits), the browser / network tier (TCP / TLS
handshakes, critical rendering path, HTTP multiplexing), and the
database tier (index lookups, lock waits, buffer pool misses). Schema
design, replication topology, and migration safety route to a future
data-modeling skill.

## Grounding

- **Brendan Gregg — *Systems Performance* (2nd ed., 2020)** —
  profile-before-optimize discipline; symptom-to-root-cause methodology;
  IO, CPU, and scheduling-latency framing.
- **Martin Kleppmann — *Designing Data-Intensive Applications* (2017)** —
  the median (p50) hides the tail; p99 represents the worst regular
  user; head-of-line blocking compounds; tail amplification under
  fan-out.
- **Gil Tene — "How NOT to Measure Latency" (Strange Loop, 2015)** —
  coordinated omission renders most homemade latency benchmarks
  misleading; HdrHistogram preserves quantile fidelity losslessly.
- **Jeffrey Dean, Luiz Andre Barroso — "The Tail at Scale" (CACM,
  2013)** — hedged requests, tied requests, micro-partitioning, and
  selective replication as tail-tolerant designs.
- **John D. C. Little — "L = lambda * W" (1961)** — concurrency,
  throughput, and latency are bound by an identity, not negotiable
  independently.
- **Ilya Grigorik — *High Performance Browser Networking* (2013)** —
  TCP / TLS handshake costs; HTTP/2 multiplexing; critical rendering
  path; browser-tier latency budgets.
- **Steve Souders — *High Performance Web Sites* (2007)** — the bulk
  of display time is client-side; original 14 front-end rules.
- **Markus Winand — *SQL Performance Explained* (2012)** — index
  anatomy and predicate selectivity drive DB-tier read latency;
  function-wrapped predicates disable indexes silently.

## Good signals

- Per-operation latency budgets are documented (e.g., checkout API p99
  < 800 ms, DB query p99 < 50 ms, FCP < 1.8 s).
- Tail percentiles (p95, p99, p99.9, max) are tracked alongside median;
  histograms preserve the shape, not just aggregates.
- Latency is recorded at the boundary the user experiences, not only at
  internal hop boundaries.
- Coordinated omission is explicitly addressed in benchmarks (HdrHistogram
  or equivalent; backpressure-aware load generation).
- For fan-out / dependency-heavy paths, the slowest dependency is the
  primary perf signal, not the average.
- DB-tier slow queries have explained plans archived alongside the
  finding; index strategy is documented.
- Browser-tier: critical rendering path is measured (FCP, LCP, TTI),
  not just network time.

## Common failures

- Averages or medians are the only reported metric; the tail is
  invisible.
- Benchmarks suffer coordinated omission — the load generator pauses
  when the system slows, hiding the latency spike.
- Latency is measured at the server boundary, not where the user
  experiences it; the network tail is absent.
- Quantiles are averaged or summed across instances, producing
  statistically meaningless numbers.
- Head-of-line blocking in a shared queue or worker pool is not
  attributed; a single slow request stalls unrelated traffic.
- DB-tier perf claims are made without an explained plan; "we added an
  index" is logged but not verified against the actual query path.
- Browser-tier work is treated as a network problem when it is a CPU /
  rendering problem (or vice versa).

## Heuristics

- **Named per-operation budget** *(design, audit)* — every user-facing
  operation has a documented target at the user-experienced boundary,
  expressed at p99 or worse.
- **Tail-percentile reporting** *(audit, design, diagnose)* — p95, p99,
  p99.9, max are first-class; histograms beat aggregates.
- **Coordinated-omission discipline** *(audit, optimize, diagnose)* —
  measurement tools are checked for coordinated omission; load
  generators are backpressure-aware.
- **Latency where the user feels it** *(design, audit)* — measure at
  the boundary that matters (user device, CDN edge, client SDK) not
  just at the server.
- **Tail-tolerant patterns under fan-out** *(design, optimize)* —
  hedged or tied requests, micro-partitioning, selective replication for
  paths where the slowest dependency dominates.
- **Little's Law sanity check** *(design, diagnose)* — concurrency,
  throughput, latency must satisfy L = lambda * W; if they do not, the
  measurement or the model is wrong.
- **DB-tier plan-first** *(diagnose, optimize)* — before adding an
  index or rewriting a query, capture the current and projected
  explained plan; verify post-change.
- **Browser-tier render budget** *(design, audit)* — FCP / LCP / TTI
  have documented targets; CPU vs network attribution is explicit.
- **Cold-start bound** *(design, audit)* — process / runtime cold-start
  latency is measured and capped; warm vs cold percentiles are
  separated.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are tail percentiles (p99+) reported? | Tail experience is hidden | Add histogram-based p95 / p99 / max reporting |
| Is coordinated omission addressed in benchmarks? | Numbers may be fictional | Switch to a backpressure-aware load generator and HdrHistogram-equivalent recorder |
| Is latency measured where the user experiences it? | Network tail is invisible | Instrument at the user-facing boundary or via RUM |
| For fan-out paths, is the tail-dependency strategy explicit? | Tail amplifies silently | Pick a tail-tolerant pattern (hedge, tie, partition, replicate) |
| For DB-tier paths, are explained plans archived? | Index claims are unverified | Capture plans before / after every perf change |
| For browser, is render budget separate from network budget? | CPU and network conflate | Add FCP / LCP / TTI alongside TTFB |

## Cross-references

- → `throughput.md` for the Little's-Law-paired concurrency / RPS view.
- → `resources.md` for CPU / IO saturation as a latency source.
- → `tracing.md` for cross-service latency attribution.
- → `metrics.md` for percentile aggregation pitfalls.
