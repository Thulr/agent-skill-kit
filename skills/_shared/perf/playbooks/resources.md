# Resources Playbook

## Scope

CPU, memory, disk, network, and process / kernel-level resources
across application, runtime, OS, and container layers. Includes GC
pressure, lock contention, file-descriptor pressure, connection-pool
exhaustion, and runtime-specific saturation modes. The database tier
is covered for performance-relevant resources (buffer pool, lock
contention, connection pool); schema design and migration safety
route to a future data-modeling skill.

## Grounding

- **Brendan Gregg — *Systems Performance* (2nd ed., 2020)** — the
  USE method (utilization, saturation, errors) as a complete-coverage
  checklist for every resource; the principle that profiling precedes
  optimization; the methodology of working from symptoms to root
  causes via a checklist rather than guessing.
- **Brendan Gregg — "Thinking Methodically about Performance" (ACM
  Queue, 2013)** — the canonical USE-method publication; checklists
  exist for Linux / Solaris / cloud / virtualization.
- **Brendan Gregg — *BPF Performance Tools* (2019)** — eBPF-era Linux
  observability; moving from coarse system metrics to fine-grained
  kernel / userspace tracing without restart.
- **Raj Jain — *The Art of Computer Systems Performance Analysis*
  (1991)** — queueing models and the foundational treatment of
  utilization vs saturation.
- **Markus Winand — *SQL Performance Explained* (2012)** — DB-tier
  index strategy, buffer-pool sensitivity, lock contention, and the
  pitfall of function-wrapped predicates that disable indexes.

## Good signals

- For every resource, utilization, saturation, and errors are tracked
  — not just utilization.
- Saturation alerts fire before utilization saturates user-visible
  latency, with calibrated headroom.
- Profiling is the first step of an optimization investigation, not an
  afterthought; flamegraphs or equivalent are archived alongside
  findings.
- GC behavior is measured (pause distribution, allocation rate, heap
  occupancy), not just heap size.
- Lock contention is observable (hot locks, queue depth at contended
  resources) — not inferred from "latency went up."
- DB connection pool sizing is derived from measured concurrency and
  query duration; not "as many as the host allows."
- File descriptors, threads, ephemeral ports, and other countable
  kernel resources have alarms before exhaustion.

## Common failures

- Utilization is the only metric; saturation and errors are missing,
  so a saturated-but-not-fully-utilized resource looks healthy.
- Optimization proceeds without profiling; effort lands on resources
  that are not actually the bottleneck.
- GC pauses are aggregated as "average pause time," hiding the
  outliers that cause user-visible latency.
- Lock contention is invisible; symptoms are misattributed to CPU or
  IO.
- Connection pool sizing is inherited from a tutorial or copied from
  another service.
- Out-of-file-descriptors, out-of-threads, or ephemeral-port exhaustion
  surfaces as an unrelated cascading failure.
- Container-level resource limits are not aligned with host-level
  reality; a workload throttled by cgroups looks like an application
  bug.

## Heuristics

- **USE method, every resource** *(audit, design, diagnose)* — for
  every resource, check utilization, saturation, AND errors. A
  complete-coverage checklist beats a creative inspection.
- **Profile before optimize** *(optimize, diagnose)* — every
  optimization investigation starts with a profile under representative
  load. The flamegraph (or equivalent) is archived with the finding.
- **Saturation-first alerting** *(design, strategize)* — saturation
  metrics (run-queue length, queue depth, pool wait time) trigger
  before utilization metrics, because saturation is what creates
  user-visible latency.
- **GC pause percentile reporting** *(audit, diagnose)* — track GC
  pause distribution (p99, max), not just average; tie pause
  percentiles to user-facing latency budgets.
- **Lock contention observability** *(audit, design)* — hot locks,
  queue depth at contended resources, and acquisition latency are
  measured; inferring contention from generic CPU graphs is unreliable.
- **Connection pool sizing from data** *(design, diagnose)* — pool
  size derives from measured concurrency × duration; tuned via
  Little's Law, not by tutorial defaults.
- **Countable kernel resources have alarms** *(design, audit)* —
  file descriptors, threads, ephemeral ports, inotify watches:
  exhaustion surfaces as a different symptom; alarm at threshold,
  not at 100%.
- **Container vs host alignment** *(audit, diagnose)* — cgroup limits,
  CPU shares, memory limits, and OOM behavior are compared against
  host capacity; cgroup throttling is distinguishable from application
  slowness.
- **DB-tier resource view** *(diagnose, audit)* — buffer pool hit
  rate, lock waits, and connection-pool saturation are first-class
  signals for DB-bound services; explained plans are captured for
  slow queries.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are utilization, saturation, AND errors tracked per resource? | Resource health is incomplete | Run the USE checklist for the platform; fill the gaps |
| Is profiling the first step of optimization? | Effort lands on the wrong resource | Require a profile artifact attached to every optimization proposal |
| Are saturation metrics the alerting trigger? | Alerts fire after users feel it | Move alert thresholds to saturation signals (queue depth, pool wait) |
| Are GC pauses tracked at p99 and max? | Outliers hide in averages | Add pause percentile metrics; tie to latency budget |
| Is lock contention observable directly? | Contention is misattributed | Add lock instrumentation (runtime-specific) |
| Is connection-pool sizing derived from data? | Pool is mis-sized | Re-derive pool size from measured concurrency × duration |
| Are countable kernel resources alarmed? | Exhaustion masquerades | Add threshold alarms below 100% |

## Cross-references

- → `latency.md` for resource-bound latency attribution.
- → `throughput.md` for the bottleneck-resource framing.
- → `metrics.md` for USE instrumentation specifics.
- → `tracing.md` for cross-service resource attribution.
