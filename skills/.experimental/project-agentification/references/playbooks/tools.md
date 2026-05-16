# tools

## What it is

The tools surface covers every mechanism an agent uses to take structured action: typed
JSON-schema function tools, Semantic Kernel-style plugin wrappers, Model Context Protocol (MCP)
servers, and open-ended sandboxed shell/filesystem tools. MCP exposes three primitives —
**tools** (callable actions), **resources** (data sources), and **prompts** (reusable message
templates) — each with typed `inputSchema` and standard discovery semantics. Anthropic developed
MCP as an open standard (November 2024) and donated it to the Linux Foundation's Agentic AI
Foundation in December 2025, alongside Block's Goose.

## Why it matters for agents

- **Context budget.** Stuffing tool definitions into the system prompt inflated context windows
  to 150,000+ tokens. MCP moves tool defs outside the window; agents "think in code" and call
  MCP APIs. Real-world tests show a 98.7% reduction — from 150,000 to 2,000 tokens. (W6)
- **Hard gates, not prose.** Tool schemas enforce action boundaries AGENTS.md prose cannot. A
  schema that omits a `force` flag makes force-push structurally inexpressible; AGENTS.md says
  "don't" and the agent complies ~70% of the time. (W3)
- **Dynamic discovery at scale.** When N > ~20 tools, agents use `search_tools` rather than
  loading all definitions upfront — the same progressive-disclosure principle as skills. (W6)
- **Sandbox isolation.** Shell/filesystem tools require process or container isolation; absent a
  boundary, model-generated code executes with harness credentials. (W10)

## Heuristics by intent

### assess

- **H1.** Verify that each tool exposes a typed `inputSchema` with required fields, enum
  constraints, and format hints — absent schema means the agent must infer valid inputs from
  description text alone, which is the leading cause of malformed tool calls. (severity cap: 4;
  lens: cold-agent)
- **H2.** Check tool descriptions for both a "when to use" clause and a "when NOT to use" clause
  — a description with only affirmative guidance is an incomplete public API doc; the agent will
  call the tool in the wrong context. (severity cap: 3; lens: maintainer)
- **H3.** Count exposed tools; if N > ~20, confirm a `search_tools` MCP method or equivalent
  catalog endpoint exists — without it, all definitions load into context on every turn. (severity
  cap: 3; lens: auditor)
- **H4.** Audit retry-unsafe error payloads — tools returning plain 429 text force the agent to
  parse the error with an LLM call; tools returning `{ "is_retriable": true,
  "retry_after_seconds": 30 }` enable deterministic recovery. (severity cap: 3; lens: adversarial)
- **H5.** Verify shell or filesystem tools run in a named sandbox (Docker, Firecracker, or harness
  sandbox mode) — "process sandbox on maintainer laptop" is the most common path to credential
  exfiltration. (severity cap: 4; lens: adversarial)
- **H6.** Check that tool specs are version-controlled alongside the application code they wrap —
  schema drift between definition and implementation is the silent failure mode in MCP. (severity
  cap: 3; lens: maintainer)

### harden

- **H1.** Agent calls wrong tool or with invalid inputs → tighten `inputSchema`: replace `string`
  with `enum` where values are finite; add length constraints on free-text fields; use
  `additionalProperties: false` — invalid actions should be structurally inexpressible.
- **H2.** 429 and transient errors cause retry storms → add a structured error envelope to every
  MCP tool response: `{ "error": "...", "is_retriable": true, "retry_after_seconds": 30 }` — the
  agent performs deterministic recovery without an LLM-parsed error message.
- **H3.** Tool discovery overloads the context at N > ~20 → implement `search_tools` as an MCP
  method that accepts a query string and returns matching tool names + short descriptions; expose
  the full `inputSchema` only on subsequent per-tool fetch.
- **H4.** Shell tool exposes unrestricted filesystem or network → wrap in Docker or harness
  sandbox (Claude Code PreToolUse hook exit-code 2; Codex sandbox modes; Copilot MCP allow-list);
  apply path allowlists and egress rules; never mount credentials in the writable workspace.
- **H5.** Tool description generates wrong-context calls → rewrite using public-API-doc pattern:
  what the tool does, preconditions, what it does NOT do (neighboring tools handle those).

### scaffold

- **Do not autogenerate tool schemas or MCP servers from templates without observed usage.**
  LLM-generated context artifacts drop task success ~3% and inflate cost >20% (W1). Each tool
  must address a specific agent action or failure mode — no placeholder tools shipped to
  production.
- **H1.** (W1 guard) Before writing a tool, name the specific agent action or failure it enables
  in a comment in the tool definition file. "Might be useful" is not a valid trigger.
