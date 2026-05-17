---
date: 2026-05-16
harness: codex
sub-surface: gates
severity: 4
status: resolved
related: [2026-05-16-hook-regex-bypasses-round1, 2026-05-16-hook-argv-bypasses-round2]
---
# Round 3: relative-path / shell-launcher / wrapper-value bypasses

## What happened

Codex PR review (PR #5, round 6) was asked to re-evaluate after round-2
hardening. Third-round bypasses:

1. `rm -rf ../../etc` — relative paths with `..` weren't canonicalized; the
   protected-dir check only fired for paths starting with `/`.
2. `cd / && rm -rf etc` — cwd from a preceding pipeline segment wasn't
   tracked, so the relative `etc` was treated as a non-protected name.
3. `env -S 'rm -rf /etc'` — `env -S` packs a command into its value, which
   the wrapper unwrap consumed as opaque rather than inspecting.
4. `bash -c 'rm -rf /etc'` — shell launchers (`bash`, `sh`, `zsh`, `dash`,
   ...) weren't in the dispatcher, so the `-c` value was never recursively
   checked.

The H5 variant matrix at this point had 10 categories; round 6 surfaced 3
new ones (relative-path resolution / cwd-tracking, wrapper-flag-value-as-command,
shell-launcher unwrap).

## What to do differently

**Pattern is now visible: each round adds new variant categories until the
matrix saturates.** Round 1 was about flag forms; round 2 added 6 more
categories; round 6 adds 3 more. The smallest gap closing each round is
"encode the category in H5 + add to template + add fixture rows."

**Skill-level corollary**: when the hook deny-list grows a new executable
(shell launchers in this round), the scaffold must add it to the matrix
categories and to the dispatcher. Failure to do so is the recurrence vector.

## Closed by

Matrix in `references/playbooks/gates.md` scaffold H5 now lists 13 categories
(rounds 1 + 2 + 3 merged). Hook template implements the pattern for each
(relative-path normalization, cwd tracking across pipeline segments, `env -S`
unwrap, shell-launcher dispatch).
