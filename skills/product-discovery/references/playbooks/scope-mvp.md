# Scope-MVP Playbook

Scoping a minimum viable product as the smallest test of the value hypothesis, working
down the product-market-fit pyramid toward fit.

## Scope

- In: clarifying the target customer and underserved need; stating the value proposition;
  selecting a minimal feature set; defining the value hypothesis the MVP tests and the
  fit signal; planning build-measure-learn iteration.
- Out: framing the business outcome (→ `frame-outcomes`); eliciting the needs (→ `define-jobs`,
  `customer-interviewing`); testing non-MVP assumptions (→ `test-assumptions`); building the UI
  (→ `ui-design`).
- Cross-references: scope an MVP only after the target need is clear and the riskiest assumptions
  are identified.

## Grounding

- *The Lean Product Playbook* (Olsen) — the lean product process and product-market-fit pyramid:
  target customer → underserved needs → value proposition → MVP feature set → UX → test, iterated
  build-measure-learn toward fit; the MVP is the smallest thing that tests the value hypothesis.

## Good signals

- The MVP is tied to a named target customer and a specific underserved need.
- The value proposition is explicit and differentiates from the alternatives the customer has now.
- The feature set is the minimum that tests value — scope is justified by the hypothesis, not by
  completeness.
- A fit signal (the metric/behavior that would show product-market fit) is defined before building.

## Common failures

- "MVP" that is just a small first version with no hypothesis being tested.
- Skipping target-customer and underserved-need clarity and over-building toward assumed fit.
- A feature set padded with "while we're at it" scope that does not serve the value test.
- Treating launch as the goal rather than the learning the MVP is meant to produce.

## Heuristics

- Trace the pyramid top-down: confirm target customer and underserved need, state the value prop,
  then derive the minimal feature set that tests it.
- Define the MVP as the smallest build that produces a real signal on the value hypothesis.
- Cut any feature that does not serve the value test this iteration; defer it explicitly.
- Name the fit signal and threshold before building, and plan the build-measure-learn loop that
  follows.
- If the riskiest assumption can be tested without code, test it before scoping the MVP at all.

## Quick diagnostic

- Is the MVP tied to a named customer and underserved need? No → fix that before scoping.
- What value hypothesis does this MVP test? Can't answer → it's a v1, not an MVP.
- Does every feature serve the value test? No → cut or defer it.
- Do you know what signal would show fit? No → define it before building.

## Cross-references

- `references/playbooks/define-jobs.md` — the underserved need the MVP serves.
- `references/playbooks/test-assumptions.md` — test before you build where you can.
- `references/intent-router.csv` row `scope-mvp` — the entry point.
