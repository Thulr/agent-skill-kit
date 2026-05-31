# Domain Model Playbook

## Scope

Tactical DDD inside a single bounded context: entities, value objects,
aggregates, domain services, domain events. When *not* to use DDD
(CRUD-shaped problems, throwaway scripts, prototypes). How to detect
the anemic-domain anti-pattern and what to do about it.

Out of scope: cross-context modeling (see `bounded-context.md`),
persistence mechanics (see `cross-cutting.md` and `boundaries.md`),
dependency direction (see `dependency-rule.md`).

## Grounding

- **Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart
  of Software* (2003)** — the foundational text; aggregates, entities,
  value objects, domain services, repositories, factories.
- **Vaughn Vernon, *Implementing Domain-Driven Design* (2013)** —
  pragmatic detail: aggregate-design rules, eventual consistency between
  aggregates, transactional boundaries.
- **Martin Fowler, "AnemicDomainModel" (2003)** — names the
  anti-pattern of data-bag entities with logic in service classes.

## Good signals

- Aggregates encapsulate their invariants; you cannot construct an
  aggregate in an invalid state.
- Entities own behavior, not just data. Mutations go through methods on
  the aggregate root.
- Value objects are immutable; equality is by value, not identity.
- Cross-aggregate references are by id; transactional boundaries match
  aggregate boundaries.
- Domain services exist *only* when behavior does not naturally belong
  to a single entity or value object.

## Common failures

- **Anemic entities.** Entity classes are just getters/setters; logic
  lives in `SomethingService` classes that mutate them. The model is
  OO-shaped but procedural in spirit.
- **God aggregate.** A single aggregate root owns most of the domain
  graph; concurrent edits collide constantly; transactions span
  unrelated changes.
- **Aggregate root passing internal collections out.** Callers mutate
  child entities directly, bypassing invariants.
- **Reference by object across aggregates.** A `Customer` aggregate
  holds a direct reference to `Order` aggregates; transactional
  boundaries are unclear.
- **Premature DDD on a CRUD problem.** The domain is genuinely flat
  (one entity per table, no invariants beyond data validation), yet
  the team has built aggregates, repositories, and domain services
  for it. Costs without benefits.

## Heuristics

1. **(audit) Open the largest entity class. Count public getters vs
   public behavior methods.** If getters dominate by ≥ 3:1 and most
   behavior is in `*Service` classes, the model is anemic (severity 2–3
   depending on whether this is core or supporting subdomain).
2. **(audit) For each aggregate, list its invariants.** If you cannot
   list any, the aggregate is probably a data structure, not an
   aggregate.
3. **(audit) Search for cross-aggregate references that are not by id.**
   Every direct object reference between aggregates is a finding;
   severity depends on whether transactional boundaries are violated.
4. **(design) Start aggregate design with the invariants, not the
   nouns.** Group entities and value objects around the smallest
   cluster that enforces one consistency rule.
5. **(design) Make value objects out of every concept with no identity
   of its own.** Money, address, date range, percentage, color, file
   path — none of these need ids.
6. **(design) Use a domain service only when behavior crosses entities
   *and* does not belong to any of them.** Otherwise place the
   behavior on the most appropriate aggregate root.
7. **(refactor) Extract value objects first.** They are the lowest-risk
   refactor (immutable, equality-by-value) and they reveal
   misplaced behavior on entities.
8. **(refactor) Split a god aggregate by listing its invariants and
   regrouping.** Two aggregates that share no invariants should be
   separate aggregates that reference each other by id.
9. **(explain) An anemic model is OO-shaped but procedural in spirit.**
   The cost is encapsulation: invariants live in service classes and
   are bypassed when entities are mutated directly.

## Quick diagnostic

In three minutes: open one entity class at random. (1) Count public
methods that do work (not getters/setters). (2) Search for class names
ending in `Service` in the same package. (3) Open one Service class and
see whether its methods mostly operate on the entity by reading and
writing its fields. If (1) is small and (3) is true, the model is anemic
in this area.

## Cross-references

- `dependency-rule.md` for where the domain layer sits in the dependency
  graph.
- `boundaries.md` for the repository pattern (domain-owned port, infra
  implementation).
- `bounded-context.md` for the limits of one model — different contexts,
  different aggregates.
- `cross-cutting.md` for transactional boundaries and event emission.
