# Glossary

Terminology in this domain is overloaded. Use these definitions
consistently; if a playbook needs a different sense, it spells out the
deviation in its `## Scope` section.

## Boundary

A seam in the code where one set of concerns ends and another begins.
Boundaries are crossed by *interfaces* (in code) or by *ports* (in
hexagonal terminology). A boundary is a property of code organization,
not of deployment.

## Bounded context

A strategic-level concept: the largest scope within which one model of
the domain is internally consistent. Different bounded contexts may use
the same word ("Customer", "Order") to mean different things.
Translation between contexts is explicit (anti-corruption layer, open
host service, conformist, customer-supplier). A bounded context is a
property of *modeling*, not of code organization. One bounded context
typically contains many code-level boundaries.

## Layer

A horizontal slice of code with a single architectural responsibility
(domain, application, interface, infrastructure). In a layered diagram,
inner layers do not know about outer layers. "Layer" and "ring" (in
onion architecture) and "circle" (in concentric diagrams) are different
visualizations of the same idea.

## Module

A unit of code organization (package, namespace, file). Modules may or
may not align with layers or with bounded contexts. A bounded context
typically maps to one *module* in a modular monolith and to one
*service* in a microservice deployment, but neither mapping is
required.

## Port

An interface owned by the application core, defined in terms the core
understands. Inbound ports describe what the application can do
(use-case interfaces); outbound ports describe what the application
needs from the outside world (repository interfaces, gateway
interfaces). Ports never reference infrastructure types.

## Adapter

An implementation of a port that translates between the core's
vocabulary and an outside technology (HTTP, ORM, message broker, file
system). Adapters live in the outer ring; they depend on the port, not
the other way around.

## Aggregate

A cluster of domain objects (entity + value objects + sometimes
sub-entities) treated as a single unit for consistency. Operations
enter through the aggregate root; invariants are enforced at the
aggregate boundary. Aggregates are transactional units; references
between aggregates are by id, not object reference.

## Entity

A domain object identified by an identity that persists through state
changes (a Customer with id 42 is the same Customer after their email
changes). Entities live inside aggregates.

## Value object

A domain object identified by the values it carries (a Money(100, USD)
is interchangeable with any other Money(100, USD)). Value objects are
immutable and have no lifecycle of their own.

## Use case

A unit of application-layer behavior triggered by an actor. In hexagonal
terms, a use case implements an inbound port. Each use case orchestrates
the domain to fulfill one intent.

## Dependency rule

The single load-bearing invariant: at every layer/ring/boundary,
dependencies point inward — outer code knows about inner code, never
the reverse. The rule is upheld by *dependency inversion* (inverting
control of the implementation choice so the inner code can declare an
interface the outer code implements).

## Anemic domain model

A pejorative term for domain objects that hold data but no behavior;
business logic lives in service classes instead. The shape *looks* OO
but loses the encapsulation benefits — usually a smell that the domain
is being treated as a data structure rather than a model.

## Anti-corruption layer (ACL)

A translation layer at the boundary of a bounded context that converts
between the context's internal model and a foreign model from another
context. The point is to prevent foreign concepts from leaking inward.

## Strangler fig

A refactoring pattern: a new implementation grows alongside the old,
gradually taking over capabilities until the old can be removed.
Borrowed from the *Ficus aurea* tree that envelops its host. Used
extensively in monolith-to-microservices refactoring.
