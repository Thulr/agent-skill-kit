---
date: 2026-06-02
harness: other
sub-surface: gates
status: resolved
severity: 2
related: ["2026-06-02-hook-find-delete-bypass.md", "2026-06-02-hook-wrapper-bypasses.md"]
---
# Non-`rm` deleters (`shred` / `truncate` / `unlink` / `rmdir`) destroyed protected files unblocked

## What happened

A `dx-heuristics` edge-pass (2026-06-02) found that the guard only knew about
`rm`, so other commands that destroy a target outright returned ALLOW:

```
check_command("shred -u /etc/passwd")     -> None  (ALLOW)
check_command("truncate -s 0 /etc/passwd")-> None  (ALLOW)
check_command("unlink /etc/passwd")       -> None  (ALLOW)
check_command("rmdir /etc")               -> None  (ALLOW)
```

These zero, shred, or unlink a protected file without invoking `rm`, so the
`rm`-only guard missed them.

## What to do differently

Add a `SIMPLE_DELETERS` set (`shred`, `truncate`, `unlink`, `rmdir`) dispatched
in `check_segment` to `check_simple_deleter`, which blocks when any non-option
token resolves to a protected path (via the shared `_protected_path_reason`).
Option *values* like the `0` in `truncate -s 0` don't resolve to a protected
path, so no precise per-command value-flag table is needed. Local files
(`./secret.key`, `/tmp/scratch`) remain allowed.

Scope note: interpreter-based deletion (`python3 -c "shutil.rmtree('/etc')"`,
`perl -e 'unlink …'`) is *not* caught — argv parsing can't see inside an
interpreter string — and is accepted as documented residual risk rather than
chased. Fixtures landed in all three hook test files first.

## Closed by

This change set: `scripts/hooks/destructive_bash_policy.py` (`SIMPLE_DELETERS` +
`check_simple_deleter` + `check_segment` dispatch) and the `Round-5` deleter
fixtures in `.claude` / `.codex` / `.cursor` `test_block_destructive_bash.py`.
(Commit SHA to be added on commit.)
