<!-- Load-bearing section: Acceptance criteria -->
# Perf and Observability Design: <surface>

## Goal
- Target persona: <persona from references/perf/core/personas.md>
- Intended outcome: <reliability / performance / observability posture the design must hold>
- Constraints: <budget, cardinality ceiling, deadline, dependency contracts, SLA>
- Playbook(s) applied: <e.g., slos.md, metrics.md>

## Good-shaped pattern

<The concrete shape the design should take — sample SLI / SLO definition, paste-ready alerting rule, span attribute schema, dashboard layout, latency budget table. Not abstract principles; the actual thing.>

## Heuristics applied

One block per heuristic.

### <named heuristic from playbook>
- Why it applies:               <one line>
- How this design satisfies it: <specific design choice>
- Measurement method:           <how the design is observable and verifiable>

## Grounding sources applied

- <skill.json inspired_by entry> - <design choice it informed>

## Anti-patterns avoided

- <Named anti-pattern from playbook common failures>: <how this design dodges it>

## Acceptance criteria

Testable conditions that prove the design met its goal. Each line should be checkable by reading the artifact, querying telemetry, or running a measurement.

- [ ] <criterion — name the measurement>
- [ ] <criterion — name the measurement>

## Edge cases handled

- <Edge case, e.g., overload / degraded dependency / clock skew / sampling at the tail>: <intended behavior>

## Open trade-offs

- <Trade-off, e.g., cardinality vs cost, sampling vs diagnose-ability, freshness vs retention>: <chosen path and rationale>

## Out of scope

- <Things deliberately not solved here>
