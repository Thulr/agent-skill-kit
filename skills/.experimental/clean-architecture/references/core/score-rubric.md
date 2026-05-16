# Score rubric (0–10) — audit intent only

A single integer per surface, summarizing how cleanly the surface
embodies the chosen approach. The audit report carries one score per
surface plus a brief justification citing the playbook's heuristics.

| Score | Band | Meaning |
|------:|------|---------|
| 9–10 | **Exemplary** | Could be used as a teaching example. Dependency rule holds cleanly; boundaries are explicit and minimal; vocabulary is consistent. |
| 7–8 | **Healthy** | Some deviations but they are documented and contained. No load-bearing violations. |
| 5–6 | **Mixed** | The shape is recognizable but several Medium-severity issues. Refactor would pay off within a quarter. |
| 3–4 | **Eroded** | Original shape is visible only in places. High-severity issues compound. Strangler-fig is more realistic than incremental cleanup. |
| 1–2 | **Inverted** | The architecture works against itself. Inner layers depend on outer; vocabulary is inconsistent across contexts. Critical findings present. |
| 0 | **Absent** | No identifiable architecture; ad-hoc structure only. |

## How to pick a score

- Start at 5. Move up for each piece of evidence the surface is healthy
  (clean dependency direction, explicit boundaries, consistent naming,
  testable seams). Move down for each Critical / High finding.
- A single Critical finding caps the score at 4.
- Two or more High findings cap the score at 6.
- The score is a summary, not a sum — multiple Low findings should not
  push a healthy surface below 7 by themselves.

## Cross-surface comparison

Scores are only comparable within the same audit run, using the same
persona and the same rubric. Do not benchmark scores across teams or
across time without recalibrating against the rubric anchors.
