# <Playbook Title> Playbook

One file per intent (or per shared rubric) under
`references/<topic-or-rubric>.md`. Single-layer playbooks are leaner
than two-level playbooks but **must** still include the canonical
sections so the static check and the validation rubric can grade them.

## Scope

What this playbook covers, and what it explicitly does not. Cross-link
to neighbor playbooks if the boundary is ambiguous.

- In:
- Out:
- Cross-references:

## Grounding

How this playbook is grounded in the skill's `inspired_by` sources.
One bullet per source actually used here. Avoid distinctive phrasing
from the source; paraphrase into operational vocabulary.

- `<Source A>` — what concept it contributes
- `<Source B>` — what concept it contributes

## Good signals

Concrete observable signs the agent is on the right track when this
playbook is active. Two to five bullets, each phrased as something
the agent can *check* — not as exhortation.

- Signal 1
- Signal 2

## Common failures

Anti-patterns and near-miss applications. Each should name a *specific*
failure mode, not a generic "be careful."

- Failure 1 — when it happens, why it happens
- Failure 2 —

## Heuristics

The load-bearing content of the playbook. Each heuristic is a rule of
thumb the agent applies. Keep them operational and short.

- Heuristic 1
- Heuristic 2
- Heuristic 3

## Quick diagnostic

Binary questions with named follow-up actions. The agent uses these
to triage *which* of the heuristics above to apply.

- Q1 — yes → action; no → action
- Q2 — yes → action; no → action

## Cross-references

Pointers to neighbor playbooks, shared rubrics, or the registry rows
that route to this file.

- `references/<other-playbook>.md` — when to consult instead
- `references/intent-router.csv` row `<intent>` — the entry point
