---
date: 2026-05-15
harness: claude-code
sub-surface: governance
severity: 3
status: resolved
related: []
---
# skill.json maintainers field had opaque string, not GitHub handle

## What happened

`project-agentification` skill (Stage 0 session, drafting `CODEOWNERS`) was
asked to generate `CODEOWNERS` from each `skill.json`'s `maintainers` field.
Could not — `"maintainers": ["justin"]` is an opaque string with no GitHub
handle. Had to fall back to `gh repo view` to find the actual owner
(`Thulr`). The field appeared authoritative for automation but wasn't
programmatically useful.

## What to do differently

**Identity fields in `skill.json` must be resolvable GitHub handles**
(`@handle` or `@org/team`). Add a regex check to each skill's
`run-static-checks.sh`: each `maintainers[]` entry matches `^@[A-Za-z0-9-]+$`
or `^@[A-Za-z0-9-]+/[A-Za-z0-9-]+$`.

Later promoted further: the maintainer-handle pattern was extracted from
four duplicate inline validators into `schemas/skill.schema.json` (caught in
PR #7 review).

## Closed by

AGENTS.md Rule 4 ("Identity fields are resolvable handles") + the pattern
lives in `schemas/skill.schema.json` and is validated by
`scripts/validate-against-schema.py` in every skill's `run-static-checks.sh`.
