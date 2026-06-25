---
name: cursor-cli
description: "Invoke Cursor CLI as an external reviewer. Triggers: 'ask Cursor to review my changes', 'get a second opinion from Cursor'."
license: MIT
---

# Cursor CLI

Invoke Cursor's headless agent (`cursor-agent`) as an external reviewer or
analysis agent. Default to read-only delegation (`--mode plan`) unless the user
explicitly asks cursor-agent to edit files. The distinctive value over the other
interop skills is **model diversity**: cursor-agent can run many providers'
models, so you can get a review from a *different* model than the one that wrote
the code.

## Boundaries

Do NOT use to invoke Codex (use codex-cli) or Claude Code (use claude-code-cli)
as the external agent, to harden a repo's own agent config (use
harden-repo-for-coding-agents), or to run this kit's own heuristic review
skills like dx-audit/ux-audit — cursor-cli shells out to the external Cursor
CLI as an independent reviewer rather than auditing a surface itself.

## Activation Contract

1. Read `references/use-case-registry.csv`.
2. If the user gave a concrete task, match it to the closest use case and load
   only that row's detail files and templates.
3. **Bare invocation** (`"use cursor-cli"`, `"start"`): show a compact menu:
   mode choice (guided / autopilot / grill me?) and numbered intents from the
   router. Wait. No file inspection, no network calls, no writes.
4. **Ambiguous invocation**: ask one — e.g., *"Are you reviewing working-tree
   changes, a branch diff, or do you want a second opinion on a design?"* or
   *"Is this a code review, setup diagnostics, or prompt preparation?"*
5. If the task would send secrets, private data, production credentials, or
   unreviewed sensitive files to cursor-agent, stop and ask for scope.
6. Never pass `-f` / `--force` / `--yolo` (or `--sandbox disabled`) unless the
   user explicitly requests it for a trusted sandbox; those drop the read-only
   guard.

## Modes

- **Autopilot**: For concrete requests like "ask Cursor to review these changes",
  run the appropriate script with read-only defaults, then summarize findings and
  caveats.
- **Guided Draft**: For ambiguous review or delegation requests, ask one question
  about scope: working tree, staged, unstaged, branch diff, or a custom prompt
  (and which model, if the user cares).
- **Grill Me**: For designing a recurring review workflow, ask one question at a
  time about trigger point, review scope, model, output format, and failure
  handling before preparing commands.

## Default Use Cases

- **Review working-tree changes**: Use when another agent edited files and the
  user wants cursor-agent to review the result.
- **Review branch diff**: Use before opening, updating, or merging a PR.
- **Second opinion**: Use when the current agent wants cursor-agent to reason
  about a decision, bug, design, or plan — optionally under a specific model.
- **Prompt preparation**: Use when the user wants the prompt and command but not
  the live cursor-agent call.
- **Diagnose Cursor**: Use when cursor-agent auth, workspace trust, model
  availability, or runtime health is unclear.

## Quick Commands

From the repository being reviewed:

```bash
bash path/to/cursor-cli/scripts/cursor-review-changes.sh
```

To ask a custom read-only question (optionally under a different model):

```bash
printf '%s\n' "Review the API boundary in this repository." \
  | bash path/to/cursor-cli/scripts/cursor-ask.sh --model gpt-5
```

Use `--dry-run` on either script to print the prompt and command without invoking
cursor-agent.

## Workflow Classification

This is a **workflow + interop** skill. It invokes another coding agent and can
produce review artifacts and handoffs for agents such as Claude Code or Codex. It
does not auto-chain other skills.

## Workflow

1. Select the use case from the registry.
2. Confirm the repository is trusted (cursor-agent requires workspace trust for
   `-p` runs) and that `cursor-agent` is available and authenticated.
3. Prefer `cursor-agent -p --mode plan --output-format text` for read-only
   delegation.
4. Use `scripts/cursor-review-changes.sh` for code review of git changes.
5. Use `scripts/cursor-ask.sh` for custom questions or second opinions.
6. Use `scripts/cursor-doctor-check.sh` when setup, auth, or trust is the blocker.
7. Present cursor-agent's output as input from an external reviewer, not as final
   truth. Reconcile disagreements against local evidence.

> **Wrong direction?** If the user says this isn't what they meant, go back to
> Understand (step 1) — do not patch in the wrong direction. Restate the
> corrected understanding and re-plan.

## Operational Memory

Do not store user identity facts or secrets. Safe repeat-use defaults can come
from environment variables:

- `CURSOR_CLI_MODEL`
- `CURSOR_CLI_MODE`
- `CURSOR_CLI_MAX_DIFF_BYTES`

Authentication uses `CURSOR_API_KEY` (cursor-agent's own variable). If persistent
workflow state is needed, use the operational templates in `templates/` and keep
only artifact paths, run ids, scope, and non-secret assumptions.

## Subagent Suitability

cursor-agent is the independent reviewer for this skill. Use additional subagents
only for high-risk reviews where separate lenses are useful (security, data
migration, UX regressions). If subagents are unavailable, perform the lenses
sequentially using `references/output-rubric.md`.

## Edge-Case Pass

Before invoking cursor-agent, check:

- **Scope**: staged, unstaged, all working-tree changes, a branch diff, or a repo
  question?
- **Trust**: Is the current directory trusted for non-interactive cursor-agent
  execution? (Untrusted repos block `-p` with a trust prompt.)
- **Read-only**: Is `--mode plan` (or `ask`) set? Bare `-p` print mode can write
  and run shell.
- **Model**: Did the user want a specific/different model for the second opinion?
- **Secrets**: Could the diff include credentials, tokens, customer data, or
  local-only files?
- **Size**: Will the diff exceed the prompt budget and need truncation?
- **Failure**: If auth, trust, model, or CLI availability fails, report the exact
  command and blocker.

## Reference Map

- `references/use-case-registry.csv`: Use-case routing.
- `references/cli-contract.md`: cursor-agent command contract, read-only modes,
  workspace trust, and safety rules.
- `references/review-changes-playbook.md`: Review workflow for agent changes.
- `references/delegation-playbook.md`: Second-opinion and prompt-prep patterns.
- `references/output-rubric.md`: Review quality and reconciliation rubric.
- `templates/review-prompt.md`: Prompt template used by `scripts/cursor-review-changes.sh`.
- `templates/delegation-prompt.md`: Prompt template used by `scripts/cursor-ask.sh`.
- `templates/review-report.md`: Optional report shape for presenting findings.
- `templates/capability-manifest.json`: Capability declaration for other skills or agents.
- `templates/handoff.json`: Prepared handoff shape.
- `templates/workflow-state.json`: Optional resumable workflow state.
- `evals/trigger-evals.json`: Canonical activation/routing eval cases (schema-validated).
- `evals/activation-cases.md`: Natural-language activation + scenario fixtures.
