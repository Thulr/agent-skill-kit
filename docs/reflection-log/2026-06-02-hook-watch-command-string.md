---
date: 2026-06-02
harness: other
sub-surface: gates
status: resolved
severity: 3
related: ["2026-06-02-hook-wrapper-bypasses.md", "2026-06-02-hook-find-option-bypass.md", "2026-06-02-hook-xargs-stdin-targets.md"]
---
# `watch '<cmd>'` ran a quoted command string the wrapper handling treated as opaque

## What happened

Codex PR review (P1, PR #42) on the wrapper-bypass change: `watch` was added to
`TRANSPARENT_WRAPPERS`, which strips the wrapper and resolves the *next argv
token* as the executable. But `watch` passes its argument to `sh -c` (man watch:
"command is given to sh -c"), so the destructive command can be a single quoted
string:

```
check_command("watch 'rm -rf /etc'")   -> None  (ALLOW)
```

The transparent-wrapper model only caught the multi-token form
(`watch -n1 rm -rf /etc`, where `rm` is its own token); the quoted-string form
left `rm -rf /etc` as one opaque "executable name" that matched nothing.

## What to do differently

`watch` is not a transparent argv wrapper — it is a *command-string* wrapper,
like `bash -c` / `flock -c`. Moved it to a new `COMMAND_STRING_WRAPPERS` set:
after skipping watch's own option flags, the entire remainder is joined and
recursively `check_command`-ed, covering both `watch 'rm -rf /etc'` and
`watch -n1 rm -rf /etc`. General lesson: before adding a wrapper to the
transparent set, check whether it execs argv directly (nohup/timeout/setsid) or
runs a shell-command string (watch) — the latter needs recursive inspection, not
token-stripping. Fixtures added to all three hook test files before patching.

## Closed by

This change set: `scripts/hooks/destructive_bash_policy.py`
(`COMMAND_STRING_WRAPPERS` + `resolve_executable` branch; `watch` removed from
`TRANSPARENT_WRAPPERS`) and the watch command-string fixtures in `.claude` /
`.codex` / `.cursor` `test_block_destructive_bash.py`. (Commit SHA on commit.)
