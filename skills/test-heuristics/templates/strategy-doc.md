# Test Strategy

**Subject:** [Module / service / product area]
**Persona:** suite operator

## Purpose-by-purpose coverage

| Purpose | Layer choice | Rationale |
|---|---|---|
| Spec (drives design) | unit | … |
| Regression (guards fix) | unit / integration | … |
| Characterization (locks legacy) | … | … |
| Exploration | exploratory | … |
| Gate (perf / contract / SLO) | … | … |

## Layer investments

| Layer | Investment | Rationale |
|---|---|---|
| unit | high | fast feedback on logic-heavy modules |
| integration | medium | one test per significant boundary |
| e2e-ui | low | minimum journey only; cost vs signal |
| … | … | … |

## What we're explicitly NOT testing at each layer

[Calling out the holes by design beats finding them by accident]

## Verification

[How we'll know the strategy is working: lead time, flake rate, escape rate, time-to-detect]
