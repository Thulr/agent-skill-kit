# Review Changes Playbook

Use this playbook when Codex is asked to review code written by Cursor, Claude,
Codex, or another agent. For a bare request like "review my changes with Codex,"
go straight to the run — skip the use-case menu and default to `uncommitted`.

## Reading scope from the request

Map the user's words to a scope, then run `scripts/codex-review-changes.sh` with
the matching `--scope`:

- "my changes" / "working tree" / "staged" / no argument → `uncommitted` (default)
- "vs main" / "this PR" / "the branch" / "since `<branch>`" → `branch`
  (`--base <branch>`, default `main`)
- "commit `<sha>`" / "last commit" → `commit` (`--commit <sha>`; `HEAD` for
  "last commit")

If scope is ambiguous and there are uncommitted changes, use `uncommitted`. Ask
one question only when it is genuinely unclear.

## Scope flags

- `uncommitted`: default for local agent work. `codex review --uncommitted`
  reviews staged, unstaged, and untracked changes.
- `branch`: `codex review --base <branch>` before PRs or merges.
- `commit`: `codex review --commit <sha>` for a single commit.

**`codex review` accepts no custom prompt with any scope flag** (every scope
errors `the argument '--<scope>' cannot be used with '[PROMPT]'`; verified on
codex-cli 0.141.0). So the severity rubric below and `--extra` are **not**
injected into `codex review` — it uses its own built-in review standard for all
scopes. The rubric still governs how you *reconcile and relay* Codex's output.

## Custom focus

For "focus on security" / "check error handling" style requests, `codex review`
can't take the focus as a prompt. Either let Codex run its built-in review and
filter its output to the focus area when you summarize, or — to actually steer
the review — use the `codex exec` path (`scripts/codex-ask.sh`), which accepts a
prompt and can be pointed at the diff with a custom rubric.

## Review Standard

Tell Codex to prioritize:

1. Correctness bugs and behavioral regressions.
2. Security, privacy, data loss, auth, and permission risks.
3. Broken build, test, or release behavior.
4. Missing tests only where changed behavior makes risk real.
5. Maintainability issues only when they are likely to cause defects.

Style preferences and formatting nits are out of scope unless they hide a bug.

## Output Shape

Require findings first, ordered by severity. Each finding should include:

- severity: `critical`, `high`, `medium`, or `low`
- file and line when possible
- concise issue statement
- why it matters
- suggested fix or verification step

If there are no findings, Codex should say so directly and list residual risk
or tests it could not run.

## Reporting to the user

Codex streams its own output. Don't dump it raw — read it and present a clean
summary:

- Lead with the overall verdict and a count of findings by severity.
- List each finding as `severity · file:line · one-line description`.
- Preserve Codex's reasoning for non-obvious findings; never silently drop one.
- Frame the result as a second opinion from another model, and offer to act on
  any finding.
- Do not apply fixes unless the user asks — this path reviews, it does not edit.

## Reconciliation

Codex's review is evidence, not authority. The calling agent should:

- verify any claimed file/line against the repository
- discard findings that contradict the actual code
- run targeted tests when feasible
- tell the user which suggestions were accepted, rejected, or left for later

If Codex and the calling agent disagree, prefer local evidence and explain the
disagreement briefly.

## Setup failures

If `codex` is missing, point the user to `brew install codex` (or
https://github.com/openai/codex) and stop. On an auth error, tell them to run
`codex login`. For anything murkier — config, sandbox, or model health — use
`scripts/codex-doctor-check.sh` (the diagnose use case).
