# Cursor CLI Contract

This skill is grounded in the local Cursor CLI (`cursor-agent`) shape:

```bash
cursor-agent -p --mode plan --output-format text
```

`cursor-agent -p` runs non-interactively and prints a response. **By default `-p`
has access to all tools, including write and shell** — so a read-only delegation
MUST pass `--mode plan` (read-only/planning) or `--mode ask` (read-only Q&A). The
wrappers default to `--mode plan`.

## Safe Default Flags

- `-p` / `--print`: non-interactive output for agent-to-agent delegation.
- `--mode plan`: read-only/planning stance — analyze and propose, no edits. The
  review/second-opinion default. `--mode ask` is the read-only Q&A stance.
- `--output-format text`: plain output another agent can summarize (also `json`,
  `stream-json`).
- `--model <model>`: optional; cursor-agent can run many providers' models (e.g.
  `gpt-5`, `sonnet-4`, `sonnet-4-thinking`). `cursor-agent --list-models` lists
  what your account can use. This is the main reason to reach for cursor-cli over
  codex-cli / claude-code-cli: a second opinion from a *different* model.
- `--api-key <key>` / `CURSOR_API_KEY`: authentication.

Because `cursor-agent` has no native diff-review subcommand, the wrapper
`scripts/cursor-review-changes.sh` assembles the git diff itself and feeds it as
prompt context — the same approach as claude-code-cli.

## Unsafe or High-Friction Flags

Avoid these unless the user explicitly asks:

- `-f` / `--force` / `--yolo` (force-allow all commands — drops the read-only guard).
- `--sandbox disabled`.
- Any `--mode` other than `plan` / `ask` for a review (those are the read-only
  modes; bare print mode can write and run shell).
- Editing-oriented prompts that ask cursor-agent to modify files directly.

## Workspace Trust

`cursor-agent` requires the working directory to be **trusted** before a
non-interactive (`-p`) run; an untrusted repo raises a "Workspace Trust Required"
prompt that blocks headless execution. Establish trust once by running
`cursor-agent` interactively in the repo (or via your Cursor config); then the
`-p` wrappers work. `scripts/cursor-doctor-check.sh` surfaces version/auth health.

## Auth and Environment Failure Modes

If invocation fails, report the blocker directly:

- `cursor-agent` is not installed or not on `PATH` (install: https://cursor.com/cli).
- Not authenticated (`CURSOR_API_KEY` unset / not logged in).
- The working directory is not trusted for non-interactive execution.
- The selected model is unavailable for the account (`cursor-agent --list-models`).

Do not silently fall back to another model provider or a different memory surface.

## Data Boundary

Before invoking cursor-agent, scan for likely secrets or sensitive local files in
the intended diff or prompt. If risk is unclear, ask for scope or use `--dry-run`
and let the user review the prompt first. Do not pass raw agent transcripts, auth
files, or large private logs unless the user explicitly approved that material.
