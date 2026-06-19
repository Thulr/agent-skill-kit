# Score rubric (0–10) — REVIEW only

One integer per surface, summarizing how well an agent can act through the surface: it can
perceive state, target actions deterministically, act within gated authority, and the
human/agent trade-offs are resolved with dual paths. The audit report carries one score per
surface plus a brief justification citing the playbook's heuristics.

| Score | Band | Meaning |
|------:|------|---------|
| 9–10 | **Exemplary** | Could teach from it. State/actions/results are machine-readable; controls have stable semantic handles; actions are idempotent/guarded; irreversible actions gate in-path with scoped on-behalf consent; load-bearing facts have a human + machine path. |
| 7–8 | **Healthy** | Minor gaps, documented and contained. No unguarded irreversible action, no unperceivable load-bearing control. |
| 5–6 | **Mixed** | Recognizable but several Medium issues — unobservable results, a non-idempotent non-destructive action, an unnamed trade-off. Cleanup pays off this quarter. |
| 3–4 | **Eroded** | Human-only affordances, coordinate-only targets, or ungated irreversible actions are pervasive; High-severity issues compound; agents fail or act past authority. |
| 1–2 | **Tangled** | The surface fights the agent — invisible state, brittle targets, unguarded destructive actions, no on-behalf consent. Critical findings present. |
| 0 | **Absent** | No agent-perceivable/actionable surface; pixels only. |

## How to pick a score

- Start at 5. Move up for each health signal (machine-readable state, stable handles, idempotent
  actions, in-path gating, visible scoped consent, dual human+machine paths). Move down for each
  Critical or High finding.
- A single Critical finding (an unguarded irreversible action) caps the score at 4.
- Two or more High findings cap the score at 6.
- The score is a summary, not a sum — multiple Low findings should not push a healthy surface
  below 7 by themselves.

## Cross-surface comparison

Scores are comparable only within the same REVIEW run, using the same persona and project
tier. Do not benchmark across teams or across time without recalibrating against the rubric
anchors in `severity-rubric.md`.
