---
date: 2026-05-16
harness: codex
sub-surface: gates
severity: 4
status: resolved
related: [2026-05-16-hook-regex-bypasses-round1, 2026-05-16-hook-path-cwd-bypasses-round3]
---
# Round 2: argv-parsed hook bypassed by wrapper/path/expansion variants

## What happened

Codex PR review (PR #5, rounds 3–5) was asked to re-evaluate the rewritten
argv-parsed hook. Second-round bypasses:

1. `sudo -u root rm -rf /etc` — wrapper flag values aren't consumed, so
   `root` is parsed as the executable.
2. `git --work-tree /path push -f origin main` — git global options with
   separate-token values shift the subcommand off `sub[0]`.
3. `rm -rf /tmp/../etc` — `..` segments not canonicalized before the
   protected-dir check.
4. `rm -rf ${HOME}/Documents` — only `~` / `$HOME` recognized, not
   `${HOME}`.
5. `echo ok\nrm -rf /etc` — `whitespace_split=True` strips real newlines,
   so only the first segment is checked.
6. `echo $(rm -rf /etc)` — nested shell execution contexts (`$()`,
   backticks, `<()`, `>()`) aren't inspected.

Six P1 flags. The hook test fixture from round 1 covered all the round-1
bypasses but none of these categories — exhaustive flag-form testing didn't
extrapolate to path traversal, shell variable expansion, command
substitution, or multi-line commands.

## What to do differently

**The H5 variant matrix is the artifact, not a per-bypass discovery process.**
Encode the full variant-category list when the test fixture is first
scaffolded, not after each round of automated review surfaces a new family.

**Skill-level corollary**: the test-fixture template
(`templates/artifacts/gates/pretooluse-hook-test.py`) must enumerate every
category in its header comment so the writer scaffolding from it sees the
full list, not just the categories that have surfaced in their repo so far.
The hook template (`pretooluse-hook.py`) ships with the implementation
pattern for each category (newline pre-processing, command-substitution
extraction, `os.path.normpath`, wrapper value-flag consumption, git
global-option value-flag consumption).

## Closed by

Hook variant matrix expanded in `references/playbooks/gates.md` scaffold H5
(rounds 1+2 merged). Hook template (`pretooluse-hook.py`) and test fixture
template (`pretooluse-hook-test.py`) implement and exercise all categories.
