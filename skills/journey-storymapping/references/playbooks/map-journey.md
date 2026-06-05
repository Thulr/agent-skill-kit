# Map-Journey Playbook

Building a story-structured journey — casting the user as protagonist and laying their
experience onto a narrative arc, beat by beat.

## Scope

- In: choosing the story type (concept / origin / usage); naming the protagonist and their
  goal; laying the arc (exposition → inciting incident → rising action → crisis → climax →
  resolution); marking where the experience should peak.
- Out: diagnosing an existing experience (→ `diagnose-experience`); writing the pitch narrative
  (→ `narrate-concept`); usability evaluation of the built screens (→ `ux-audit`).
- Cross-references: a mapped arc is the baseline `diagnose-experience` compares against.

## Grounding

- *The User's Journey* (Lichaw) — storymapping: map the intended experience plot point by plot
  point, with the user as protagonist; the concept / origin / usage story types; the narrative
  arc that peaks near the end.

## Good signals

- The protagonist is the user with a concrete goal; the product is the helper, not the hero.
- The chosen story type fits the question (concept = the why/value, origin = arriving/onboarding,
  usage = the recurring core loop).
- Every beat of the arc is present, including an inciting incident and a clear climax.
- The map shows where the experience peaks and how the user feels at each beat.

## Common failures

- Making the product the hero — the arc becomes a feature demo, not the user's story.
- A flat list of steps with no inciting incident, no rising stakes, and no climax.
- Mixing story types — an origin story that wanders into the core usage loop.
- A climax buried in the middle, so the experience deflates before it ends.

## Heuristics

- Name the protagonist and the single goal that pulls them through before drawing any beats.
- Pick one story type per map; if you need all three, make three maps.
- Place the inciting incident early — the moment a need becomes urgent — and build rising action
  toward a climax near the end.
- For each beat, note what the user does and how they feel, so the emotional curve is visible.
- Put the peak (the payoff/aha) close to the end; everything before it should build toward it.

## Quick diagnostic

- Who is the protagonist — the user or the product? Product → recast the user as the hero.
- Is there an inciting incident and a climax? No → add the missing beats.
- Is it one story type or a blur? Blur → split into concept / origin / usage maps.
- Does the experience peak near the end? No → resequence so it builds.

## Cross-references

- `references/playbooks/diagnose-experience.md` — test an existing experience against this arc.
- `references/playbooks/narrate-concept.md` — turn the concept beat into a pitch.
- `references/intent-router.csv` row `map-journey` — the entry point.
