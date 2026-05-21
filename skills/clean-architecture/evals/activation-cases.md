# Activation cases — clean-architecture

Plain-English companion to `trigger-evals.json`. Each subsection
explains *why* the listed queries activate or don't, and which surface
the routing picks for edge cases.

## Should activate

These prompts should route into the skill. The category in
`trigger-evals.json` is `positive`.

- **"is my domain code leaking into infrastructure?"** — direct
  invocation of the dependency rule; route to `audit/dependency-rule`.
- **"review this module for clean architecture violations"** — names
  the skill outright; route to `audit/boundaries` by default unless
  the agent can pick a more specific surface from context.
- **"clean architecture audit all with parallel sub-agents"** —
  explicit all-surface audit plus delegation request; route to
  `audit/all` and dispatch when the host permits it.
- **"find anemic domain models in this codebase"** — the anemic-domain
  anti-pattern is the canonical `domain-model` audit signal.
- **"how should I split this monolith into services aligned to bounded
  contexts?"** — strategic split intent; route to
  `design/bounded-context`.
- **"design layer boundaries for this new payments feature"** —
  greenfield design at the boundary surface.
- **"extract a pure use case from this controller without breaking
  callers"** — refactor toward a port; `refactor/boundaries`.
- **"strangler fig refactor to extract the billing bounded context"**
  — refactor pathway named explicitly; `refactor/bounded-context`.
- **"full clean architecture audit produced 8 findings"** —
  threshold-triggered follow-through; route to `audit/tracking` and
  create a findings ledger by default.
- **"audit found a severity 3 boundary leak"** — severity-triggered
  follow-through; route to `audit/tracking` and create a findings ledger.
- **"turn these clean-architecture findings into a tracked roadmap"**
  — explicit roadmap request after audit; load
  `references/trackable-findings.md` and use the ledger as the source
  before creating roadmap artifacts.
- **"verify whether CA-DEP-003 was fixed in this PR"** — closeout pass;
  rerun the narrow verification rule for that finding ID before checking it off.
- **"why did the audit use CA-dependency-rule-001 instead of CA-DEP-001?"**
  — mechanics follow-up; load `references/audit-mechanics.md` and normalize
  future findings to canonical ID prefixes.
- **"what is the difference between an aggregate and an entity?"** —
  explain intent on a `domain-model` distinction.

## Should NOT activate

These prompts share keywords with the skill but address a different
domain. Routing into clean-architecture would waste the user's time.

- **"make my CSS architecture cleaner"** — "architecture" here means
  visual design / file-organization for CSS, not software architecture.
- **"audit my dependency versions for CVEs"** — "dependency" here
  refers to package versions (security), not source-code
  dependency direction.
- **"design a clean UI for this form"** — UX design, not software
  design.
- **"audit checkout accessibility and form usability"** — product UX and
  accessibility, not code architecture; route to
  `ux-accessibility-heuristics`.
- **"refactor this regex to be more readable"** — refactor at a scale
  below the skill's smallest unit.
- **"what is the best React component library?"** — library choice,
  not architecture.
- **"set up CI/CD for my repo"** — infrastructure/tooling, not
  software architecture.
- **"speed up my test suite"** — performance / testing, not
  architecture (route to `test-heuristics` instead).
- **"audit my docker image for vulnerabilities"** — container security,
  not architecture.
- **"close these GitHub issues because the PR merged"** — issue closure
  alone is not clean-architecture verification; requires a referenced
  finding ID or architecture audit evidence.

## Boundary cases

These prompts could plausibly route elsewhere; the routing choice and
rationale is documented here so the description-optimization loop has
a stable target.

- **"explain SOLID principles"** — *activates.* SOLID is the
  class-scale expression of the dependency rule; route to
  `explain/dependency-rule`. Rationale: every SOLID principle except
  SRP (open/closed, Liskov, interface segregation, dependency
  inversion) operationalizes a clean-architecture concern. The
  `dependency-rule.md` playbook treats SOLID explicitly.
- **"how do I structure my React components?"** — *activates.* The
  question is shape-of-code, not styling; route to
  `design/boundaries` because Flux/Elm-style unidirectional flow is
  in the playbook's grounding. Rationale: the playbook's frontend
  representatives (Flux 2014, Elm 2015) explicitly cover this. If
  the prompt instead said "what library should I use" it would NOT
  activate. If it asks whether the form is usable or accessible, route to
  `ux-accessibility-heuristics` instead.
- **"microservices vs monolith for a 5-person startup?"** —
  *activates.* The trade-off is about context boundaries and team
  size, both `bounded-context` concerns; route to
  `design/bounded-context`. Rationale: this is exactly the
  question Newman's *Building Microservices* and Khononov's
  *Learning DDD* address.
- **"should I use Repository pattern with my ORM?"** — *activates.*
  The Repository pattern is in the `cross-cutting` playbook's
  grounding (Fowler, PoEAA 2002) and the design question is about
  the boundary between domain and persistence; route to
  `design/cross-cutting` (could also defensibly go to
  `design/boundaries`; tie-break to cross-cutting because the
  question is about persistence mechanics).

## What this is not

This file is not the activation runtime — it is documentation for
contributors. The runtime activation logic lives in
`SKILL.md` plus the routing CSVs. This file explains *why* the
runtime should behave the way it does and gives the description-
optimization loop a target.

## Delegation boundary

`audit all` alone selects the all-surface fan-out route. Try sub-agent
dispatch whenever user, project, session, or host policy already permits it.
If the host requires fresh explicit opt-in and none exists, ask once before
spawning, then use sequential passes only if consent is absent or dispatch is
blocked.

## Tracking behavior

- Large audit outputs (7+ findings) and any severity 3–4 finding must create a
  Markdown findings ledger plus workflow-state JSON by default, not merely
  offer or inline tracking choices.
- The ledger and workflow-state filenames start with the skill name, for example
  `clean-architecture-findings-ledger-2026-05-19-payments.md`, so ledgers from
  different audit skills are distinguishable.
- Roadmaps and GitHub issues require explicit user request. External issues
  still require confirmation.
- A roadmap or GitHub issue groups related finding IDs into issue-sized work;
  do not produce one issue per finding unless requested.
- A finding is checked off only after the verification rule attached to that
  ID passes. `implemented` and "issue closed" are not final statuses.
