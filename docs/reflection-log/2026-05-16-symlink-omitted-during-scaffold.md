---
date: 2026-05-16
harness: claude-code
sub-surface: instruction-surface
severity: 3
status: resolved
related: []
---
# Scaffold wrote AGENTS.md and hook but skipped the symlink step

## What happened

`project-agentification` skill (Stage 1 `scaffold` intent) was asked to
scaffold the instruction-surface (AGENTS.md + symlink contract). Wrote
`AGENTS.md` and the Claude PreToolUse hook, but skipped the prescribed
`ln -sf AGENTS.md CLAUDE.md` and `ln -sf ../AGENTS.md .github/copilot-instructions.md`.

The `instruction-surface` playbook's H2-harden lists the symlink + CI
assertion explicitly, and the `maintainer` lens names "AGENTS.md and
CLAUDE.md drift instead of one being a symlink" as a failure mode it
catches. Neither caught it.

## What to do differently

**Post-write auditor lens.** Pre-write lens dispatch (step 5) didn't catch
the omission because there was nothing on disk yet to audit. Add step 8.5:
after write-to-disk confirmation, dispatch a fresh-context auditor sub-agent
that re-reads the chosen playbook + the git diff and flags every `harden`
heuristic that wasn't applied. Verification external to the writer;
checklist self-attestation gets rubber-stamped.

## Closed by

SKILL.md workflow step 8.5 ("post-write audit") + `references/lenses.md`
post-write auditor persona. The scaffold-bundle template now includes a
post-write audit table the auditor fills out.
