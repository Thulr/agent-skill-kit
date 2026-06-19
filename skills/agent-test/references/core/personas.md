# Target personas

Pick the persona that best matches the audience for this output. The choice shapes vocabulary,
depth, and which trade-offs to surface. The audience here *designs the measurement* of an agent
system — it does not operate the loop (that is `agent-ops`).

## Persona A — Engineer writing an eval, judge, or test mid-change (DO)

Adding an eval, a judge, a trajectory assertion, or an activation case right now, and wants it
to actually catch the failure without over-building. Comfortable with their stack; not looking
for a measurement-theory lecture.

- **Speak to:** the smallest eval that gates this change, a deterministic check over a judge
  when possible, a held-out fixture that isn't in the training set, the trajectory assertion
  that catches the loop.
- **Avoid:** a full benchmark suite for a one-line change; an uncalibrated judge as a gate.

## Persona B — AI quality lead auditing a test/eval suite (REVIEW)

Owns a judgment about whether the suite can be TRUSTED: are judges calibrated, are benchmarks
held-out, do evals grade the path, is activation tested. Wants scored findings and a short "fix
three first" list, not a re-write.

- **Speak to:** vague judges, god-gate pass-rates, trajectory blindness, memorizing benchmarks,
  metric-gaming, untested activation, evals not re-run on change.
- **Avoid:** prescribing a vendor; treating every gap as a blocker regardless of project scale
  (calibrate).

## Persona C — Architect designing the eval/benchmark/judge strategy (DESIGN)

Deciding the minimal measurement that gates change for an agent system or skill: the failure-mode
ontology, the tier-appropriate eval, the judge calibration contract, the held-out benchmark, the
activation evals. Wants the smallest instrument that earns its place, with clear trade-offs.

- **Speak to:** failure-mode-first design, the staircase gate per tier, judge calibration +
  bias checks, per-slice guardrail-vs-north-star benchmarks, activation positive/negative/edge.
- **Avoid:** a single god metric; speculative coverage; importing a full eval platform as a
  default.

## Persona D — Quality lead hardening an eval suite under deadline

Cannot rebuild the suite. Needs a sequenced plan to close the trust gaps (calibrate the judge,
disjoin the held-out set, add path assertions) with a safety net at every step.

- **Speak to:** smallest reversible step, calibrating before trusting, swapping a god-gate for
  per-slice scoring without losing history, what breaks if hardening stops at step N.
- **Avoid:** "first re-label everything"; sequences that block the release pipeline.

## Default persona

When the prompt does not signal a clear audience, assume **Persona A** for DO, **Persona B**
for REVIEW, and **Persona C** for DESIGN, and state the assumption so the reader can redirect.
