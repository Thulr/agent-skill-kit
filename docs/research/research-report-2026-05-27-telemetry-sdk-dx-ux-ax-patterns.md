# Research Report — Effective design patterns for DX, UX, and AX in telemetry SDKs for AI, agents, and evals

**Date:** 2026-05-27
**Depth mode:** survey
**Methodology grounding:** see `skill.json.inspired_by` for the `topic-research` skill

---

## 1. Research question

**What design patterns produce a good developer experience (DX), end-user experience (UX), and agent experience (AX) when building telemetry SDKs that instrument AI applications, autonomous agents, and evaluation pipelines?**

- **In scope:**
  - Instrumentation APIs (decorators, context managers, auto-instrumentation, manual spans).
  - Semantic conventions for AI/agent/eval signals (tokens, tool calls, prompts/responses, eval scores, costs, latency).
  - SDK init and configuration ergonomics (zero-config defaults, env-var contracts, secrets handling).
  - Error-message and structured-output design that is consumable by agents (AX) as well as humans (DX).
  - End-user observability surfaces (trace waterfalls, eval dashboards, alerting) where they are shaped by the SDK contract.
  - PII redaction and sampling patterns at the telemetry boundary.
  - Eval-vs-production telemetry — treated together, with divergences flagged.
- **Out of scope:**
  - Storage backends, query engines, sampling at the collector tier (downstream of the SDK).
  - General APM patterns for non-AI workloads, except as reference for canonical DX patterns.
  - Vendor procurement decisions ("which platform should I buy").
- **Audience / use:** SDK authors building or evolving a telemetry SDK that targets one or more of (AI app, agent, eval) workloads, and want a synthesized view of patterns from current standards and prior art.

## 2. Search strategy

- **Source types consulted:** standards-body documents (OpenTelemetry GenAI SIG specs and blog), peer-reviewed academic (CHI Extended Abstracts), institutional preprints (arXiv), vendor primary docs (Vercel, Stripe, Langfuse, Traceloop, Datadog, AWS, Microsoft), expert practitioner blogs (WorkOS, Nordic APIs), and editorial comparisons.
- **Search terms:** "OpenTelemetry GenAI semantic conventions", "OTel agent traces SIG 2026", "LangSmith Langfuse Arize Phoenix SDK comparison", "OpenLLMetry Traceloop auto-instrumentation", "LLM observability SDK developer experience", "multi-agent OpenTelemetry tracing", "DeepEval Inspect Promptfoo Braintrust eval SDK", "Stripe Twilio SDK idempotency error", "agent-friendly structured error LLM tool calls", "LLM telemetry PII redaction sampling", "\"agent experience\" SDK machine-readable telemetry", "Vercel AI SDK experimental_telemetry", "LLM tracing decorator context manager".
- **Engines / archives:** general web search, arXiv (linked from results), ACM Digital Library (Extended Abstracts of CHI 2025), Semantic Scholar (linked from results), OpenTelemetry official specs.
- **Snowballing:** light — followed citations from OTel blog posts to the GenAI SIG spec pages, and from comparison articles to primary vendor docs.
- **Exclusions:**
  - **Vendor marketing without primary content.** Cited vendor docs only where they describe their own SDK contract (primary), not where they make comparative claims (vendor-aligned secondary).
  - **Posts older than 18 months.** This is a fast-moving field; OTel GenAI SIG output post-April 2024 supersedes earlier proposals. Older industry posts on generic telemetry were considered only as reference patterns (e.g., Stripe idempotency, dated but seminal).
  - **Tertiary content** (encyclopedic summaries, regurgitated comparison posts).
- **Stop criterion:** saturation on the four search axes (OTel standards, vendor SDK shape, eval frameworks, AX/DX patterns) — by the second pass, new searches were returning sources already collected, with only marginal new claims.

## 3. Background

### 3.1 The three audiences

A telemetry SDK for AI/agent/eval systems has three distinct consumer audiences, each with different expectations of the SDK surface:

