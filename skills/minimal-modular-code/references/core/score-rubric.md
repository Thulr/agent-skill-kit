# Score rubric (0–10) — REVIEW only

One integer per surface, summarizing how minimal, legible, and parallel-ready the surface is.
The audit report carries one score per surface plus a brief justification citing the
playbook's heuristics.

| Score | Band | Meaning |
|------:|------|---------|
| 9–10 | **Exemplary** | Could teach from it. Reused over rebuilt; deep modules behind simple interfaces; dependency direction clean; load-bearing boundaries enforced by gates; names grep-unique. |
| 7–8 | **Healthy** | Minor slop, documented and contained. No load-bearing coupling or un-enforced invariant. |
| 5–6 | **Mixed** | Recognizable but several Medium issues — duplication, shallow modules, dense or unclear code, weak gates. Cleanup pays off within a quarter. |
| 3–4 | **Eroded** | Slop and coupling are pervasive; High-severity issues compound; parallel work is risky. Strangler-style cleanup more realistic than incremental tidying. |
| 1–2 | **Tangled** | Structure works against itself — wrong-direction dependencies, no stable contracts, no safe concurrency. Critical findings present. |
| 0 | **Absent** | No identifiable structure; ad-hoc only. |

## How to pick a score

- Start at 5. Move up for each health signal (reuse over duplication, deep modules, clean
  dependency direction, enforced boundaries, grep-unique names, partitionable work). Move
  down for each Critical or High finding.
- A single Critical finding caps the score at 4.
- Two or more High findings cap the score at 6.
- The score is a summary, not a sum — multiple Low findings should not push a healthy surface
  below 7 by themselves.

## Cross-surface comparison

Scores are comparable only within the same REVIEW run, using the same persona and the same
project tier. Do not benchmark across teams or across time without recalibrating against the
rubric anchors.
