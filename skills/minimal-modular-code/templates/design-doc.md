# Minimal Modular Code — DESIGN — <feature or system>

**Target persona:** <from references/core/personas.md>
**Surfaces in scope:** <list>
**Project tier:** <Prototype | Growing | Load-bearing>
**Date:** <YYYY-MM-DD>

## Goal

<1–2 sentences: what is being built and why.>

## Acceptance criteria

<Observable, testable. Each ties to a surface in scope.>

- [ ] <criterion 1> — surface: <surface>
- [ ] <criterion 2>

## Target shape

<The smallest set of module boundaries the present requirement forces, and which way
dependencies point. Describe each unit in one phrase (the one concept it owns) and the
contract between units. A text sketch is fine.>

## Seams deliberately NOT added

<The ports, layers, abstractions, or extension points you considered and are leaving out
because no present need forces them (YAGNI). This section is required — it is the difference
between right-sized and over-engineered.>

## Work-partitioning (if for parallel agents)

<Which units sit in the same dependency layer and could be built by different agents in
parallel; which contracts are the high-blast-radius artifacts to freeze and own first; what
must be serialized across layers.>

## Decisions

For each load-bearing decision, name the playbook heuristic that underwrites it.

- **<Decision 1>:** <choice> — playbook heuristic: <playbook>#<n> (<intent>)

## Open questions

<Items where lenses disagreed, or where the design depends on context the agent did not have.>

## Verification

<How to verify the design satisfies the acceptance criteria — tests, a dependency-graph check,
peer review, a prototype.>

## Grounding sources applied

- <skill.json inspired_by entry> — <design decision it informed>
