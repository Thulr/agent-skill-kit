---
date: 2026-05-21
harness: claude-code
sub-surface: gates
severity: 3
status: open
related: [2026-05-16-hook-path-cwd-bypasses-round3]
---
# Bash hook self-resolution broke when shell CWD drifted into a sub-directory

## What happened

Mid-scaffold for `skills/perf-observability-heuristics/`, an agent ran this
one-liner to create the four shared-content symlinks in a single Bash call:

```bash
cd skills/perf-observability-heuristics/references && \
  ln -s ../../_shared/modes.md modes.md && \
  ln -s ../../_shared/trackable-findings.md trackable-findings.md && \
  cd ../templates && \
  ln -s ../../_shared/templates/findings-ledger.md findings-ledger.md && \
  ln -s ../../_shared/templates/workflow-state.json workflow-state.json && \
  cd ../..
```

The trailing `cd ../..` was meant to return to the repo root from
`skills/perf-observability-heuristics/templates/`, but two `..` levels land
in `skills/`, not the repo root. The Bash tool persists shell CWD between
calls, so every subsequent Bash invocation ran with CWD = `<repo-root>/skills/`.

The PreToolUse Bash hook is configured in `.claude/settings.json` as:

```json
{ "type": "command", "command": "python3 .claude/hooks/block-destructive-bash.py" }
```

The hook command path is relative. The harness invokes the hook subprocess
with the persistent shell CWD, so Python tried to resolve
`.claude/hooks/block-destructive-bash.py` against `skills/` and failed with
`[Errno 2] No such file or directory`. The hook process exited non-zero,
and the harness — correctly, by hook contract — blocked every subsequent
Bash tool call, including the recovery `cd <repo-root>` that would have
un-wedged the shell.

Recovery required user intervention: the user typed `! cd <repo-root>` in
the prompt, which executed in the same persisted shell and reset CWD.
Bash worked again immediately.

Concrete error reported on the blocked call (absolute paths sanitized
to `<repo-root>`):

```
PreToolUse:Bash hook error: [python3 .claude/hooks/block-destructive-bash.py]:
.../Python: can't open file
'<repo-root>/skills/.claude/hooks/block-destructive-bash.py':
[Errno 2] No such file or directory
```

This bypassed Read (because Read is not Bash) but blocked any Bash-based
self-recovery the agent could attempt. The agent had to ask the user to
issue a `! cd` from the prompt.

## What to do differently

**Smallest gate**: make the hook command path absolute in
`.claude/settings.json` so it cannot be broken by shell-CWD drift. Claude
Code exports `$CLAUDE_PROJECT_DIR` to hook environments; the canonical fix
is:

```json
{
  "type": "command",
  "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/block-destructive-bash.py\""
}
```

This removes the dependency on shell CWD entirely. The hook script already
self-resolves `ROOT` via `pathlib.Path(__file__).resolve().parents[2]`, so
once Python can find the script, everything downstream works.

**Agent-side discipline (corollary, not a substitute for the gate fix)**:
prefer absolute paths in Bash one-liners that touch multiple directories;
avoid trailing `cd` that depends on counting `..` correctly. If a one-liner
must `cd`, return to a known absolute path (`cd "$CLAUDE_PROJECT_DIR"` or
`cd "$(git rev-parse --show-toplevel)"`) rather than a relative one.

**Recording bar note (W1)**: this is the first observed CWD-drift wedge in
this repo. Per the W1 ≥3 promotion floor, do not auto-promote to an
`AGENTS.md` rule yet — the settings.json fix above is the right
single-entry move because it removes the failure mode at the gate, not at
agent discipline.

## Closed by

<unfilled — pending PR that switches the hook command to use
`$CLAUDE_PROJECT_DIR`>
