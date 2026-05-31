# Severity Rubric — 0–4

Applied to every finding in `harden`, `scaffold`, `diagnose`, and to each gap in `assess`. Shares the 0–4 scale with `skills/dx-critique/references/core/severity-rubric.md`; adapted to agent-specific failure language.

| Score | Label | Description | Examples |
|-------|-------|-------------|----------|
| 0 | Cosmetic | Style or convention nit. No measurable agent-behavior impact. | Inconsistent heading levels in AGENTS.md; minor wording choice. |
| 1 | Minor friction | Agent occasionally trips but recovers. Doc clarity issue, weak example, or recoverable ambiguity. | A worked example is slightly outdated; the agent burns a few extra tokens but finishes the task. |
| 2 | Significant | Agent regularly trips. Wastes tokens, causes wrong-file edits, or produces low-quality output. | Two nested AGENTS.md files contradict each other; agent picks one arbitrarily. |
| 3 | Blocking | Agent reliably fails or produces unsafe output. Missing gate, ambiguous critical rule, or untestable acceptance criterion. | No approval tier for DB migrations; agent rewrites a migration in place. |
| 4 | Dangerous | Active exploit path, privilege escalation, exfiltration vector, sandbox escape, or runaway-autonomy risk. | AGENTS.md is editable by anyone and is loaded into Claude/Cursor every session — a known injection vector. |

## How to use

- Every finding emitted by any intent must carry a severity score.
- For `assess`: aggregate severity-3 and severity-4 findings into the "blocking gaps" section of the report.
- For `harden`: severity drives ordering — close 4s and 3s first.
- For `diagnose`: severity is the impact-of-recurrence, not the impact-of-this-failure.
- For `scaffold`: severity tags each generated file with the failure mode it closes.

## Notes

- A finding's severity is independent of its layer or surface.
- A single missing artifact can be severity 1 for `cold-context-agent` (minor friction) and severity 4 for `adversarial` (exfiltration vector). Report the **higher** severity and note the contributing lenses.
