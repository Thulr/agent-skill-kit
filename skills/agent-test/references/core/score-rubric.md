# Score rubric (0–10) — REVIEW only

One integer per surface, summarizing how *trustworthy* the measurement is: decomposed to failure
modes, judges calibrated, paths graded (not just spans), benchmarks held-out and
gaming-resistant, activation tested. The audit report carries one score per surface plus a brief
justification citing the playbook's heuristics.

| Score | Band | Meaning |
|------:|------|---------|
| 9–10 | **Exemplary** | Could teach from it. Failure modes named and localized; judges calibrated with bias checks + explanations; trajectories graded as paths; benchmarks held-out, per-slice, baseline+rollback; activation tested positive/negative/edge; re-run on change. |
| 7–8 | **Healthy** | Minor gaps, documented and contained. No invalid instrument, no uncalibrated gate. |
| 5–6 | **Mixed** | Recognizable but several Medium issues — per-step-only bars, thin activation cases, evals not re-run on change. Cleanup pays off this quarter. |
| 3–4 | **Eroded** | Vague judges, god-gate pass-rates, or trajectory blindness are pervasive; High-severity issues compound; the suite certifies more than it measures. |
| 1–2 | **Tangled** | The instruments mislead — memorizing benchmarks, uncalibrated gates, no path grading. Critical findings present. |
| 0 | **Absent** | No identifiable measurement; vibes only. |

## How to pick a score

- Start at 5. Move up for each health signal (named+localized failure modes, calibrated judge
  with explanations, path-graded trajectories, held-out per-slice benchmark, tested activation,
  re-run-on-change). Move down for each Critical or High finding.
- A single Critical finding (invalid instrument trusted as the gate) caps the score at 4.
- Two or more High findings cap the score at 6.
- The score is a summary, not a sum — multiple Low findings should not push a healthy surface
  below 7 by themselves.

## Cross-surface comparison

Scores are comparable only within the same REVIEW run, using the same persona and project
tier. Do not benchmark across teams or across time without recalibrating against the rubric
anchors in `severity-rubric.md`.
