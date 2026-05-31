# Logs Playbook

## Scope

Structured logging across services, including log schema, severity
discipline, correlation with traces and metrics, volume and retention,
sampling, and the role of logs in incident recovery and post-incident
review. Covers application logs, request logs, audit logs, and
event logs.

## Grounding

- **Cindy Sridharan — *Distributed Systems Observability* (2018)** —
  the three-pillars framing positions logs as the irreplaceable
  per-event record; logs answer questions metrics cannot because they
  preserve the shape of the event.
- **Charity Majors, Liz Fong-Jones, George Miranda — *Observability
  Engineering* (2022)** — structured events as the primitive;
  high-cardinality is a feature, not a problem; logs that cannot be
  joined to traces and metrics are diagnostically weaker than they
  appear.

## Good signals

- Every log line is structured (key-value or JSON), not free-text;
  schema is documented.
- Trace ID and span ID are present on every log line emitted in a
  request scope; correlation requires no manual join.
- Severity levels (DEBUG / INFO / WARN / ERROR / FATAL) are used by
  rule, not by feel; the rule is documented and enforced.
- Log volume per service is bounded and predictable; spikes are
  alarmed.
- Retention is sufficient to span the longest plausible incident
  investigation window plus post-incident review.
- High-cardinality identifying information is captured intentionally
  in the event payload, not in the message string where it cannot be
  queried.
- Secret leakage is checked (token / password / PII redaction rules);
  log pipeline has a redaction stage.

## Common failures

- Logs are free-text strings; queries depend on regex against the
  message; cross-service joins are impossible.
- Trace IDs are absent; correlating a request across services requires
  human cross-referencing under incident pressure.
- Severity levels are assigned by author preference; ERROR is used
  for warnings and INFO for things that should be ERROR; alerting on
  ERROR fires on noise.
- Log volume scales with traffic but is not budgeted; cost blowup is
  the first signal that something is wrong.
- Retention is too short for incident investigation; the bug that
  manifests on Monday cannot be diagnosed from logs that aged out on
  Friday.
- Secrets, tokens, or PII end up in logs because no redaction stage
  exists in the pipeline.
- Sampling is applied uniformly, losing the rare error log; or
  sampling is absent and cost is uncontrolled.

## Heuristics

- **Structured-event discipline** *(audit, design, strategize)* — every
  log line is structured key-value; schema is documented; free-text
  is forbidden in new code.
- **Trace correlation everywhere** *(design, audit)* — trace ID and
  span ID injected into log MDC (or equivalent) for every
  request-scope log; correlation is one query away.
- **Severity rule, not severity feel** *(audit, design)* — the rule
  for picking DEBUG / INFO / WARN / ERROR / FATAL is written down;
  alerts on ERROR fire on errors, not noise.
- **Volume budget** *(design, strategize, optimize)* — per-service
  log volume has a budget; spikes are alarmed; cost is predictable.
- **Retention matches investigation window** *(design, strategize)* —
  retention spans the longest plausible incident window plus
  post-incident review; logs that age out before they can be queried
  do not exist.
- **Redaction in pipeline** *(audit, design)* — secret, token, and PII
  redaction happens in the collection pipeline, not at the source;
  defense in depth.
- **Sampling preserves error coverage** *(design, optimize)* —
  sampling, if applied, preserves error and slow-path logs at full
  fidelity.
- **High-cardinality in the event** *(design, audit)* — IDs, customer
  identifiers, route variants belong in the event payload (queryable),
  not interpolated into the message string.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is every log line structured? | Cross-service queries are impossible | Migrate to structured logging; lint free-text |
| Are trace IDs on every request-scope log line? | Correlation is manual | Inject trace context into log MDC at the request boundary |
| Are severity levels assigned by a documented rule? | Alerts fire on noise | Write the rule; audit existing call sites |
| Is log volume budgeted and alarmed? | Cost surprises arrive late | Add per-service volume metrics with alarms |
| Does retention span the investigation window? | Stale incidents are undiagnosable | Extend retention or add long-term archival |
| Is there a redaction stage in the pipeline? | Secret leakage is unmitigated | Add redaction in the collector; verify with samples |
| Does sampling preserve error coverage? | Rare errors lost | Switch to error-prioritized sampling |

## Cross-references

- → `tracing.md` for trace-log correlation pattern.
- → `metrics.md` for the role-of-logs vs role-of-metrics framing.
- → `slos.md` for log-derived SLI sources.
