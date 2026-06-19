# SDK Playbook

## Scope

Client libraries and language bindings on top of an API: method naming,
type models, error handling, retry and timeout defaults, pagination, and
testability seams. Routes to `api.md` for the HTTP/RPC contract,
`errors.md` for exception and error-message copy, and `ide.md` for
autocomplete and hover-doc shape.

## Grounding

- **Joshua Bloch — *How to Design a Good API and Why It Matters*** —
  modules over methods; if-in-doubt-leave-it-out; SDKs should be
  self-documenting; a good API is easy to use correctly and hard to misuse.
- **John Ousterhout — *A Philosophy of Software Design*** — deep modules:
  small, clean surface area hiding complex implementation; shallow modules
  that mirror their internals are a design smell.
- **Postel's Law (robustness principle)** — be conservative in what you
  send, liberal in what you accept; apply to SDK serialization and
  deserialization respectively.

## Good signals

- Method and type names follow the idioms and casing conventions of the
  target language, not the HTTP or wire format.
- One obvious way to accomplish each common task — the happy path is
  never a choice between three equivalent methods.
- Domain types model the business object, not the wire shape; callers work
  with `Invoice`, not `CreateInvoiceResponseBody`.
- Errors are typed: a tiered exception hierarchy keyed to HTTP semantics
  (`APIError` → `RateLimitError`, `AuthenticationError`, etc.), not string
  comparison.
- Retry, streaming, auth, waiters, and webhook verification are deep
  built-ins — full-jitter retry with budget and `Retry-After`,
  forward-compatible iterators, a pluggable auth strategy, declarative
  waiters, and a signature helper — none rolled at the callsite.
- A published test seam lets unit tests run offline; both sync and async
  surfaces exist with identical shapes; the concurrency model is
  documented.

## Common failures

- Pass-through wrappers that expose HTTP request/response shapes
  verbatim — the SDK adds no abstraction value.
- Methods with eight or more positional parameters and no options object;
  call sites are unreadable and argument order is easy to swap.
- All errors caught and re-thrown as a generic `Exception` or `Error` —
  callers can't distinguish a network failure from a validation failure.
- "Retry 3x" with no jitter, no budget, no `Retry-After` honoring —
  failing clients synchronize into a thundering herd.
- Streaming returns raw chunks, or the iterator panics on an event type
  the SDK predates; auth is hard-coded and a second scheme requires
  forking; eventually-consistent operations have no waiter; webhook
  verification is a copy-paste snippet integrators get wrong.
- No test seam: unit tests hit the network and carry credentials.
- Pagination exposes raw cursors and requires manual looping; concurrency
  safety is unspecified, so users guess.
- Sync-only in an async ecosystem (or vice versa); consumers bridge
  colors at every callsite.

## Heuristics

- **Deep-module shape** *(design)* — the public surface is small;
  complexity (auth, serialization, retry, backoff) is handled inside,
  not delegated to callers.
- **Idiomatic-for-language** *(audit, design)* — naming, errors, and
  lifecycle look native (Python snake_case + context managers; Go
  `(value, error)`). A Java port in Python is a failure.
- **Typed errors** *(design, debug)* — each failure class has a distinct
  exception or `Result` variant; callers catch what they handle and let
  the rest propagate.
- **Full-jitter retry with budget** *(design, audit)* — backoff is
  `random(0, min(cap, base × 2^retry))`; a per-client token-bucket
  blocks further retries once the failure rate drains the budget;
  `Retry-After` / `x-amz-retry-after` is honored without added jitter,
  including a producer-side `429` carrying a concrete wait time.
  Defaults are safe; a `RetryPolicy` lets callers tune without forking.
- **Middleware pipeline** *(design, audit)* — auth, logging, retry,
  signing, and telemetry plug into named lifecycle stages; new behavior
  is composable without forking the call path.
- **Pluggable auth strategy** *(design, audit)* — `authStrategy` (or
  credential-provider chain) accepts OAuth, request signing, app
  installations, and custom HMAC without forking the client.
- **Waiters / pollers** *(design, audit)* — eventually-consistent
  operations expose a waiter with declarative acceptors, a bounded
  `maxWaitTime`, and backoff-with-jitter polling — no manual sleep loops.
  For durable execution, distinguish at-most-once steps from retried
  activities, pair side effects with compensation finalizers, and pass
  large payloads by reference, not inline.
- **Streaming as iterator** *(design, audit)* — SSE / chunked
  responses surface as language-native iterators; the open event union
  means unknown event types do not crash forward-compatible clients.
- **Webhook signature helper** *(design, audit)* — `verify(payload,
  signature, secret)` is a one-call helper doing HMAC, timestamp
  tolerance, constant-time compare, multi-secret rotation, and
  scheme-pinning.
