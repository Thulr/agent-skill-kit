# ADR 0002: Three Install Lanes and Path-Based Gates Enumerate Them

**Status:** Accepted (2026-05-16)

## Context

This repository has three distinct “install lanes”:

- `skills/<name>/` (published skills)
- `skills/.experimental/<name>/` (WIP/caveat-heavy skills; still installable)
- `.agents/skills/<name>/` (repo-local skills; authoring/review helpers)

Several gates (local scripts, CI loops, ignore patterns) operate “over all skills”.
A real failure mode in this repo was a glob that matched `skills/*` but silently
skipped `skills/.experimental/*`, allowing an entire lane to bypass static checks.

## Decision

Any path-based gate that intends to apply to “all skills” MUST explicitly
enumerate all three lanes:

- `skills/*`
- `skills/.experimental/*`
- `.agents/skills/*`

Do not rely on implicit dotfile matching behavior or shell options as the only
mechanism; the gate should be correct by construction when read in isolation.

## Consequences

- Slightly more verbose loops in scripts/CI.
- Fewer silent bypasses when adding new lanes or dot-prefixed directories.
- Makes “what is covered?” audit-able by reading the gate code, not by running it
  and hoping it prints everything.

