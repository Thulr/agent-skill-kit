# Severity rubric (0–4)

Apply to every finding in an audit, every risk in a design, every step
in a refactor runbook, and every caveat in an explanation.

| Level | Label | Meaning |
|------:|-------|---------|
| 4 | **Critical** | Dependency-rule violation in the core path; data corruption risk; security boundary failure. Block release / merge. |
| 3 | **High** | Architectural seam reversed (e.g., domain importing infrastructure); change costs compound across all future work; refactor is large but tractable. |
| 2 | **Medium** | Anti-pattern present but contained (e.g., anemic entity in a non-core subdomain); fix when next touching the code. |
| 1 | **Low** | Stylistic deviation from the chosen approach; no behavioral impact; queue for cleanup if it accumulates. |
| 0 | **Note** | Observation worth recording; not a defect. E.g., "this boundary is unusual but defensible because X." |

## How to pick a level

1. **Blast radius.** Does this affect the whole system (4), one module
   (3), one feature (2), one file (1), or nothing observable (0)?
2. **Reversibility.** Critical and High changes get harder to fix the
   longer they sit; Medium and Low can be deferred without compounding.
3. **Discipline cost.** A Critical violation invalidates downstream
   reasoning ("if the dependency rule doesn't hold here, where does it
   hold?"). Mark accordingly.

## Calibration anchors

- "Repository interface lives in the infrastructure layer, domain
  imports it" → **4** (dependency rule reversed in the core path).
- "Use case calls an HTTP client directly without an outbound port" →
  **3** (architectural seam reversed).
- "Aggregate has a getter for a child collection that callers mutate
  in place" → **2** (encapsulation violation, contained).
- "Naming convention differs from the chosen DDD style" → **1**.
- "Two bounded contexts share a Customer concept with the same shape" →
  **0** if the shapes were independently arrived at; **2** if it was
  copy-paste with no translation layer.
