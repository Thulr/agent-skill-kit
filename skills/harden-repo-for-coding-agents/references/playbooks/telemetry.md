# telemetry

## What it is

Telemetry is the control-plane record of what an agent actually did: every model generation, tool
call, handoff, guardrail hit, and custom event, joined into a correlated trace that can be replayed,
audited, and used as input to evaluation. Three complementary shapes:

- **Traces** — OpenAI Agents SDK records model generations, tool calls, handoffs, guardrails, and
  custom events by default; AutoGen exposes the same via OpenTelemetry; OpenHands SDK auto-traces
  agent steps, tool calls, LLM calls, browser sessions, and conversation lifecycle events.
- **Append-only event history** (OpenHands pattern) — immutable, ordered log of every run event;
  doubles as a memory surface and integration surface; downstream consumers replay without
  re-executing.
- **Replayable execution artifacts** — SWE-agent `.traj` JSON trajectories capture the full
  thought/action/observation sequence; Aider's benchmark metadata records repo git hash, model,
  edit format, and settings so any run can be reproduced inside Docker.

OpenTelemetry provides the portable backbone: traces, metrics, and logs correlated via trace context
and resource context. OTel is the *substrate*; the LLM/agent span semantics ride on top as a separate
convention layer — and there are two distinct, separately-governed ones, not a single "GenAI/OpenInference"
vocabulary. **OpenInference** (Arize) is the agent-aware layer many popular frameworks and SDKs ship
instrumentation for today: prompt text, completion text, model name, token counts, tool calls, and explicit
span kinds including `GUARDRAIL` and `EVALUATOR`; many popular frameworks ship an
`openinference-instrumentation-*` package. The **OTel GenAI**
semantic conventions (`gen_ai.*`) are the standards-body track but are still **Development status** (not
frozen). Pick one and emit its names accurately rather than slashing them together. Generic OTel `code.*`
attributes (`code.filepath`, `code.function`, `code.lineno`) describe code location, not model I/O, so
they cannot by themselves answer an eval question about a prompt or completion.

Every trace must carry run metadata: model identifier, prompt hash, tool-schema version, commit SHA,
and environment. Without these, two identical-looking traces may differ in prompt or schema — making
regression detection impossible.

"Documentation tells the agent what to do. Telemetry tells it whether it worked." — Hamel Husain

## Why it matters for agents

- **Auditability across handoffs.** Multi-agent handoffs scatter causality across processes; a
  shared trace context propagated through each handoff is the only artifact that joins the whole
  run into a coherent audit trail. (W4)
- **On-demand, not always-loaded.** Full trace payloads exhaust the token budget if loaded by
  default; expose the tracing system as an MCP server so agents query specific spans on demand. (W6)
- **Self-verification.** The Codex "Harness Engineering" pattern has the agent query distributed
  traces to verify its own output — closing the feedback loop without a human in every iteration.
- **Eval foundation.** Replaying `.traj` files or append-only event histories against a grader is
  more reliable than re-running the live agent because inputs and tool outputs are fixed.
- **Scratchpad continuity.** Notes (`.agents/notes.md`, `docs/specs/<feature>/plan.md`) and
  compaction strategies (Spotify's Honk, HumanLayer's FIC) bridge ephemeral sessions and prevent
  context rot between handoffs.

## Heuristics by intent

### assess

- **H1.** Verify that traces carry model identifier, prompt hash, tool-schema version, commit SHA,
  and environment metadata on every run — missing commit SHA breaks causality between a trace and
  the code that produced it. (severity cap: 4; lens: auditor)
- **H2.** Check handoff boundaries for shared trace context — sub-agent spans that omit
  `traceparent` appear as disconnected roots, hiding causal chains. (severity cap: 4; lens: cold-agent)
- **H3.** Confirm the event log is append-only and immutable — mutability undermines its use as a
  memory surface and makes it inadmissible for audit. (severity cap: 3; lens: auditor)
- **H4.** Verify LLM/agent spans carry an LLM-aware semantic convention (OpenInference, or the OTel
  GenAI `gen_ai.*` conventions) — prompt text, completion text, model name, token counts, and tool
  calls — not just generic OTel `code.*` location attributes; without the LLM-span layer, traces cannot
  fuel trace-to-eval. The link back is the **join**: an eval result should be navigable from the trace
  that produced it (a trace-linked eval-result event on the same trace), not a detached score. Confirm
  traces, logs, and metrics correlate via trace context + resource context. (severity cap: 3; lens: maintainer)
- **H5.** Check whether the tracing system is exposed as an MCP query surface — loading full trace
  payloads into context exhausts the token budget on any non-trivial trajectory. (severity cap: 3;
  lens: cold-agent)
- **H6.** Confirm retention and redaction policies exist — traces capture raw prompts and tool
  arguments; no policy means the first incident is also a data-handling incident. (severity cap: 4;
  lens: adversarial)

### harden

- **H1.** Run metadata missing → instrument at the harness level, not the application level:
  inject model, prompt hash, tool-schema version, commit SHA, and environment as OpenTelemetry
  resource attributes so every span inherits them automatically.
- **H2.** Handoffs break trace continuity → propagate W3C `traceparent` / `tracestate` through
  every handoff call; verify the receiving agent starts a child span, not a new root span.
