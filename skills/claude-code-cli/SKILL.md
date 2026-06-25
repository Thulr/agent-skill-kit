---
name: claude-code-cli
description: "Invoke Claude Code CLI as an external reviewer. Covers print mode (-p) for one-shot review and interactive PTY mode for multi-turn sessions."
license: MIT
---

# Claude Code CLI

Invoke Claude Code as an external reviewer, analysis agent, or cross-project
reflection source. Default to read-only delegation (`--permission-mode plan`)
unless the user explicitly asks for Claude Code to edit files.

## Boundaries

Do NOT use to invoke Codex (use codex-cli) or Cursor (use cursor-cli) as the
external agent, to harden a repo's own agent config (use
harden-repo-for-coding-agents), or to run this kit's own heuristic review
skills like dx-audit/ux-audit — claude-code-cli shells out to the external
Claude Code CLI as an independent reviewer rather than auditing a surface itself.

## Prerequisites

Before invoking Claude Code, verify the setup:

```bash
# Check installation
command -v claude || echo "NOT INSTALLED"

# Check auth status (JSON output)
claude auth status 2>/dev/null || echo "NOT AUTHED"

# Full health check
claude doctor 2>/dev/null || echo "NEEDS ATTENTION"
```

**Install if missing:** `npm install -g @anthropic-ai/claude-code`
**Auth for CI/scripting:** set `ANTHROPIC_API_KEY` env var (bypasses OAuth)
**Auth for interactive use:** run `claude` once for browser OAuth, or
`claude auth login --console` for API key billing

**Error if missing:** Report the exact install/auth command that needs to run.
Do not proceed with invoking Claude Code if the CLI is unavailable.

## Core Invocation Modes

### Mode 1: Print Mode (`-p`) — PREFERRED for reviews

One-shot, non-interactive. No PTY needed. No dialog handling. Cleanest path.

```bash
# Review git diff against a branch
claude -p --permission-mode plan --output-format text \
  "Review this diff for bugs, security issues, and style problems." \
  --max-turns 1

# Pipe a diff directly
git diff main...feature | claude -p --permission-mode plan \
  "Review this diff" --max-turns 1

# Ask a custom question with file context
cat src/auth.py | claude -p --permission-mode plan \
  "Review this file for security vulnerabilities" --max-turns 3
```

### Mode 2: Interactive PTY via tmux — Multi-turn sessions

Requires tmux orchestration for dialog handling. Use when the review needs
back-and-forth or the user wants to see Claude's thinking:

```bash
# Start session
terminal(command="tmux new-session -d -s claude-review -x 140 -y 40", workdir="/repo")
terminal(command="tmux send-keys -t claude-review 'cd /repo && claude' Enter")

# Handle workspace trust dialog (Enter = default "Yes")
terminal(command="sleep 5 && tmux send-keys -t claude-review Enter")

# Send the review task
terminal(command="tmux send-keys -t claude-review 'Review changes vs main. Check for bugs, race conditions, and missing tests.' Enter")

# Capture output periodically
terminal(command="sleep 30 && tmux capture-pane -t claude-review -p -S -50")
```

**Bare mode (fastest startup, CI/scripting):**
`claude --bare -p "task" --allowedTools 'Read,Bash' --max-turns 10`
Skips hooks, plugins, MCP discovery, CLAUDE.md, and OAuth. Requires
`ANTHROPIC_API_KEY`.

## Use Cases

### Review working tree changes (PRIMARY USE CASE)

```bash
# All changes (staged + unstaged)
terminal(command="git diff | claude -p --permission-mode plan --output-format text 'Review these changes for bugs, security issues, and style problems. Be thorough.' --max-turns 3", workdir="/path/to/repo", timeout=120)

# Branch diff vs main
terminal(command="git diff main...HEAD | claude -p --permission-mode plan --output-format text 'Review this branch diff for bugs, design issues, and test coverage gaps.' --max-turns 3", workdir="/path/to/repo", timeout=120)

# Staged changes only (pre-commit)
terminal(command="git diff --cached | claude -p --permission-mode plan --output-format text 'Review these staged changes before commit. Flag any issues.' --max-turns 2", workdir="/path/to/repo", timeout=60)
```

### Second opinion on a design or plan

```bash
# Pass context via stdin
terminal(command="printf '%s\n' 'Here is the architecture plan...' | claude -p --permission-mode plan --output-format text 'Review this plan for risks, missing constraints, and failure modes.' --effort high --max-turns 5", timeout=120)

# With file context
terminal(command="cat docs/architecture.md | claude -p --permission-mode plan --output-format text 'Review the proposed architecture. What are the failure modes?' --effort high --max-turns 5", timeout=120)
```

### Cross-project reflection

For recurring agent mistakes and workflow patterns, must run from a neutral
directory such as `$HOME` — not from the current repository:

```bash
terminal(command="claude -p --permission-mode plan --output-format text 'Review my agent workflows across all projects in the last 30 days. What recurring mistakes do you see? What patterns should I adopt?' --effort high --max-turns 10 --max-budget-usd 1.00", workdir="$HOME", timeout=180)
```

### Session continuation

