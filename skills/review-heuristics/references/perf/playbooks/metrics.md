# Metrics Playbook

## Scope

Time-series metrics and their selection, instrumentation, aggregation,
cardinality, and the relationship between metrics and dashboards,
alerts, and SLOs. Covers RED / USE / Four-Golden-Signal coverage,
quantile aggregation, label / attribute cardinality, and the role of
metrics versus events.

## Grounding

- **SRE book (eds. 2016)** — the Four Golden Signals (latency,
  traffic, errors, saturation) as the minimum-coverage set for any
  user-facing service; the priority order matters.
- **Tom Wilkie — "The RED Method" (2015)** — Rate / Errors /
  Duration for service-tier instrumentation as a complement to USE for
  resources; service-shaped metrics belong on services, resource-
  shaped metrics belong on resources.
- **Brendan Gregg — "Thinking Methodically about Performance" (ACM
  Queue, 2013)** — the USE method as the resource-tier counterpart.
- **Gil Tene — "How NOT to Measure Latency" (2015)** — averaging or
  summing pre-aggregated quantiles is statistically meaningless; the
  HdrHistogram approach preserves quantile fidelity for later
  aggregation.
- **Cindy Sridharan — *Distributed Systems Observability* (2018)** —
  metrics as the aggregate signal, distinct from events; what metrics
  cannot answer that traces and logs can.
- **Charity Majors, Liz Fong-Jones, George Miranda — *Observability
  Engineering* (2022)** — the cardinality cost of metrics; the role
  of metric pre-aggregation versus structured events.

## Good signals

- Every user-facing service has RED metrics (rate, errors, duration);
  every shared resource has USE metrics (utilization, saturation,
  errors); the Four Golden Signals are covered.
- Latency metrics are histograms, not averages; quantiles are computed
  correctly (no averaging of pre-aggregated quantiles across instances
  or time windows).
- Label / attribute cardinality has a documented budget; new labels
  pass review.
- Metric naming, units, and labels follow a documented convention;
  cross-service comparison is meaningful.
- Dashboards answer specific operational questions ("is this service
  meeting its SLO?", "what is the saturation source?"), not "what
  did we have data for?"
- The same metric is computable from the same code path across
  environments; staging metrics correspond to production metrics.

## Common failures

- Latency is reported as an average; the tail experience is invisible.
- Pre-aggregated quantiles (p99 stored per instance, then averaged in
  the dashboard) produce numbers that look reasonable but mean
  nothing.
- Cardinality is unbounded; a label takes a user ID or request ID;
  the metric backend collapses under series count.
- The dashboard is decoration — it has graphs but does not answer the
  diagnostic question.
- A service is missing one of the Four Golden Signals (typically
  saturation), so a saturation-driven failure looks unrelated.
- Metric naming is per-team and inconsistent; cross-service rollups
  are not possible.
- Service metrics and resource metrics are conflated; saturation
  metrics on a service obscure the underlying resource bottleneck.

## Heuristics

- **Four Golden Signals coverage** *(audit, design)* — every
  user-facing service emits latency, traffic, errors, saturation; gaps
  are findings.
- **RED for services, USE for resources** *(design, audit)* —
  service-shaped metrics on services, resource-shaped metrics on
  resources; do not conflate them.
- **Histograms, not averages** *(design, audit, optimize)* — latency
  is a histogram; quantiles are computed correctly; never average
  pre-aggregated quantiles.
- **Label cardinality budget** *(design, optimize, strategize)* —
  documented budget per metric; new labels pass review; runaway labels
  are caught before backend collapse.
- **Dashboards answer questions** *(audit, design)* — every dashboard
  has a named question it exists to answer; graphs without an
  operational question are removed.
- **Naming and unit conventions** *(design, strategize)* — units in
  the metric name (or label); naming follows convention; cross-service
  rollups are coherent.
- **Production-staging metric parity** *(audit, design)* — the same
  metric is emitted in staging and production from the same code
  path; staging behavior maps to production behavior.
- **Pre-aggregation discipline** *(audit, design)* — pre-aggregated
  metrics are paired with structured events for novel-question
  debuggability; pre-aggregation is not the only signal.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are the Four Golden Signals covered? | Saturation-driven failures are mysterious | Add the missing signals (typically saturation) |
| Are latency metrics histograms? | Tail is hidden | Replace average / pre-aggregated quantiles with histograms |
| Are pre-aggregated quantiles avoided across instances? | Reported p99 is meaningless | Compute quantiles from histogram buckets, not from instance averages |
| Is there a label-cardinality budget? | Backend will collapse | Define a budget; audit existing labels |
| Does every dashboard have a named question? | Dashboards are decoration | Cull or annotate; require a question per panel |
| Are service vs resource metrics distinguished? | Bottleneck attribution is muddled | Use RED for services, USE for resources |

## Cross-references

- → `latency.md` for the percentile-aggregation pitfalls.
- → `tracing.md` for attribute cardinality discipline.
- → `slos.md` for SLI sourcing from metrics.
- → `resources.md` for USE coverage of resources.
