# Define-Jobs Playbook

Articulating the customer's job-to-be-done, mapping it into stable steps, writing
solution-free desired-outcome statements, and ranking underserved needs.

## Scope

- In: stating the core functional (and emotional/social) job; mapping the job into
  step-by-step stages; writing desired-outcome statements; ranking needs by importance vs.
  satisfaction to find underserved ones.
- Out: framing the business outcome (→ `frame-outcomes`); structuring the opportunity tree
  (→ `map-opportunities`); the interviews that surface jobs (→ `customer-interviewing`);
  testing whether addressing a need is viable (→ `test-assumptions`).
- Cross-references: jobs and underserved needs feed the opportunity space in `map-opportunities`.

## Grounding

- *Jobs to Be Done: Theory to Practice* (Ulwick) — outcome-driven innovation: the job map of
  stable, solution-free steps; desired-outcome statements (direction + metric + object +
  context); ranking opportunity as importance plus the gap between importance and satisfaction.
- *The Jobs To Be Done Playbook* (Kalbach) — practical job mapping and applying the job lens to
  product decisions.

## Good signals

- The job is stated independent of any solution and stays true over time and technology.
- The job map is a sequence of what the customer is trying to get done, not your product's steps.
- Desired-outcome statements are measurable and solution-free.
- Underserved needs (high importance, low satisfaction) are distinguished from served ones.

## Common failures

- "Jobs" that are really features or your solution restated ("the job is to use our app").
- A job map that traces your UI flow instead of the customer's real-world process.
- Outcome statements that smuggle in a solution or are unmeasurable.
- Treating every stated want as equally important without an importance/satisfaction read.

## Heuristics

- Express the core functional job as a verb + object + context, free of any solution.
- Map the job into discrete steps the customer moves through; look for struggle at each step.
- Write desired-outcome statements as direction of change + unit of measure + object + clarifier
  (e.g. "minimize the time to detect an error during checkout").
- Rank needs by importance against current satisfaction; the underserved gap is where to focus.
- Use the job and its underserved outcomes as the source material for opportunities, not invented
  feature ideas.

## Quick diagnostic

- Is the job stated without mentioning your product? No → strip the solution out.
- Does the job map follow the customer or your UI? UI → re-map around the customer's process.
- Are outcome statements measurable and solution-free? No → rewrite them.
- Do you know which needs are underserved? No → get an importance vs. satisfaction read.

## Cross-references

- `references/playbooks/map-opportunities.md` — feed underserved needs into the tree.
- `references/playbooks/frame-outcomes.md` — connect the job to a business outcome.
- `references/intent-router.csv` row `define-jobs` — the entry point.
