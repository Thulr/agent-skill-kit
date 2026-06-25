---
name: codex-cli
description: "Invoke Codex CLI as an external reviewer. Triggers: 'ask Codex to review my changes', 'get a second opinion from Codex', 'review this before I push'."
license: MIT
---

# Codex CLI

Invoke Codex as an external reviewer, analysis agent, or cross-project
reflection source. Default to read-only delegation for general analysis, and
use Codex's native `review` command for code review.

## Boundaries

Do NOT use to harden a repo's own agent config (use
harden-repo-for-coding-agents), to promote observed failures into AGENTS.md
rules (use rules-from-coding-agent-failures), or to run this kit's own
heuristic review skills like dx-audit/ux-audit — codex-cli shells out to the
external Codex CLI as an independent reviewer rather than auditing a surface
itself.

## Activation Contract

1. Read `references/use-case-registry.csv`.
2. If the user gave a concrete task, match it to the closest use case and load
   only that row's detail files and templates.
3. **Bare invocation** (`"use codex-cli"`, `"start"`): show a compact menu:
   mode choice (guided / autopilot / grill me?) and numbered intents from the
   router. Wait. No file inspection, no network calls, no writes.
4. **Ambiguous invocation**: ask one — e.g., *"Are you reviewing uncommitted
   changes, a branch/commit diff, or do you want a second opinion on a design
   decision?"* or *"Is this a code review, cross-project reflection, or setup
   diagnostics?"*
5. If the task would expose secrets, private data, production credentials, or
   sensitive local files to Codex, stop and ask for scope.
6. Never use `--dangerously-bypass-approvals-and-sandbox` or
   `--dangerously-bypass-hook-trust` unless the user explicitly requests it for
   a trusted external sandbox.

## Modes

- **Autopilot**: For concrete requests like "ask Codex to review my changes" or
  "ask Codex what mistakes it keeps making", run the appropriate script with
  safe defaults, then summarize findings and caveats.
- **Guided Draft**: For ambiguous review or delegation requests, ask one
  question about scope: uncommitted changes, base branch, commit,
  cross-project reflection window, or custom prompt.
- **Grill Me**: For designing a recurring Codex delegation workflow, ask one
  question at a time about trigger point, review scope, output format, and
  failure handling before preparing commands or prompts.

## Default Use Cases

- **Review uncommitted changes**: Use when another agent changed files and the
  user wants Codex to review staged, unstaged, and untracked work.
- **Review branch or commit**: Use before opening, updating, or merging a PR.
- **Second opinion**: Use when the current agent wants Codex to reason about a
  technical decision, bug, architecture, or plan.
- **Cross-project reflection**: Use when a reflection workflow wants Codex to
  report recurring mistakes, user feedback patterns, and improvement ideas
  across projects. This must run from a neutral/global directory such as
  `$HOME`, not from the current repository as the implied scope.
- **Prompt preparation**: Use when the user wants the prompt and command but
  not the live Codex call.
- **Diagnose Codex**: Use when Codex CLI auth, config, sandbox, or runtime
  health is unclear.

## Quick Commands

From the repository being reviewed:

```bash
bash path/to/codex-cli/scripts/codex-review-changes.sh
```

To ask a custom read-only question:

```bash
printf '%s\n' "Review the API boundary in this repository." \
  | bash path/to/codex-cli/scripts/codex-ask.sh
```

Use `--dry-run` on either script to print the command and prompt without
invoking Codex.

To ask Codex for global/cross-project reflection:

```bash
bash path/to/codex-cli/scripts/codex-cross-project-reflect.sh \
  --since "last 30 days"
```

## Workflow Classification

This is a **workflow + interop** skill. It invokes another coding agent,
produces review or analysis artifacts, and can prepare handoffs for agents such
as Cursor, Claude Code, or Codex. It does not auto-chain other skills.

## Workflow

1. Select the use case from the registry.
2. Confirm the repository is trusted and that `codex` is available.
3. Use `scripts/codex-review-changes.sh` for code review with native
   `codex review`.
4. Use `scripts/codex-ask.sh` for read-only `codex exec` second opinions.
5. Use `scripts/codex-cross-project-reflect.sh` for global/cross-project
   reflection. Its prompt must explicitly say not to treat the invocation
   repository as the audit scope.
6. Use `scripts/codex-doctor-check.sh` when setup or auth is the blocker.
7. Present Codex output as input from an external reviewer, not as final truth.
   Reconcile disagreements against local evidence.

> **Wrong direction?** If the user says this isn't what they meant, go back to
> Understand (step 1) — do not patch in the wrong direction. Restate the
> corrected understanding and re-plan.

## Operational Memory

Do not store user identity facts or secrets. Safe repeat-use defaults can come
from environment variables:

- `CODEX_CLI_MODEL`
- `CODEX_CLI_PROFILE`
- `CODEX_CLI_SANDBOX`
- `CODEX_CLI_APPROVAL_POLICY`

If persistent workflow state is needed, use the operational templates in
`templates/` and keep only artifact paths, run ids, scope, and non-secret
assumptions.

## Subagent Suitability

Codex is the independent reviewer for this skill. Use additional subagents only
for high-risk reviews where separate lenses are useful, such as security, data
migration, or UX regressions. If subagents are unavailable, perform the lenses
sequentially using `references/output-rubric.md`.

## Edge-Case Pass

Before invoking Codex, check:

- **Scope**: Is the intended review uncommitted work, a base branch diff, a
  commit, a repo question, or a global/cross-project reflection?
- **Trust**: Is the current directory trusted for non-interactive Codex
  execution?
- **Current-repo bias**: For cross-project reflection, is `--cd` set to a
  neutral directory and does the prompt prohibit treating the current repository
  as the audit target?
- **Secrets**: Could the prompt or reviewed changes include credentials,
  tokens, customer data, or local-only files?
- **Authority**: Is Codex reviewing/analyzing, or has the user explicitly asked
  it to edit files?
- **Sandbox**: For `codex exec`, is `--sandbox read-only` sufficient? If not,
  ask before raising permissions.
- **Failure**: If auth, model, sandbox, or CLI availability fails, report the
  exact command and blocker.

## Reference Map

- `references/use-case-registry.csv`: Use-case routing.
- `references/cli-contract.md`: Codex CLI command contract and safety rules.
- `references/review-changes-playbook.md`: Native Codex review workflow.
- `references/delegation-playbook.md`: Second-opinion and prompt-prep patterns.
- `references/doctor-playbook.md`: Setup diagnostics workflow.
- `references/output-rubric.md`: Review quality and reconciliation rubric.
- `templates/review-prompt.md`: Prompt template used by
  `scripts/codex-review-changes.sh`.
- `templates/delegation-prompt.md`: Prompt template used by
  `scripts/codex-ask.sh`.
- `templates/cross-project-reflection-prompt.md`: Prompt template used by
  `scripts/codex-cross-project-reflect.sh`.
- `templates/review-report.md`: Optional report shape for presenting findings.
- `templates/capability-manifest.json`: Capability declaration for other
  skills or agents.
- `templates/handoff.json`: Prepared handoff shape.
- `templates/workflow-state.json`: Optional resumable workflow state.
- `evals/trigger-evals.json`: Canonical activation/routing eval cases (schema-validated).
- `evals/activation-cases.md`: Natural-language activation + scenario fixtures.
