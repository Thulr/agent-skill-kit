---
name: claude-code-cli
description: Use when an agent should invoke the Claude Code CLI (`claude -p`) as an external reviewer or analysis agent — get a second opinion, review working-tree/staged/branch changes another agent made, run read-only repo analysis, ask Claude Code for cross-project self-reflection about recurring agent mistakes and user workflow patterns, kick off a hosted `claude ultrareview`, or prepare a delegated prompt without running it. Triggers on 'ask Claude Code to review my changes', 'get a second opinion from Claude', 'have Claude review what Cursor did', 'run an ultrareview'. Do NOT use to invoke Codex (use codex-cli) or Cursor (use cursor-cli) as the external agent, to harden a repo's own agent config (use harden-repo-for-coding-agents), or to run this kit's own heuristic review skills like dx-audit/ux-audit — claude-code-cli shells out to the external Claude Code CLI as an independent reviewer rather than auditing a surface itself.
license: MIT
---

# Claude Code CLI

Invoke Claude Code as an external reviewer, analysis agent, or cross-project
reflection source. Default to read-only delegation unless the user explicitly
asks for Claude Code to edit files.

## Activation Contract

1. Read `references/use-case-registry.csv`.
2. If the user gave a concrete task, match it to the closest use case and load
   only that row's detail files and templates.
3. If the user only invokes this skill, asks what it can do, or says "start",
   present a short menu of use cases and modes, then wait. Do not run `claude`.
4. If the task would send secrets, private data, production credentials, or
   unreviewed sensitive files to Claude Code, stop and ask for scope.
5. Never use `--dangerously-skip-permissions` or
   `--allow-dangerously-skip-permissions` unless the user explicitly requests it
   for a trusted sandbox.

## Modes

- **Autopilot**: For concrete requests like "ask Claude to review Cursor's
  changes" or "ask Claude what mistakes it keeps making", run the appropriate
  script with read-only defaults, then summarize findings and caveats.
- **Guided Draft**: For ambiguous review or delegation requests, ask one
  question about scope: working tree, staged changes, branch diff, cross-project
  reflection window, or a custom prompt.
- **Grill Me**: For designing a recurring review workflow, ask one question at
  a time about trigger point, review scope, output format, and failure handling
  before preparing commands or prompts.

## Default Use Cases

- **Review working tree changes**: Use when Cursor or another agent has edited
  files and the user wants Claude Code to review the result.
- **Second opinion**: Use when the current agent wants Claude Code to reason
  about a technical decision, bug, design, or plan.
- **Cross-project reflection**: Use when a reflection workflow wants Claude Code
  to report recurring mistakes, user feedback patterns, and improvement ideas
  across projects. This must run from a neutral/global directory such as
  `$HOME`, not from the current repository as the implied scope.
- **Prompt preparation**: Use when the user wants the prompt and command but
  not the live Claude Code call.
- **Claude ultrareview**: Use only for branch or PR-level review when the user
  accepts the hosted multi-agent review behavior and any auth/cost implications.

## Quick Commands

From the repository being reviewed:

```bash
bash path/to/claude-code-cli/scripts/claude-review-changes.sh
```

To ask a custom read-only question:

```bash
printf '%s\n' "Review the API boundary in this repository." \
  | bash path/to/claude-code-cli/scripts/claude-ask.sh
```

Use `--dry-run` on either script to print the prompt without invoking Claude
Code.

To ask Claude Code for global/cross-project reflection:

```bash
bash path/to/claude-code-cli/scripts/claude-cross-project-reflect.sh \
  --since "last 30 days"
```

## Workflow Classification

This is a **workflow + interop** skill. It invokes another coding agent, can
produce review artifacts, and can prepare handoffs for agents such as Cursor,
Codex, or Claude Code. It does not auto-chain other skills.

## Workflow

1. Select the use case from the registry.
2. Confirm the repository is trusted and that `claude` is available.
3. Prefer `claude -p --permission-mode plan --output-format text` for
   read-only delegation.
4. Use `scripts/claude-review-changes.sh` for code review of git changes.
5. Use `scripts/claude-ask.sh` for custom questions or second opinions.
6. Use `scripts/claude-cross-project-reflect.sh` for global/cross-project
   reflection. Its prompt must explicitly say not to treat the invocation
   repository as the audit scope.
7. Present Claude's output as input from an external reviewer, not as final
   truth. Reconcile disagreements against local evidence.

## Operational Memory

Do not store user identity facts or secrets. Safe repeat-use defaults can come
from environment variables:

- `CLAUDE_CODE_CLI_MODEL`
- `CLAUDE_CODE_CLI_EFFORT`
- `CLAUDE_CODE_CLI_MAX_BUDGET_USD`
- `CLAUDE_CODE_CLI_MAX_DIFF_BYTES`
- `CLAUDE_CODE_CLI_PERMISSION_MODE`

If persistent workflow state is needed, use the operational templates in
`templates/` and keep only artifact paths, run ids, scope, and non-secret
assumptions.

## Subagent Suitability

Claude Code is the independent reviewer for this skill. Use additional
subagents only for high-risk reviews where separate lenses are useful, such as
security, data migration, or UX regressions. If subagents are unavailable,
perform the lenses sequentially using `references/output-rubric.md`.

## Edge-Case Pass

Before invoking Claude Code, check:

- **Scope**: Is the intended diff staged, unstaged, all working tree changes,
  a branch diff, a repo question, or a global/cross-project reflection?
- **Trust**: Is the current directory trusted for non-interactive Claude Code
  execution?
- **Current-repo bias**: For cross-project reflection, is the command running
  from a neutral directory and does the prompt prohibit treating the current
  repository as the audit target?
- **Secrets**: Could the diff include credentials, tokens, customer data, or
  local-only files?
- **Size**: Will the diff exceed the prompt budget and need truncation?
- **Authority**: Is Claude reviewing, or has the user explicitly asked it to
  make edits?
- **Failure**: If auth, model, budget, or CLI availability fails, report the
  exact command and blocker.

## Reference Map

- `references/use-case-registry.csv`: Use-case routing.
- `references/cli-contract.md`: Claude Code CLI command contract and safety
  rules.
- `references/review-changes-playbook.md`: Review workflow for Cursor or agent
  changes.
- `references/delegation-playbook.md`: Second-opinion and prompt-prep patterns.
- `references/ultrareview-playbook.md`: Hosted multi-agent review guidance.
- `references/output-rubric.md`: Review quality and reconciliation rubric.
- `templates/review-prompt.md`: Prompt template used by
  `scripts/claude-review-changes.sh`.
- `templates/delegation-prompt.md`: Prompt template used by
  `scripts/claude-ask.sh`.
- `templates/cross-project-reflection-prompt.md`: Prompt template used by
  `scripts/claude-cross-project-reflect.sh`.
- `templates/review-report.md`: Optional report shape for presenting findings.
- `templates/capability-manifest.json`: Capability declaration for other
  skills or agents.
- `templates/handoff.json`: Prepared handoff shape.
- `templates/workflow-state.json`: Optional resumable workflow state.
- `evals/trigger-evals.json`: Canonical activation/routing eval cases (schema-validated).
- `evals/activation-cases.md`: Natural-language activation + scenario fixtures.
