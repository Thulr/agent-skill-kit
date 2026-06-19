# Tools and MCP Playbook

## Scope

Tools as the hard API boundary an agent calls through: typed function tools,
schema derivation, the four guardrail checkpoints, and MCP as a tool source
with a trust boundary — tool-description injection, the lethal trifecta,
credential isolation, and delegated auth.

- **In:** typed tool definitions, schema-from-signature, hook/guardrail
  placement, MCP registration and trust, injection defense, token exchange.
- **Out:** the agent loop that calls tools (see `sdk-design.md`); the
  structured-output contract a tool *returns* (see `structured-output.md`);
  the error a failed tool call hands back (see `errors-and-retry.md`).
- **Intents this surface answers:** do, review, design.

## Grounding

- **A tool is a public API the model calls without a human in the loop.** Its
  schema, name, and description are the entire contract the model sees, so they
  are held to API-permanence standards, not docstring standards.
- **Accepting third-party tools makes the SDK an injection and credential
  surface.** A server's model-visible tool name/description/schema reaches the
  model before any human sees it (tool-description injection), so tool metadata
  is untrusted input, not configuration.
- **The risk shape is the lethal trifecta** — private data + untrusted content
  + a way to exfiltrate. Breaking any one leg defuses it; the SDK's job is to
  make breaking a leg the default, not an expert option.

## Good signals

- Tools are defined as typed functions with auto-derived JSON schema (Zod,
  Pydantic, language type hints); no hand-written schemas drift from the
  signature.
- Guardrails exist at all four execution points — user input, tool call, tool
  response, and final output — with structured (not stringly-typed) approve/deny
  decisions.
- The approval surface shows a tool's real side effects, not just its name, so
  a human (or a policy) sees what `delete_account` actually does before it runs.
- Untrusted tool metadata and tool responses are validated deterministically at
  the hook boundary as injection defense, not only for loop control.
- MCP is a first-class tool source alongside hand-defined functions; in-process
  MCP servers avoid the subprocess requirement.
- Tool metadata is scanned and pinned *before registration*; a description
  change is re-reviewed, not silently trusted.
- Credentials never enter the agent's context: secrets are isolated by process,
  by network/container reach, and by token exchange.
- When the agent acts for a user, it uses delegated, short-lived, narrowly
  scoped credentials minted at a broker — not the user's forwarded raw token.

## Common failures

- Tool schemas are hand-written JSON next to the function and drift out of sync
  the first time the signature changes.
- The only intervention point is wrapping the whole call in `try/except`, which
  catches errors but cannot deny a tool *before* it runs.
- Guardrails cover only the model's final output (or only user input); the
  tool-call and tool-response checkpoints are unguarded.
- MCP/third-party tools are accepted as a pure capability win: metadata is
  trusted as benign, the approval surface shows only the tool name, and
  credentials sit in the agent's context where a hostile description can
  exfiltrate them.
- The agent holds the user's durable access token, so a single prompt injection
  reaches every system that token can reach.
- A broker/env-var indirection is treated as a hard guarantee when no real
  enforcement primitive backs it.

## Heuristics

- **(design, review) Derive tool schemas from the function signature.** A
  `@tool` decorator or `tool({ inputSchema })` helper generates the JSON schema
  from the language-native type; hand-written schemas next to functions are a
  maintenance liability that drifts silently.
- **(design, review) Guard all four checkpoints.** Hooks belong at user input,
  tool call, tool response, and final output. Output-only or input-only
  guardrails are an anti-pattern; minimum production coverage checks both the
  user input and the model's final output, with structured decisions.
- **(do, review) Treat tool metadata as untrusted input.** Scan and pin a tool's
  name/description/schema before registration; validate arguments
  deterministically; re-review on change. The description reaches the model
  before any human — it is an injection vector, not config.
- **(design, review) Surface real side effects at the approval hook.** The
  approval prompt names what the tool *does*, not just what it is called, so the
  human or policy gate is deciding on consequence, not label.
- **(design) Break a leg of the lethal trifecta by default.** Private data +
  untrusted content + exfiltration path is the danger; design so at least one
  leg is absent by default (e.g., no durable secret in context, no open egress
  from tool reach).
- **(design, review) Isolate credentials behind three walls.** Process (the
  secret never enters the agent process), container/network (not reachable from
  the tool's reach), and token exchange (an RFC 8693-style exchange mints a
  token constrained by resource/audience/scope and short TTL by policy). Treat a
  proxy/env-var broker as defense-in-depth, not a guarantee, unless a real
  enforcement primitive backs it.
- **(design, review) Delegate auth, don't borrow secrets.** When the agent acts
  on a user's behalf, identify the subject, call downstream on that subject's
  behalf, gate sensitive actions on human confirmation, and exchange the user's
  token for a short-lived narrowly-scoped one at a broker — never forward the
  raw access token into the runtime.
- **(design) Make MCP a tool source, with the boundary attached.** Accept MCP
  servers as one tool shape (in-process supported), but ship the trust boundary
  in the same surface — registration-time scanning, argument validation, and
  the credential walls — so adopting MCP is not adopting an exfiltration path.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are tool schemas derived from function signatures? | Hand-written schemas drift | Add a `@tool` / `tool({ inputSchema })` helper |
| Are guardrails present at all four checkpoints? | A tool runs (or output ships) unchecked | Add input/tool-call/tool-response/output hooks |
| Is tool metadata scanned and pinned before registration? | Tool-description injection reaches the model | Scan + pin + re-review on change |
| Does the approval surface show real side effects? | Humans approve a label, not a consequence | Render side effects at the approval hook |
| Are credentials isolated from the agent context? | One injection exfiltrates the user's token | Apply the three walls + token exchange |
| Does the agent use delegated short-lived tokens? | Raw user token lives in the runtime | Exchange for a scoped token at a broker |

## Cross-references

- `sdk-design.md` — the loop and hook execution points these tools plug into.
- `structured-output.md` — the typed result a tool returns.
- `errors-and-retry.md` — what a failed or denied tool call hands back to the model.
- → `harden-repo-for-coding-agents` to scaffold and enforce the gates/hooks in a
  repo (the doing); → `agent-ops` for operating the trust boundary at runtime.
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` —
  REVIEW scales; finding IDs `AGENT-DX-TOOL-NNN`.
- `references/intents/{do,review,design}.csv` row `tools-and-mcp` — the entry points.
