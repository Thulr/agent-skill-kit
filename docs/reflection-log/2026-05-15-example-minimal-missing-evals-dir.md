---
date: 2026-05-15
harness: claude-code
sub-surface: skills
severity: 3
status: resolved
related: []
---
# example-minimal had no evals/ directory, breaking the template contract

## What happened

`project-agentification` skill (`assess` intent) was asked to identify eval
gaps in the `skills/` tree. Found that `skills/example-minimal/` had no
`evals/` directory. A contributor templating from it would produce skills
that pass `npx skills add --list` but bypass the CI static-check gate
(which requires `evals/run-static-checks.sh` to exist).

## What to do differently

**`example-minimal` is the template contract.** Anything required of
published skills must exist in `example-minimal` — even as a minimal
placeholder — so the template-to-skill path can't ship ungated. Add
`evals/run-static-checks.sh` (exits 0), `evals/trigger-evals.json` (valid
shape), and `evals/activation-cases.md` (header + one example).

## Closed by

AGENTS.md Rule 3 ("`example-minimal` is the template contract") + the missing
files were added to `skills/example-minimal/evals/`.
