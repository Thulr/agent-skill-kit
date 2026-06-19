# Agent DX — DESIGN — <feature or surface>

**Target persona:** <from references/core/personas.md>
**Surfaces in scope:** <list>
**Project tier:** <Prototype | Growing | Load-bearing>
**Date:** <YYYY-MM-DD>

## Goal

<1–2 sentences: what agent-facing surface is being built and why an agent consumes it.>

## Acceptance criteria

<Observable, testable. Each ties to a surface in scope.>

- [ ] <criterion 1> — surface: <surface>
- [ ] <criterion 2>

## Target shape

<The smallest agent-facing contract the present requirement forces: who owns the loop, the
tool boundary, the structured-output guarantee level, the error envelope, the telemetry axes.
Describe each in one phrase and the contract a consuming agent sees. A text sketch is fine.>

## Agent-consumability guarantees

- **Contract:** <schemas derived from code; typed output + refusal; stable error `code`.>
- **Recovery:** <stop+verify; retry-shaped errors; semantic vs transport retry.>
- **Trust:** <four guardrail checkpoints; credential walls; content capture default-off.>

## Seams deliberately NOT added

<The ports, layers, provider shims, or extension points you considered and are leaving out
because no present need forces them (YAGNI). This section is required — it is the difference
between right-sized and over-engineered.>

## Decisions

For each load-bearing decision, name the playbook heuristic that underwrites it.

- **<Decision 1>:** <choice> — playbook heuristic: <playbook>#<heuristic> (<intent>)

## Open questions

<Items where lenses disagreed, or where the design depends on context the agent did not have.>

## Verification

<How to verify the design satisfies the acceptance criteria — schema round-trip tests, a
loop-bound test, an injection test, a redaction test, peer review, a prototype.>

## Grounding sources applied

- <skill.json inspired_by entry> — <design decision it informed>
