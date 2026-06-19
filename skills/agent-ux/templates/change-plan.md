# Change Plan — <what agent-facing surface you are changing>

**Target persona:** <from references/core/personas.md> (usually Persona A)
**Surfaces in scope:** <machine-readable-state | deterministic-actions | approval-and-agency | audience-conflicts>
**Date:** <YYYY-MM-DD>

A pre-flight plan for an in-progress change to a surface an agent acts through. Fill it before
writing much; it is a thinking tool, not a deliverable to track.

## What already exists

<What an agent can already perceive and do on this surface — the structured state, the stable
handles, the approval gates. Confirm load-bearing state/actions are in the accessibility tree (not
pixels-only) before relying on them.>

## The minimal change

- **Reuse:** <existing roles/labels/handles/gates this builds on>
- **Add:** <the smallest agent-facing affordance the present need forces>
- **Remove:** <human-only affordances or fragile targets this lets you retire — answer even if "nothing">

## Agent-usability check

- **Perceive:** <is state/actions/results in the tree — roles, labels, text — not color/icon/toast?>
- **Act:** <stable semantic handle; idempotent/retry-safe?>
- **Authority:** <does any irreversible action gate in-path; is on-behalf consent visible + scoped?>

## Seams I am deliberately NOT adding

<The agent affordances, modes, or consent flows you considered and are leaving out because no
present need forces them (YAGNI). Naming them documents the restraint.>

## Blast radius

<Which agents act through this and what they can do. If it touches an irreversible/authority-
crossing action, note it is a coordinate-or-gate change, not a free one.>

## Routing

- **Mechanical** (role/label wiring, test id, live region): handled by <gate / locally>.
- **Judgment call to flag to a human:** <enabling an agent on a destructive action, an on-behalf
  consent scope, a human/agent trade-off — or "none">.

## Grounding sources applied

- <skill.json inspired_by entry> — <how it shaped this plan>
