# Tracing Playbook

## Scope

Distributed tracing across service boundaries: trace context
propagation, span structure and naming, sampling strategy, attribute
cardinality, dependency-graph fidelity, and the role of traces in
diagnosis versus aggregation. Covers OpenTelemetry-shaped pipelines and
their predecessors; does not specify a particular backend.

## Grounding

- **Benjamin H. Sigelman et al. — "Dapper, a Large-Scale Distributed
  Systems Tracing Infrastructure" (2010)** — the foundational
  distributed-tracing model: trace context propagation, span causality
  via parent / child relationships, sampling discipline, and the
  dependency graph as the unit of system understanding.
- **Cindy Sridharan — *Distributed Systems Observability* (2018)** —
  the three-pillars framing alongside its limits; traces alone do not
  constitute observability; the role of traces vs metrics vs logs.
- **Charity Majors, Liz Fong-Jones, George Miranda — *Observability
  Engineering* (2022)** — high-cardinality, structured-event
  observability; the critique of pre-aggregation; why novel-question
  debuggability requires preserving the per-request shape rather than
  rolling up to metrics.

## Good signals

- Context propagation is end-to-end: every service that participates in
  a request emits a span tied to the same trace ID; no propagation
  breaks at the gateway, queue, batch worker, or external SDK
  boundary.
- Span names are stable, low-cardinality, and operationally meaningful
  (e.g., `POST /v1/checkout` not `POST <uuid>`); span attributes carry
  the high-cardinality bits (customer ID, request ID, route variant).
- Sampling is tail-aware: 100% of error / slow traces are captured;
  head sampling thresholds are documented; sampling decisions are
  propagated, not re-rolled per service.
- The dependency graph derived from traces matches the team's mental
  model; surprises (unknown dependency, missing dependency) are
  triaged.
- Traces are correlated with logs and metrics via trace ID; an
  on-call engineer can pivot from "slow request" to "the spans for
  that request" without manual joins.
- Span attribute cardinality has a budget; new attributes are
  reviewed before they ship.

## Common failures

- Context propagation breaks at the queue / batch / external-SDK
  boundary; traces appear to "end" mid-request.
- Span names embed high-cardinality data (request IDs in the name),
  exploding the trace store and breaking aggregation.
- Sampling is uniform random at the gateway, losing the rare-but-
  expensive trace.
- High-cardinality attributes (user IDs, request IDs) are coerced into
  metric labels, exploding cardinality.
- Trace IDs are absent from logs and metrics; correlation requires
  manual joins under incident pressure.
- Sampled traces lose error-path coverage because errors are rare and
  random sampling does not preserve them.

## Heuristics

- **End-to-end propagation discipline** *(audit, design, strategize)* —
  every boundary (sync HTTP, async queue, batch worker, external SDK,
  CDN, browser) propagates trace context; propagation gaps are tracked
  as findings, not tolerated as known limitations.
- **Stable, low-cardinality span names** *(audit, design)* — names
  carry the operation; attributes carry the per-request data.
- **Tail-aware sampling** *(design, audit, optimize)* — errors and
  slow traces sampled at 100%; head sampling decisions documented and
  propagated.
- **Trace-log-metric correlation** *(design, audit)* — trace ID is
  present in every log line emitted in the request scope and in
  request-level metrics where applicable.
- **Span attribute cardinality budget** *(design, optimize,
  strategize)* — new attributes pass through review against a
  documented cardinality budget; runaway attributes are caught before
  they break the backend.
- **Dependency graph as system understanding** *(audit, diagnose)* —
  the dependency graph derived from traces is reviewed; unknown or
  missing dependencies are triaged.
- **Sampling preserves error coverage** *(design, audit)* — sampling
  strategy guarantees the rare error trace is kept; uniform random
  sampling fails this and is replaced with error-prioritized or
  tail-based sampling.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does context propagate end-to-end through every boundary? | Traces are misleading | Audit boundary points (queue, batch, external SDK); add propagation |
| Are span names stable and low-cardinality? | Trace store / aggregation breaks | Move high-cardinality data to attributes; pin operation in name |
| Does sampling guarantee error / slow trace coverage? | Diagnosis depends on luck | Switch to tail-aware or error-prioritized sampling |
| Are traces correlated with logs and metrics via trace ID? | Joining under incident is manual | Inject trace ID into log MDC / metric exemplars |
| Is there a span-attribute cardinality budget? | Backend will be surprised | Define a budget; review new attributes |
| Does the dependency graph match the team's mental model? | Unknown dependencies bite during incidents | Surface graph; triage gaps |

## Cross-references

- → `logs.md` for trace-ID correlation.
- → `metrics.md` for attribute / label cardinality discipline.
- → `latency.md` for cross-service latency attribution.
- → `slos.md` for SLI sourced from traces.
