<!-- Load-bearing section: Program scope and adoption sequence -->
# Perf and Observability Strategy: <program / surface area>

## Program scope
- Surfaces covered: <e.g., SLO program, instrumentation budget, trace strategy, capacity roadmap>
- Target persona: <persona from references/core/personas.md>
- Time horizon: <e.g., 2 quarters, 1 year>
- Constraint: <budget, headcount, dependency stability, deadline>
- Playbook(s) applied: <e.g., slos.md, metrics.md, tracing.md>

## Current state (baseline)

<One-paragraph honest assessment of the starting posture. Cite the audit that produced it if applicable. Name measurements, not vibes.>

## Target end-state

<The posture the program is meant to achieve. Concrete: "every customer-facing service has user-boundary SLIs, SLOs derived from measured baseline, multi-window multi-burn-rate alerting, and a written error-budget policy.">

## Heuristics applied

One block per heuristic.

### <named heuristic from playbook>
- Why it applies:                       <one line>
- How the program adopts it:            <specific organizational / technical move>
- Measurement of adoption:              <how we know the program is meeting it>

## Adoption sequence

Ordered, with explicit dependencies and measurement-of-adoption gates per step.

### Phase 1 — <name>
- Scope:         <which services / surfaces>
- Move:          <the specific change>
- Owner:         <team / person>
- Gate:          <measurement that proves Phase 1 is done>
- Dependency:    <upstream prerequisite, if any>

### Phase 2 — ...

## Grounding sources applied

- <skill.json inspired_by entry> - <strategic choice it informed>

## Anti-patterns avoided

- <Named anti-pattern>: <how the program dodges it>

## Open trade-offs

- <Trade-off, e.g., cardinality budget vs novel-question debuggability, sampling rate vs cost, retention vs cost>: <chosen path and rationale>

## Out of scope

- <Things deliberately not solved by this program>

## Review cadence

<How often the program is reviewed and against which signals — error-budget burn, SLO drift, instrumentation cost trend, post-incident review themes.>
