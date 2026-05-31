# <Surface> Playbook

One file per surface under `references/playbooks/<surface>.md`.
Two-level playbooks are the canonical example — see
`skills/dx-critique/references/playbooks/` for working playbooks
that match this skeleton. **Every section here is required**: the
static check and the validation rubric verify them.

## Scope

What this surface covers, and what it explicitly does not. Mention
the intent dimensions (audit / design / debug / etc.) this surface
participates in.

- In:
- Out:
- Intents this surface answers:

## Grounding

Map this playbook's concepts back to the sources listed in
`skill.json.inspired_by`. One bullet per source. Each source should
also appear in the source's own `playbooks` list in `skill.json`.

- `<Source A>` (author, year) — contribution to this surface
- `<Source B>` (author, year) — contribution to this surface

Avoid distinctive phrasing and long quotes; paraphrase into the
skill's operational vocabulary.

## Good signals

Two to five observable signs the agent is applying this playbook
correctly. Phrase each as a *check*, not an exhortation.

- Signal 1
- Signal 2

## Common failures

Anti-patterns specific to this surface. Each failure names a
mechanism, not a vague warning.

- Failure 1 — when it happens, why it happens, what to do instead
- Failure 2 —

## Heuristics

The load-bearing content. Each heuristic is tagged with one or more
intents in parentheses so the agent knows when to surface it.

- (audit, design) Heuristic 1 — short rule of thumb
- (debug) Heuristic 2 —
- (edge-pass) Heuristic 3 —

Aim for 5–12 heuristics per playbook. Fewer than 3 is a sign the
surface should fold into a neighbor; more than 15 is a sign the
surface should split.

## Quick diagnostic

Binary questions with named actions, used when the agent enters this
surface without knowing which heuristic to apply.

- Q1 — yes → action; no → action
- Q2 — yes → action; no → action

## Cross-references

Pointers to neighbor playbooks, shared rubrics in `references/core/`,
and the intent CSV row that routes here.

- `references/playbooks/<neighbor>.md` — when to consult instead
- `references/core/<rubric>.md` — shared scale this playbook uses
- `references/intents/<intent>.csv` row `<surface>` — the entry point

## Word budget

Target 400–1500 words per playbook. Below 400 words: probably folds
into a neighbor. Above 1500: probably splits, or the surface itself
is two surfaces masquerading as one.
