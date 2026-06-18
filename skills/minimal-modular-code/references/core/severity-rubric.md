# Severity rubric (0–4)

Apply to every finding in a REVIEW, every risk in a DESIGN, and every step in a refactor
runbook.

| Level | Label | Meaning |
|------:|-------|---------|
| 4 | **Critical** | A frozen contract or dependency-direction invariant broken in the core path; a change that forces serializing all parallel work; data-loss or security-boundary failure. Block merge. |
| 3 | **High** | A wrong abstraction whose cost compounds across future work; coupling that prevents parallelization; a load-bearing boundary enforced only by prose; a shallow module at a key seam. Large but tractable fix. |
| 2 | **Medium** | Contained duplication or over-abstraction; a leaky adapter off the core path; a legibility issue that measurably raises review cost. Fix when next touching the code. |
| 1 | **Low** | Stylistic verbosity, an imprecise name, a needless indirection with no behavioral impact. Queue for cleanup if it accumulates. |
| 0 | **Note** | An observation worth recording, not a defect — e.g. "this boundary is unusual but defensible because X." |

## How to pick a level

1. **Blast radius.** Whole system / all parallel work (4), one module or contract (3), one
   feature (2), one file (1), nothing observable (0)?
2. **Reversibility.** Critical and High get harder and costlier to fix the longer they sit;
   Medium and Low can be deferred without compounding.
3. **Review-attention cost.** A finding that silently consumes reviewer attention every time
   the code is touched (a wrong abstraction, an un-enforced invariant) rates higher than one
   that is merely untidy.

## Calibration anchors

- "Stable inner module imports a volatile outer one (core imports a framework type)" → **3**;
  escalate to **4** in the most stable code or across a security boundary.
- "An early abstraction is now patched with parameters and conditionals for cases it did not
  foresee (the wrong abstraction)" → **3** — the cost compounds.
- "A load-bearing boundary (forbidden import, dependency direction) is stated in prose but no
  check enforces it" → **3**.
- "A block is copy-pasted and tweaked where the two copies encode the same decision" → **2**.
- "A function name needs a comment to disambiguate it" → **1**.
- "Duplication of two fragments that encode genuinely different decisions" → **0** (not a DRY
  violation; record only if it will mislead).
