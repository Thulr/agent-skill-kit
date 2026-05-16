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
  activate.
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
