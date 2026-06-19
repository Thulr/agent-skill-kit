# Glossary

Terms used across the agent-DX playbooks. Definitions are operational, not exhaustive.

- **Agent-DX** — the developer experience of a surface where an **AI agent is the developer**:
  an SDK, tool, structured output, error envelope, or telemetry an agent consumes to build
  with or act through. The agent-actor analog of human DX.
- **Agent loop** — the multi-step cycle (call model → run tool → feed result back) an SDK
  drives until a stop condition holds.
- **Stop condition** — a declarative predicate (`stopWhen: stepCountIs(n) | hasToolCall(…)`)
  plus a turn cap that bounds the loop; paired with a verification step so "done" is observed.
- **Verify, don't trust** — confirm a loop step's claimed success with a deterministic check
  (tests ran, file written, side effect observed) rather than the model's assertion.
- **Compaction** — compressing the context window on a long run; loop-owned, with the
  compaction point exposed and state externalized so a later step does not silently lose a
  fact ("compaction amnesia").
- **Two-altitude streaming** — exposing both a raw event iterator and a typed accumulator so
  UI and infrastructure consumers each read at the right level.
- **Agent-as-tool vs handoff** — two delegation semantics: agent-as-tool keeps the caller's
  loop (the sub-agent returns a result); explicit handoff transfers control and session state.
- **Tool edge / client edge** — the two standardizable edges of an Agent SDK: the tool edge
  (what the model can call, e.g. MCP) and the client edge (how a host/editor drives the
  session).
- **Typed function tool** — a tool defined as a typed function whose JSON schema is derived
  from the signature, so the contract cannot drift from the code.
- **Structured output** — model output validated against a native schema and returned as a
  typed result, with refusals surfaced as a typed field.
- **Validate-then-repair vs constrained decoding** — the two structured-output guarantee
  levels: catch a bad object *after* generation (repair + semantic retry) vs make illegal
  tokens unreachable *during* generation.
- **Semantic retry vs transport retry** — a semantic retry appends the validation/tool-failure
  detail to the next request (the model corrects); a transport retry is silent backoff on the
  client floor.
- **Agent-readable error envelope** — a typed error with a stable `code`, parameter-specific
  `message`, and `recovery_hint`, stable across minor versions, that an LLM can branch on.
- **Retry-shaped tool feedback** — a failed tool call returned in the same JSON shape the model
  produced, naming the offending input, so the next attempt is informed.
- **Replay-ready capture** — persisting on the tool-call span the exact error the model saw,
  so offline replay and eval reproduce the real recovery path.
- **Retryable discriminator** — a typed field marking each error code/class retryable or
  terminal, so the loop backs off or fails fast without parsing prose.
- **Guardrail / hook** — deterministic code at a loop checkpoint (user input, tool call, tool
  response, final output) that returns a structured approve/deny decision.
- **Tool-description injection** — a hostile tool's model-visible name/description/schema
  reaching the model before any human reviews it; tool metadata is untrusted input.
- **Lethal trifecta** — private data + untrusted content + an exfiltration path; breaking any
  one leg defuses the risk.
- **Credential walls** — process (secret never enters the agent process), container/network
  (not reachable from the tool's reach), and **token exchange** (an RFC 8693-style broker
  mints a short-lived, narrowly-scoped token by policy).
- **Delegated auth** — acting on a user's behalf via a scoped, short-lived exchanged token
  rather than forwarding the user's durable access token into the runtime.
- **Content-capture toggle** — a single boolean (`record_content`) that flips raw
  prompt/response capture without disabling structural telemetry; default off when PII risk is
  unknown.
- **Boundary redaction** — running a pluggable redactor on inputs/outputs at the SDK boundary,
  before any span attribute, rather than at the downstream collector.
- **Structural vs content telemetry** — low-cardinality structural attributes (token counts,
  latencies, finish reasons, tool-call shape) kept on a separate axis from high-cardinality
  raw content and per-request IDs.
- **Inline-vs-reference content** — capturing a prompt/response either inlined with a
  documented size cap or as a typed reference (object key, content hash, dataset row ID).
- **Named convention** — one telemetry attribute convention (OTel GenAI or OpenInference) used
  accurately, with spans it lacks modelled as custom rather than mislabelled.
