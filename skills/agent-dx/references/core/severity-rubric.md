# Severity rubric (0–4)

Apply to every finding in a REVIEW, every risk in a DESIGN, and every step in a hardening
runbook. Agent-DX severity weighs how badly a stochastic, machine-speed consumer is harmed —
a surface a human would shrug off can strand an agent in a loop.

| Level | Label | Meaning |
|------:|-------|---------|
| 4 | **Critical** | A security/trust boundary failure (untrusted tool metadata reaches the model, credentials live in the agent context, raw PII captured by default under regulated data); an error or schema contract broken in a core tool surface a fleet depends on. Block merge. |
| 3 | **High** | A consuming agent cannot recover — free-text errors it can't branch on, no stop/verify in the loop, string-only "structured" output. A contract that breaks across minor versions. Large but tractable fix. |
| 2 | **Medium** | Contained drift: a hand-written tool schema, a single unguarded checkpoint off the core path, content/structural telemetry on one switch. Fix when next touching the surface. |
| 1 | **Low** | A telemetry attribute on the wrong convention, an imprecise tool description, a needless serialization step. Queue for cleanup if it accumulates. |
| 0 | **Note** | An observation worth recording, not a defect — e.g. "this surface is provider-specific but documents the gap." |

## How to pick a level

1. **Blast radius.** Every agent/tool call (4), one tool or contract (3), one surface (2), one
   field/attribute (1), nothing a consumer observes (0)?
2. **Agent-recoverability.** Does the flaw strand a stochastic consumer (no stable error code,
   no retry shape, no verification)? Un-recoverable rates higher than merely untidy.
3. **Trust exposure.** Anything that lets untrusted content reach the model or lets a secret
   leave the boundary escalates toward 4 regardless of blast radius.

## Calibration anchors

- "Untrusted tool metadata is registered without scanning/pinning; a tool-description
  injection reaches the model" → **4** (trust boundary).
- "The user's durable credential lives in the agent context" → **4**.
- "Raw prompts/responses are captured in spans by default" → **3**; escalate to **4** under
  regulated data.
- "An LLM-facing error is free text with no stable `code`; a consuming agent cannot branch on
  it" → **3**; escalate to **4** on a core tool surface a fleet depends on.
- "The agent loop has no stop predicate, or no deterministic verification step" → **3**.
- "Structured output is string-only — no schema, no validation, no refusal field" → **3**.
- "A tool schema is hand-written next to the function and drifts from the signature" → **2**.
- "Content capture and structural telemetry share one switch" → **2**.
- "A span mixes convention sets ad hoc (`guardrail` labelled OTel GenAI)" → **1**.
- "A provider-specific gap that is honestly documented" → **0** (record only).

## Cross-surface comparison

Scores and severities are comparable only within one REVIEW run, using the same persona and
project tier. Do not benchmark across teams or across time without recalibrating against these
anchors.
