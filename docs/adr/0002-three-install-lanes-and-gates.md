# ADR 0002: Path-Based Gates Enumerate Every Skill Lane

**Status:** Accepted (2026-05-16)

## Context

This repository has three skill lanes that path-based gates must understand:

- `skills/<name>/` (published product skills)
- `skills/.experimental/<name>/` (reserved and intentionally empty in the
  current release model)
- `.agents/skills/<name>/` (repo-local skills; authoring/review helpers)

Several gates (local scripts, CI loops, ignore patterns) operate “over all skills”.
A real failure mode in this repo was a glob that matched `skills/*` but silently
skipped `skills/.experimental/*`, allowing an entire lane to bypass static checks.
That lane is currently empty, but it remains part of path-based gate contracts so
it cannot be silently reopened without coverage.

As of 2026-05-21, installable public skills do not use per-skill draft or
experimental maturity. Repository prerelease maturity is communicated by release
tags such as `0.0.1-alpha`.

## Decision

Any path-based gate that intends to apply to “all skills” MUST explicitly
enumerate all three lanes:

- `skills/*`
- `skills/.experimental/*`
- `.agents/skills/*`

Do not rely on implicit dotfile matching behavior or shell options as the only
mechanism; the gate should be correct by construction when read in isolation.
Repo-level release gates also assert that `skills/.experimental/` stays empty
until a future decision reopens it.

## Consequences

- Slightly more verbose loops in scripts/CI.
- Fewer silent bypasses when adding new lanes or dot-prefixed directories.
- Makes “what is covered?” audit-able by reading the gate code, not by running it
  and hoping it prints everything.
