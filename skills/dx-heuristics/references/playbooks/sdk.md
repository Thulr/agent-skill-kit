# SDK Playbook

## Scope

Client libraries and language bindings on top of an API: method naming,
type models, error handling, retry and timeout defaults, pagination, and
testability seams. Routes to `api.md` for the underlying HTTP/RPC contract,
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
- One obvious way to accomplish each common task — the happy path is never
  a choice between three equivalent methods.
- Domain types model the business object, not the wire shape; callers work
  with `Invoice`, not `CreateInvoiceResponseBody`.
- Errors are typed: a tiered exception hierarchy keyed to HTTP semantics
  (`APIError` → `RateLimitError`, `AuthenticationError`, etc.), not string
  comparison.
- Retry policy is exponential backoff with **full jitter** plus a
  per-client retry budget (token bucket), and honors a server-supplied
  `Retry-After` / `x-amz-retry-after` header on `429` / `503`.
- Streaming exposes language-native iterators; unknown event shapes do
  not crash the iterator (forward-compatible).
- Middleware / plugin pipeline composes auth, signing, logging, retry,
  and telemetry — none hard-coded into the call path.
- Authentication is a strategy interface, not a hard-coded bearer
  token — supports OAuth, request signing, instance profiles, app
  installations.
- Long-running operations expose a waiter with declarative acceptors
  and a bounded `maxWaitTime`, not a manual sleep-loop.
- Webhook signature verification ships as a helper (HMAC + timestamp
  tolerance + constant-time compare + secret rotation), not rolled
  by hand at every callsite.
- Both sync and async surfaces exist with identical method shapes.
- A deterministic test boundary (spec-generated HTTP mock or swappable
  transport) is published, not just an internal fixture.
- The SDK ships a test seam — a `TestClient`, an interface, or an injected
  transport — so unit tests run offline.
- The thread-safety or concurrency model is documented; users don't have to
  guess whether a client instance is safe to share.

## Common failures

- Pass-through wrappers that expose HTTP request and response shapes
  verbatim — the SDK adds no abstraction value.
- Methods with eight or more positional parameters and no options object;
  call sites are unreadable and argument order is easy to swap.
- All errors caught and re-thrown as a generic `Exception` or `Error` —
  callers can't distinguish a network failure from a validation failure.
- "Retry 3x" with no jitter, no budget, no `Retry-After` honoring —
  failing clients synchronize into a thundering herd and stacked
  retries multiply load.
- Streaming returns raw chunks the caller reassembles; or the iterator
  panics on an event type the SDK predates.
- Auth is hard-coded; a second scheme requires forking.
- Eventually-consistent operations have no waiter; every caller writes
  their own polling loop.
- Webhook verification is a copy-paste snippet in the docs; integrators
  get timestamp tolerance wrong or use non-constant-time compare.
- No test seam: unit tests hit the network and carry credentials.
- Pagination exposes raw cursors and requires manual looping.
- Concurrency safety is unspecified; users guess.
- Sync-only in a primarily-async ecosystem (or vice versa); consumers
  thread-pool-wrap or run-loop-bridge at every callsite.

## Heuristics

- **Deep-module shape** *(design)* — the public surface area is small;
  complexity (auth, serialization, retry, rate-limit backoff) is handled
  inside, not delegated to callers.
- **Idiomatic-for-language** *(audit, design)* — naming, error
  handling, and lifecycle look native: Python uses snake_case + context
  managers; Go returns `(value, error)`. A Java port in Python is a
  failure.
- **Typed errors** *(design, debug)* — each failure class has a distinct
  exception or `Result` variant; callers can catch what they can handle and
  let the rest propagate.
- **Full-jitter retry with budget** *(design, audit)* — backoff is
  `random(0, min(cap, base × 2^retry))`; a per-client token-bucket
  blocks further retries once the failure rate drains the budget;
  `Retry-After` / `x-amz-retry-after` is honored without added jitter.
  Defaults are safe and documented; a `RetryPolicy` lets callers tune
  without forking.
