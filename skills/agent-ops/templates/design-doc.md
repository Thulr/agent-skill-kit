# Agent Ops — DESIGN — <loop or system>

**Target persona:** <from references/core/personas.md>
**Surfaces in scope:** <list>
**Project tier:** <Prototype | Growing | Load-bearing>
**Date:** <YYYY-MM-DD>

## Goal

<1–2 sentences: what operating loop or control is being designed and why.>

## Acceptance criteria

<Observable, testable. Each ties to a surface in scope.>

- [ ] <criterion 1> — surface: <surface>
- [ ] <criterion 2>

## Target loop

<The smallest operating loop the present need forces: what is traced, how the trajectory is
graded, how signal becomes change, the cadence, and the stop/rollback. Describe each piece in
one phrase. A text sketch is fine.>

## Operations guarantees

- **Observable:** <spans carry prompt+completion+tool I/O; trajectory graded as a path.>
- **Loop closes:** <trace-to-eval yields a non-trivial candidate; readiness on observed emission.>
- **Autonomy gated:** <held-out eval, circuit-breaker, one-diff-per-cycle, revert-on-failed-gate.>
- **Release gate:** <decomposed by failure mode; guardrail vs north-star; per-slice baseline + rollback.>

## Seams deliberately NOT added

<The dashboards, tiers, autonomy, or platform pieces you considered and are leaving out because
no present need forces them (YAGNI). This section is required — it is the difference between
right-sized and over-built.>

## Decisions

For each load-bearing decision, name the playbook heuristic that underwrites it.

- **<Decision 1>:** <choice> — playbook heuristic: <playbook>#<heuristic> (<intent>)

## Open questions

<Items where lenses disagreed, or where the design depends on context the agent did not have.>

## Verification

<How to verify the design satisfies the acceptance criteria — a real captured trajectory, a
held-out eval run, a forced-rollback drill, a budget breach test.>

## Grounding sources applied

- <skill.json inspired_by entry> — <design decision it informed>
