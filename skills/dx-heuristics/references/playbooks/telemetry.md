# Telemetry Playbook

## Scope

Analytics opt-in/out, data collection scope, consent UX, telemetry
transparency, default-off vs default-on, data retention, and PII handling in
telemetry payloads. Routes to `setup.md` for first-run consent integration and
`errors.md` for telemetry-error UX.

## Grounding

- **Ann Cavoukian — *Privacy by Design: The 7 Foundational Principles*** —
  privacy by default: the strongest protections apply automatically with no
  action required from the user. User control and visibility: individuals must
  be able to see what is collected and revoke their consent. Embed privacy into
  design: data minimisation and consent are architectural decisions, not
  bolt-ons applied after the fact.
- **European Parliament and Council — GDPR Article 7 (Conditions for
  Consent)** — consent must be freely given, specific, informed, unambiguous,
  and withdrawable at any time. Bundling consent with terms of service or
  making opt-out harder than opt-in violates these conditions.
- **Adam Wiggins — *The Twelve-Factor App*** — logs treated as event streams:
  the application emits structured events and the operator decides the sink and
  retention. Telemetry follows the same principle: the tool shapes and emits
  events; the destination and lifetime are the operator's concern, not
  silently hard-coded defaults.
- ***Safe Observability: A Framework for Automated PII Redaction from LLM
  Prompts in OpenTelemetry Pipelines*** (*Int'l Journal of Computer*, 2026) —
  in AI/agent systems, observability pipelines account for 25–40% of all
  discovered PII exposure in post-incident reviews, because traces and error
  reports retain raw prompts and responses for longer than the inference path
  itself and are read by more people. Redaction at the SDK boundary is more
  effective than at the downstream collector: raw spans are already exposed
  to telemetry-tier readers by the time they leave the SDK process.

## Good signals

- Telemetry is opt-in, or an unmissable first-run consent prompt explains what
  will be collected before any data is sent.
- What is collected is documented in plain language with concrete field
  examples — not "anonymous usage data."
- Opt-out is a single command (`<tool> telemetry off` or equivalent) and is
  visibly confirmed; the inverse command re-enables it.
- No PII or secrets appear in telemetry payloads; an automated test runs
  sanitisation against real or representative event captures.
- Data retention is documented: how long data is kept and when it is deleted.
- Opt-out works without a network call — disabling telemetry is a local
  operation only.
- Opt-out persists across upgrades; the tool does not silently re-enable
  telemetry on install.
- For AI/agent SDKs, a single SDK-layer flag (`record_content`,
  `capture_inputs`, or equivalent) controls whether raw prompt and response
  bodies are written to spans; redaction is not deferred to the downstream
  collector.
- A redactor extension point accepts a pluggable function (regex, NER, or
  ML-classifier-based) that runs on inputs/outputs *before* they leave the
  SDK process; the contract documents recall/precision expectations.
- Token-usage and structural attributes (`gen_ai.usage.*`, finish reasons,
  latencies) flow even when content capture is off — observability survives
  redaction.

## Common failures

- Telemetry on by default with no notice at first run.
- "We collect anonymous usage data" with no concrete list of fields or events.
- Opt-out requires editing a config file the user doesn't know exists.
- PII such as email addresses, file paths, or environment variables leaks into
  telemetry payloads.
- Opt-out does not actually stop network calls — it only hides the indicator
  in the UI.
- Updates silently re-enable telemetry after the user has opted out.
- Data retention is unlimited or completely undocumented.
- For AI/agent SDKs, raw prompts and responses are written to span attributes
  with no redaction layer in the SDK — the downstream collector is treated
  as the redaction boundary, exposing PII to every reader of the trace
  store, error reporter, and replay tooling.
- Redaction is co-located with inference (NER on the same GPU as the model),
  measurably degrading generation throughput under peak load; or
  placeholder inflation from redaction skews token-usage metrics and eval
  scores without that side-effect being documented.
- Inline content capture is on by default with no opt-out path; full chat
  histories sit in `gen_ai.input.messages` / `gen_ai.output.messages` and
  bloat span sizes past backend limits.

## Heuristics

- **Opt-in or first-run consent** *(design, audit)* — telemetry is either
  off by default or asks unmissably at first run before any event is emitted.
  Silence is not consent.
- **Plain-language data inventory** *(audit, design)* — every event type and
  field is documented in plain English with an example value. Abstract claims
  like "usage statistics" are not sufficient.
- **One-command opt-out** *(design, audit)* — toggling telemetry off is one
  command and produces a visible confirmation. The inverse re-enables it.
  Neither direction requires a config file search.
- **No-PII guarantee** *(audit, design)* — telemetry payloads are sanitised
  before transmission; an automated test asserts no PII or secrets appear in
  representative captures.
- **Persistent opt-out** *(design)* — the opt-out state survives upgrades. An
  upgrade test confirms telemetry is not silently re-enabled when the tool is
  updated.
- **Documented retention** *(design, audit)* — the public docs state how long
  data is retained and describe the deletion process.
- **Local-first opt-out** *(design)* — disabling telemetry is a local write to
  a config or flag file; it does not require a network call to take effect.
- **SDK-layer content-capture toggle** *(design, audit)* — for AI/agent
  SDKs, a single boolean (`record_content` or equivalent) flips raw
  prompt/response capture without disabling structural telemetry. Default
  to *off* when PII risk is unknown; document the trade-off explicitly
  rather than relying on the downstream collector to redact.
- **Pluggable redactor at the SDK boundary** *(design, audit)* — a
  redactor function runs on inputs and outputs before they hit any span
  attribute. The interface accepts regex, NER, or ML-classifier
  implementations; the docs name the redactor's recall/precision profile
  and warn that placeholder inflation can shift token-usage metrics and
  eval scores. Co-locating heavy NER on the inference GPU is called out
  as a perf footgun.
- **Survive-redaction telemetry** *(design)* — token counts, latencies,
  finish reasons, and tool-call shape stay observable even when content
  capture is disabled. An operator can answer "what is slow, what failed,
  what cost what" without ever reading a prompt body.
- **Inline-vs-reference content discipline** *(design, audit)* — when a
  prompt or response is captured, the SDK either inlines it on the span
  with a documented size cap, or stores a reference (object key, content
  hash, eval-dataset row ID) and a typed pointer on the span. The choice
  is named in the docs because inline content makes traces self-contained
  for replay but bloats span size and broadens the PII surface.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is telemetry opt-in or first-run-consent? | Silent collection | Add consent prompt or flip default to off |
| Is the data inventory in plain language? | Vague "usage data" claim | Document each event type and field |
| Is opt-out a single command? | Config file digging required | Add `telemetry off` subcommand |
| Is PII excluded from payloads? | Leakage risk | Add sanitisation + automated payload tests |
| Does opt-out persist across updates? | Silent re-enable on upgrade | Add upgrade integration test |
| Is retention documented? | Unbounded or unknown | Publish retention policy in public docs |
| Does an AI/agent SDK expose an SDK-layer content-capture toggle? | Redaction deferred to collector; PII leaks to trace-store readers | Add `record_content` (or equivalent) on the SDK with documented default |
| Is the redactor a pluggable extension point? | Hard-coded regex or no redaction at all | Expose a redactor interface with named recall/precision profile |
| Do token-usage and structural attributes survive redaction? | Disabling content kills all observability | Separate content capture from structural telemetry on the span |
| Is the inline-vs-reference content choice documented? | Span bloat or missing context, unpredictably | Pick a model (inline-with-cap or reference-by-ID); document the cap and pointer shape |

## Cross-references

- → `setup.md` for first-run consent integration.
- → `errors.md` for telemetry-error UX.
