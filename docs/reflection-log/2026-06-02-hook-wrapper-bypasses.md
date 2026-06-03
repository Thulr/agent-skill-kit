---
date: 2026-06-02
harness: other
sub-surface: gates
status: resolved
severity: 3
related: ["2026-06-02-hook-find-delete-bypass.md", "2026-06-02-hook-nonrm-deleters.md", "2026-05-16-hook-argv-bypasses-round2.md"]
---
# Execution wrappers (`nohup` / `timeout` / `flock` / `xargs` / …) hid the wrapped command

## What happened

A `dx-heuristics` edge-pass (2026-06-02) found that `TRANSPARENT_WRAPPERS`
covered `sudo` / `doas` / `command` / `exec` / `time` / `nice` / `ionice` / `env`
but **not** the other common execution wrappers. Because `resolve_executable`
only unwraps listed wrappers, the wrapped command was never reached:

```
check_command("nohup rm -rf /etc")        -> None  (ALLOW)
check_command("timeout 5 rm -rf /etc")    -> None  (ALLOW)
check_command("flock /tmp/x rm -rf /etc") -> None  (ALLOW)
check_command("setsid rm -rf /etc")       -> None  (ALLOW)
check_command("xargs rm -rf /etc")        -> None  (ALLOW)
```

`nohup bash -c 'rm -rf /etc'` also slipped because the outer wrapper was opaque,
so the inner `bash -c` handler was never reached.

## What to do differently

Add `nohup`, `setsid`, `stdbuf`, `timeout`, `flock`, `watch`, `xargs` to
`TRANSPARENT_WRAPPERS` (W3 — close the gate, don't rely on prose). Two of them
take a positional token between their flags and the wrapped command
(`timeout DURATION cmd`, `flock LOCKFILE cmd`), so a `WRAPPER_POSITIONAL_ARGS`
table makes `resolve_executable` consume the positional and then re-skip flags
(so `flock LOCKFILE -c '<cmd>'` is seen too). `flock -c`/`--command` carries a
command string and was added to `WRAPPER_COMMAND_VALUE_FLAGS` for recursive
inspection; per-wrapper value-flag tables were added for `stdbuf`/`timeout`/
`flock`/`watch`/`xargs`. Fixtures landed in all three hook test files first.

Residual (logged, not closed): absolute-path binaries (`/bin/rm`) and unlisted
wrappers remain matched by bare command name only — a separate hardening item.

## Closed by

This change set: `scripts/hooks/destructive_bash_policy.py`
(`TRANSPARENT_WRAPPERS` + `WRAPPER_POSITIONAL_ARGS` + value-flag tables +
`resolve_executable` positional handling) and the `Round-5` wrapper fixtures in
`.claude` / `.codex` / `.cursor` `test_block_destructive_bash.py`. (Commit SHA to
be added on commit.)
