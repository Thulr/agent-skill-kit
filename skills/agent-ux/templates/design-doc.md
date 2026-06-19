# Agent UX — DESIGN — <surface or flow>

**Target persona:** <from references/core/personas.md>
**Surfaces in scope:** <list>
**Project tier:** <Prototype | Growing | Load-bearing>
**Date:** <YYYY-MM-DD>

## Goal

<1–2 sentences: what agent-facing interaction surface is being designed and what an agent does
through it.>

## Acceptance criteria

<Observable, testable. Each ties to a surface in scope.>

- [ ] <criterion 1> — surface: <surface>
- [ ] <criterion 2>

## Target shape

<The smallest agent-facing surface the present need forces: the machine-readable state, the stable
action handles, the approval/authority gate, the human/agent dual path. Describe each in one phrase
and what an agent does with it. A text sketch is fine.>

## Agent-usability guarantees

- **Perceive:** <state/actions/results in the tree — roles, labels, text — observable after action.>
- **Act:** <stable semantic handles; idempotent / retry-safe actions.>
- **Authority:** <irreversible actions gate in-path; on-behalf consent visible, scoped, revocable.>
- **Reconcile:** <human affordance + machine-readable path; one source, many renderings.>

## Seams deliberately NOT added

<The agent affordances, modes, or consent flows you considered and are leaving out because no
present need forces them (YAGNI). This section is required — it is the difference between
right-sized and over-built.>

## Decisions

For each load-bearing decision, name the playbook heuristic that underwrites it.

- **<Decision 1>:** <choice> — playbook heuristic: <playbook>#<heuristic> (<intent>)

## Open questions

<Items where lenses disagreed, or where the design depends on context the agent did not have.>

## Verification

<How to verify the design satisfies the acceptance criteria — an accessibility-tree read, a
selector-stability test, an idempotency/retry test, a destructive-action gate drill.>

## Grounding sources applied

- <skill.json inspired_by entry> — <design decision it informed>
