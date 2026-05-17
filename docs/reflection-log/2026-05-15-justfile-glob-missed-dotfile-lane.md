---
date: 2026-05-15
harness: claude-code
sub-surface: gates
severity: 3
status: resolved
related: []
---
# Justfile glob silently skipped the .experimental install lane

## What happened

`project-agentification` skill (`assess` intent) was asked to run `just check`
and verify all skill static checks pass. It reported "all checks passed" —
true for the 2 published skills under `skills/*/`, but the Justfile glob
`skills/*/evals/run-static-checks.sh` does not match dotfile directories, so
`skills/.experimental/project-agentification/evals/run-static-checks.sh` was
silently skipped. Two of ten sub-agents flagged this independently.

## What to do differently

**Path-based gates must enumerate all three install lanes.** Use explicit
globs for `skills/*`, `skills/.experimental/*`, and `.agents/skills/*`, or
set `shopt -s dotglob`. When adding any new gate (glob, CI matrix, ignore
pattern, hook), verify it picks up at least one skill in each lane.

Promoted to AGENTS.md Rule 1.

## Closed by

AGENTS.md Rule 1 ("Path-based gates enumerate every install lane") + Justfile
glob updated to enumerate the three lanes explicitly. Validated in `just check`
and `.github/workflows/ci.yml`.
