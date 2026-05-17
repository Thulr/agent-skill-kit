---
date: 2026-05-16
harness: codex
sub-surface: gates
severity: 4
status: resolved
related: [2026-05-16-hook-argv-bypasses-round2, 2026-05-16-hook-path-cwd-bypasses-round3]
---
# Round 1: regex-on-string hook bypassed by idiomatic command variants

## What happened

Codex PR review (PR #5) was asked to evaluate
`.claude/hooks/block-destructive-bash.py`, which used regex against the raw
command string. Multiple idiomatic variants bypassed it:

- `git push -f origin HEAD:main` (refspec form).
- `git push origin +main` (`+`-refspec force-update with no `-f` flag).
- `--force-with-lease=main` (the `=` form).
- `rm -rf -- /etc` (`--` terminator).
- `rm -r -f /etc` (split flags).
- `rm --recursive --force /etc` (long-form flags).

The regex `\brm\s+-[rRfF]*[rR][rRfF]*\s+/…` doesn't survive any of these.
Four bypasses were flagged P1 by the Codex review bot; the variant list is
longer (env-var prefixes, transparent wrappers like `sudo`/`time`,
`git -C path push`, etc.).

## What to do differently

**Deny-list hooks need argv parsing + negative-case tests for every variant.**
Replace regex-on-string with `shlex`-tokenized argv inspection that splits
pipelines (`;`, `&&`, `||`, `|`, `&`) and unwraps common prefixes (`sudo`,
`time`, `env`, `command`, env-var assignments, `git -C path`). Ship a fixture
table next to the hook covering every known-bypass form; CI runs it on every
PR.

**Skill-level corollary** (for `project-agentification` `scaffold` gates):
when generating a deny-list hook, also generate the negative-case test
fixture, populated from variants of every flag in the pattern (split short
flags, long-form aliases, `=` forms, `--` terminator, wrapper prefixes). The
hook and its tests are one scaffold artifact, not two.

## Closed by

`.claude/hooks/block-destructive-bash.py` rewritten to argv-parsed form +
`.claude/hooks/test_block_destructive_bash.py` test fixture (109 unit + 3
subprocess cases). Skill template at
`skills/.experimental/project-agentification/templates/artifacts/gates/`
ships both files together.