- **H3.** Traces not queryable by agents → wrap the tracing backend in an MCP server exposing
  `get_trace(trace_id)`, `list_spans(trace_id, filter)`, `get_run_metadata(run_id)`; agents
  call these on demand instead of loading full payloads. (W6)
- **H4.** Replayability absent → persist `.traj`-style JSON for every run: each entry captures
  role (`thought` / `action` / `observation`), timestamp, tool name, raw input, and raw output;
  store alongside commit SHA and model identifier; replay against a grader for regressions.
- **H5.** Secrets or PII in traces → define field-level redaction at the harness exporter; apply
  before write; audit quarterly; use a separate low-retention store for raw prompts.

### scaffold

- **Do not autogenerate instrumentation from templates without a named observability goal (W9).** Generic
  spans with no semantic meaning add noise and cost without enabling diagnosis or eval.
- **H1.** (W9 guard) Before adding a span, name the failure mode or eval question it answers;
  "more observability is better" is not a valid trigger.
- **H2.** Scaffold in three layers: (1) run metadata as OTel resource attributes (model, prompt
  hash, tool-schema version, commit SHA, env); (2) per-step LLM/agent spans using one LLM-aware
  convention — OpenInference or OTel GenAI `gen_ai.*` (prompt, completion, model, token counts, tool
  calls), with `code.*` reserved for
  code-location attributes; (3) replayable artifact export (`.traj` JSON or append-only event log).
  Do not ship layer 3 as a TODO — it is the foundation of offline eval.
- **H3.** Wire the tracing MCP server at harness bootstrap: agent completes a run → queries its
  own trace → checks expected spans are present → reports anomalies before human review.
- **H4.** Add scratchpad surfaces alongside traces: `.agents/notes.md` for cross-session state;
  `docs/specs/<feature>/plan.md` for long-horizon plans; apply FIC (Frequent Intentional
  Compaction) so notes do not grow unbounded.

### diagnose

- **H1.** Cannot reproduce a failure → rank: (1) run metadata incomplete — commit SHA or prompt
  hash missing; (2) no `.traj`-style artifact — only final output logged, steps lost; (3) mutable
  event log — entries modified after the fact.
- **H2.** Multi-agent run appears as disconnected spans → rank: (1) `traceparent` not propagated
  through handoff — receiving agent starts a new root; (2) resource context inconsistent across
  agents; (3) OTel collector not configured for all agent processes.
- **H3.** Agent cannot self-verify → rank: (1) tracing system not exposed as MCP server; (2)
  trace written asynchronously and not flushed before the verification step; (3) span granularity
  too coarse — individual tool calls not recorded as separate spans.
- **H4.** Trace store contains secrets or PII → rank: (1) redaction not applied before write;
  (2) raw prompt captured in span attributes — move to a shorter-retention store; (3) approval log
  captures full env — audit the approval event schema and redact before storage.

## Empirical warnings

- **W4** — Multi-agent handoffs scatter causality across processes; shared trace context is the
  only artifact that makes the full run auditable as a single causal chain.
- **W6** — Full trace payloads exhaust the token budget when always-loaded; expose telemetry as
  an on-demand MCP query surface.
- **W9** — Generic instrumentation without a named observability goal produces noisy, high-cost
  traces; every span should answer a specific failure-mode or eval question.

## Canonical examples

- **SWE-agent `.traj` JSON trajectories** — records the full thought/action/observation sequence
  as structured JSON; replay against a grader produces deterministic eval results without
  re-running the live agent; canonical reference for replayable execution artifacts.
- **Aider benchmark metadata records** — records repo git hash, model, edit format, and settings;
  runs execute inside Docker; makes any run reproducible and cross-run comparison valid. Reference
  for run-metadata discipline.
- **OpenHands append-only event history** — immutable ordered log of agent steps, tool calls, LLM
  calls, browser sessions, and conversation lifecycle; doubles as memory and integration surface.
- **"Agent queries its own traces to self-verify" (Codex Harness Engineering)** — after a run, the
  agent calls the trace system (exposed as MCP) to verify expected spans are present; closes the
  feedback loop without human review on every iteration.

## Sources

- "OpenTelemetry Semantic Conventions" — `code.filepath`, `code.function`, `code.lineno`;
  trace context + resource context as the correlation mechanism; W3C `traceparent` propagation.
- "OpenInference (Arize)" — the agent-aware LLM/agent span layer on top of OTel: prompt, completion,
  model name, token counts, tool-call attributes, and explicit span kinds (incl. `GUARDRAIL`,
  `EVALUATOR`); `openinference-instrumentation-*` packages across many popular frameworks. This is the span
  layer trace-to-eval actually reads — distinct from the OTel GenAI `gen_ai.*` conventions, which are
  the standards-body track and still in Development status.
- "SWE-agent" — `.traj` JSON trajectory format; replayable execution histories for debugging,
  auditing, and evaluation.
- "Harness Engineering: Leveraging Codex in an Agent-First World" — agent self-verification via
  distributed trace queries; tracing system exposed as MCP; Hamel Husain telemetry framing.
- "Effective Context Engineering for AI Agents" — on-demand telemetry (W6); append-only event
  history as memory surface; scratchpad + compaction; W4 multi-agent handoff auditability.
