# Score rubric (0–10) — REVIEW only

One integer per surface, summarizing how *agent-consumable* it is: typed and stable as a
contract, recoverable by a stochastic consumer, and safe at the trust boundary. The audit
report carries one score per surface plus a brief justification citing the playbook's
heuristics.

| Score | Band | Meaning |
|------:|------|---------|
| 9–10 | **Exemplary** | Could teach from it. Typed schemas derived from code; errors a stable typed envelope; output validated with typed refusals; loop bounded and verified; tool metadata scanned and credentials isolated; spans on one named convention. |
| 7–8 | **Healthy** | Minor drift, documented and contained. No trust-boundary gap, no unrecoverable error path. |
| 5–6 | **Mixed** | Recognizable but several Medium issues — hand-written schemas, one switch over content+structural telemetry, partial guardrails. Cleanup pays off within a quarter. |
| 3–4 | **Eroded** | Unrecoverable error paths, string-only output, or an unguarded trust boundary are pervasive; High-severity issues compound; agents loop or fail silently. |
| 1–2 | **Tangled** | The surface works against its consumer — no stable contracts, secrets in context, no injection defense. Critical findings present. |
| 0 | **Absent** | No identifiable agent-facing contract; ad-hoc only. |

## How to pick a score

- Start at 5. Move up for each health signal (typed schemas from code, stable error codes,
  validated output with refusals, bounded+verified loop, isolated credentials, scanned tool
  metadata, single-convention spans). Move down for each Critical or High finding.
- A single Critical finding (trust-boundary or broken core contract) caps the score at 4.
- Two or more High findings cap the score at 6.
- The score is a summary, not a sum — multiple Low findings should not push a healthy surface
  below 7 by themselves.

## Cross-surface comparison

Scores are comparable only within the same REVIEW run, using the same persona and project
tier. Do not benchmark across teams or across time without recalibrating against the rubric
anchors in `severity-rubric.md`.
