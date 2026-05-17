---
date: 2026-05-15
harness: claude-code
sub-surface: skills
severity: 3
status: resolved
related: []
---
# Three incompatible trigger-evals.json schemas across skills

## What happened

`project-agentification` skill (`assess` intent) was asked to audit eval
coverage across the `skills/` tree. Found three incompatible
`trigger-evals.json` schemas in three skills:

- `dx-heuristics` used `[{query, should_trigger}]`.
- `test-heuristics` used `{skill, queries: [{query, should_activate, expected_route}]}`.
- `project-agentification` used `{skill, version, should_match, should_not_match, edge_cases}`.

No runner exists because none could handle all three; the files were dead
weight.

## What to do differently

**Skills share a canonical `trigger-evals.json` schema.** Define it in
`AGENTS.md`; enforce via each skill's `run-static-checks.sh`. Schema changes
migrate all skills in the same PR.

Later promoted further: the canonical schema was extracted to
`schemas/trigger-evals.schema.json` after duplicate-inline-validators landed
twice (PR #5 and PR #7). Per-skill `run-static-checks.sh` now validates via
`scripts/validate-against-schema.py`; inline shape validators are forbidden.

## Closed by

AGENTS.md Rule 2 ("Cross-skill schema parity") + `schemas/trigger-evals.schema.json`
+ `scripts/validate-against-schema.py`. Per-skill static checks now only carry
assertions that genuinely vary per skill.
