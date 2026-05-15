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

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is telemetry opt-in or first-run-consent? | Silent collection | Add consent prompt or flip default to off |
| Is the data inventory in plain language? | Vague "usage data" claim | Document each event type and field |
| Is opt-out a single command? | Config file digging required | Add `telemetry off` subcommand |
| Is PII excluded from payloads? | Leakage risk | Add sanitisation + automated payload tests |
| Does opt-out persist across updates? | Silent re-enable on upgrade | Add upgrade integration test |
| Is retention documented? | Unbounded or unknown | Publish retention policy in public docs |

## Cross-references

- → `setup.md` for first-run consent integration.
- → `errors.md` for telemetry-error UX.