- **Middleware pipeline** *(design, audit)* — auth, logging, retry,
  signing, and telemetry plug into named stages of the request
  lifecycle; new behavior is composable without forking the call path.
- **Pluggable auth strategy** *(design, audit)* — `authStrategy` (or
  credential-provider chain) accepts OAuth, request signing, app
  installations, custom HMAC without forking the client.
- **Waiters / pollers** *(design, audit)* — eventually-consistent
  operations expose a waiter with declarative acceptors, a bounded
  `maxWaitTime`, and exponential-backoff-with-jitter polling. No
  manual sleep loops in user code.
- **Streaming as iterator** *(design, audit)* — SSE / chunked
  responses surface as language-native iterators; the event union is
  open so unknown event types do not crash forward-compatible clients.
- **Webhook signature helper** *(design, audit)* — `verify(payload,
  signature, secret)` is a one-call helper doing HMAC, timestamp
  tolerance, constant-time compare, multi-secret rotation, and
  scheme-pinning to block downgrade.
- **Dual sync/async surface** *(design)* — both `Client()` and
  `AsyncClient()` (or the language equivalent) with identical method
  shapes; consumers pick without thread-pool or run-loop contortions.
- **Deterministic test boundary** *(design, audit)* — a published
  HTTP-mock artifact (generated from the API spec) or a swappable
  transport lets consumers write integration tests without hitting
  the real network or carrying credentials.
- **Offline testability** *(design)* — a `TestClient`, injected transport,
  or interface seam is part of the public API; the README shows how to use it
  in a unit test.
- **Documented concurrency** *(audit, design)* — the library is either
  thread-safe by default (document it) or explicitly not (mark it clearly
  and explain the correct pattern).
- **Pagination iterators** *(design)* — paginated list responses are exposed
  as async iterators or generators; the caller writes `for item in
  client.list(...)` rather than managing cursor state in a loop.
- **Robustness on read** *(audit)* — unknown or optional fields in API
  responses are ignored or preserved, not panicked or discarded silently;
  serialization out is strict.
- **Version disclosure** *(audit, design)* — the SDK exposes its own
  version (`client.version`, `__version__`) and includes it in the
  User-Agent. Support traces any request to a specific SDK build.
- **Cancellation and deadlines** *(design, audit)* — long-running
  methods accept a native cancellation token (`context.Context`,
  `AbortSignal`, `asyncio.timeout`); cancel without leaking
  connections.
- **Debug-mode logging hook** *(design, audit)* — a logger interface and
  `debug` mode emit request/response data with secrets masked. Callers
  don't monkey-patch internals to see the wire.
- **Pinned-and-printable construction** *(audit, design)* — the
  constructor accepts every option a script would override (base URL,
  timeout, retry policy, transport) and exposes them on the instance
  so integrators can verify effective configuration at runtime.

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
| Is streaming exposed as a native iterator? | Callers reassemble chunks | Return an async iterator with an open event union |
| Is webhook verification a one-call helper? | Each integrator rolls crypto | Ship HMAC + timestamp + constant-time helper |
| Are both sync and async surfaces available? | Wrong-color contortions at every callsite | Add the missing surface with identical method shapes |
| Is pagination exposed as an iterator? | Callers manage cursors manually | Provide an async iterator or generator |
| Is thread-safety documented? | Users guess, concurrency bugs emerge | Add a Concurrency section to the README |

## Cross-references

- → `api.md` for the underlying HTTP/RPC contract and error envelope.
- → `errors.md` for exception message copy and recovery hints.
- → `ide.md` for autocomplete and hover-doc shape.
- → `package.md` for type definitions, source maps, and registry-page metadata
  that ship with the SDK.
- → `examples.md` for runnable sample apps integrators paste from.
- → `logging.md` for the SDK's debug-mode and secret-redaction contract.
