# Boundaries Playbook

## Scope

How layers, hexagons, and onions express the same idea — separation of
concerns enforced by direction — and how to design, audit, and refactor
the seams themselves. Covers ports & adapters mechanics, layer roles
(domain / application / interface / infrastructure), deep-modules vs
shallow-modules, and frontend analogs (Flux/Elm unidirectional flow).

Out of scope: which direction the dependencies should point (see
`dependency-rule.md`), domain modeling inside a layer (see
`domain-model.md`).

## Grounding

- **Alistair Cockburn, "Hexagonal Architecture" (2005)** — ports and
  adapters; symmetric inbound/outbound framing.
- **Jeffrey Palermo, "The Onion Architecture" (2008)** — concentric
  rings as a visualization of the same dependency-rule.
- **Robert C. Martin, *Clean Architecture* (2017)** — entity /
  use-case / interface-adapter / framework concentric layers.
- **Martin Fowler, *Patterns of Enterprise Application Architecture*
  (2002)** — Repository, Unit of Work, Data Mapper, Service Layer:
  the catalog underwriting most adapter-side mechanics.
- **John Ousterhout, *A Philosophy of Software Design* (2018)** — deep
  modules (simple interface, rich implementation) as the seam-quality
  test.
- **David Parnas (1972)** — information hiding as the criterion for
  what a boundary should hide.
- **Facebook, "Flux: An Application Architecture for React" (2014)**
  and **Evan Czaplicki, "The Elm Architecture" (2015)** — frontend
  analogs: unidirectional flow as the dependency-rule for UI state.

## Good signals

- Inbound ports (use-case interfaces) and outbound ports (repository,
  gateway interfaces) are both expressed in domain vocabulary.
- Each layer has a single, named purpose; a new contributor can describe
  it in one sentence.
- Adapters are *thin* — translation only, no business logic.
- Frontend: actions flow one direction (action → reducer/update → view);
  views never mutate state directly.
- Deep modules: the interface is smaller than the implementation by an
  order of magnitude.

## Common failures

- **Anemic port.** An "interface" that exposes every internal method;
  callers couple to implementation shape rather than to a sealed
  contract.
- **Leaky adapter.** An adapter that returns framework types
  (`ResultSet`, `HttpResponse`, `EntityManager`) up the call stack
  rather than translating them.
- **Layer-skipping.** A controller calls the repository directly,
  bypassing the use case; the application layer becomes vestigial.
- **God use case.** A single use case grows to coordinate every action
  on an aggregate; should split along command boundaries.
- **Framework-coupled use case.** A use case takes
  `HttpServletRequest` (or equivalent) as a parameter; its inbound
  port now leaks HTTP.

## Heuristics

1. **(audit) Walk the call path of one real request inward.** Note
   every type crossing a layer boundary. Each framework type that
   survives more than one boundary inward is a leaky adapter (severity
   2–3).
2. **(audit) Apply the deep-module test to every port.** Count public
   methods; estimate implementation complexity. Shallow ports (many
   methods, little behavior) are smells; severity 2.
3. **(design) Define inbound and outbound ports symmetrically.** Inbound
   = what the application can do; outbound = what the application
   needs. Adapter directions invert: inbound adapters call the
   application; outbound adapters are called by the application.
4. **(design) Use the Repository pattern as the canonical outbound
   port for persistence.** The repository interface speaks domain
   vocabulary (`findCustomerById`, not `executeQuery`); the
   implementation lives in infrastructure.
5. **(design) For frontend code, treat the store as the outbound port
   and the view as the inbound adapter.** Effects (HTTP, storage,
   timers) live in middleware/effect-handlers; updates are pure.
6. **(refactor) Extract a port with characterization tests as a
   safety net.** Write tests that pin current behavior at the seam,
   introduce the port behind the seam, switch callers, verify tests
   still pass.
7. **(refactor) Lift framework types out of the use case with a DTO.**
   The use case takes a plain-old object; an inbound adapter
   constructs the DTO from the framework's request type. The use
   case's port no longer mentions the framework.
8. **(explain) Layered, hexagonal, and onion are three drawings of the
   same idea.** Layered shows horizontal stripes; hexagonal shows
   inbound/outbound symmetry; onion shows concentric rings. Pick the
   drawing that helps the reader; the rule does not change.

## Quick diagnostic

In five minutes: pick one inbound port (a use case or controller
method). Trace from it down to the database or external service.
Count how many types you cross that are *not* defined in your codebase
(framework types, library types, vendor SDK types). If any of those
types are *return* values that flow back up past the use case, you
have a leaky adapter. If any are *parameters* to the use case itself,
your inbound port leaks the framework.

## Cross-references

- `dependency-rule.md` for which direction the boundaries enforce.
- `domain-model.md` for what lives inside the innermost layer.
- `bounded-context.md` for boundaries at the strategic scale.
- `cross-cutting.md` for how errors, transactions, and side-effects
  cross boundaries without violating them.
