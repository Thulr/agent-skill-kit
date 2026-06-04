---
date: 2026-06-03
harness: codex
sub-surface: gates
severity: 2
status: resolved
related: []
---
# Two published skills shipped descriptions over Codex's 1024-char limit and were silently skipped

## What happened

Codex logged, on every session start:

```
⚠ Skipped loading 2 skill(s) due to invalid SKILL.md files.
⚠ /Users/justin/.agents/skills/docs-design/SKILL.md: invalid description: exceeds maximum length of 1024 characters
⚠ /Users/justin/.agents/skills/docs-audit/SKILL.md: invalid description: exceeds maximum length of 1024 characters
```

The parsed frontmatter `description` was 1123 chars (`docs-design`) and 1107
chars (`docs-audit`) — the only two skills in the repo over 1024 (next highest
was `perf-design` at 952). Both routing-dense descriptions had accreted "Do NOT
use … (use X)" fences over several PRs (most recently #48) and crossed the
ceiling. `just check` passed the whole time: nothing gated description length.
Claude Code loaded the skills fine, so the defect was invisible until Codex —
which enforces the 1024 limit hard — surfaced it to the user.

This is the same failure class the existing `check_skill_md_frontmatter` gate
was built for ("the skills CLI runs a real YAML parser and silently SKIPS a
skill whose frontmatter won't parse"): a downstream loader dropping a published
skill for a frontmatter defect our checks didn't model.

## What to do differently

Gate the parsed description length in the one shared place that already parses
the frontmatter. Added `MAX_DESCRIPTION_CHARS = 1024` and a length check to
`check_skill_md_frontmatter` in `scripts/check-release-contract.py`, right after
the required-key loop. Because `check-release-contract.py` also enforces that
`skill.json.description` mirrors the SKILL.md value, gating the parsed string
covers both files. The error message names the offending length and tells the
author to trim routing prose (moving marketing/provenance to
`metadata.catalog_summary`) — consistent with the repo's error-message bar.

1024 is an external platform contract (Codex CLI + skills loader), not a rule
extrapolated from observed failures, so it does not sit under the W1 ≥3
promotion floor — same footing as the YAML-parse gate beside it.

## Closed by

Trimmed both descriptions to 995 (`docs-design`) / 997 (`docs-audit`) chars,
preserving every routing fence and trigger phrase, and synced the mirrored
`skill.json` descriptions. Added the `MAX_DESCRIPTION_CHARS` gate to
`scripts/check-release-contract.py` so a future over-limit description fails
`just check` and CI before release. `just check` green.
