# ADR 0012: A `interop` Family for Cross-Agent Tooling

**Status:** Accepted (2026-06-20). **Updates** (does not supersede)
[ADR 0011](./0011-actor-axis-agent-mirror-family.md): the agent-mirror family is
about shaping surfaces *for* an agent-as-actor; this ADR adds a sibling family for
skills that *use another agent as an instrument*. Introduced alongside the first
member, `codex-cli`.

## Context

The catalog grouped published skills into four families: `heuristics` (per-domain
audit/design pairs), `research`, `discovery`, and `ax` (the actor-axis agent-mirror
family from ADR 0011). Every family shares a property: each skill **evaluates or
shapes a surface** — a developer surface, a doc surface, a UX surface, an
agent-facing surface — grounded in cited sources.

`codex-cli` (long used by the maintainer, now moved into the kit) does not fit that
shape. It does not audit or design anything. It **drives another coding agent** —
the external Codex CLI — as a second-opinion reviewer, a read-only analysis pass, or
a cross-project reflection source, and reconciles that output against local
evidence. Forcing it into `ax` would muddy the family that ADR 0011 had just
tightened to pure actor-axis mirrors (`ax` shapes surfaces *for* agents;
`codex-cli` *uses* an agent). Forcing it into `heuristics` is a category error — it
has no audit/design counterpart and no source-grounded lens set. Marking it
`metadata.internal` would hide a skill the maintainer uses heavily from the very
people who would want it.

The grouping axis that *does* fit is the pragmatic one used by
[`mattpocock/skills`](https://github.com/mattpocock/skills): group engineering
skills by **what you do with them**, not only by the surface they reason about.
"Reach for another agent to get a second opinion" is a distinct, durable kind of
thing.

## Decision

Add a fifth catalog family, **`interop`** ("Cross-agent interop & tooling"): skills
that drive another coding agent or CLI as part of your own workflow, rather than
auditing or designing a surface themselves. `codex-cli` is its charter member,
`function: singleton`.

Mechanically, a new family touches exactly three sources of truth plus the
generated README:

- `scripts/catalog_taxonomy.py` — add `interop` to `FAMILIES`.
- `schemas/skill.schema.json` — add `interop` to `metadata.family.enum`.
- `catalog/catalog.json` — add the family's prose block and a `Pick a skill`
  routing-matrix row for `codex-cli`.
- `python3 scripts/build-catalog.py --write` regenerates the README catalog +
  routing sections; `--check` (in `just check` / CI) keeps them in sync.

The family-coverage check (`catalog_taxonomy.validate()` → "catalog family has no
skills") means an empty family fails the build, so `interop` cannot exist without at
least one member — it is introduced together with `codex-cli`, not ahead of it.

## Consequences

- The catalog now groups on two axes: *surface reasoned about* (the four original
  families) and *what you do with the skill* (`interop`). This is a deliberate, if
  small, broadening of the taxonomy toward the `mattpocock/skills` model. If more
  tool-driving skills land, `interop` is where they go, and a future ADR may split
  it (e.g. interop vs. local tooling) the way ADR 0008 split the review pairs.
- `codex-cli` ships the full published-skill contract (SKILL.md + license,
  `skill.json`, `evals/{trigger-evals.json,activation-cases.md,run-static-checks.sh}`).
  Its static checks additionally exercise each script's hermetic `--dry-run` path
  and assert the safety invariants (read-only sandbox default; no hardcoded
  `--dangerously-bypass-*`; cross-project reflection targets a neutral dir, never
  the launching repo).
- Risk: a single-member family can read as over-structured (W1's "scaffolding ahead
  of evidence"). Mitigation: the member exists today and is used heavily; the family
  is named for an observed kind of work, not a speculative one. **Update:** the family
  reached three members — `codex-cli`, `claude-code-cli`, and `cursor-cli`, each wrapping
  a different external coding-agent CLI as a read-only reviewer / second-opinion source
  (Codex via `codex review`/`codex exec`; Claude Code via `claude -p --permission-mode
  plan` + `claude ultrareview`; Cursor via `cursor-agent -p --mode plan`, with multi-model
  diversity). The single-member risk is resolved; the family now clears the W1 ≥3 floor.
- A lighter, user-invoked `codex-review` skill (a `/codex-review` slash command that
  runs `codex review` directly, no wrapper) was considered as a second `interop`
  member. It was **folded into `codex-cli`** rather than published separately: two
  skills both routing on "review my changes with Codex" would compete in activation
  (the exact failure `trigger-evals` / `just eval` guard against). Its strengths —
  natural-language scope mapping, the zero-ceremony quick path, and the user-facing
  reporting shape — now live in `references/review-changes-playbook.md`. The one
  thing consolidation gives up is the standalone `/codex-review` trigger; bare
  "review my changes with Codex" requests reach the same path via model activation.
