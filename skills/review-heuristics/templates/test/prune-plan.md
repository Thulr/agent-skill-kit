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

## Findings ledger

If this prune plan has 7+ candidates, any severity 3–4 candidate, or a
save/track request, create both tracking artifacts now: the Markdown ledger
from `templates/test/findings-ledger.md` at
`docs/audits/test-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
and the workflow state from `templates/test/workflow-state.json` at
`docs/audits/test-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
If the target is not a repo or `docs/audits/` is not writable, use matching
`audit-artifacts/test-heuristics-...` paths. Report both paths; do not merely
offer tracking. Roadmaps and external issues require explicit confirmation.

## Verification

[How we'll know the prune was right: suite runtime drop, no escape uptick, etc.]

## Grounding sources applied

- [skill.json inspired_by entry] — [deletion or quarantine principle it informed]