- **H2.** Choose surface tier before writing any code — apply the escalation ladder:
  (1) **JSON-schema function tool** when action is stable and deterministic; (2) **plugin
  wrapper** (Semantic Kernel-style) when exposing existing services; (3) **MCP tool/resource**
  when you need cross-client reuse and `search_tools` discoverability; (4) **sandboxed
  shell/filesystem tool** only for open-ended or legacy-shaped tasks.
- **H3.** Structure each MCP tool with: `name` (verb-noun, e.g. `run_tests`), `description`
  (when to use / when not to use), typed `inputSchema` (`additionalProperties: false`), and a
  structured error envelope. Implement `search_tools` when the server exposes more than 20 tools.
- **H4.** Wire dynamic discovery at agent connect time — agent connects → auto-detects MCP
  servers → queries capabilities + `inputSchema`; do not hardcode tool lists in AGENTS.md.

### diagnose

- **H1.** Agent forms malformed tool calls → rank: (1) `inputSchema` too permissive — uses
  `string` where an `enum` would eliminate invalid values; (2) description has no negative clause
  — agent applies tool in the wrong context; (3) schema not version-controlled — implementation
  diverged silently.
- **H2.** Context window inflates despite MCP → rank: (1) `search_tools` absent — all schemas
  load on connect; (2) tool defs duplicated in AGENTS.md prose — remove prose, trust discovery;
  (3) resources or prompts loaded as always-on vs. on-demand — reclassify to on-demand fetch.
- **H3.** Retry storms on transient errors → rank: (1) error payload is plain text — the agent
  retries immediately without back-off; (2) `is_retriable` field absent — add structured envelope;
  (3) harness-level retry policy conflicts with tool-level retry signals — audit both layers.
- **H4.** Shell tool produces non-deterministic output → rank: (1) missing idempotency keys or
  existence checks before writes; (2) no dry-run mode — add `dry_run: boolean` to `inputSchema`;
  (3) side-effecting adapters not isolated — move to a separate adapter module with explicit
  rollback steps.

## Empirical warnings

- **W1** — Autogenerated tool schemas and MCP servers drop task success ~3% and inflate cost
  >20%; scaffold only from observed agent actions or specific failure modes.
- **W3** — Hard gates (tool schema, harness hook, sandbox policy) enforce action bounds; prose
  in AGENTS.md achieves ~70% compliance — never substitute prose for a structural constraint on
  a high-risk action.
- **W6** — Token budget is the dominant cost driver; MCP + `search_tools` cuts context payloads
  by 98.7% (150,000 → 2,000 tokens); load tool definitions on-demand, not at session start.
- **W10** — Shell and filesystem tools without sandbox isolation expose harness credentials to
  model-generated code; Docker or process sandboxing is a baseline, not an advanced option.

## Canonical examples

- **Anthropic's MCP reference implementations** — canonical `list_tools`, `call_tool`, resource
  fetch, and prompt-template patterns; reference for `inputSchema` shape and error envelopes.
- **steipete/mcp-agentify** — MCP orchestrator that converts MCP servers into sub-agents;
  demonstrates composing tool servers into agent topologies without custom harness code.
- **Wren AI / WrenEngine** — semantic database queries via MCP; demonstrates the dynamic-discovery
  pattern for domain-specific tools (SQL/semantic layer) without loading full schemas upfront.
- **`search_tools` pattern** — when a server exposes N > ~20 tools, `search_tools(query)` returns
  matching tool names + short descriptions; full `inputSchema` fetched per-tool on demand;
  eliminates context bloat at scale.

## Sources

- "Model Context Protocol" — tools / resources / prompts as the three MCP primitives; typed
  `inputSchema`; `list_tools` and `search_tools` discovery semantics; donated to Linux
  Foundation's Agentic AI Foundation (Dec 2025, alongside Block's Goose).
- "Harness Engineering: Leveraging Codex in an Agent-First World" — explicit guidance on MCP
  for sensitive data and composable capabilities; `search_tools` recommendation when N > ~20;
  98.7% token reduction claim (150,000 → 2,000 tokens) from code-execution-with-MCP pattern.
- "Effective Context Engineering for AI Agents" — token-budget framing (W6); on-demand vs.
  always-loaded tool definitions; smallest-high-signal-token principle; dynamic discovery at
  agent connect time.
- "OWASP LLM and Agent Top 10" — prompt injection, tool abuse, privilege escalation, and data
  exfiltration as primary threat model; least-privilege tool surfaces; sandbox isolation baseline;
  approval classes by action type.
