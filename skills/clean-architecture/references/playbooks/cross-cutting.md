# Cross-Cutting Concerns Playbook

## Scope

How errors, transactions, side-effects, observability, and integration
flow *through* layered/hexagonal/onion architecture without violating
the dependency rule. Effect isolation patterns from the Elm
architecture; integration patterns between bounded contexts; the
"defining errors out of existence" framing for error design.

Out of scope: layer mechanics (see `boundaries.md`), modeling inside
one layer (see `domain-model.md`).

## Grounding

- **Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns*
  (2003)** — messaging, channels, translators, routers: integration
  between contexts without shared state.
- **Vlad Khononov, *Learning Domain-Driven Design* (2021)** — how
  subdomain type informs cross-cutting choices (eventual consistency
  between contexts, transactional consistency within a context).
- **John Ousterhout, *A Philosophy of Software Design* (2018)** —
  defining errors out of existence; exceptions as part of the API
  surface.
- **Martin Fowler, *Patterns of Enterprise Application Architecture*
  (2002)** — Unit of Work, transactions across repositories.
- **Evan Czaplicki, "The Elm Architecture" (2015)** — explicit
  side-effect handling via commands; pure updates separated from
  effects.

## Good signals

- Errors are typed at the layer that owns them; outer layers map them
  into their own vocabulary (HTTP status, UI message) rather than
  propagating raw.
- Transactions are scoped to a single aggregate's invariants;
  cross-aggregate consistency is eventual.
- Side-effects are made explicit at the layer boundary (a command
  returned from an update, a use case calling an outbound port) rather
  than buried in domain methods.
- Cross-context communication is asynchronous when subdomain types
  allow (consumer of a generic subdomain), synchronous only with
  explicit reason.
- Observability is layered: the domain emits domain events; the
  application layer emits use-case telemetry; infrastructure handles
  request/response logging.

## Common failures

- **Throwing infrastructure exceptions from the domain.** A
  `SQLException` or `JpaException` propagates up unchanged; outer
  layers must know infrastructure types to handle them.
- **Cross-aggregate transactions.** A single transaction modifies
  three aggregates; concurrent edits collide; transactions get longer
  over time.
- **Side-effects buried in domain methods.** An entity method writes
  to an audit log or sends an email directly; the method is no
  longer testable in isolation.
- **Synchronous cross-context calls in chains.** A → B → C → D as
  blocking HTTP calls; one slow service slows them all; failures
  cascade.
- **Untyped errors.** Every layer throws `Exception`; callers cannot
  distinguish recoverable from non-recoverable failures.

## Heuristics

1. **(audit) Search for infrastructure exception types in the domain
   layer.** Any catch or throw of an ORM, HTTP, or messaging exception
   from inside the domain is a High finding (3).
2. **(audit) Map transactional scope to aggregates.** If a single
   transaction modifies multiple aggregates, it is a finding — severity
   2–3 depending on whether aggregate consistency is at risk.
3. **(audit) For each cross-context call, name the failure mode.** If
   you cannot name what happens when the called context is unavailable
   (queue, retry, fallback, fail-fast), the integration is undefined.
4. **(design) Type errors at the layer that owns the concept.** A
   `CustomerNotFound` is a domain or application error; `JdbcConnectionFailed`
   is an infrastructure error. Outer layers map between them.
5. **(design) Make side-effects return from update functions, not
   happen inside them.** A use case returns a command describing the
   effect; an effect-handler/coordinator executes it; the use case
   stays testable as a pure function over its inputs.
6. **(design) Choose async-by-default for cross-context integration in
   supporting and generic subdomains.** Async with idempotent
   consumers tolerates more failure modes than synchronous chains.
7. **(design) Define errors out of existence where possible.** A
   nullable return type, an empty collection, a no-op operation can
   often replace an exception; reserve exceptions for unrecoverable
   conditions.
8. **(refactor) Lift side-effects out of the domain with the
   command/event pattern.** Domain methods return a list of intents;
   the application layer executes them; tests assert the returned
   intents rather than mocking effect ports.
9. **(refactor) Replace cross-aggregate transactions with eventual
   consistency.** Emit a domain event from one aggregate; a handler
   in the application layer reads the event and modifies the other
   aggregate in a separate transaction.
10. **(explain) The dependency rule does not say layers cannot
    communicate — only that the direction of source-code dependency
    is fixed.** Cross-cutting concerns flow through the layers; they
    do not invert them.

## Quick diagnostic

In five minutes: pick one HTTP endpoint. Trace down to a database
write. Note every exception type that could escape that path; for
each, identify which layer owns the type. Then look for any side-
effect (email, log, audit, metric, queue publish) executed along the
path; identify which layer triggers it and whether the trigger is
explicit (port/command) or implicit (method call inside the domain).

## Cross-references

- `dependency-rule.md` for the direction errors and effects must
  respect.
- `boundaries.md` for the layer boundaries errors cross.
- `domain-model.md` for the aggregate boundary that transactions
  must respect.
- `bounded-context.md` for cross-context integration choices.
