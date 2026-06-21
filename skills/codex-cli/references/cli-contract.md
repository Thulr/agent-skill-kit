# Codex CLI Contract

This skill is grounded in the local Codex CLI shape:

```bash
codex review --uncommitted
codex --sandbox read-only --ask-for-approval never --cd <repo> exec --ephemeral -- -
codex doctor --summary --ascii
```

`codex review` is the preferred review path because it understands git scopes
directly. `codex exec` is the preferred second-opinion path because it accepts a
prompt from stdin and can run with a read-only sandbox.

## Safe Default Flags

- `codex review --uncommitted`: review staged, unstaged, and untracked changes.
- `codex review --base <branch>`: review branch changes against a base.
- `codex review --commit <sha>`: review one commit.
- **`codex review` accepts no `[PROMPT]` with any scope flag.** Every scope
  rejects one (`error: the argument '--uncommitted' cannot be used with
  '[PROMPT]'`, and likewise `--base` / `--commit`; verified on codex-cli 0.141.0).
  So the review-prompt template and `--extra` are **not** delivered to
  `codex review` — it applies its built-in review standard. To inject a custom
  review rubric, use the `codex exec` path (`scripts/codex-ask.sh`) instead.
- `codex --sandbox read-only --ask-for-approval never --cd <repo> exec --ephemeral -- -`:
  non-interactive read-only analysis with no persisted session. Keep sandbox,
  approval, and working-directory flags before `exec`; some Codex CLI builds
  reject `--ask-for-approval` after the subcommand even when inherited help
  displays it there.
- `-- -` (for `codex exec`, not `codex review`): terminate flag parsing, then
  pass `-` as the prompt positional so Codex reads instructions from stdin. Do
  not omit the `--`; otherwise the stdin sentinel can be mistaken for a flag.
  `codex review` takes no prompt, so it never uses `-- -`.
- `--cd <dir>`: set the working root for `codex exec`.
- `-m <model>`: optional model override when the user asks.
- `-p <profile>`: optional config profile from `~/.codex/config.toml`.
- `-c key=value`: optional config override; preserve exact user intent.

The wrapper `scripts/codex-ask.sh` also supports `--cd <dir>`,
`--template <file>`, and `--skip-git-repo-check` so a caller can run neutral,
non-repo-scoped prompts. Use these for cross-project reflection. The wrapper
keeps the Codex sandbox and approval policy explicit; it does not grant
additional permissions.

## Unsafe or High-Friction Flags

Avoid these unless the user explicitly asks:

- `--dangerously-bypass-approvals-and-sandbox`
- `--dangerously-bypass-hook-trust`
- `--sandbox danger-full-access`
- Editing-oriented prompts that ask Codex to modify files directly.

For review tasks, Codex should inspect and reason. The calling agent remains
responsible for deciding whether to apply fixes.

## Auth and Environment Failure Modes

If invocation fails, report the blocker directly:

- `codex` is not installed or not on `PATH`.
- Codex is installed but not authenticated.
- The selected model or profile is unsupported.
- The repository is not a git repo and `--skip-git-repo-check` was not used.
- Sandbox or approval settings prevent the requested analysis.

Do not silently fall back to another model provider or a different memory
surface.

## Data Boundary

Before invoking Codex, scan for likely secrets or sensitive local files in the
intended prompt or review scope. If risk is unclear, ask for scope or use
`--dry-run` and let the user review the command and prompt first.

For cross-project reflection, prefer compact context files and safe history
summaries. Do not pass raw agent transcripts, auth files, paste caches, or large
private logs unless the user explicitly approved that exact material.
