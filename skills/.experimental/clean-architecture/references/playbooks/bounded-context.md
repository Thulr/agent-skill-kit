# Bounded Context Playbook

## Scope

Strategic-level DDD: bounded contexts, context mapping, ubiquitous
language, integration patterns (anti-corruption layer, open host
service, conformist, customer-supplier, shared kernel). Modular
monolith and microservice splits as deployment-time expressions of
context boundaries. Strangler-fig and branch-by-abstraction as the
refactor pathways.

Out of scope: tactical patterns inside one context (see
`domain-model.md`), code-level boundaries inside one module (see
`boundaries.md`).

## Grounding

- **Eric Evans, *Domain-Driven Design* (2003)** — ubiquitous language,
  bounded contexts, the context map, ACL/OHS/Conformist/Customer-
  Supplier/Shared-Kernel patterns.
- **Vaughn Vernon, *Implementing Domain-Driven Design* (2013)** —
  pragmatic context-integration patterns; eventual consistency across
  contexts.
- **Vlad Khononov, *Learning Domain-Driven Design* (2021)** — modern
  framing; subdomain types (core, supporting, generic) inform which
  integration pattern fits.
- **Martin Fowler, "BoundedContext" (2014)** — compact restatement: a
  model is valid only within its context.
- **Sam Newman, *Building Microservices*, 2e (2021)** — service
  decomposition aligned to bounded contexts.
- **Sam Newman, *Monolith to Microservices* (2019)** — strangler-fig
  and branch-by-abstraction pathways for extracting contexts without
  big-bang rewrites.

## Good signals

- Different bounded contexts use the same word ("Customer", "Order")
  to mean different things, and the team can articulate the
  difference.
- Cross-context interaction goes through an explicit translation
  layer; no shared mutable model.
- Each context has one team (or one clearly-responsible group); the
  context boundary aligns with team boundaries.
- Subdomain type (core / supporting / generic) is named; integration
  patterns chosen reflect it (e.g., conformist for generic
  subdomains, ACL when consuming from a foreign core).

## Common failures

- **Shared database across contexts.** Two contexts read and write the
  same table; the model is implicitly shared and changes ripple.
- **No translation at the boundary.** A context consumes another's
  events or DTOs and lets the foreign vocabulary leak inward; every
  internal model now carries the other context's concepts.
- **Big-ball-of-mud disguised as microservices.** Services are
  technically split but they call each other synchronously in long
  chains; the "context" boundary is a network hop, not a model
  boundary.
- **Premature split.** A bounded context is extracted into a service
  before the team understands its model; the boundary turns out to be
  wrong and a network call has been baked in.

## Heuristics

1. **(audit) For each pair of contexts, name the integration pattern
   in use.** If you cannot name one (ACL, OHS, conformist,
   customer-supplier, shared kernel), the integration is undefined —
   severity 3.
2. **(audit) Check whether shared concepts are independently modeled
   in each context.** A `Customer` with the same shape in two contexts
   is either (a) genuinely the same concept (shared kernel, rare) or
   (b) copy-paste with no translation (Medium severity, will diverge).
3. **(audit) Walk one cross-context request.** Note every model
   conversion. If foreign vocabulary survives across the boundary,
   the translation is incomplete — severity 2–3.
4. **(design) Pick the integration pattern from the subdomain type.**
   Core subdomain consuming from a foreign system: ACL. Generic
   subdomain consumed widely: OHS with a published language. Two
   supporting subdomains owned by the same team: shared kernel,
   accepted carefully.
5. **(design) Align context boundaries with team boundaries (Conway).**
   A context owned by no one is a context with no model discipline.
6. **(design) Choose deployment topology *after* boundaries are
   stable.** Modular monolith first; service extraction only when the
   boundary has proven stable under change.
7. **(refactor) Use strangler-fig to extract a bounded context.** New
   code lands in the new context; old code is incrementally rerouted;
   the old context shrinks until it is empty.
8. **(refactor) Use branch-by-abstraction for the data layer.**
   Introduce an abstraction over the existing data access; swap
   implementations behind the abstraction; the old implementation
   can be removed when no callers remain.
9. **(refactor) Stop the refactor partway is the safety net.** Every
   step should leave the system shippable. If a refactor cannot be
   stopped after step N, redesign the refactor.
10. **(explain) Bounded contexts are about modeling, not deployment.**
    A context can be a module in a monolith, a service, or several
    services. The boundary is the model boundary, not the network
    boundary.

## Quick diagnostic

In ten minutes: list the top-level modules or services in the system.
For each, write one sentence describing its model. Now look for shared
words across the sentences ("customer", "order", "payment"). For each
shared word, ask: does it mean exactly the same thing in both
contexts? If not, where is the translation? Each shared word with no
named translation is a Medium-or-higher finding.

## Cross-references

- `dependency-rule.md` for the cross-context dependency rule (ACL is
  the inversion).
- `boundaries.md` for code-level boundaries inside one context.
- `domain-model.md` for tactical modeling inside one context.
- `cross-cutting.md` for cross-context concerns (events, eventual
  consistency, integration).
