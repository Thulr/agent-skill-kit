# Enforcement Playbook

## Scope

Making the boundaries and invariants the other surfaces define hold *mechanically* rather
than by instruction, and routing work between agent and human. This playbook decides **what
to enforce and why, and what to escalate** — it does **not** wire the machinery. Building
the actual hooks, CI gates, AGENTS.md, and sandboxes is owned by
`harden-repo-for-coding-agents`; route there for the implementation.

- **In:** gates-vs-prose for load-bearing invariants, gate-coverage review, prevent-vs-
  detect, mechanical-vs-judgment routing, change-impact gating.
- **Out:** the boundary *design* itself (see `boundaries.md` / `parallel-readiness.md`); the
  concrete hook/CI/AGENTS.md wiring (use `harden-repo-for-coding-agents`).
- **Intents this surface answers:** review, design.

## Grounding

- **Saad et al. (2025)** — LLM coupling reasoning is brittle under noise (F1 drops over 50%
  in noisy, open-ended scenarios); boundaries an agent must merely *reason about* will be
  violated.
- **Herbsleb & Grinter (1999)** — integration is where split work breaks; gate the
  integration surface with tests.
- **Bairi et al., CodePlan (2024)** — change-impact analysis can gate a repo-scale edit
  before it lands.

## Good signals

- Every load-bearing invariant (dependency direction, forbidden imports, a frozen schema)
  has a mechanical check that fails the build when violated — not just a sentence in
  AGENTS.md.
- The check is CI-required / branch-protected, so it cannot be skipped.
- Mechanical failures (format, types, lint, tests) are routed back to the agent
  automatically; they do not reach a human reviewer.
- Judgment-bearing changes (migrations, permissions, new dependencies, reliability
  decisions, boundary changes) are surfaced to a human deliberately.

## Common failures

- **Boundary-as-prose** — the rule lives only in a comment or AGENTS.md; an agent under
  noise ignores it and the violation is caught (if at all) in review.
- **Gate exists but is not required** — a check runs but is advisory, so it is skipped under
  deadline.
- **Misrouted friction** — humans spend review attention on mechanical lint failures while
  agents silently make architecture, permission, or dependency decisions no one gates.
- **Stale gate** — a rule kept after the model or codebase changed, now blocking valid work
  or enforcing a boundary that moved.
- **Detect-repeatedly instead of prevent** — the same class of violation is caught in review
  every week because nothing makes it structurally impossible.

## Heuristics

- **(review, design) Make load-bearing boundaries gates, not prose.** Dependency direction,
  forbidden imports, and frozen schemas belong in import-linters, architecture/dependency
  tests, and CI-required checks — because an agent's coupling reasoning degrades under noise,
  a sentence holds far less reliably than a check.
- **(review) Audit gate coverage.** For each invariant the design relies on, ask: is it
  enforced by a failing check, or only stated? An invariant that is only stated is a finding
  — severity scales with its blast radius.
- **(design) Route mechanical to the agent, judgment to a human.** Formatting, type errors,
  forbidden imports, and missing tests go back to the agent via lint/CI. Migrations,
  permission/authorization changes, new dependencies, reliability/SLO choices, and
  architecture/boundary changes are surfaced to a human — these are where local progress can
  raise global entropy.
- **(design) Prefer prevent-entirely over detect-repeatedly.** Encode the boundary so the
  violation is structurally impossible (an import rule the build rejects), with the rejection
  message pointing at the reason, so the agent self-corrects instead of a reviewer re-finding
  it.
- **(review, design) Gate the high-blast-radius artifacts.** Put integration tests and
  required checks around the shared contracts and dependency direction that parallel work
  depends on.
- **(design) Gate repo-scale edits with change-impact analysis.** Use a dependency/impact
  pass to bound what an edit may touch before it is dispatched or merged.

## Quick diagnostic

- Is this invariant enforced by a check that fails the build, or only written down? — only
  written → it will be violated; make it a gate (then route the wiring to
  `harden-repo-for-coding-agents`).
- Does the gate block merge, or is it advisory? — advisory → it will be skipped.
- Is a human being asked to catch something a linter could? — yes → route it back to the
  agent and reserve the human for judgment calls.
- Is this gate still serving an invariant that is still true? — no → retire it; a stale gate
  is friction.

## Cross-references

- `harden-repo-for-coding-agents` — builds the actual hooks, CI gates, AGENTS.md, and
  sandboxes this playbook says to add.
- `boundaries.md` / `parallel-readiness.md` — define the boundaries and contracts this
  playbook makes mechanical.
- `references/core/severity-rubric.md` — severity for un-enforced invariants.
- `references/intents/{review,design}.csv` row `enforcement` — the entry points.
