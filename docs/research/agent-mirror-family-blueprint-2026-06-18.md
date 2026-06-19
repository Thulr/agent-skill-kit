# Agent-mirror family — blueprint & migration map (2026-06-18)

> Working design doc for reorganizing the catalog by **actor**. **Formalized as [ADR 0011](../adr/0011-actor-axis-agent-mirror-family.md) (Accepted 2026-06-18)**, which supersedes the structural claim of [ADR 0007](../adr/0007-experience-disciplines-are-audience-peers.md) and updates 0005/0006/0008. Status: **accepted — see the ADR for the binding decision and the locked decomposition cut** (this doc is the design rationale + the verbatim seed content for `agent-dx`).

## The actor model

Two orthogonal dimensions:
- **Actor** — human | agent. *Agent is an actor TYPE, not an audience peer*: an agent can play any role (user, developer, operator).
- **Role / relationship to the software** — user (uses the product), developer (builds against it), operator (runs it).

The operative distinction: a surface an agent **consumes** (API/SDK/CLI/errors/telemetry/UI) is still dx/ux/perf **for an agent actor**; a surface that exists **only because agents exist** (MCP, llms.txt, AGENTS.md, agent loops, RAG/context) is the agent-native platform.

This supersedes ADR-0007's "UX/DX/AX are audience peers." The catalog is organized by **actor as the top axis**, with an agent mirror for each human-experience domain where the agent-actor content is real.

## Target matrix

| Human domain | Agent mirror | Build? | Seed / maps from |
|---|---|---|---|
| dx (API/SDK/CLI/errors/telemetry) | **agent-dx** | yes — strong | dx's pulled errors/telemetry agent blocks (this doc, appendix) + most of `design-for-agent-users` SDK/tool content |
| docs | **agent-docs** | yes — strong | `design-for-agent-users` docs parts (llms.txt/AGENTS.md/RAG/machine-readable reference) |
| ux/ui | **agent-ux** | yes — NET-NEW | nothing today: agent-as-end-user, computer-use, deterministic selectors, machine-readable state, action affordances, auth-on-behalf |
| perf/ops | **agent-ops** | yes | `agent-evals` + `harden-repo-for-coding-agents` (agent observability/reliability/cost) |
| test | **agent-test** | yes | `agent-evals` (evals, trajectory tests, judge calibration) |
| code-craft (`minimal-modular-code`) | — | no | already agent-oriented; + `harden-repo` for repo structure |
| writing | — | **no (user: leave as-is)** | — |
| research, discovery | — | no (vacuous) | — |

## How the current agent family decomposes

- **`design-for-agent-users`** (today: umbrella + AX heuristics) → decomposes into **agent-dx** (SDK/tool/error/structured-output surfaces) + **agent-docs** (llms.txt/AGENTS.md/RAG). The umbrella role (routing across the agent family) either retires or becomes a thin front-door over the new per-domain agent skills.
- **`harden-repo-for-coding-agents`** → the repo/infrastructure slice of **agent-ops** (gates, hooks, sandboxes, AGENTS.md scaffolding). May keep its name as the "repo-hardening" arm.
- **`agent-evals`** → **agent-test** (evals/trajectory/judge) + the eval-loop slice of **agent-ops** (observability, optimization loops).
- **`rules-from-coding-agent-failures`** → stays as the feedback-loop/governance arm under agent-ops.

(Exact decomposition — split vs front-door vs rename — is the open design question for step 2/3; this map is the target, not the final cut.)

## Sequencing

1. **Ship human-dx (this branch, `feat/dx-wiki-gap-implementation`).** Pull the agent blocks out of dx `errors.md` + `telemetry.md` (captured below); dx becomes human-developer-only. Commit + PR the human-DX wiki-gap adds.
2. **Design + ADR.** This doc → an ADR superseding 0007; lock the 5 agent skills' names/scopes and the decomposition cut.
3. **Build in phases** (workflow per skill): agent-dx + agent-docs first (most substance, mostly restructure), then net-new agent-ux, then re-cast agent-ops + agent-test. Each = full SKILL.md + playbooks + evals, like `minimal-modular-code`. No private-wiki citations; `inspired_by` encouraged-not-required.
4. **Catalog rewire + validate** — README/catalog families, cross-refs, install lanes, CODEOWNERS; `just check` across the re-architecture.

---

## Appendix — agent content pulled from dx (seed for agent-dx)

Captured verbatim so it is not lost when removed from `dx` in step 1. These belong in **agent-dx** (errors/telemetry for an agent developer).

### From `errors.md`

**Grounding (agent-callable surfaces, WorkOS practitioner framing):** an LLM consuming an error cannot read tooltips or recover from ambiguity the way a human can; it decides on surfaced text alone, at machine speed. Agent-consumable errors must be deterministic, structured, and name the failing input in a format the model parses.

**Heuristics (the "When the consumer is an agent" block):**
- **Agent-readable error envelope** — for LLM-callable surfaces, errors are a typed structure with `code`, parameter-specific `message`, and `recovery_hint`; the schema is part of the public contract and does not break between minor versions.
- **Tool-error feedback shaped for retry** — failed tool calls return the same JSON shape the LLM produced, naming the offending input; the error path does not collapse to free text.
- **Replay-ready error capture** — the error stored on the tool-call span is identical to what the LLM saw, so offline replay and eval simulate the recovery path without hitting production.

**Supporting good-signals / failures / diagnostics (agent-specific):** typed envelope with discrete fields over narrative text, stable across SDK versions; tool-execution failures name which input was problematic in the same tool-result shape and persist that shape on the tool-call span; failure modes — free-text errors agents can't branch on, tool errors omitting the offending parameter, error wording changing across versions with no stable code.

### From `telemetry.md`

**Grounding (Safe Observability — PII redaction from LLM prompts in OpenTelemetry, 2026):** in AI/agent systems, observability pipelines account for 25–40% of discovered PII exposure post-incident, because traces/error reports retain raw prompts/responses longer than the inference path and are read by more people; redact at the SDK boundary, not the downstream collector.

**Heuristics (the "When the consumer is an agent" block):**
- **SDK-layer content-capture toggle** — a single boolean (`record_content` or equivalent) flips raw prompt/response capture without disabling structural telemetry; default off when PII risk is unknown; emit structural spans against the standard convention (OpenTelemetry `gen_ai.*`) so one flag yields portable telemetry.
- **Pluggable redactor at the SDK boundary** — a redactor function runs on inputs/outputs before any span attribute; accepts regex/NER/ML implementations; docs name recall/precision; co-locating heavy NER on the inference GPU is a perf footgun.
- **Survive-redaction telemetry** — low-cardinality structural attributes (token counts, latencies, finish reasons, tool-call shape) stay observable when high-cardinality content capture is off; keep the two on separate axes (raw content / per-request IDs as indexed dimensions blow up cardinality).
- **Inline-vs-reference content discipline** — a captured prompt/response is either inlined with a documented size cap or stored as a reference (object key, content hash, eval-dataset row ID) with a typed pointer; docs name the choice.

> Note: the **"detect silent provider degradation"** heuristic (degraded-but-200 detected via quality/latency drift) STAYS in dx `telemetry.md` — it is a general human-DX concern (any upstream dependency can degrade), not agent-specific.
