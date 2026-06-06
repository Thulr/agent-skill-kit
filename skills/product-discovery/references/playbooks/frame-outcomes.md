# Frame-Outcomes Playbook

Turning an output request ("ship feature X") into a measurable outcome, diagnosing
feature-factory risk, and naming which product risk most threatens the bet.

## Scope

- In: reframing outputs as outcomes; diagnosing build-trap symptoms; connecting a request
  to product strategy; naming the dominant product risk (value, usability, feasibility,
  viability) for a bet.
- Out: building the opportunity tree under the outcome (→ `map-opportunities`), testing the
  named risk (→ `test-assumptions`), and scoping the build (→ `scope-mvp`).
- Cross-references: an outcome framed here becomes the root of `map-opportunities`.

## Grounding

- *Escaping the Build Trap* (Perri) — the build trap / feature factory; product strategy as
  deployable decisions; the product-kata loop (set outcome, study state, pick next step, learn).
- *Inspired* (Cagan) — measure outcomes not output; the four product risks as the things a bet
  must survive before it deserves to be built.

## Good signals

- The reframed goal is a measurable result for a segment ("move M for S by D"), not a feature.
- The request is traced to a product objective, not justified by "a stakeholder asked."
- The most uncertain of the four risks is named, with a reason.
- Output-shaped work that is genuinely necessary is acknowledged, not shamed.

## Common failures

- Feature-factory thinking — treating features shipped, velocity, or a full roadmap as the
  scoreboard while no metric moves.
- Outcome dogma — insisting every item be an outcome and dismissing legitimate output work
  (compliance, platform, table-stakes, contractual commitments).
- A vanity outcome — a metric chosen because it is easy, not because it reflects value.
- Reframing the words but keeping the predetermined solution underneath.

## Heuristics

- Restate "build X" as "for segment S, move metric M, because it reflects value V"; if you
  cannot name M, the request is not ready to prioritize.
- Ask what would be observably different in the world if this succeeded — that is the outcome.
- Map the bet against the four risks and call out the one with the least evidence; route it to
  `test-assumptions`.
- Separate the outcome (the result) from outputs (the work) and from impact (the longer-term
  business effect); keep the team accountable to the outcome.
- When work is legitimately output-shaped, say so and frame its success criteria honestly
  rather than forcing a fake metric.

## Quick diagnostic

- Is success defined as a shipped feature? Yes → restate it as a metric move for a segment.
- Can you name the metric this changes? No → find it before prioritizing.
- Which of value / usability / feasibility / viability is least proven? → route that to
  `test-assumptions`.
- Is this genuinely output work (compliance/platform)? Yes → frame honest success criteria,
  don't force an outcome.

## Cross-references

- `references/playbooks/map-opportunities.md` — build the tree under this outcome.
- `references/playbooks/test-assumptions.md` — test the named risk.
- `references/intent-router.csv` row `frame-outcomes` — the entry point.
