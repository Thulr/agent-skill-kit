# Activation cases — agent-dx

Natural-language behavioral cases for the surface where an **AI agent is the developer**: the
SDK/tool/structured-output/error/telemetry an agent consumes. Each negative names the sibling
skill it disambiguates from. The agent should activate on realistic agent-DX prompts, ask at
most one blocker question, and route to `<intent>/<surface>`.

## Positive

### P1 — Design an Agent SDK surface
**Prompt:** `Design the public surface of our Agent SDK — the loop, stop conditions, streaming, handoffs.`
**Expected:** activates; intent `design`, surface `sdk-design`; emits a design doc naming the
loop-ownership and stop+verify decisions; names the HTTP-client floor as inherited from
dx-design, not re-specified.

### P2 — Review an MCP tool surface
**Prompt:** `Review our MCP tool surface — are the descriptions and schemas safe for an agent to call?`
**Expected:** activates; intent `review`, surface `tools-and-mcp`; scores the surface; flags
tool-description injection, approval-surface side effects, and credential isolation.

### P3 — Shape retryable tool errors
**Prompt:** `Our agent keeps retrying the same broken tool call — shape the errors so the model can recover.`
**Expected:** activates; intent `do`, surface `errors-and-retry`; recommends a typed envelope
that names the offending input in the produced shape, plus a retryable discriminator.

### P4 — Audit structured output
**Prompt:** `Are our structured outputs validated, or are we asking for JSON and hoping? Review it.`
**Expected:** activates; intent `review`, surface `structured-output`; checks native-schema
validation, typed refusal, and semantic-vs-transport retry.

### P5 — Audit SDK telemetry for PII
**Prompt:** `Is our agent telemetry leaking raw prompts and PII into spans? Audit the instrumentation.`
**Expected:** activates; intent `review`, surface `sdk-telemetry`; checks the content-capture
toggle, boundary redaction, and structural-vs-content axis split.

### P6 — Full agent-DX review (fan-out)
**Prompt:** `Full agent-DX review of our Agent SDK across loop, tools, output, errors, telemetry — score each.`
**Expected:** activates; intent `review`, surface `all`; fans out one agent per surface and
synthesizes a scored report with `AGENT-DX-*` finding IDs.

## Negative

### N1 — Human developer API/SDK
**Prompt:** `Review our public REST API and SDK for human developers — first-call, errors, pagination.`
**Expected:** does not activate; defers to `dx-audit` / `dx-design` (the human HTTP-client
floor agent-dx sits atop).

### N2 — Agent-readable docs
**Prompt:** `Audit our llms.txt and AGENTS.md so coding agents can read our docs.`
**Expected:** does not activate; defers to `agent-docs` (agent-native documentation, not the
SDK/tool contract).

### N3 — Repo agent-hardening
**Prompt:** `Scaffold our repo's AGENTS.md, hooks, and CI gates so Claude Code stops tripping.`
**Expected:** does not activate; defers to `harden-repo-for-coding-agents` (scaffolding and
enforcing repo gates, not designing an SDK).

### N4 — Operating eval/observability loops
**Prompt:** `Set up an eval and optimization loop for our shipped AI product and watch the metrics.`
**Expected:** does not activate; defers to `agent-ops` (operating the loop) / `agent-test`
(designing the evals).

### N5 — Prose / product UX
**Prompt:** `Tighten the prose in this blog post.` / `Review our checkout flow for usability.`
**Expected:** does not activate; defers to `writing-audit` / `ux-audit`.

## Edge / boundary

### E1 — Dual-audience SDK (humans + agents)
**Prompt:** `Our SDK serves both human integrators and an agent loop — review the error envelope for the agent's ability to recover.`
**Expected:** activates on the *agent-consumer* framing; intent `review`, surface
`errors-and-retry`; explicitly notes the human-DX error-copy half belongs to `dx-audit` and
scopes to the machine-branchable contract.

### E2 — Telemetry convention choice
**Prompt:** `Should our agent tracing follow OTel GenAI or OpenInference, and how do we keep structural spans when content capture is off?`
**Expected:** activates; intent `design`, surface `sdk-telemetry`; routes to the named-convention
and structural-vs-content-axis heuristics rather than to `agent-ops` (which operates the
resulting telemetry).
