# Claude Code CLI Contract

This skill is grounded in the local Claude Code CLI shape:

```bash
claude -p --permission-mode plan --output-format text
```

`claude -p` runs non-interactively and prints a response. Non-interactive mode
skips the workspace trust dialog, so only use it from a repository the user or
current agent already trusts.

## Safe Default Flags

- `-p` or `--print`: non-interactive output for agent-to-agent delegation.
- `--permission-mode plan`: keeps Claude in a read-only planning/review stance.
- `--output-format text`: plain output that another agent can summarize.
- `--model <model>`: optional; prefer environment default unless requested.
- `--effort <low|medium|high|xhigh|max>`: optional; use higher effort for
  review and architecture questions.
- `--max-budget-usd <amount>`: optional guardrail for API spend.
- `--name <name>`: optional display name for session traceability.

The wrapper `scripts/claude-ask.sh` also supports `--cwd <dir>` and
`--template <file>` so a caller can run neutral, non-repo-scoped prompts. Use
these for cross-project reflection. The wrapper changes directory before
invoking `claude`; it does not grant additional permissions.

## Unsafe or High-Friction Flags

Avoid these unless the user explicitly asks:

- `--dangerously-skip-permissions`
- `--allow-dangerously-skip-permissions`
- `--permission-mode bypassPermissions`
- Editing-oriented prompts that ask Claude to modify files directly.

For review tasks, Claude should inspect and reason. The calling agent remains
responsible for deciding whether to apply fixes.

## Auth and Environment Failure Modes

Flag sets drift between Claude Code releases — on any unknown-option error,
run `claude --help` and trust the live output over this file.

If invocation fails, report the blocker directly:

- `claude` is not installed or not on `PATH`.
- Claude Code is installed but not authenticated.
- The selected model, effort, or budget is unsupported.
- The repository is not trusted for non-interactive execution.
- The prompt was truncated or omitted necessary context.

Do not silently fall back to another model provider or a different memory
surface.

## Data Boundary

Before invoking Claude Code, scan for likely secrets or sensitive local files in
the intended prompt material. If risk is unclear, ask for scope or use
`--dry-run` and let the user review the prompt first.

For cross-project reflection, prefer compact context files and safe history
summaries. Do not pass raw agent transcripts, auth files, paste caches, or large
private logs unless the user explicitly approved that exact material.
