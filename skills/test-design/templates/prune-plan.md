# Test Prune Plan

**Scope:** [Suite or directory or layer]
**Persona:** suite operator

## Deletion candidates

| Test | Layer | Reason | Failure mode | Severity of keeping |
|---|---|---|---|---|
| `path::name` | unit | Duplicates X | cost | 2 |
| `path::name` | e2e-ui | Quarantined 30 days | flakiness | 3 |
| `path::name` | unit | Characterizes dead code | cost, confusion | 2 |

## Quarantine candidates (delete after N days if no triage)

| Test | Layer | Why quarantine | Deadline |
|---|---|---|---|

## Verification

[How we'll know the prune was right: suite runtime drop, no escape uptick, etc.]

## Grounding sources applied

- [skill.json inspired_by entry] — [deletion or quarantine principle it informed]
