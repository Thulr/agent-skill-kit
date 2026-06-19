# SDK Telemetry Playbook

## Scope

Instrumentation an SDK author builds *into* an agent/AI client so the loop is
observable and safe to observe: per-step spans on a named convention, an
SDK-boundary content-capture toggle, a pluggable redactor, redaction-surviving
structural telemetry, and the inline-vs-reference content decision.

- **In:** structural spans + attribute conventions, content-capture toggle,
  boundary redaction, cardinality discipline, content storage choice.
- **Out:** *operating* the traces — dashboards, alerting, drift detection, cost
  monitoring (see `agent-ops`); generic application logging/metrics/consent UX
  (see `dx-audit` / `dx-design` telemetry).
- **Intents this surface answers:** do, review, design.

## Grounding

- **In agent systems the observability pipeline is a primary PII surface.**
  Traces and error reports retain raw prompts/responses longer than the
  inference path and are read by more people; a large share of post-incident PII
  exposure is discovered there. The implication: redact at the SDK boundary,
  before any span attribute is set — not at the downstream collector.
- **Structural telemetry and content telemetry are different axes.** Token
  counts, latencies, finish reasons, and tool-call shapes are low-cardinality
  and safe; raw prompts/responses and per-request IDs are high-cardinality and
  sensitive. Coupling them means turning off content capture blinds the
  structural view too.
- **Tracing belongs in the SDK, not above it.** A multi-step loop must emit a
  span per step by default; turning tracing on at the application layer captures
  nothing the SDK already executed.

## Good signals

- A single boolean (`record_content` or equivalent) flips raw prompt/response
  capture without disabling structural telemetry; default is off when PII risk
  is unknown.
- A span is emitted per agent-loop step (LLM call, tool execution, retrieval,
  guardrail, sub-agent) against one named convention (OpenTelemetry `gen_ai.*`
  or OpenInference), batch-exported via a vendor-plugin API.
- A redactor function runs on inputs/outputs *before* any span attribute is set;
  it accepts regex/NER/ML implementations and the docs state its
  recall/precision.
- Low-cardinality structural attributes (token counts, latencies, finish
  reasons, tool-call shape) stay observable when content capture is off.
- Captured content is either inlined with a documented size cap or stored as a
  typed reference (object key, content hash, eval-dataset row ID); the docs name
  which.
- Attribute names follow the chosen convention accurately:
  `gen_ai.operation.name`, `gen_ai.usage.{input,output}_tokens`,
  `gen_ai.response.finish_reasons`, `gen_ai.conversation.id` for session
  correlation; vendor-specific attributes ride alongside canonical ones.

## Common failures

- Tracing is opt-in and bolted on; a misbehaving agent cannot be reconstructed
  without re-running with `--verbose`.
- Raw prompts and responses land in spans by default, so the trace store becomes
  the largest uncontrolled PII repository in the system.
- Content capture and structural telemetry share one switch, so disabling
  content for privacy also blinds latency/token/finish-reason monitoring.
- Redaction is deferred to the collector, so raw content already transited and
  persisted in the SDK's exporter before anything scrubbed it.
- Per-request IDs and raw content are indexed as high-cardinality dimensions,
  blowing up the metrics backend.
- Heavy NER redaction is co-located on the inference GPU, turning a privacy
  control into a latency regression.
- Spans mix convention sets ad hoc (`guardrail`/`evaluator` are OpenInference,
  not OTel GenAI; `handoff` is a custom span), so backends cannot interpret
  them.

## Heuristics

- **(design, review) Put an SDK-boundary content-capture toggle in.** A single
  `record_content` boolean flips raw capture without disabling structural spans;
  default it off when PII risk is unknown so the safe state is the default.
- **(design, review) Redact at the SDK boundary, before the span.** A pluggable
  redactor runs on inputs/outputs before any attribute is set; it accepts
  regex/NER/ML and the docs name its recall/precision. Deferring to the
  collector is too late — the raw content already persisted.
- **(design) Keep structural and content telemetry on separate axes.**
  Low-cardinality structural attributes stay observable when content is off;
  never index raw content or per-request IDs as high-cardinality dimensions.
- **(do, design) Decide inline-vs-reference explicitly.** Inline captured
  content with a documented size cap, or store a typed reference (object key,
  content hash, dataset row ID); name the choice rather than letting payloads
  grow unbounded in the span.
- **(design, review) Trace per step on one named convention.** Emit a span per
  loop step and pick one convention (OTel GenAI or OpenInference); use its
  attribute names accurately and model spans it lacks (e.g. `handoff`) as custom
  spans rather than mislabelling them.
- **(review) Don't put the redactor on the hot path's GPU.** Co-locating heavy
  NER on the inference accelerator trades privacy for latency; run it where it
  does not steal inference cycles.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is there a content-capture toggle separate from structural telemetry? | Privacy-off blinds structural monitoring | Add a `record_content` boolean; default off |
| Does a redactor run at the SDK boundary before span attributes? | Raw PII persists in the exporter | Add a pluggable boundary redactor |
| Do structural attributes survive content being off? | Disabling content blinds the loop | Split the two onto separate axes |
| Is captured content inlined-with-cap or stored as a reference? | Span payloads grow unbounded | Document the inline cap or the typed pointer |
| Are spans on one named convention with accurate attributes? | Backends can't interpret traces | Pick OTel GenAI or OpenInference; map custom spans |

## Cross-references

- `sdk-design.md` — the loop whose steps these spans instrument.
- `errors-and-retry.md` — capturing the verbatim error on the tool-call span.
- → `agent-ops` for *operating* the resulting telemetry: dashboards, drift
  detection, cost circuit-breakers, and trace-based loop monitoring.
- → `dx-audit` / `dx-design` (`telemetry`) for generic application telemetry,
  metrics, and consent UX as human developer DX.
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` —
  REVIEW scales; finding IDs `AGENT-DX-TEL-NNN`.
- `references/intents/{do,review,design}.csv` row `sdk-telemetry` — the entry points.