```bash
# Continue most recent session in current directory
terminal(command="claude -p --continue 'Continue the review. What did you find?' --max-turns 3", workdir="/repo", timeout=60)

# Resume a specific session by ID
terminal(command="claude -p --resume <session-id> 'Continue and also check for performance issues.' --max-turns 3", timeout=60)
```

## Activation Contract

1. **Check prerequisites.** Run `command -v claude` and `claude auth status`
   before any delegation. If missing, report the exact fix.

2. **Read `references/use-case-registry.csv`** for the full use-case catalog.

3. **Bare invocation** (`"use claude-code-cli"`, `"start"`): show a compact menu
   with mode choice (guided / autopilot / grill me?) and numbered use cases.
   Wait. No file inspection, no network calls, no writes.

4. **Concrete invocation**: match the user's request to a use case above and
   run the corresponding `claude -p` inline command.

5. **Ambiguous invocation**: ask one — e.g., *"Are you reviewing working-tree
   changes, a branch diff, or do you want a second opinion on a design?"* or
   *"Is this a code review or a cross-project reflection?"*

6. **Safety check**: If the task would send secrets, private data, production
   credentials, or unreviewed sensitive files to Claude Code, stop and ask for
   scope. Never use `--dangerously-skip-permissions` or
   `--allow-dangerously-skip-permissions` unless the user explicitly requests
   it for a trusted sandbox.

7. **Present results.** Claude's output is input from an external reviewer,
   not final truth. Reconcile disagreements against local evidence. Summarize
   what Claude found and any caveats about scope or reliability.

> **Wrong direction?** If the user says this isn't what they meant, go back to
> step 1 — do not patch in the wrong direction. Restate the corrected
> understanding and re-plan.

## Modes

- **Autopilot**: For concrete requests like "ask Claude to review my changes",
  match the use case and run the inline command with defaults. Summarize
  findings and caveats.
- **Guided Draft**: For ambiguous requests, ask one question about scope before
  running Claude.
- **Grill Me**: For designing a recurring review workflow, ask about trigger
  point, scope, output format, and failure handling before running commands.

## Safety Rules

1. **Read-only by default.** Use `--permission-mode plan` (read-only analysis)
   unless the user explicitly asks Claude to make edits.
2. **No `--dangerously-skip-permissions`** without explicit user approval.
3. **Check for secrets** before piping diffs. If the diff might contain
   credentials, tokens, or customer data, stop and ask for scope.
4. **Set `--max-turns`** (3–10 for reviews) to prevent runaway loops.
5. **Set a reasonable timeout** in `terminal()` — 60s for small diffs, 120s+
   for branch reviews, 180s+ for cross-project reflection.
6. **Cross-project reflection must run from `$HOME`** — not from the current
   repo, to avoid repo-scope bias.
7. **If `claude` is unavailable**, report the exact install command. Do not
   try alternate CLIs or fabricate output.

## Scripts (optional, when scripts are findable)

The skill ships helper scripts under `scripts/` for advanced use cases:

```bash
# Review changes (all, staged, unstaged, or branch scope)
bash /path/to/this/skill-dir/scripts/claude-review-changes.sh --scope branch --base main

# Ask a custom question with context files
bash /path/to/this/skill-dir/scripts/claude-ask.sh "Review this migration plan" --effort high

# Cross-project reflection
bash /path/to/this/skill-dir/scripts/claude-cross-project-reflect.sh --since "last 30 days"
```

These scripts handle diff collection, prompt assembly, and template rendering.
Use them when the skill directory is known and the task is complex. For simple
reviews, prefer the inline `claude -p` commands above.

## Edge-Case Pass

Before invoking Claude Code, check:

- **Scope**: Is the intended diff staged, unstaged, branch, or a repo question?
- **Trust**: Is the current directory trusted for non-interactive execution?
- **Current-repo bias**: For cross-project reflection, run from a neutral dir
  and ensure the prompt prohibits treating the current repo as the audit target.
- **Secrets**: Could the diff include credentials, tokens, or customer data?
- **Size**: Will the diff exceed the prompt budget? Truncate or narrow scope.
- **Authority**: Is Claude reviewing (read-only) or editing (explicit request)?
- **Failure**: If auth, model, budget, or CLI availability fails, report the
  exact command and blocker. Do not fabricate results.

## Subagent Suitability

Claude Code is the independent reviewer for this skill. Use additional
subagents only for high-risk reviews where separate lenses are useful
(security, data migration, UX regressions). If subagents are unavailable,
perform the lenses sequentially.

## Reference Map

- `references/use-case-registry.csv`: Use-case routing.
- `references/cli-contract.md`: Claude Code CLI command contract and safety rules.
- `references/review-changes-playbook.md`: Review workflow for agent changes.
- `references/delegation-playbook.md`: Second-opinion and prompt-prep patterns.
- `references/ultrareview-playbook.md`: Hosted multi-agent review guidance.
- `references/output-rubric.md`: Review quality and reconciliation rubric.
- `scripts/claude-review-changes.sh`: Helper script for git diff reviews.
- `scripts/claude-ask.sh`: Helper script for custom questions with context.
- `scripts/claude-cross-project-reflect.sh`: Cross-project reflection script.
- `templates/*.md`: Prompt templates used by the helper scripts.
- `evals/`: Activation cases, static checks, trigger evals.
