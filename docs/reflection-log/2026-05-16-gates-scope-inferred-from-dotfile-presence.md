---
date: 2026-05-16
harness: claude-code
sub-surface: gates
severity: 3
status: resolved
related: [2026-05-16-symlink-omitted-during-scaffold]
---
# Scaffold inferred harness scope from .claude/ presence, missed other harnesses

## What happened

`project-agentification` skill (Stage 1 `scaffold` intent) was asked to
scaffold the gates layer (forbidden-action hook). Created only
`.claude/hooks/block-destructive-bash.py` and `.claude/settings.json`.
AGENTS.md punted on other harnesses ("Cursor, Codex, Copilot, etc. should
configure equivalents from this list") — the user had to do the cross-harness
work themselves. The skill inferred scope from the presence of `.claude/`
and never asked which harnesses were actually in use.

## What to do differently

**Harness-inventory step before scaffolding gates or instruction-surface.**
Add step 3.5 to the workflow: for `scaffold` or `harden` intents touching
those sub-surfaces, ask the user which harnesses are in use (Claude Code /
Cursor / Codex / Copilot / Aider / Windsurf / AGENTS.md-compatible-only).
Default to producing per-harness equivalents for every harness named, not
just the one whose dotfile happens to exist. Absence-of-dotfile is not
absence-of-use.

## Closed by

SKILL.md workflow step 4.5 ("collect harness inventory") + the scaffold-bundle
template now has a required "Harness inventory" section.
