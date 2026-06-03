# AI-SDK Playbook

## Scope

Client libraries that call LLM endpoints and/or orchestrate multi-step
agentic workflows: streaming, tool use, structured output, validation
retries, agent loops with stop conditions, handoffs, guardrails,
tracing, batch submodules, MCP transport, opaque reasoning artifacts,
and provider-agnostic dispatch. Distinct from the underlying HTTP/RPC
client layer (which an AI SDK *inherits* unchanged) and from `agent.md`
(sibling — making your repo readable by coding agents). For
retry/streaming/auth primitives, typed exception design, and tracing
exporters, see `dx-audit` / `dx-design` (`sdk`, `errors`,
`telemetry`).

## Grounding

- **API client SDK patterns inherit unchanged.** A well-designed AI SDK
  is a superset of a well-designed HTTP client SDK: typed error
  hierarchy, full-jitter backoff with retry budgets, streaming
  iterators, webhook signature verification, sensible defaults. The
  unique surface area is what *additionally* falls on the SDK because
  the call is stochastic, multi-step, and emits typed artifacts the
  caller must round-trip.
- **Stochastic systems require observability in the SDK, not above
  it.** A multi-step agent loop needs tracing spans per step (LLM
  call, tool call, guardrail, handoff) wired in by default — turning
  tracing on at the application layer happens too late to capture
  what the SDK already executed.
- **Schema-first beats string-first.** Structured-output APIs accept a
  native schema type and validate on the way out; semantic retries on
  validation failure are distinct from transport retries and belong
  in the SDK.

## Good signals

- Per-content-block parameters (cache control, citations) attach to
  individual content blocks rather than the whole request; effects are
  observable in the response (`usage.cache_read_input_tokens`,
  `citations[]` with location and `cited_text`).
- Streaming ships at two altitudes: a raw event iterator
  (`message_start` / `content_block_delta` / `message_stop`) and a
  higher-level accumulator with `.snapshot` / `get_final_message()`.
- Structured outputs accept a native schema and round-trip a typed
  result; `.parse()` (or `generateObject({ schema })`) validates,
  surfaces model refusals as a typed field, and throws a typed error
  with raw text attached on validation failure.
- Validation-error retries are a first-class parameter: schema
  validation failure triggers a semantic retry with the validator
  message appended — distinct from HTTP retries.
- Tools are defined as typed functions with auto-derived JSON schema
  (Zod, Pydantic, or language type hints); no hand-written schemas
  that drift from the signature.
- The agent loop has a declarative stop predicate (`stopWhen:
  stepCountIs(n) | hasToolCall("submit")`), per-step callbacks, and a
  turn cap. Primitive APIs that deliberately do *not* loop document
  the `stop_reason: "tool_use"` contract so callers know loop
  ownership is theirs.
- Sub-agents / handoffs are first-class, exposed via the same
  tool-call surface so one loop handles both.
- Hooks run at agent decision points (`PreToolUse`, `PostToolResult`,
  `OnHandoff`) and short-circuit with structured deny reasons.
- Tracing is on by default: spans per LLM call, tool invocation,
  guardrail, handoff; batch exporter; vendor-plugin API.
- Opaque reasoning artifacts (thinking blocks, reasoning items) are
  typed and round-tripped unchanged across turns — a "must echo"
  category closer to a session cookie than a response field.
- Batch / async-job workloads live in a separate namespace
  (`client.messages.batches`) with the same request body shape as the
  online endpoint; batch is a *resource*, not a flag.
- MCP is a first-class tool source alongside hand-defined functions;
  in-process MCP servers avoid the subprocess requirement.

## Common failures

- Streaming returns raw chunks the caller must reassemble; no typed
  accumulator, no `for event in stream` shape native to the language.
- "Structured output" means "ask the model to emit JSON and hope" —
  no schema validation, no refusal field, no semantic retry on
  parse failure.
- Validation errors trigger an HTTP retry instead of a semantic retry
  with the validator message — the model gets the same prompt back and
  emits the same broken JSON.
- Tool schemas are hand-written JSON next to the function and drift
  out of sync the first time the signature changes.
- The agent loop is buried in the SDK with no stop predicate, no
  per-step callback, and a default turn cap that is either too tight
  to finish real workflows or too loose to bound cost.
- Hooks / guardrails do not exist; the only intervention point is
  "wrap the whole call in a try/except," which catches errors but
  cannot deny a tool *before* it runs.
- Tracing is opt-in and bolted on; downstream teams cannot reconstruct
  what a misbehaving agent did without re-running with `--verbose`.
- Reasoning blocks are discarded by the SDK's serializer; the next
  turn breaks because the continuity signature does not validate.
- Provider-agnostic abstraction lowest-common-denominators away
  prompt caching, citations, and reasoning blocks; the abstraction
  leaks the first time the user needs a provider-specific feature.
- MCP / third-party tools are accepted as a pure capability win — tool
  metadata is trusted as benign, the approval surface shows only the
  tool name (not its real side effects), and credentials live in the
  agent's context where a hostile tool description can exfiltrate them.

## Heuristics