- **Developer Experience (DX)** — the human engineer integrating the SDK into an application. Cares about install ergonomics, mental model fit, sensible defaults, debuggability of the SDK itself.
- **User Experience (UX)** — the human consumer of the *telemetry output*: an SRE reading a trace waterfall, a PM reading an eval dashboard, an ML engineer triaging a regression.
- **Agent Experience (AX)** — autonomous agents both **emit** and **consume** telemetry. They emit it because the application they implement *is* an agent; they consume it because (a) downstream agents read upstream agents' traces to coordinate or debug, and (b) the SDK's own error messages and validation responses are read by an LLM that may retry or recover. The WorkOS framing: *"agents don't read tooltips, recover from errors gracefully, or maintain context across sessions the way humans do. They operate at machine speed with aggressive retries and rely entirely on surfaced text for decision-making."* ([WorkOS, "Agent Experience"](https://workos.com/blog/agent-experience-oujuh), 2025; editorial, fresh — confidence M).

The three are coupled but not interchangeable. What is good DX (intuitive layout, graceful degradation) may handicap AX (which needs deterministic structured output) ([WorkOS](https://workos.com/blog/agent-experience-oujuh) — confidence M).

### 3.2 OpenTelemetry as the substrate

OpenTelemetry (OTel) is the de-facto industry telemetry standard for AI/agent systems as of 2026. The OTel GenAI Observability SIG began work in April 2024; by Q1 2026, most major agent frameworks (LangChain, CrewAI, AutoGen, AG2) emit OTel-compliant spans either natively or via instrumentation packages ([OpenTelemetry blog, "Inside the LLM Call"](https://opentelemetry.io/blog/2026/genai-observability/), 2026; institutional primary — confidence H). Major vendors including Datadog, Honeycomb, and New Relic support these conventions ([Datadog](https://www.datadoghq.com/blog/llm-otel-semantic-convention/); vendor-aligned primary — confidence H for the fact that Datadog supports them).

The standards are still maturing. As of May 2026, GenAI semantic conventions remain in **Development** status with most attributes marked **experimental**, and dual-emission via `OTEL_SEMCONV_STABILITY_OPT_IN` is the recommended migration path ([OpenTelemetry GenAI agent spans spec](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/); institutional primary — confidence H).

### 3.3 The canonical schema

The current OTel GenAI agent surface defines four span operations ([OpenTelemetry GenAI agent spans spec](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/); institutional primary — confidence H):

- `gen_ai.operation.name = "create_agent"` — agent factory.
- `gen_ai.operation.name = "invoke_agent"` (client) — remote agent invocation.
- `gen_ai.operation.name = "invoke_agent"` (internal) — same-process invocation.
- `gen_ai.operation.name = "invoke_workflow"` — coordinated multi-agent process.

Required attributes are `gen_ai.operation.name` and `gen_ai.provider.name`. Conditional attributes cover agent identity (`gen_ai.agent.{id,name,version,description}`), session correlation (`gen_ai.conversation.id`), and RAG data sources (`gen_ai.data_source.id`). Tool invocations use `gen_ai.tool.definitions` and tool execution follows the `Execute Tool Span` spec. Token usage uses `gen_ai.usage.{input_tokens,output_tokens}` and finish reason uses `gen_ai.response.finish_reasons` ([OpenTelemetry, "Inside the LLM Call"](https://opentelemetry.io/blog/2026/genai-observability/) — confidence H).

Note: version 1.37 of the conventions reworked chat-history capture, replacing per-message events with three aggregated attributes (`gen_ai.system_instructions`, `gen_ai.input.messages`, `gen_ai.output.messages`) carried on the span or a dedicated event ([OpenTelemetry blog, 2026](https://opentelemetry.io/blog/2026/genai-observability/) — confidence H).

## 4. Current state

Design patterns organized by audience, then cross-cutting concerns.

### 4.1 DX patterns

**P1 — Auto-instrumentation as the default integration path.** Every major LLM telemetry SDK ships auto-instrumentation as the primary onboarding surface. OpenLLMetry (Traceloop) auto-instruments 40+ LLM providers, vector databases, and frameworks ([Traceloop docs](https://www.traceloop.com/docs/openllmetry/introduction), [OpenLLMetry GitHub](https://github.com/traceloop/openllmetry); vendor-aligned primary — confidence H). Vercel AI SDK exposes `experimental_telemetry` as a single option on `generateText`/`streamText` calls that emits OTel spans with prompt, response, token counts, latency, and tool-call details ([Vercel AI SDK Telemetry docs](https://ai-sdk.dev/docs/ai-sdk-core/telemetry); vendor primary — confidence H). The DX bar: *minimal code changes, library wraps the call, instrumentation lives in code rather than alongside* ([TokenMix](https://tokenmix.ai/blog/llm-observability-2026-tools-best-practices); editorial — confidence M).

**P2 — Three interoperable instrumentation primitives.** Decorator, context manager, and manual span. The pattern is consistent across Langfuse, Confident AI / DeepEval, LangSmith, and Datadog LLM Observability ([Langfuse instrumentation docs](https://langfuse.com/docs/observability/sdk/instrumentation); [Confident AI tracing](https://www.confident-ai.com/docs/llm-tracing/quickstart); [Datadog LLM Observability SDK reference](https://docs.datadoghq.com/llm_observability/instrumentation/sdk/); vendor primary on each — confidence H for the cross-vendor pattern).
- **Decorator** (`@observe`) — wraps a function; captures inputs, outputs, execution flow; maintains a call stack via Python `contextvars` for async-safe nesting.
- **Context manager** — sets a span as the active observation for a block; child spans auto-nest.
- **Manual span** — explicit start/end for custom control flow.

These three nest cleanly: a decorator-created span can sit inside a context manager, and manual spans can mix with native integrations ([Langfuse docs](https://langfuse.com/docs/observability/sdk/instrumentation) — confidence H).

**P3 — Single-line init + env-var config.** `Traceloop.init()` or equivalent + `OTEL_EXPORTER_OTLP_*` env vars. Vercel's `@vercel/otel` package reads the standard OTLP env vars and configures the exporter automatically ([SigNoz](https://signoz.io/docs/vercel-ai-sdk-observability/); editorial — confidence M; [Vercel instrumentation docs](https://vercel.com/docs/tracing/instrumentation); vendor primary — confidence H). The DX bar matches the general SDK ergonomics rule that "the 90% case should require zero configuration" — observed across the LLM-telemetry SDKs as much as across general-purpose APIs.

**P4 — CHI EA '25 design principles for LLM observability.** Chen, Li et al. ran focus groups (n=10 across three groups) with developers at varying proficiency, plus a designer rating survey, and surfaced four design principles: **Awareness, Monitoring, Intervention, Operability** ([Chen, Li et al., "Design Principles and Guidelines for LLM Observability," CHI EA '25](https://dl.acm.org/doi/10.1145/3706599.3719914); peer-reviewed — confidence H for the principles being published, M for the specific applicability claims since the full paper body was not directly accessible).
- *Awareness* — make model behavior visible so developers understand what is happening inside the system.
- *Monitoring* — real-time feedback during training and evaluation to catch issues early.
- *Intervention* — let developers act on problems as they surface, not after the fact.
- *Operability* — support long-term maintainability as models and requirements evolve.

The paper names DX dimensions impacted by these principles: **mental models, efficiency, visualization, understandability**.

**P5 — Treat prompts as versioned artifacts.** Multiple practitioner sources converge: prompt templates are the primary lever for behavior change, so treating them as first-class observables lets teams correlate prompt changes with latency, cost, and eval metrics ([Comet](https://www.comet.com/site/blog/llm-observability/), [LaunchDarkly](https://launchdarkly.com/blog/llm-observability/), [TokenMix](https://tokenmix.ai/blog/llm-observability-2026-tools-best-practices); editorial — industry consensus, confidence M).

**P6 — OTel semantic conventions as the SDK schema substrate.** Adopting OTel GenAI attribute names (`gen_ai.*`) lets the SDK output flow into any compliant backend without translation ([OpenTelemetry blog, "AI Agent Observability"](https://opentelemetry.io/blog/2025/ai-agent-observability/); institutional primary — confidence H). Langfuse v3 rebuilt its SDK around OTel for this reason ([Langfuse v3 OTel rebuild](https://langfuse.com/integrations/frameworks/vercel-ai-sdk); vendor primary on their own architecture — confidence H).

### 4.2 UX patterns

**P7 — Waterfall trace view of nested spans.** Each agent run renders as a nested timeline; each node a span; click into any span to inspect input, output, latency, token count, error status. This is universal across LangSmith, Langfuse, Arize Phoenix, Helicone, Datadog LLM Observability, and Honeycomb LLM Observability ([Groundcover AI Agent Observability Guide](https://www.groundcover.com/learn/observability/ai-agent-observability); [DigitalApplied 2026 comparison](https://www.digitalapplied.com/blog/agent-observability-platforms-langsmith-langfuse-arize-2026); editorial — confidence H for the pattern's universality).

**P8 — Connect tracing, evaluation, and alerting into a single feedback loop.** LLM observability is only useful if traces enter the development and alerting workflow; Braintrust, LangSmith, and Arize all explicitly architect for this loop ([Braintrust comparison](https://www.braintrust.dev/articles/best-llm-evaluation-tools-integrations-2025); vendor-aligned on Braintrust's own positioning — confidence M; [Inference.net eval tools comparison](https://inference.net/content/llm-evaluation-tools-comparison/); editorial — confidence M). The pattern: production traces feed eval datasets, eval failures gate deployments, eval scores tie back to specific spans.

**P9 — Eval-as-CI vs eval-as-platform split.** Two distinct UX surfaces have emerged. Lightweight CI gating frameworks (DeepEval, RAGAS, Promptfoo) use pytest-style or YAML-style assertions for offline regression detection. Platforms (Braintrust, LangSmith, Arize) handle human annotation, regression tracking, dashboards ([Inference.net](https://inference.net/content/llm-evaluation-tools-comparison/); [Braintrust DeepEval alternatives](https://www.braintrust.dev/articles/deepeval-alternatives-2026); editorial — confidence M). Many teams pair one of each. DeepEval explicitly models itself on pytest — Python test cases with typed metric objects ([DeepEval GitHub](https://github.com/confident-ai/deepeval); vendor primary — confidence H).

**P10 — Replayable traces for debugging.** Production traces should be replayable in a debug mode without re-running against production systems ([Nordic APIs "10 Tips for Improving Agentic Experience," tip 9](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/); editorial — confidence M). LangSmith's "replay-against-new-models" surface is the canonical instantiation ([DigitalApplied 2026 comparison](https://www.digitalapplied.com/blog/agent-observability-platforms-langsmith-langfuse-arize-2026); editorial — confidence M).

### 4.3 AX patterns (novel angle)

These patterns matter because agents read SDK output, agents call SDK methods, and downstream agents reconstruct what upstream agents did from trace data.

**P11 — Machine-readable errors with stable codes and actionable guidance.** Error messages should carry stable error codes (not free-text strings that drift), specific descriptions of the failure mode, and an action the caller (human or agent) can take ([WorkOS](https://workos.com/blog/agent-experience-oujuh) — confidence M; [Nordic APIs tip 7](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/) — confidence M). Stripe's API is the canonical reference outside the AI space: error responses include a `code`, a human description, a `request_id`, and a doc link ([Stripe advanced error handling](https://docs.stripe.com/error-low-level); vendor primary on their own contract, seminal in API DX — confidence H). The pattern translates directly to telemetry SDK error output: if an agent's instrumentation call fails (invalid span attributes, transport error), the error must be parseable by the calling agent for recovery, not just renderable to a human.

**P12 — Idempotency keys for retries.** Agents retry aggressively at machine speed; any state-changing SDK operation (eval run submission, span export with at-least-once semantics, dataset upload) must accept an idempotency key ([Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests); vendor primary, seminal — confidence H; [WorkOS](https://workos.com/blog/agent-experience-oujuh) — confidence M for applicability to AX). Stripe's client libraries auto-generate idempotency keys and retry with exponential backoff plus jitter ([Stripe idempotency blog](https://stripe.com/blog/idempotency); vendor primary — confidence H).

**P13 — Publish a complete machine-readable interface contract.** OpenAPI spec for HTTP surfaces, GraphQL schema, or MCP tool descriptions. Most LLM agents can consume an OpenAPI spec directly to call APIs without additional prompting ([WorkOS](https://workos.com/blog/agent-experience-oujuh) — confidence M). For telemetry SDKs specifically, the OTel GenAI semantic conventions *are* the machine-readable contract for what attributes mean ([OpenTelemetry semconv specs](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/) — confidence H).

**P14 — Surface operational characteristics and limits as discoverable metadata.** Publish expected latencies, rate limits, costs, idempotency guarantees, and common error codes so agents can plan rather than fail-and-retry ([Nordic APIs tip 7](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/) — confidence M).

**P15 — Structured output over free-text for SDK responses.** When the SDK returns information to an agent (e.g., the result of an eval run, a query for trace data, a feedback handle), the response should be structured (JSON, Pydantic schema, typed tool-result) rather than narrative text ([WorkOS](https://workos.com/blog/agent-experience-oujuh); [Agenta structured outputs guide](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms); editorial — confidence M).

**P16 — Tool-error feedback shaped for LLM recovery.** When tool execution fails and an agent will retry, the error message back to the LLM should clearly indicate *which input parameter was problematic and why*, in a format the LLM has been trained to parse ([apxml LangChain error handling](https://apxml.com/courses/langchain-production-llm/chapter-2-sophisticated-agents-tools/agent-error-handling); editorial — confidence M). This is a telemetry concern because tool-call spans capture exactly this exchange, and the *shape* of the error stored in the span attribute determines whether a downstream replay or eval can simulate the recovery path.

**P17 — The "golden triangle" / multi-perspective SDK architecture.** Microsoft's Agent Framework explicitly architects three top-level surfaces: a developer-facing debug UI (DevUI), an agent-user interaction protocol (AG-UI), and OpenTelemetry observability — with OTel positioned as cross-cutting infrastructure rather than a vertex ([Microsoft Agent Framework "Golden Triangle"](https://devblogs.microsoft.com/agent-framework/the-golden-triangle-of-agentic-development-with-microsoft-agent-framework-ag-ui-devui-opentelemetry-deep-dive/); vendor primary on their own architecture — confidence H for the architecture, M for the broader principle). AWS Strands SDK takes a similar shape: built-in OTel instrumentation hooks, agent trajectory recording (model calls + tool calls) emitted as OTel spans ([AWS Strands SDK deep dive](https://aws.amazon.com/blogs/machine-learning/strands-agents-sdk-a-technical-deep-dive-into-agent-architectures-and-observability/); vendor primary — confidence H).

### 4.4 Cross-cutting: PII redaction at the telemetry boundary

**P18 — Telemetry is the highest-leverage PII exposure point in an AI system.** Logs, traces, and error reports tend to capture raw prompts and responses; they are retained longer and read by more people than the inference path itself. **Observability systems account for 25–40% of all discovered PII exposure in documented post-incident reviews**, even when the inference path is well-redacted ([IJC, "Safe Observability: A Framework for Automated PII Redaction from LLM Prompts in OpenTelemetry Pipelines"](https://ijcjournal.org/InternationalJournalOfComputer/article/view/2458); peer-reviewed — confidence H for the figure as stated in that paper; M for it being a stable industry-wide finding given a single source).

**P19 — Redaction at the SDK layer has measurable cost.** Co-locating NER on LLM GPUs cuts generation throughput 8–15% under peak load; moving NER to a dedicated tier restores LLM throughput at the cost of ~3–8 ms network hop, and improves NER utilization 30–50%. Distilled INT8-quantized NER cuts redaction compute 40–60% for a 1–2 point recall loss ([IJC, "Safe Observability"](https://ijcjournal.org/InternationalJournalOfComputer/article/view/2458); peer-reviewed — confidence H for the figures as reported, M for generalizability). Token inflation from redaction placeholders can also degrade answer quality and skew eval metrics ([IJC, "Safe Observability"](https://ijcjournal.org/InternationalJournalOfComputer/article/view/2458) — confidence M).

**Implication for SDK design:** the redaction toggle should be an SDK-level concern (`record_content=true|false`, plus a redaction plugin slot), not a downstream-collector concern, because raw spans are already exposed to telemetry-tier readers by the time they leave the SDK process.

### 4.5 Cross-cutting: multi-agent and workflow correlation

**P20 — Trace context propagation across agent boundaries.** When one agent calls another or invokes a tool, the trace context must propagate so the multi-agent workflow renders as a single causal tree. AG2's OTel integration captures every conversation, agent turn, LLM call, tool execution, and speaker selection as a structured span connected by a shared trace ID ([AG2 OpenTelemetry tracing](https://docs.ag2.ai/latest/docs/blog/2026/02/08/AG2-OpenTelemetry-Tracing/); vendor primary on AG2's own implementation — confidence H). `gen_ai.conversation.id` is the OTel-canonical correlation attribute for session state ([OpenTelemetry agent spans spec](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/) — confidence H).

## 5. Key debates and open questions

### 5.1 Auto-instrumentation vs explicit instrumentation

*Empirical disagreement.* Auto-instrumentation wins on time-to-first-trace (single-line setup, broad coverage), but captures generic spans that may miss application-specific signals; explicit instrumentation captures internal variables, control flow, and intermediate states that auto-instrumentation can't see ([TokenMix 2026](https://tokenmix.ai/blog/llm-observability-2026-tools-best-practices); editorial — confidence M). The pragmatic answer most SDKs ship is *both*: auto-instrumentation for the 90% case, plus interoperable decorator/context-manager/manual primitives for the 10%.

### 5.2 OTel substrate vs proprietary SDK protocol

*Interpretive disagreement.* Langfuse v3 explicitly rebuilt around OTel ([Langfuse](https://langfuse.com/integrations/frameworks/vercel-ai-sdk) — confidence H). LangSmith historically uses a proprietary protocol optimized for LangChain trace depth (node-by-node state diffs, full agent graphs) ([DigitalApplied 2026](https://www.digitalapplied.com/blog/agent-observability-platforms-langsmith-langfuse-arize-2026); editorial — confidence M). The bet is whether proprietary fidelity is worth lock-in cost; the trajectory of the GenAI SIG output suggests OTel will close the fidelity gap. Open question: do agent-framework-specific extensions (LangGraph state diffs, CrewAI role models) sit inside OTel via vendor-specific attributes, or outside it via parallel surfaces? OTel's own guidance is that vendor-specific extensions are acceptable so long as the common AI-agent semantic convention is also adopted ([OpenTelemetry, "AI Agent Observability"](https://opentelemetry.io/blog/2025/ai-agent-observability/) — confidence H).

### 5.3 Where AX fits relative to DX

*Open question.* No consensus on whether AX is a sub-discipline of DX (because agents-as-callers extend the developer-as-caller story) or a distinct design surface (because agents lack tooltips, can't recover gracefully from ambiguity, and retry at machine speed). WorkOS and Nordic APIs treat AX as distinct; Confucius Code Agent reportedly treats AX, UX, DX as a three-axis philosophy ([Confucius Code Agent arXiv:2512.10398](https://arxiv.org/pdf/2512.10398); preprint — confidence L since the three-axis philosophy was *attributed* in a search snippet but not located in the PDF body during fetch). The CHI EA '25 paper covers DX without naming AX as separate ([Chen, Li et al.](https://dl.acm.org/doi/10.1145/3706599.3719914) — confidence M). For SDK design today, treating AX as first-class is a forward-looking call; treating it as a subset of DX is the conservative call.

### 5.4 Inline content capture vs reference-by-ID

*Open question.* OTel v1.37 reworked chat history capture from per-message events to aggregated `gen_ai.input.messages` and `gen_ai.output.messages` attributes ([OpenTelemetry, 2026](https://opentelemetry.io/blog/2026/genai-observability/) — confidence H), but this puts potentially-large prompt/response bodies inline on the span. The unresolved trade-off: inline content makes traces self-contained (good for replay, eval, audit) but bloats span size and increases the PII surface. The redaction question (§4.4) is downstream of this.

## 6. Implications

**Sourced implications** (directly stated by cited sources):

- **Adopt OTel GenAI semantic conventions as the schema.** Direct guidance from the OpenTelemetry GenAI SIG ([OpenTelemetry, "AI Agent Observability"](https://opentelemetry.io/blog/2025/ai-agent-observability/) — confidence H). Without it, your output won't flow into agent-framework-aware backends without translation.
- **Make every state-changing SDK operation accept an idempotency key.** Stripe's pattern, lifted to AX context: agents retry at machine speed, and any operation that creates an artifact (an eval run, an annotated trace, a labeled dataset row) must be safe to retry ([Stripe](https://docs.stripe.com/api/idempotent_requests) — confidence H).
- **Make every load-bearing error message machine-readable.** Stable code + parameter-specific description + recovery hint ([WorkOS](https://workos.com/blog/agent-experience-oujuh), [Stripe](https://docs.stripe.com/error-low-level) — confidence M from WorkOS, H from Stripe).
- **Build redaction into the SDK, not downstream.** Telemetry pipelines are the dominant PII exposure surface ([IJC](https://ijcjournal.org/InternationalJournalOfComputer/article/view/2458) — confidence H for the empirical claim, M for the SDK-vs-collector choice as a follow-on).

**Inferred implications** (synthesis across sources):

- **Treat the SDK as a triadic API: human-callable, agent-callable, agent-readable** — inferred from WorkOS (AX vs DX), Nordic APIs (AX tips), and CHI EA '25 (DX principles). No single source articulates the triad as an SDK-design rule, but it follows from combining them.
- **Couple eval and production telemetry through shared span schema rather than separate SDKs.** Inferred from the convergence of OTel substrate adoption across both surfaces (production: Vercel, Traceloop; eval: Braintrust connects scoring with tracing in a single system per [Braintrust comparison](https://www.braintrust.dev/articles/best-llm-evaluation-tools-integrations-2025) — confidence M). Splitting eval-SDK and prod-SDK forces double-instrumentation and breaks replay-from-prod.
- **Default to structured-output return types from telemetry SDK methods** that agents may call (e.g., `client.evals.run()` returning a typed result, not a print-string). Inferred from WorkOS structured-data principle plus the observation that telemetry SDKs are increasingly called by agents during self-evaluation or self-monitoring loops.

## 7. Sources

Annotated bibliography. Entries are grouped by source class; within each, recency / primacy / vetting markers follow [`source-triage.md`](../../) terminology.

### Standards bodies and institutional

1. **OpenTelemetry GenAI Agent Spans Specification.** [opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/). Primary, institutional, fresh. Defines the canonical attribute schema for agent telemetry; load-bearing for §3.3 and §4.5.
2. **OpenTelemetry GenAI Client Spans Specification.** [opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/). Primary, institutional, fresh. LLM-call (non-agent) span attribute schema.
3. **OpenTelemetry blog, "AI Agent Observability — Evolving Standards and Best Practices,"** 2025. [opentelemetry.io/blog/2025/ai-agent-observability/](https://opentelemetry.io/blog/2025/ai-agent-observability/). Primary, institutional, recent. SIG guidance on baked-in vs external instrumentation and adoption of the common semconv.
4. **OpenTelemetry blog, "Inside the LLM Call: GenAI Observability with OpenTelemetry,"** 2026. [opentelemetry.io/blog/2026/genai-observability/](https://opentelemetry.io/blog/2026/genai-observability/). Primary, institutional, fresh. v1.37 chat-history rework, current state of attributes.

### Peer-reviewed academic

5. **Chen, Li et al., "Design Principles and Guidelines for LLM Observability: Insights from Developers,"** Extended Abstracts of CHI '25. [doi.org/10.1145/3706599.3719914](https://dl.acm.org/doi/10.1145/3706599.3719914). Primary, peer-reviewed, fresh. Source for the Awareness / Monitoring / Intervention / Operability principles and the DX dimensions in §4.1. Full body not directly retrieved (paywall returned 403); cited at the level of published abstract content and the SIGCHI program entry.
6. **"Safe Observability: A Framework for Automated PII Redaction from LLM Prompts in OpenTelemetry Pipelines,"** *International Journal of Computer*. [ijcjournal.org/InternationalJournalOfComputer/article/view/2458](https://ijcjournal.org/InternationalJournalOfComputer/article/view/2458). Primary, peer-reviewed, fresh. Source for the 25–40% PII exposure figure and redaction-tier cost numbers in §4.4.

### Preprint / arXiv

7. **"AgentTrace: A Structured Logging Framework for Agent System Observability."** [arxiv.org/html/2602.10133v1](https://arxiv.org/html/2602.10133v1). Preprint, recent. Referenced but not the load-bearing source for any single claim in this report; provides context for §4.5.
8. **"Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases,"** arXiv 2512.10398. [arxiv.org/pdf/2512.10398](https://arxiv.org/pdf/2512.10398). Preprint, fresh. Attributed in search results as articulating an AX/UX/DX three-axis philosophy; the specific framework was not located in the body of the PDF during fetch (see §5.3 — confidence L).

### Vendor primary (own architecture / SDK contract)

9. **Vercel AI SDK Core: Telemetry docs.** [ai-sdk.dev/docs/ai-sdk-core/telemetry](https://ai-sdk.dev/docs/ai-sdk-core/telemetry). Vendor primary, fresh. `experimental_telemetry`, custom tracer config.
10. **Vercel Instrumentation docs (`@vercel/otel`).** [vercel.com/docs/tracing/instrumentation](https://vercel.com/docs/tracing/instrumentation). Vendor primary, fresh.
11. **Traceloop OpenLLMetry docs.** [traceloop.com/docs/openllmetry/introduction](https://www.traceloop.com/docs/openllmetry/introduction). Vendor primary, fresh. Auto-instrumentation coverage.
12. **Traceloop OpenLLMetry GitHub.** [github.com/traceloop/openllmetry](https://github.com/traceloop/openllmetry). Vendor primary, fresh.
13. **Langfuse instrumentation docs.** [langfuse.com/docs/observability/sdk/instrumentation](https://langfuse.com/docs/observability/sdk/instrumentation). Vendor primary, fresh. Decorator + context manager + manual span interoperability.
14. **Langfuse Vercel AI SDK integration.** [langfuse.com/integrations/frameworks/vercel-ai-sdk](https://langfuse.com/integrations/frameworks/vercel-ai-sdk). Vendor primary, fresh. Source for Langfuse v3 OTel rebuild.
15. **Datadog LLM Observability SDK Reference.** [docs.datadoghq.com/llm_observability/instrumentation/sdk/](https://docs.datadoghq.com/llm_observability/instrumentation/sdk/). Vendor primary, fresh.
16. **Datadog blog, "LLM Observability natively supports OpenTelemetry GenAI Semantic Conventions."** [datadoghq.com/blog/llm-otel-semantic-convention/](https://www.datadoghq.com/blog/llm-otel-semantic-convention/). Vendor primary, fresh. Adoption evidence.
17. **Microsoft Agent Framework, "The Golden Triangle of Agentic Development."** [devblogs.microsoft.com/agent-framework/the-golden-triangle-of-agentic-development-with-microsoft-agent-framework-ag-ui-devui-opentelemetry-deep-dive/](https://devblogs.microsoft.com/agent-framework/the-golden-triangle-of-agentic-development-with-microsoft-agent-framework-ag-ui-devui-opentelemetry-deep-dive/). Vendor primary, fresh. Architecture pattern in §4.3 P17.
18. **AWS, "Strands Agents SDK: A technical deep dive into agent architectures and observability."** [aws.amazon.com/blogs/machine-learning/strands-agents-sdk-a-technical-deep-dive-into-agent-architectures-and-observability/](https://aws.amazon.com/blogs/machine-learning/strands-agents-sdk-a-technical-deep-dive-into-agent-architectures-and-observability/). Vendor primary, fresh.
19. **AG2 OpenTelemetry Tracing blog.** [docs.ag2.ai/latest/docs/blog/2026/02/08/AG2-OpenTelemetry-Tracing/](https://docs.ag2.ai/latest/docs/blog/2026/02/08/AG2-OpenTelemetry-Tracing/). Vendor primary, fresh. Multi-agent trace correlation example.
20. **Stripe API idempotent requests reference.** [docs.stripe.com/api/idempotent_requests](https://docs.stripe.com/api/idempotent_requests). Vendor primary, dated but seminal in API DX.
21. **Stripe blog, "Designing robust and predictable APIs with idempotency."** [stripe.com/blog/idempotency](https://stripe.com/blog/idempotency). Vendor primary, dated but seminal.
22. **Stripe advanced error handling docs.** [docs.stripe.com/error-low-level](https://docs.stripe.com/error-low-level). Vendor primary, dated but seminal in machine-readable error design.
23. **DeepEval GitHub.** [github.com/confident-ai/deepeval](https://github.com/confident-ai/deepeval). Vendor primary, fresh.
24. **Confident AI LLM Tracing Quickstart.** [confident-ai.com/docs/llm-tracing/quickstart](https://www.confident-ai.com/docs/llm-tracing/quickstart). Vendor primary, fresh.

### Expert practitioner / editorial

25. **WorkOS, "Agent Experience: How to design products that agents can actually use."** [workos.com/blog/agent-experience-oujuh](https://workos.com/blog/agent-experience-oujuh). Editorial / practitioner, fresh. Load-bearing for §3.1 and the AX patterns in §4.3.
26. **Nordic APIs, "10 Tips for Improving Agentic Experience (AX)."** [nordicapis.com/10-tips-for-improving-agentic-experience-ax/](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/). Editorial, fresh. Source for tips 3, 7, 9 cited in §4.3 P14 and §4.2 P10.
27. **DigitalApplied, "Agent Observability: LangSmith, Langfuse, Arize 2026."** [digitalapplied.com/blog/agent-observability-platforms-langsmith-langfuse-arize-2026](https://www.digitalapplied.com/blog/agent-observability-platforms-langsmith-langfuse-arize-2026). Editorial comparison, fresh.
28. **TokenMix, "LLM Observability in 2026: Tools & Best Practices Compared."** [tokenmix.ai/blog/llm-observability-2026-tools-best-practices](https://tokenmix.ai/blog/llm-observability-2026-tools-best-practices). Editorial, fresh.
29. **Inference.net, "LLM Evaluation Tools: The Complete Comparison Guide (2026)."** [inference.net/content/llm-evaluation-tools-comparison/](https://inference.net/content/llm-evaluation-tools-comparison/). Editorial, fresh.
30. **Braintrust, "Best LLM evaluation tools with SDK integrations (2026)."** [braintrust.dev/articles/best-llm-evaluation-tools-integrations-2025](https://www.braintrust.dev/articles/best-llm-evaluation-tools-integrations-2025). Vendor-aligned editorial, fresh.
31. **Groundcover, "AI Agent Observability Guide: Telemetry, Traces, Metrics, and Evals."** [groundcover.com/learn/observability/ai-agent-observability](https://www.groundcover.com/learn/observability/ai-agent-observability). Vendor-aligned editorial, fresh.
32. **Comet, "What is LLM Observability? The Ultimate Guide for AI Developers."** [comet.com/site/blog/llm-observability/](https://www.comet.com/site/blog/llm-observability/). Vendor-aligned editorial, fresh.
33. **LaunchDarkly, "LLM Observability: Tutorial & Best Practices."** [launchdarkly.com/blog/llm-observability/](https://launchdarkly.com/blog/llm-observability/). Vendor-aligned editorial, fresh.
34. **apxml, "Handling Tool Errors and Agent Recovery."** [apxml.com/courses/langchain-production-llm/chapter-2-sophisticated-agents-tools/agent-error-handling](https://apxml.com/courses/langchain-production-llm/chapter-2-sophisticated-agents-tools/agent-error-handling). Editorial, fresh.
35. **Agenta, "The guide to structured outputs and function calling with LLMs."** [agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms). Editorial, fresh.
36. **SigNoz, "Vercel AI SDK Observability & Monitoring with OpenTelemetry."** [signoz.io/docs/vercel-ai-sdk-observability/](https://signoz.io/docs/vercel-ai-sdk-observability/). Vendor-aligned editorial, fresh.

## 8. Limitations

**Coverage gaps.**
- **Quantitative outcome studies.** No empirical study of *whether* adopting any of these patterns measurably improves agent task success, developer time-to-first-trace, or downstream eval reliability. The CHI EA '25 paper is the only peer-reviewed source on developer-side perceptions, and the IJC PII paper is the only peer-reviewed source on the redaction-cost trade-off. Everything else is institutional or editorial.
- **Cross-language SDK shape.** The decorator / context-manager / manual-span pattern is documented strongly in Python; less material on whether the same primitives transfer cleanly to TypeScript, Go, or Rust SDK ergonomics. The Langfuse TS SDK and the Vercel AI SDK (TS-native) are the strongest TS data points; that's thin.
- **MCP-specific telemetry.** Mentioned in passing in Greptime's coverage of MCP tools, but no deep treatment of how MCP tool calls correlate with OTel spans was found.
- **Cost-of-telemetry studies.** Apart from the PII redaction cost data, no comprehensive measurement of SDK overhead (latency, throughput) across the leading platforms.

**Source-type gaps.**
- Heavy reliance on vendor primary sources and editorial / practitioner posts. Only two peer-reviewed sources directly relevant (Chen et al. on observability DX, IJC on PII redaction).
- No standards-body sources outside OpenTelemetry — no IEEE / ISO / NIST coverage of AI telemetry.

**Confidence floor.** The lowest-confidence claims:
- The "Confucius three-axis philosophy" (§5.3) — attribution from a search snippet; not located in the PDF body. Treat as L.
- "Treating AX as first-class is forward-looking; treating it as a subset of DX is conservative" — synthesis, not stated by any source.
- The specific applicability of CHI EA '25 principles to telemetry-SDK design — the paper covers LLM observability broadly; the projection to SDK-design-as-product is inferred.

**What would change this report.**
- A controlled study comparing developer productivity or agent task success rates across SDKs with vs without auto-instrumentation, idempotent retries, or structured errors.
- A stable (post-Development-status) release of the OTel GenAI semantic conventions — would resolve §5.4 and harden §3.3.
- Industry-wide post-incident data on PII exposure attributable to telemetry vs other surfaces, to corroborate the 25–40% figure.
- A peer-reviewed treatment of "agent experience" as a design discipline that's distinct from DX — would resolve §5.3.

---

*Generated using the topic-research skill (`survey` depth, Autopilot mode). Methodology grounded in the sources listed in `skill.json.inspired_by`.*
