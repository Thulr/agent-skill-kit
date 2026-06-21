# Review Changes Playbook

Use this playbook when cursor-agent is asked to review code written by Claude,
Codex, Cursor, or another agent. For a bare "review my changes with Cursor"
request, go straight to the run and default to the `all` working-tree scope.

## Reading scope from the request

Run `scripts/cursor-review-changes.sh` with the matching `--scope`:

- "my changes" / "working tree" / no argument → `all` (staged + unstaged + untracked)
- "staged" → `staged`
- "unstaged" → `unstaged`
- "vs main" / "this PR" / "the branch" / "since `<branch>`" → `branch` (`--base <ref>`)

The wrapper builds the git diff and feeds it to `cursor-agent -p --mode plan`
(read-only). cursor-agent has no native review subcommand, so the diff is
assembled locally and passed as prompt context.

## Picking a model

`--model` is optional but is the point of this skill: get the review from a
*different* model than the one that wrote the code — e.g. `--model gpt-5` or
`--model sonnet-4`. `cursor-agent --list-models` shows what's available.

## Review Standard

Tell cursor-agent to prioritize:

1. Correctness bugs and behavioral regressions.
2. Security, privacy, data loss, auth, and permission risks.
3. Broken build, test, or release behavior.
4. Missing tests only where changed behavior makes risk real.
5. Maintainability issues only when they are likely to cause defects.

Style preferences and formatting nits are out of scope unless they hide a bug.

## Output Shape

Require findings first, ordered by severity, each with: severity
(`critical`/`high`/`medium`/`low`), file/line when possible, a concise issue
statement, why it matters, and a suggested fix or verification step. If there are
no findings, say so directly and list residual risk or tests not run.

## Reporting to the user

cursor-agent streams its own output. Don't dump it raw — summarize: lead with the
verdict and a severity count, list each finding as `severity · file:line ·
description`, frame it as a second opinion from another model, and offer to act.
Do not apply fixes unless the user asks — this path reviews, it does not edit.

## Reconciliation

cursor-agent's review is evidence, not authority. Verify any claimed file/line
against the repository, discard findings that contradict the actual code, run
targeted tests when feasible, and tell the user which suggestions were accepted,
rejected, or deferred. Prefer local evidence on disagreement.
