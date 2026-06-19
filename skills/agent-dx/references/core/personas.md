# Target personas

Pick the persona that best matches the audience for this output. The choice shapes
vocabulary, depth, and which trade-offs to surface. The audience here is whoever *builds the
surface an agent consumes* — not the agent itself.

## Persona A — SDK/tool author mid-change (DO)

Writing or changing an AI/Agent SDK, a tool definition, an error envelope, or telemetry right
now, and wants the agent-facing surface correct without slowing down. Comfortable with their
language and the model API; not looking for an architecture lecture.

- **Speak to:** deriving a tool schema from the signature, typing the result and refusal,
  shaping a retryable error, verifying a loop step, defaulting content capture off.
- **Avoid:** heavy framework vocabulary, speculative extension points, ceremony for a small
  change.

## Persona B — Reviewer auditing an agent-facing surface (REVIEW)

Owns a judgment about whether an existing SDK/tool/error/telemetry surface is safe and usable
*by an agent*: can a stochastic consumer recover, is the trust boundary intact, is the
contract stable. Wants scored findings and a short "fix three first" list, not a rewrite.

- **Speak to:** unrecoverable error paths, untrusted tool metadata, credential exposure,
  string-only output, unbounded loops, PII in spans.
- **Avoid:** prescribing a named framework; treating every gap as a blocker regardless of
  project scale (calibrate).

## Persona C — Architect designing an Agent SDK (DESIGN)

Deciding the minimal contract set for a new agent-facing surface: loop ownership, tool
boundary, structured-output guarantee level, error envelope, telemetry axes. Wants the
smallest surface that earns its place, with clear trade-offs.

- **Speak to:** loop vs caller ownership, the two structured-output guarantee levels, the four
  guardrail checkpoints, the credential walls, structural-vs-content telemetry axes.
- **Avoid:** speculative generality; importing a full agent framework as a default.

## Persona D — Tech lead hardening an SDK under deadline

Cannot rewrite the SDK. Needs a sequenced plan to close trust-boundary and recoverability gaps
with a safety net at every step and a way to stop partway.

- **Speak to:** smallest reversible step, contract/version compatibility, adding hooks and
  redaction without breaking callers, what breaks if hardening stops at step N.
- **Avoid:** "first redesign the SDK"; sequences that require freezing the public contract.

## Default persona

When the prompt does not signal a clear audience, assume **Persona A** for DO, **Persona B**
for REVIEW, and **Persona C** for DESIGN, and state the assumption so the reader can redirect.
