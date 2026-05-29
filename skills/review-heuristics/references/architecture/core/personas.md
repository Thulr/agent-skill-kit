# Target developer personas

Pick the persona that best matches the audience for this analysis. The
choice shapes vocabulary, depth, and which trade-offs to surface.

## Persona A — Senior backend engineer, no DDD background

Familiar with layered or MVC code. Has heard of "clean architecture" and
"DDD" but has not internalized the dependency rule or aggregate design.
Comfortable with interfaces, dependency injection, and unit-of-work-style
patterns from their framework's ORM.

- **Speak to:** dependency direction, interfaces as seams, why anemic
  models cost more than they save.
- **Avoid assuming:** familiarity with ubiquitous language, context
  mapping vocabulary, eventual consistency between aggregates.

## Persona B — Architect or staff engineer evaluating a split

Owns a decision about whether to extract a service, modularize a
monolith, or carve a new bounded context. Wants strategic guidance with
clear trade-offs, not tactical prescriptions.

- **Speak to:** context boundaries, integration patterns (ACL, OHS,
  customer-supplier), strangler-fig pathways, coupling-vs-cohesion.
- **Avoid:** prescribing a specific framework; treating microservices as
  the only strategic split.

## Persona C — Full-stack developer mapping backend ideas to frontend

Knows React/Vue/etc. and has seen Redux or Flux. Wants to understand
where the dependency rule, layered boundaries, and effect isolation map
onto frontend code.

- **Speak to:** unidirectional data flow, pure update functions, effect
  isolation, store/view boundaries; flag explicitly when the backend
  literature does not extend cleanly to a frontend pattern.
- **Avoid:** importing all DDD tactical vocabulary into a frontend
  context where it does not fit.

## Persona D — Tech lead refactoring under deadline pressure

Cannot do a big-bang rewrite. Needs a sequenced plan with safety nets at
every step and a way to stop partway.

- **Speak to:** smallest reversible step, characterization tests as
  safety net, branch-by-abstraction, parallel-change patterns.
- **Avoid:** "first, write the perfect domain model"; refactor
  prescriptions that require freezing feature work.

## Default persona

When the prompt does not signal a clear audience, assume **Persona A**
(senior backend engineer, no DDD background) and call out the assumption
in the output so the reader can redirect.
