# Diagnose-Experience Playbook

Finding why an experience feels flat or loses people — walking it against the narrative arc
and naming the specific missing or weak beat.

## Scope

- In: comparing an existing experience to the arc; locating the missing/weak beat (no clear
  goal, no inciting incident, anticlimax, dead cliffhanger); pinpointing where users emotionally
  drop and why.
- Out: building the target arc from scratch (→ `map-journey`); fixing usability/accessibility
  defects in the built UI (→ `ux-audit`); pitching the fixed story (→ `narrate-concept`).
- Cross-references: diagnose against the baseline arc from `map-journey`.

## Grounding

- *The User's Journey* (Lichaw) — mapping a flow onto the arc reveals how users emotionally move
  through it and where the story stalls; the arc's beats are the diagnostic checklist.

## Good signals

- The diagnosis names a specific beat that is missing or weak, not a vague "needs more delight."
- It identifies where the user's goal or motivation goes unclear or unrewarded.
- It distinguishes a story break (a narrative gap) from a usability nit (a UI defect).
- It locates the drop-off at a beat boundary and explains the emotional reason.

## Common failures

- Confusing a usability problem (a confusing button, a slow load) with a story break — route the
  former to `ux-audit`.
- Over-dramatizing a habitual or nonlinear flow that legitimately has no arc.
- "Add more delight" with no named beat — undiagnosable and unactionable.
- Treating every drop-off as a story problem when the inciting incident (the reason to care) was
  never established.

## Heuristics

- Lay the current experience on the arc and ask, beat by beat: is the protagonist's goal clear?
  Is there an inciting incident? Do stakes rise? Is there a real climax/payoff?
- Find the first beat that is missing or weak — that is usually where the experience breaks.
- Locate drop-off at beat boundaries; name the unmet need or unpaid-off setup that caused it.
- Separate narrative gaps from interface defects; only the former is in scope here.
- If the flow has no natural arc (a reference tool, a habitual utility), say so rather than
  forcing a story onto it.

## Quick diagnostic

- Can you point to the exact missing/weak beat? No → walk the arc again until you can.
- Is the problem a narrative gap or a UI defect? UI → route to `ux-audit`.
- Was an inciting incident ever established? No → that is likely the root cause.
- Does this experience even have an arc? No → don't force one; recommend a different lens.

## Cross-references

- `references/playbooks/map-journey.md` — the target arc to compare against.
- `references/intent-router.csv` row `diagnose-experience` — the entry point.
