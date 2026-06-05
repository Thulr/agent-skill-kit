# Test-Assumptions Playbook

Surfacing the assumptions a bet rests on, ranking them by risk and evidence, and choosing
the cheapest experiment that produces real evidence on the riskiest one first.

## Scope

- In: enumerating desirability/viability/feasibility assumptions; plotting them by importance ×
  evidence; selecting an experiment proportional to the risk; defining what evidence would
  confirm or kill the assumption.
- Out: framing the outcome (→ `frame-outcomes`); generating the solutions whose assumptions you
  test (→ `map-opportunities`); the interview mechanics of a qualitative test (→
  `customer-interviewing`); scoping the build (→ `scope-mvp`).
- Cross-references: assumptions usually come from the leaves of the opportunity tree.

## Grounding

- *Testing Business Ideas* (Bland & Osterwalder) — assumptions mapping across desirability,
  viability, and feasibility; prioritizing by importance and evidence; running the cheapest
  experiment that yields evidence on the riskiest, least-evidenced assumption.
- *Inspired* (Cagan) — the four product risks (value, usability, feasibility, viability) as the
  categories of assumption a discovery effort must reduce.

## Good signals

- The assumptions a bet depends on are written explicitly, across desirability, viability, and
  feasibility (or value/usability/feasibility/viability).
- Each is ranked by how important it is and how much evidence exists.
- The chosen experiment is the cheapest one that still moves the evidence on the riskiest assumption.
- Pass/fail evidence is defined before the experiment runs.

## Common failures

- Testing what is easy or comfortable rather than what is riskiest and least proven.
- Calling a survey or a single interview "validation" when the assumption needed a behavioral test.
- One elaborate experiment where three cheap ones would learn faster.
- No predefined success threshold, so any result is read as encouraging.

## Heuristics

- List the assumptions the bet would need true; sort by importance × (lack of) evidence and start
  top-right (most important, least evidence).
- Match the experiment to the risk: cheap, fast signals first; escalate fidelity only as evidence accrues.
- Prefer evidence of behavior (what people did) over stated intent (what they say they'd do),
  especially for desirability.
- State the metric and threshold that would confirm or kill the assumption before you run the test.
- Re-rank after each result — new evidence changes which assumption is now riskiest.

## Quick diagnostic

- Are the bet's assumptions written down and categorized? No → map them first.
- Is the riskiest, least-evidenced assumption the one you're testing? No → re-prioritize.
- Does the experiment produce behavioral evidence or just opinions? Opinions → pick a stronger test.
- Did you set a pass/fail threshold up front? No → set it before running.

## Cross-references

- `references/playbooks/map-opportunities.md` — the solutions whose assumptions you're testing.
- `references/playbooks/frame-outcomes.md` — the risk you named to test.
- `references/intent-router.csv` row `test-assumptions` — the entry point.