- **Inherit the HTTP-client floor first** *(design, audit)* — apply
  every heuristic in `sdk.md` before adding AI-specific ones. Typed
  errors, jittered retries, streaming iterators, webhook verification
  are not optional just because the body is a `messages[]` array.
- **Streaming at two altitudes** *(design, audit)* — expose the raw
  event iterator *and* a typed accumulator; consumers writing UIs
  paint from the accumulator, consumers writing infrastructure log
  from the events.
- **Schema-typed structured output** *(design, audit, debug)* — accept
  the language's native schema type; round-trip a typed object;
  surface model refusals as a typed field, not a status code.
- **Semantic retry distinct from transport retry** *(design)* —
  `max_retries` for validation failures appends the validator's
  message to the next request; HTTP retries follow the rules in
  `sdk.md`. Conflating them is a design smell.
- **Tool schema from function signature** *(design, audit)* — a `@tool`
  decorator or `tool({ inputSchema })` helper derives the JSON schema
  from the language-native type. Hand-written schemas next to
  functions are a maintenance liability.
- **Declarative stop conditions** *(design, audit)* — if the SDK owns
  the agent loop, expose `stopWhen` predicates, per-step callbacks,
  and a turn cap. If it does not, document the `stop_reason` contract
  so callers know to own the loop.
- **Handoffs as tools** *(design)* — sub-agents are exposed via the
  same tool-call mechanism; one loop handles tools and handoffs alike.
- **Hooks at decision points** *(design, audit)* — `PreToolUse`,
  `PostToolResult`, `OnHandoff` hooks let deterministic code intervene
  inside a stochastic flow. Approval/deny decisions are structured,
  not stringly-typed. This is also the deterministic checkpoint for
  validating untrusted tool metadata and tool responses (injection
  defense), not only loop control.
- **Tracing as a default, OTel GenAI-shaped** *(design, audit)* — emit
  spans per LLM call, tool invocation, guardrail, handoff; batch-export
  via a vendor-plugin API. Attributes follow OTel GenAI semconv:
  `gen_ai.operation.name` (`create_agent` / `invoke_agent` /
  `invoke_workflow`), `gen_ai.usage.{input,output}_tokens`,
  `gen_ai.response.finish_reasons`, `gen_ai.conversation.id` for session
  correlation. Vendor-specific attributes ride alongside canonical ones
  so downstream backends do not need translation.
- **Round-trippable opaque artifacts** *(audit, debug)* — the type
  system has a category for "must echo unchanged"; the serializer
  preserves it; loss of the artifact is a documented failure mode.
- **Batch as a resource, not a flag** *(design)* — non-interactive
  workloads get a separate namespace with the same request body
  shape and a results-streaming interface; SLA is documented.
- **MCP as a tool source — with a trust boundary** *(design, audit)* —
  if the SDK accepts tools, MCP servers are one of the accepted shapes;
  in-process MCP is supported so custom tools do not require a
  subprocess. But accepting third-party MCP/tools makes the SDK an
  injection and credential surface: a server's model-visible tool
  name/description/schema reaches the model before any human sees it
  (tool-description injection). Validate/pin tool metadata, surface real
  side effects at the approval hook (not just the tool name), and isolate
  credentials behind a broker so a compromised tool can't read secrets
  from context.
- **Cross-provider honesty** *(audit)* — provider-agnostic dispatch
  documents where features lowest-common-denominator away; provider
  packages implement a shared model interface; per-provider
  capabilities are discoverable, not implied.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does streaming expose both raw events and a typed accumulator? | UI consumers reassemble chunks; infra logs the wrong altitude | Ship two-tier streaming helpers |
| Does structured output accept a native schema and surface refusals? | Callers parse JSON strings and miss refusal cases | Add `.parse(response_format=…)` with typed refusal field |
| Are validation-error retries distinct from HTTP retries? | Same broken JSON returned N times | Add semantic `max_retries` that appends validator messages |
| Are tool schemas derived from function signatures? | Hand-written schemas drift from code | Add a `@tool` / `tool({ inputSchema })` helper |
| Does the agent loop have declarative stop conditions? | Unbounded cost or premature termination | Expose `stopWhen` + turn cap + per-step callbacks |
| Are guardrails available at decision points? | No way to deny a tool before it runs | Add `PreToolUse` / approval hooks with structured decisions |
| Is tracing on by default with per-step spans? | Misbehaviors are unreproducible | Wire tracing into the loop; expose a vendor-plugin API |
| Are opaque reasoning artifacts round-tripped intact? | Continuity signature breaks on the next turn | Add a typed "must echo" category and preserve it through serde |

## Cross-references

- → `dx-audit` / `dx-design` for the inherited HTTP-client floor
  (`sdk`: retries with jitter, streaming iterators, typed errors, webhook
  verification), typed exception hierarchy (`errors`), tracing exporters
  (`telemetry`), per-provider sub-packages (`package`), and paste-runnable
  snippets (`examples`).
- → `agent.md` (sibling) for the *distinct* surface of making your repo
  readable by coding agents (not to be confused with this playbook).
