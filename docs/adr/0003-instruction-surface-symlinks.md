# ADR 0003: Keep One Instruction Surface via Symlinks

**Status:** Accepted (2026-05-16)

## Context

Different harnesses read different “instruction surface” files:

- `AGENTS.md` (portable surface used by multiple tools)
- `CLAUDE.md` (Claude Code)
- `.github/copilot-instructions.md` (GitHub Copilot)

Maintaining these as separate files creates a drift risk: one gets updated, the
others do not, and agents receive conflicting guidance.

## Decision

Maintain `AGENTS.md` as the single source of truth, and keep harness-specific
instruction files as symlinks:

- `CLAUDE.md` → `AGENTS.md`
- `.github/copilot-instructions.md` → `../AGENTS.md`

Enforce this via `scripts/check-instruction-surface.sh`, run in `just check` and
CI.

## Consequences

- Updates happen in one place (`AGENTS.md`), reducing conflicting instructions.
- CI fails fast if a symlink is replaced with a copied file.
- Some tools that do not follow symlinks will not pick up instructions; for those
  harnesses, add an equivalent configuration surface rather than duplicating text.

