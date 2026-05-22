# Throughput Playbook

## Scope

Sustained request / transaction rate, scalability behavior under load,
queueing dynamics, and load-shedding posture for backend services,
data pipelines, and the database tier. Covers the shape of the
scalability curve, the bottleneck resource, and the regime where
adding capacity stops helping.

## Grounding

- **Neil J. Gunther — *Guerrilla Capacity Planning* (2006)** — the
  Universal Scalability Law extends Amdahl with a coherency term;
  beyond a system-specific node count, additional capacity degrades
  throughput. Fit USL parameters from measured throughput-at-load to
  project the ceiling.
- **John D. C. Little — "L = lambda * W" (1961)** — at steady state,
  concurrency = throughput × latency. Two of three pin the third; a
  proposed throughput target must be consistent with the concurrency
  and latency budget.
- **Martin Kleppmann — *Designing Data-Intensive Applications*
  (2017)** — partitioning, replication, and the trade-offs that
  determine where the throughput ceiling lives.
- **Raj Jain — *The Art of Computer Systems Performance Analysis*
  (1991)** — load model selection, common measurement mistakes, and
  the discipline of separating open-loop from closed-loop testing.
- **SRE book (eds. 2016)** — load shedding, graceful degradation, and
  the Four Golden Signals (traffic, errors, saturation) as the
  throughput-relevant triplet.

## Good signals

- Throughput is measured against a load model that matches production
  traffic (arrival distribution, request mix, concurrency).
- The scalability curve has been characterized — throughput is plotted
  against concurrency to find the knee.
- The bottleneck resource is named (CPU, memory bandwidth, disk
  IOPS, DB connections, network egress, lock contention) — not
  guessed.
- Load-shedding policy is explicit and tested (which requests get
  dropped, retried, queued, prioritized).
- Retry storms, thundering herds, and synchronized backoff are
  considered in the load model.
- DB-tier connection-pool sizing matches workload (not "as many as
  the host allows").

## Common failures

- Throughput is reported as a single number ("we do 10k RPS") with no
  concurrency or latency context — meaningless under Little's Law.
- Benchmarks run open-loop against a closed-loop production system, or
  vice versa.
- Adding nodes is assumed to lift throughput linearly; the USL
  coherency term is ignored until the system degrades.
- The bottleneck resource is misattributed — "we need more CPU" when
  it is lock contention or DB connection saturation.
- Load shedding is implicit (timeouts cascade) rather than designed
  (priority-aware shedding).
- Retry storms after a brief upstream blip cause sustained throughput
  collapse.

## Heuristics

- **Characterize the scalability curve** *(audit, design, strategize)* —
  measure throughput against concurrency steps; identify the knee and
  the regime where capacity stops helping.
- **Name the bottleneck resource** *(diagnose, audit)* — before
  proposing a fix, identify which resource saturates first under the
  load model. Common candidates: CPU, IO, DB connections, locks, GC.
- **Little's Law as a sanity check** *(design, diagnose)* — proposed
  throughput must be consistent with target latency and available
  concurrency; if not, one of the three is wrong.
- **Load model matches production** *(audit, design)* — arrival
  distribution, request mix, and concurrency in the benchmark reflect
  observed production traffic; otherwise the throughput number is
  fictional.
- **Open-loop vs closed-loop discipline** *(audit, diagnose)* — open-
  loop generators expose queueing dynamics; closed-loop generators hide
  them. Pick the one that matches the deployed surface.
- **Explicit load-shedding policy** *(design, strategize)* — under
  overload, the system drops, retries, or prioritizes by an explicit
  rule, not by accidental timeout.
- **Retry / herd safeguards** *(design, audit)* — jittered retry,
  exponential backoff, request hedging caps, and circuit breakers are
  in place before the system meets sustained overload.
- **USL parameter fit** *(strategize, audit)* — for capacity-planning
  decisions, fit a USL curve to measured throughput-at-load and
  project the headroom before committing.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is the scalability curve characterized? | Capacity is a guess | Run a stepped load test; plot throughput vs concurrency |
| Is the bottleneck resource named? | Optimizations target the wrong thing | Profile under representative load before proposing fixes |
| Does Little's Law hold across the latency / throughput / concurrency claims? | Numbers are inconsistent | Re-measure; identify which of the three is wrong |
| Does the load model match production? | Benchmark is fictional | Re-derive the load model from production telemetry |
| Is load-shedding explicit? | Overload cascades unpredictably | Design a priority-aware shedding rule with tests |
| Are retry safeguards in place? | A blip becomes an outage | Add jitter, backoff, hedging caps, and circuit breakers |

## Cross-references

- → `latency.md` for the Little's-Law-paired latency view and tail
  amplification under load.
- → `resources.md` for saturation as the bottleneck signal.
- → `slos.md` for load-shedding policy alignment with error budget.
- → `metrics.md` for traffic-and-saturation instrumentation.
