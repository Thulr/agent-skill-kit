# Agent Docs — DESIGN — <doc surface>

**Target persona:** <from references/core/personas.md>
**Surfaces in scope:** <list>
**Project tier:** <Prototype | Growing | Load-bearing>
**Date:** <YYYY-MM-DD>

## Goal

<1–2 sentences: what agent-native doc surface is being designed and which agents read it.>

## Acceptance criteria

<Observable, testable. Each ties to a surface in scope.>

- [ ] <criterion 1> — surface: <surface>
- [ ] <criterion 2>

## Target shape

<The smallest agent-native doc surface the present need forces: the AGENTS.md contract, the
curated index, the tool-description conventions, the chunk/anchor discipline, the context-budget
tiers. Describe each in one phrase and what an agent does with it. A text sketch is fine.>

## Agent-readability guarantees

- **Found:** <curated index; placement-by-access-pattern.>
- **Survives:** <chunk-survivable sections; stable-anchor contract.>
- **Triggers:** <descriptions state purpose / use / near-miss exclusions.>
- **Budgeted + true:** <tiered budget; single-source with drift checks; invariants in gates.>

## Seams deliberately NOT added

<The bundles, mirrors, or always-loaded content you considered and are leaving out because no
present need forces them (YAGNI). This section is required — it is the difference between
right-sized and an everything-dump.>

## Decisions

For each load-bearing decision, name the playbook heuristic that underwrites it.

- **<Decision 1>:** <choice> — playbook heuristic: <playbook>#<heuristic> (<intent>)

## Open questions

<Items where lenses disagreed, or where the design depends on context the agent did not have.>

## Verification

<How to verify the design satisfies the acceptance criteria — a retrieval test, a mirror-parity
check, a chunk-survivability spot-check, a trigger eval (hand to agent-test).>

## Grounding sources applied

- <skill.json inspired_by entry> — <design decision it informed>
