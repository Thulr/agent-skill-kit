# Target personas

Pick the persona that best matches the audience for this output. The choice shapes
vocabulary, depth, and which trade-offs to surface. The audience here *operates* a running
agent system — it does not build the SDK (that is `agent-dx`) or design the evals
(`agent-test`).

## Persona A — Engineer wiring a loop or observability mid-change (DO)

Standing up a trace stream, a trace-to-eval step, a budget, or a release gate right now, and
wants it operational without over-building. Comfortable with their telemetry stack; not
looking for a maturity lecture.

- **Speak to:** wrapping the LLM client so spans carry real content, the smallest loop that
  closes, a circuit-breaker before autonomy, a rollback threshold.
- **Avoid:** maturity-ladder ceremony for a one-loop change; dashboards that don't feed a fix.

## Persona B — AI quality lead or SRE auditing an ops posture (REVIEW)

Owns a judgment about whether a running agent system is observable, improving, and safe to let
run: is the loop real, is autonomy gated, will a regression be caught. Wants scored findings
and a short "fix three first" list, not a re-platforming.

- **Speak to:** telemetry/dashboard theater, trajectory blindness, god-gate release gates,
  ungated autonomy, observed-emission readiness, march-of-nines reliability.
- **Avoid:** prescribing a vendor; treating every gap as a blocker regardless of project scale
  (calibrate).

## Persona C — Architect designing the optimization loop or autonomy (DESIGN)

Deciding the minimal loop and autonomy controls for an agent system: what to trace, how the
flywheel closes, when a controller may self-improve, how the release gate decomposes. Wants the
smallest operating loop that earns its place, with clear trade-offs.

- **Speak to:** the six loop-readiness fields, the staircase tier and its gate-before-
  persistence, controller preconditions and circuit-breakers, per-slice guardrail-vs-north-star
  gates.
- **Avoid:** speculative autonomy; a god metric; importing a full MLOps platform as a default.

## Persona D — On-call / ops lead operating under incident or deadline

Cannot pause the system. Needs a sequenced rollout/rollback plan with a safety net at every
step and a way to stop partway.

- **Speak to:** smallest reversible step, the rollback threshold, staging only green changes,
  what breaks if the rollout stops at step N, who owns the revert.
- **Avoid:** "first instrument everything"; sequences that require freezing the production loop.

## Default persona

When the prompt does not signal a clear audience, assume **Persona A** for DO, **Persona B**
for REVIEW, and **Persona C** for DESIGN, and state the assumption so the reader can redirect.
