# Constitution — informed-skills

**Ratified:** 2026-05-16  
**Version:** 0.1.0

This document is the highest-precedence spec for how this repository is built and
maintained. When other docs conflict, this wins.

## Purpose

`informed-skills` publishes installable Agent Skills grounded in cited literature.
The published skill directories are the product.

## Non-goals

- This repo is not a generic “agent repo template”; it is evidence-driven and
  hand-curated from observed failures.
- This repo does not optimize for rapid, unaudited iteration. Skill files load
  into downstream agent sessions and are treated as production artifacts.

## Invariants (MUST)

1. **Skills are release artifacts.** Treat any PR touching `skills/`,
   `skills/.experimental/`, `.agents/skills/`, or `.github/` as shipping
   production behavior.
2. **`just check` stays green.** It must pass before commit and before PR.
3. **Evidence before scaffolding.** New rules, hooks, and instruction-surface
   changes must trace back to observed failures logged in `docs/agent-failures.md`.
4. **AGENTS.md stays short.** `AGENTS.md` is a table of contents and a set of
   load-bearing rules. Depth lives in `docs/`. Keep it ≤ 200 lines.
5. **Path-based gates enumerate all install lanes.** Any glob/gate operating on
   skills must cover `skills/*`, `skills/.experimental/*`, and `.agents/skills/*`.
6. **Schema parity across skills.** Shared schemas (e.g. `trigger-evals.json`)
   are canonical. When a schema changes, migrate every skill in the same PR.
7. **Identity fields are resolvable.** `skill.json` `maintainers` entries are
   GitHub handles (`@user` or `@org/team`), not opaque names.

## Change process

- **Architectural/structural changes:** write (or update) an ADR under `docs/adr/`
  describing the decision and tradeoffs, and link it from the PR description.
- **Operational changes:** add/update a runbook under `docs/runbooks/`.
- **Agent-surface changes:** add a row to `docs/agent-failures.md` and reference
  it in the commit message that closes the gap.

