---
date: 2026-06-02
harness: other
sub-surface: gates
status: resolved
severity: 3
related: ["2026-06-02-hook-find-delete-bypass.md", "2026-06-02-hook-wrapper-bypasses.md", "2026-06-02-hook-nonrm-deleters.md"]
---
# Leading GNU `find` global options hid the protected root from `check_find`

## What happened

The Codex PR reviewer (`chatgpt-codex-connector`) flagged a P1 on PR #42:
`check_find` collected search roots by walking leading operands until the first
token starting with `-`/`(`/`!`/`)`. GNU find, however, accepts global options
*before* the path — `find [-H] [-L] [-P] [-D debugopts] [-Olevel] [path...]
[expression]`. So a leading global option made the root list empty, `check_find`
fell back to the default `.`, and the actual protected path was never inspected:

```
# cwd not under a protected dir (e.g. /tmp/project)
check_find("find -H /etc -delete")        -> None  (ALLOW — /etc deleted)
check_find("find -O3 /etc -delete")       -> None  (ALLOW)
check_find("find -L -- /usr -exec rm {} +") -> None  (ALLOW)
```

Same-impact hole as the original `find -delete` bypass it sat next to: the guard
is the agent-session backstop for `rm`-of-protected-paths (W3 — prose is ~70%),
and a single `-H`/`-L`/`-P`/`-O`/`-D` token in front of the path defeated it.
(In a cwd that is itself protected the command happened to block, but on the
wrong target — `.` — masking the bug.)

## What to do differently

Skip the leading global-option block before collecting roots: consume `-H`/`-L`/
`-P` (no arg), `-O<level>` (attached), `-D debugopts` (one following arg), and a
`--` end-of-options terminator, then collect path operands as before. Per
AGENTS.md §Forbidden actions, fixtures (5 positive + 2 negative) were added to
all three hook test files (`.claude` / `.codex` / `.cursor`) **before** patching
the policy. General lesson: when a gate parses a real tool's argv, model that
tool's *global options that precede operands*, not just the operand/expression
split — the option grammar is part of the attack surface.

## Closed by

This change set: `scripts/hooks/destructive_bash_policy.py` (`check_find`
leading global-option skip) and the find-option fixtures in `.claude` / `.codex`
/ `.cursor` `test_block_destructive_bash.py`. (Commit SHA to be added on commit.)
