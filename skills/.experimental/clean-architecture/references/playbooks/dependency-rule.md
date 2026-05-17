# Dependency Rule Playbook

## Scope

The dependency rule says: **at every architectural boundary, source-code
dependencies point inward, toward more abstract code.** This playbook
covers detecting violations, designing for the rule from the start, and
inverting wrong-direction dependencies that already exist. SOLID is
treated as the per-class refinement of the same idea, with the
Dependency Inversion Principle as the load-bearing element.

Out of scope: layer mechanics (see `boundaries.md`), domain modeling
(see `domain-model.md`), strategic split (see `bounded-context.md`).

## Grounding

- **Robert C. Martin, *Clean Architecture* (2017)** — the dependency
  rule as the architecture's only load-bearing invariant.
- **Robert C. Martin, *Agile Software Development: Principles, Patterns,
  and Practices* (2003)** — SOLID and the package principles (REP, CCP,
  CRP, ADP, SDP, SAP) that operationalize the rule at module scope.
- **David Parnas, "On the Criteria To Be Used in Decomposing Systems
  into Modules" (1972)** — the earlier framing: information hiding as
  the criterion that predates dependency direction.

## Good signals

- Domain code does not import application code; application code does
  not import infrastructure code; infrastructure code does not import
  framework-vendor types into the domain.
- Outbound interfaces (repository, gateway) are defined in the
  application or domain layer; their implementations live in
  infrastructure.
- Build-time tooling enforces direction (module declarations, package
  visibility, lint rules, archunit/dependency-cruiser).
- Cycle count between top-level modules is zero.

## Common failures

- A domain entity imports its ORM annotations from a framework package.
- A use case calls an HTTP client directly without an outbound port.
- A repository interface lives in the infrastructure module and the
  domain module imports it — the seam is in the right place, but the
  direction is reversed.
- A "core" or "common" module accumulates everything that imports
  everything, becoming a dependency-graph black hole.

## Heuristics

1. **(audit) Run a dependency-direction sweep on the module graph.**
   Generate the static dependency graph (jdeps, madge, pydeps,
   dependency-cruiser). Every arrow from outer-named module to
   inner-named module is a Critical or High finding depending on
   whether it crosses the domain boundary.
2. **(audit) Search for framework imports inside the domain.** Grep for
   ORM annotation imports, HTTP client types, message broker SDK types
   in domain packages. Any hit is High (3); a hit inside an aggregate
   root is Critical (4).
3. **(design) Place every outbound interface in the layer that owns the
   abstraction, not the layer that implements it.** A `CustomerRepository`
   interface used by the domain belongs in the domain; its JPA, Mongo,
   or HTTP implementation belongs in infrastructure.
4. **(design) Apply DIP at every boundary.** When inner code needs to
   trigger an effect, define an outbound port the inner code calls; let
   outer code adapt to it. Never let inner code reach for outer code.
5. **(refactor) Invert a wrong-direction dependency with the
   parallel-change pattern.** Introduce the inner-owned interface;
   point existing callers at it; implement it from the outer layer; flip
   wiring; delete the old direction.
6. **(refactor) Break cycles with the "lift the abstraction" move.** A
   cycle between modules A and B is broken by extracting the shared
   abstraction into a third module C that A and B both depend on,
   without depending on each other.
7. **(explain) The dependency rule and SOLID are the same idea at
   different scales.** The Dependency Inversion Principle expresses
   direction at the class level; the dependency rule expresses
   direction at the architectural level. SDP/SAP express it at the
   package level.

## Quick diagnostic

In two minutes: open the project's top-level package list. Pick the
package whose name you would expect to be most stable (often `domain`,
`core`, or the equivalent). Search for imports inside that package that
reference any other top-level package. Every hit is a candidate
violation; verify against this playbook before classifying severity.

## Cross-references

- `boundaries.md` for how layers, hexagons, and onions present the
  dependency rule geometrically.
- `bounded-context.md` for the dependency rule at the bounded-context
  scale (anti-corruption layer as the cross-context inversion).
- `cross-cutting.md` for how transactions and effects cross the
  dependency-direction boundary without violating it.