- **Dual sync/async surface** *(design)* — both `Client()` and
  `AsyncClient()` (or equivalent) with identical method shapes;
  consumers pick without color-bridging contortions.
- **Deterministic test boundary** *(design, audit)* — a published test
  seam (`TestClient`, injected transport, or spec-generated HTTP mock) is
  part of the public API, so consumers test offline without the real
  network or credentials; the README shows it in a unit test.
- **Documented concurrency** *(audit, design)* — the library is either
  thread-safe by default (document it) or explicitly not (mark it and
  explain the correct pattern).
- **Pagination iterators** *(design)* — paginated lists surface as async
  iterators or generators; the caller writes `for item in client.list(...)`
  instead of managing cursor state.
- **Robustness on read** *(audit)* — unknown or optional response fields
  are ignored or preserved, not panicked or discarded silently;
  serialization out is strict.
- **Parse, don't validate** *(design, audit)* — decoding returns the
  usable typed value (`parse(str) -> URL`), not a boolean validity check
  the caller re-decodes after. Once it parses, the type proves the
  invariant; downstream code never re-validates.
- **Caller-transparent batch-coalescing** *(design)* — expose a narrow
  per-item interface (`.load(key)` returning one value) and coalesce
  concurrent calls into a single backend batch behind it; callers never
  hand-roll batch coordination.
- **Adoption friction as a design axis** *(audit, design)* — minimize the
  assumptions the library forces on the consumer's stack (runtime, build
  step, type system, framework); the fewer assumed, the thinner the slice
  a consumer can adopt. Weigh adoption cost as a first-class constraint.
- **Per-call cost bound and fallback** *(design, audit)* — calls to
  metered or degradable backends carry an explicit cost/budget bound and
  a documented fallback or provider-switch contract; a consumer caps
  spend and reroutes without forking.
- **Version disclosure** *(audit, design)* — the SDK exposes its own
  version (`client.version`, `__version__`) and sends it in the
  User-Agent, so support traces any request to a specific build.
- **Cancellation and deadlines** *(design, audit)* — long-running
  methods accept a native cancellation token (`context.Context`,
  `AbortSignal`, `asyncio.timeout`) and cancel without leaking
  connections.
- **Resource-safety finalizers** *(design, audit)* — client and
  connection lifecycles run cleanup on success, failure, AND
  cancellation/interrupt (bracket / try-with-resources / RAII), so no
  exit path leaks a handle — not just on cancel.
- **Debug-mode logging hook** *(design, audit)* — a logger interface and
  `debug` mode emit request/response data with secrets masked, so callers
  never monkey-patch internals to see the wire.
- **Pinned-and-printable construction** *(audit, design)* — the
  constructor accepts every option a script would override (base URL,
  timeout, retry policy, transport) and exposes them on the instance, so
  integrators verify effective config at runtime.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are method signatures idiomatic for the language? | Feels like a mechanical port | Restructure to language idioms |
| Are errors distinguishable by type? | Callers pattern-match on strings | Add typed exception classes |
| Can the SDK be stubbed in tests? | Tests hit the network | Add a test seam to the public API |
| Are retries configurable? | Hard-coded or undocumented | Expose a `RetryPolicy` parameter |
| Does retry use full jitter and honor `Retry-After`? | Thundering herd on recovery | Switch to full-jitter backoff + retry budget; honor server timing |
| Is auth a strategy interface? | Second auth scheme requires forking | Accept a credential-provider chain or `authStrategy` |
| Do long operations expose a waiter? | Callers write manual polling loops | Ship declarative waiters with acceptors and bounded timeouts |
| Is streaming a native iterator with an open event union? | Callers reassemble chunks | Return an async iterator |
| Is webhook verification a one-call helper? | Each integrator rolls crypto | Ship HMAC + timestamp + constant-time helper |
| Does decoding return the usable typed value? | Caller re-validates after a boolean check | Parse, don't validate |
| Do finalizers run on success, failure, AND cancel? | A handle leaks on some exit path | Wrap lifecycles in bracket / try-with-resources |
| Is thread-safety documented? | Users guess, concurrency bugs emerge | Add a Concurrency section to the README |

## Cross-references

- → `api.md` for the underlying HTTP/RPC contract and error envelope.
- → `errors.md` for exception message copy and recovery hints.
- → `ide.md` for autocomplete and hover-doc shape.
- → `package.md` for type definitions, source maps, and registry-page metadata
  that ship with the SDK.
- → `examples.md` for runnable sample apps integrators paste from.
- → `logging.md` for the SDK's debug-mode and secret-redaction contract.
