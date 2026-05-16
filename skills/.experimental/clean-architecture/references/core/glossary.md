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
visualizations of the same idea. Different authors name the layers
differently; this glossary uses the *domain / application / interface /
infrastructure* set as the canonical reference, with other naming
conventions called out in the playbooks as needed.

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

## Aggregate root

The single entity within an aggregate that callers reference and through
which all operations on the aggregate flow. The root enforces the
aggregate's invariants at its boundary; internal entities and value
objects are never accessed directly from outside the aggregate.

## Branch-by-abstraction

A refactoring pattern: introduce an abstraction over the current
implementation, route callers through it, add a new implementation
alongside the old, swap implementations behind the abstraction, then
remove the old. Lets large changes happen incrementally on a single
branch without long-lived feature branches.

## Characterization test

A test written against existing behavior — even behavior that is wrong
or undocumented — to pin it before refactoring. The point is to detect
unintended changes; the test asserts "this is what the system does
today," not "this is what the system should do."

## Conformist

A context-mapping relationship: the downstream context adopts the
upstream context's model wholesale rather than translating. Cheaper
than ACL but the downstream is now coupled to the upstream's design
decisions.

## Customer-Supplier

A context-mapping relationship where the downstream (customer) has a
clear voice in what the upstream (supplier) provides. The upstream is
willing to negotiate, and the downstream's needs influence the
upstream's roadmap.

## Dependency Inversion Principle (DIP)

The "D" in SOLID: depend on abstractions, not concretions. At class
scope, DIP is the local form of the dependency rule — an inner class
declares an interface that an outer class implements, inverting who
depends on whom.

## Domain event

A record of something meaningful that happened in the domain (e.g.,
`OrderPlaced`, `PaymentReceived`). Domain events let aggregates
communicate without holding references to each other and enable
eventual consistency across aggregates or contexts.

## Domain service

A piece of behavior that does not naturally belong to a single entity
or value object — it operates across them. Used only when no single
aggregate is the right home; otherwise the behavior goes on the
aggregate root.

## Eventual consistency

A consistency model where state changes propagate asynchronously and
observers may briefly see stale data. Used between aggregates (within
a context) and between bounded contexts; the alternative —
transactional consistency across aggregates — usually scales poorly.

## Open host service (OHS)

A context-mapping relationship: the upstream context publishes a
stable, well-documented protocol that any downstream can consume.
Often paired with a *published language* so the protocol is the
contract, not the upstream's internal model.

## Repository

A pattern from PoEAA: an outbound port that mediates between the
domain and persistence. The repository interface speaks the domain's
vocabulary (`findCustomerById`, `save(customer)`); its implementation
lives in infrastructure and translates to whatever persistence
technology is in use.

## Shared kernel

A context-mapping relationship where two contexts agree to share a
small subset of the model — but only by explicit coordination. Used
sparingly; changes to the shared kernel require both teams' agreement.

## Subdomain (core / supporting / generic)

A partition of the business domain by strategic importance. **Core**
subdomains are the competitive differentiator (build in-house, invest
heavily). **Supporting** subdomains are necessary but not
differentiating (build pragmatically, often in-house). **Generic**
subdomains are commodity (buy or use off-the-shelf). The subdomain
type informs the integration pattern between contexts.

## Ubiquitous language

A team-agreed vocabulary for one bounded context: every term means the
same thing to every team member and appears unchanged in
conversations, documentation, and code. Drift in the language is a
signal that the context boundary is wrong or that a sub-context is
forming.

## Unit of Work

A pattern from PoEAA: an object that tracks changes to a set of
objects within one transactional scope and coordinates flushing them
atomically. Often implemented under the hood by ORMs (e.g., a session
or a context object).
