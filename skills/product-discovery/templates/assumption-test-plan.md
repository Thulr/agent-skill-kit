# Assumption Test Plan: <bet / solution>

Output shape for the `test-assumptions` intent. Map the assumptions, prioritize by risk and
evidence, then plan the cheapest test for the riskiest one.

## The bet

- **Solution / bet:** <what we're considering building>
- **Tied to opportunity / outcome:** <…>

## Assumption map

<Every assumption the bet needs true, by type. Rank by importance × (lack of) evidence.>

| Assumption | Type (desirability / viability / feasibility) | Importance | Evidence today | Priority |
|---|---|---|---|---|
| <assumption> | desirability | hi | none | **1 (test first)** |
| <assumption> | feasibility | hi | some | 2 |
| <assumption> | viability | med | none | 3 |

## Test the riskiest first

- **Assumption under test:** <the top-priority one>
- **Experiment:** <cheapest test that yields real evidence — prefer behavioral over stated intent>
- **What we'll measure:** <metric>
- **Pass / fail threshold (set before running):** <confirm if ≥ X; kill if < Y>
- **Effort / cost / time:** <…>

## After the result

- **Result & decision:** <persevere / pivot / kill>
- **Re-rank:** <which assumption is now riskiest>

> Don't call interview or survey enthusiasm "validation" for an assumption that needed a
> behavioral test.
