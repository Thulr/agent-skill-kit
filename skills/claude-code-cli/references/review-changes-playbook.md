# Review Changes Playbook

Use this playbook when Claude Code is asked to review code written by Cursor,
Codex, Claude, or another agent.

## Scope Selection

- `all`: default for uncommitted agent work. Includes git status, staged diff,
  unstaged diff, and small untracked text files.
- `staged`: use when the user is preparing a commit.
- `unstaged`: use when reviewing the latest local edits before staging.
- `branch`: use when reviewing committed branch work against a base ref.

If the scope is ambiguous, ask one question. If the user says "review Cursor's
changes" and there are uncommitted changes, use `all`.

## Review Standard

Tell Claude Code to prioritize:

1. Correctness bugs and behavioral regressions.
2. Security, privacy, data loss, auth, and permission risks.
3. Broken build, test, or release behavior.
4. Missing tests only where the changed behavior makes risk real.
5. Maintainability issues only when they are likely to cause defects.

Style preferences and formatting nits are out of scope unless they hide a bug.

## Output Shape

Require findings first, ordered by severity. Each finding should include:

- severity: `critical`, `high`, `medium`, or `low`
- file and line when possible
- concise issue statement
- why it matters
- suggested fix or verification step

If there are no findings, Claude should say so directly and list residual risk
or tests it could not run.

## Reconciliation

Claude's review is evidence, not authority. The calling agent should:

- verify any claimed file/line against the repository
- discard findings that contradict the actual code
- run targeted tests when feasible
- tell the user which suggestions were accepted, rejected, or left for later

If Claude and the calling agent disagree, prefer local evidence and explain the
disagreement briefly.
