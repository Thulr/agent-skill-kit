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
- **OpenTelemetry GenAI Semantic Conventions (2024–2026, GenAI
  Observability SIG)** — the institutional schema for tracing AI and
  agent workloads. Defines `gen_ai.operation.name` (`create_agent`,
  `invoke_agent`, `invoke_workflow`), `gen_ai.usage.{input,output}_tokens`,
  `gen_ai.response.finish_reasons`, `gen_ai.conversation.id` for session
  correlation, and (as of v1.37) aggregated chat-history attributes
  (`gen_ai.system_instructions`, `gen_ai.input.messages`,
  `gen_ai.output.messages`) carried on the span or a dedicated event.
  Status is still *Development* with most attributes *experimental*;
  dual-emission via `OTEL_SEMCONV_STABILITY_OPT_IN` is the documented
  migration path.

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
- AI/agent workloads emit OTel GenAI semconv attributes
  (`gen_ai.operation.name`, `gen_ai.usage.{input,output}_tokens`,
  `gen_ai.response.finish_reasons`); multi-agent runs render as one
  causal tree via `gen_ai.conversation.id` and an enclosing
  `invoke_workflow` span. Vendor-specific extensions ride alongside the
  canonical attributes rather than replacing them.
- Inline chat-history capture has a documented size cap, or large
  prompts/responses are stored by reference (object key, content hash,
  eval-dataset row ID) with a typed pointer on the span. Token-usage
  and structural attributes remain on the span even when content is
  redacted or referenced.

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
- AI/agent workloads emit ad-hoc attribute names (`prompt_tokens`,
  `model`, `chain_id`) instead of OTel GenAI semconv; spans cannot be
  joined with vendor-aware backends and dashboards require
  per-team-bespoke translation.
- Multi-agent or workflow traces are rendered as disconnected trees:
  context does not propagate across the agent-to-agent boundary, so
  workflow-level latency or failure attribution is reconstructed by
  hand from log timestamps.
- Inline prompt and response bodies on `gen_ai.input.messages` /
  `gen_ai.output.messages` blow past the backend's per-span size limit,
  silently truncating high-value evidence; or full chat histories are
  inlined on every span with no PII boundary and become the dominant
  source of telemetry-tier data exposure.

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
- **OTel GenAI semconv for AI/agent workloads** *(design, audit,
  strategize)* — LLM and agent spans use the canonical `gen_ai.*`
  attribute namespace, not a per-team ad-hoc shape. Vendor-specific
  extensions are accepted as long as the canonical attributes are also
  emitted, so downstream backends do not need translation. Treat
  experimental-status conventions as movable: dual-emit via
  `OTEL_SEMCONV_STABILITY_OPT_IN` rather than pin to one version.
- **Workflow and conversation correlation** *(design, audit,
  diagnose)* — multi-agent runs are wrapped in an `invoke_workflow`
  span; per-call spans share a `gen_ai.conversation.id` so a session
  reconstructs across agent-to-agent and tool-to-tool hops as one
  causal tree. Propagation gaps at the agent boundary are findings, not
  known limitations.
- **Inline-vs-reference content discipline** *(design, optimize,
  strategize)* — when prompts and responses are captured, the playbook
  either inlines them with a documented size cap or stores them by
  reference with a typed span pointer. The choice is made deliberately
  because inline content makes traces self-contained for replay and
  eval but bloats span size and widens the PII surface; observability
  pipelines have been shown to dominate post-incident PII exposure in
  AI workloads.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does context propagate end-to-end through every boundary? | Traces are misleading | Audit boundary points (queue, batch, external SDK); add propagation |
| Are span names stable and low-cardinality? | Trace store / aggregation breaks | Move high-cardinality data to attributes; pin operation in name |
| Does sampling guarantee error / slow trace coverage? | Diagnosis depends on luck | Switch to tail-aware or error-prioritized sampling |
| Are traces correlated with logs and metrics via trace ID? | Joining under incident is manual | Inject trace ID into log MDC / metric exemplars |
| Is there a span-attribute cardinality budget? | Backend will be surprised | Define a budget; review new attributes |
| Does the dependency graph match the team's mental model? | Unknown dependencies bite during incidents | Surface graph; triage gaps |
| Do AI/agent spans use OTel GenAI semconv (`gen_ai.*`)? | Backends and dashboards need per-team translation | Adopt the canonical attribute names; emit vendor extensions alongside, not instead |
| Does multi-agent context propagate via `gen_ai.conversation.id` + `invoke_workflow`? | Workflow latency reconstructed by hand from log timestamps | Propagate session ID and wrap the workflow in a parent span |
| Is the inline-vs-reference content choice documented with a size cap? | Span truncation or PII bloat, unpredictably | Pick a model; document the cap and pointer shape |

## Cross-references

- → `logs.md` for trace-ID correlation.
- → `metrics.md` for attribute / label cardinality discipline.
- → `latency.md` for cross-service latency attribution.
- → `slos.md` for SLI sourced from traces.
