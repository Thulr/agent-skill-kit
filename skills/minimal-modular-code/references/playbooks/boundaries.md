# Boundaries Playbook

## Scope

Where the seams go and which way dependencies point — at the scale of one module or one
change. Covers dependency direction, deep modules, information hiding, and adding the seam
a present need forces rather than a prescribed target architecture.

- **In:** dependency direction, deep vs shallow modules, information hiding, thin adapters,
  inverting a wrong-direction dependency, breaking cycles.
- **Out:** repo-scale partitioning and contracts for parallel agents (see
  `parallel-readiness.md`); how much code there is (see `minimalism.md`).
- **Intents this surface answers:** do, review, design.

## Grounding

- **David Parnas (1972)** — information hiding: hide the likely-to-change decision behind a
  stable interface; that is the criterion for where a boundary goes.
- **John Ousterhout, A Philosophy of Software Design (2018)** — deep modules: a simple
  interface over substantial behavior; shallow modules (big interface, little behavior) are
  the smell.
- **Baldwin & Clark, Design Rules (2000)** — a stable interface lets the implementation
  behind it change or be replaced cheaply.
- **Rich Hickey, "Simple Made Easy" (2011)** — do not complect independent concerns into
  one module; one concept per unit.
- **Meng & Jackson (2025)** — independent concepts joined by explicit synchronizations,
  not hidden coupling.

## Good signals

- A module's interface is markedly smaller than its implementation.
- Source-code dependencies point toward the more stable, more abstract code; the volatile
  outer code depends on the stable inner code, not the reverse.
- Adapters translate at the edge; framework and vendor types do not travel inward past the
  boundary.
- The decision most likely to change is hidden behind the interface, so callers do not
  break when it changes.
- The number of distinct concepts a unit touches is one, not several braided together.

## Common failures

- **Shallow module / anemic interface** — an "interface" exposing every internal method;
  callers couple to the implementation shape, so the seam buys nothing.
- **Leaky adapter** — a function returns a framework type (`ResultSet`, `HttpResponse`) up
  the call stack instead of translating it; inner code now knows an outer concern.
- **Wrong-direction dependency** — stable inner code imports volatile outer code; a change
  to the edge ripples into the core.
- **Speculative hexagon** — ports, adapters, and rings added as a target architecture
  before any present need forces the seam; ceremony that is itself over-engineering (see
  `minimalism.md`).
- **Braided module** — one unit owns several independent concerns; a change to one forces
  understanding all of them.

## Heuristics

- **(do, review) Check dependency direction.** Dependencies should point toward the stable
  abstraction. A volatile-to-stable import is fine; a stable-to-volatile import (core code
  importing a framework, a domain importing its ORM types) is a finding — severity 3, or 4
  inside the most stable code.
- **(review) Apply the deep-module test.** Count interface surface against implementation
  weight; a many-method module with little behind it is shallow — severity 2.
- **(design) Add the seam you need, not a prescribed target.** Layered, hexagonal, and
  onion drawings all express the same direction idea; pick the one that helps a reader and
  introduce a port only when a present need (an effect to isolate, a second implementation)
  forces it.
- **(do) Keep adapters thin.** Translate framework/vendor types at the edge; do not let
  them travel inward. A foreign type surviving more than one boundary inward is a leak.
- **(design) Place an interface in the layer that owns the abstraction**, not the one that
  implements it; the implementation depends on the interface, not the reverse.
- **(do) Keep patch snippets complete at the boundary they introduce.** If the answer shows
  a port or adapter in code, include the imports for newly referenced local types. With
  partial context, prefer concise guidance over invented multi-file snippets; keep uncertain
  adapter details conceptual and say their import paths depend on the repo. An incomplete
  snippet is not a safe minimal patch.
- **(do, design) Hide the likely-to-change decision.** Choose the boundary by what should
  be hidden behind it, so callers are insulated from the volatile part.
- **(design) Keep one concept per unit.** If a module is hard to name, it is probably
  braiding several concerns — split along the concepts.
- **(design) Invert a wrong-direction dependency with parallel-change.** Introduce the
  stable-side interface, point callers at it, implement it from the outer layer, flip the
  wiring, delete the old direction. Break a cycle by lifting the shared abstraction into a
  third module both depend on.

## Quick diagnostic

- Is the interface smaller than the implementation? — no → the module is shallow; deepen it
  or fold it in.
- Does the most stable module import any less-stable one? — yes → candidate wrong-direction
  dependency; verify against the dependency graph.
- Are you adding a port/adapter for a need that exists today? — no → defer it; the seam is
  speculative.
- Can you state the one concept this unit owns in a single phrase? — no → it is braided;
  split it.

## Cross-references

- `minimalism.md` — a seam you do not need yet is over-engineering.
- `parallel-readiness.md` — boundaries at repo scale become the contracts that let agents
  work in parallel.
- `legibility.md` — a well-placed seam should also be readable from the unit.
- `references/intents/{do,review,design}.csv` row `boundaries` — the entry points.
