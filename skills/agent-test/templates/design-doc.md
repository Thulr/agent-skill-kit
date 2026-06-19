# Agent Test — DESIGN — <measurement system>

**Target persona:** <from references/core/personas.md>
**Surfaces in scope:** <list>
**Project tier:** <Prototype | Growing | Load-bearing>
**Date:** <YYYY-MM-DD>

## Goal

<1–2 sentences: what is being measured and why, and what change the measurement gates.>

## Acceptance criteria

<Observable, testable. Each ties to a surface in scope.>

- [ ] <criterion 1> — surface: <surface>
- [ ] <criterion 2>

## Failure-mode ontology

<The named ways the system fails (loops, wrong-tool, lost hand-off, hallucinated fields, format
breaks, …). Every later eval must attribute a red result to a mode here.>

## Target instruments

<The smallest measurement the present need forces: which staircase tier, which evals, the judge
calibration contract (if any), the held-out benchmark shape, the activation evals. Describe each
in one phrase and the gate it clears. A text sketch is fine.>

## Trust guarantees

- **Decomposed:** <per-mode/per-slice, never one aggregate as the gate.>
- **Calibrated:** <judges measured against a human-labeled set + bias checks + explanations.>
- **Held-out:** <fixtures disjoint from training, with a count margin; baseline + rollback.>
- **Gaming-resistant:** <rewards the behavior, not a proxy a change can game.>

## Seams deliberately NOT added

<The benchmark suites, judges, or coverage you considered and are leaving out because no present
need forces them (YAGNI). This section is required — it is the difference between right-sized and
over-built measurement.>

## Decisions

For each load-bearing decision, name the playbook heuristic that underwrites it.

- **<Decision 1>:** <choice> — playbook heuristic: <playbook>#<heuristic> (<intent>)

## Open questions

<Items where lenses disagreed, or where the design depends on context the agent did not have.>

## Verification

<How to verify the design satisfies the acceptance criteria — a held-out run, a judge-calibration
report, a forced-rollback drill, an activation positive/negative/edge pass.>

## Grounding sources applied

- <skill.json inspired_by entry> — <design decision it informed>
