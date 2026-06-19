# Score rubric (0–10) — REVIEW only

One integer per surface, summarizing how well a running agent system is *operated*: observable,
its loop actually closes, autonomy is gated, it is reliable and bounded in cost, and it is
governed. The audit report carries one score per surface plus a brief justification citing the
playbook's heuristics.

| Score | Band | Meaning |
|------:|------|---------|
| 9–10 | **Exemplary** | Could teach from it. Spans carry prompt/completion/tool I/O; trajectories graded as paths; traces feed evals and rollback; loop readiness proven by observed emission; autonomy gated by held-out evals + circuit-breakers; release gates decomposed by failure mode; maturity placed and governed. |
| 7–8 | **Healthy** | Minor gaps, documented and contained. No ungated autonomy, no single-metric gate, no telemetry theater. |
| 5–6 | **Mixed** | Recognizable but several Medium issues — dashboards that don't close the loop, readiness scored from fields, per-step bars mistaken for production. Cleanup pays off this quarter. |
| 3–4 | **Eroded** | Telemetry theater, trajectory blindness, or god-gate release gates are pervasive; High-severity issues compound; the loop does not actually improve anything. |
| 1–2 | **Tangled** | The system operates blind — ungated autonomy, no circuit-breakers, no reconstructable signal. Critical findings present. |
| 0 | **Absent** | No identifiable operating loop; ad-hoc only. |

## How to pick a score

- Start at 5. Move up for each health signal (reconstructable spans, path-graded trajectories,
  traces that become evals/rollback, observed-emission readiness, gated autonomy, decomposed
  release gates, placed maturity). Move down for each Critical or High finding.
- A single Critical finding (ungated autonomy, no circuit-breaker, unreconstructable signal)
  caps the score at 4.
- Two or more High findings cap the score at 6.
- The score is a summary, not a sum — multiple Low findings should not push a healthy surface
  below 7 by themselves.

## Cross-surface comparison

Scores are comparable only within the same REVIEW run, using the same persona and project
tier. Do not benchmark across teams or across time without recalibrating against the rubric
anchors in `severity-rubric.md`.
