---
date: 2026-06-02
harness: other
sub-surface: gates
status: resolved
severity: 3
related: ["2026-06-02-hook-find-delete-bypass.md", "2026-06-02-hook-find-option-bypass.md", "2026-06-02-hook-xargs-stdin-targets.md"]
---
# `find <safe> -exec rm -rf <protected>` deleted a protected path check_find never inspected

## What happened

Codex PR review (P1, PR #42): `check_find` detected `-exec rm` only to set a
flag, then checked the find *roots* against protected paths. When the root is
safe but the exec'd rm names a literal protected target, nothing checked it:

```
check_command(r"find /tmp -exec rm -rf /etc \;")   -> None  (ALLOW — runs rm -rf /etc)
```

GNU find runs `-exec COMMAND ;` / `-exec COMMAND {} +` as that command, so the
rm argv is a destructive surface independent of the search root.

## What to do differently

When `-exec`/`-execdir rm` is present, collect the rm argv (tokens after `rm`
up to the `;`/`+` terminator) and run it through `check_rm` — the same
protected-path logic used everywhere else. The `{}` placeholder expands to found
files (already covered by the root check when the root is protected), so safe-root
`find /tmp -exec rm -rf {} +` stays allowed; a literal protected target blocks.
General lesson: a sub-command embedded in another tool's invocation (`find -exec`,
`xargs <cmd>`, `watch '<cmd>'`) is its own argv to inspect — checking only the
outer tool's operands misses it. Fixtures added to all three hook test files
before patching.

## Closed by

This change set: `scripts/hooks/destructive_bash_policy.py` (`check_find`
`-exec`/`-execdir rm` argv inspection via `check_rm`) and the find-exec fixtures
in `.claude` / `.codex` / `.cursor` `test_block_destructive_bash.py`.
(Commit SHA on commit.)
