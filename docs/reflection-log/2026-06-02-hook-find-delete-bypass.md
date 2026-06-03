---
date: 2026-06-02
harness: other
sub-surface: gates
status: resolved
severity: 3
related: ["2026-06-02-hook-wrapper-bypasses.md", "2026-06-02-hook-nonrm-deleters.md", "2026-05-16-hook-argv-bypasses-round2.md"]
---
# `find -delete` / `-exec rm` slipped past the destructive-bash guard

## What happened

A `dx-heuristics` edge-pass (2026-06-02) probed `scripts/hooks/destructive_bash_policy.py`
and found that `check_segment` only dispatched `rm`, `git`, and shell-launcher
`-c` payloads. `find` was never inspected, so deletion of protected paths via
`find` returned ALLOW:

```
check_command("find /etc -delete")                  -> None  (ALLOW)
check_command("find / -type f -exec rm -rf {} +")   -> None  (ALLOW)
check_command("find ~ -delete")                     -> None  (ALLOW)
```

`find /etc -delete` removes exactly what `rm -rf /etc` (correctly blocked) would,
so the guard had a same-impact hole. The hook is the agent-session backstop for
`rm`-of-protected-paths (W3 — prose is ~70%), so an agent that reached for `find`
instead of `rm` was unguarded.

## What to do differently

Dispatch `find` in `check_segment` (W3 — hard gate, not prose). Added `check_find`:
it collects the leading non-option operands as search roots (default `.`),
detects the destructive actions `-delete` and `-exec`/`-execdir rm` (incl.
`/bin/rm` via basename), and blocks when any root resolves to `/`, a protected
top dir, `$HOME`, or a `..`-escape — reusing a shared `_protected_path_reason`
helper so the protected-path rules stay identical to `check_rm`. Relative/cwd-local
roots (`.`, `/tmp`) remain allowed, matching `rm` semantics. Per AGENTS.md
§Forbidden actions, fixtures were added to all three hook test files
(`.claude` / `.codex` / `.cursor`) **before** patching the policy.

## Closed by

This change set: `scripts/hooks/destructive_bash_policy.py` (`check_find` +
`_protected_path_reason` + `check_segment` dispatch) and the `Round-5` fixtures
in `.claude` / `.codex` / `.cursor` `test_block_destructive_bash.py`. (Commit SHA
to be added on commit.)
