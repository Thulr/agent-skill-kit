# Score Rubric

Use for audit summaries after recording individual findings with the severity rubric.

| Score | Interpretation |
|---|---|
| 0 | No usable documentation for the target audience; core tasks require guessing. |
| 1–2 | Fragmentary docs exist but are stale, unfindable, or unsafe for the main task. |
| 3–4 | Some paths work, but first success, recovery, or retrieval fails for common cases. |
| 5–6 | Adequate baseline: users can complete common tasks with effort; gaps remain in examples, errors, accessibility, versioning, or agent readability. |
| 7–8 | Strong docs: mode separation, tested examples, actionable errors/help, stable links, and audience-specific paths are mostly present. |
| 9 | Excellent: docs are current, measured, accessible, retrieval-friendly, and conflict-tested across audiences. |
| 10 | Reference quality: examples and contracts are CI-verified, telemetry closes the loop, agents and humans share a drift-resistant source of truth, and new product work cannot ship without docs coverage. |

## Scoring rules

- Score the documented user journey, not the docs team's effort.
- A critical severity finding caps the score at 4.
- A high severity finding caps the score at 6 unless it is explicitly scoped out.
- Missing measurement caps a program-level score at 8 even when page quality is high.
- Missing accessibility basics caps public end-user help at 6.
- Missing machine-readable contracts caps agent-facing API/tool docs at 6.
