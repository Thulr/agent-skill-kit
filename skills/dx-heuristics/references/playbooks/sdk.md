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
- Errors are typed: distinguishable exception classes or `Result` types,
  not string comparison.
- Retries and timeouts have sensible out-of-the-box defaults and are
  configurable per-client or per-call.
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
- No test seam: unit tests must hit the network, making them slow,
  flaky, and credential-dependent.
- Retry behavior is hard-coded or undocumented; callers can't reason about
  or override it.
- Pagination exposes raw cursors and requires the caller to loop manually
  rather than providing an iterator or generator.
- Concurrency safety is unspecified; users guess and occasionally corrupt
  shared state.

## Heuristics

- **Deep-module shape** *(design)* — the public surface area is small;
  complexity (auth, serialization, retry, rate-limit backoff) is handled
  inside, not delegated to callers.
- **Idiomatic-for-language** *(audit, design)* — naming, error handling, and
  resource lifecycle look native. A Python SDK uses snake_case and context
  managers; a Go SDK returns `(value, error)`. A Java port in Python is a
  failure.
- **Typed errors** *(design, debug)* — each failure class has a distinct
  exception or `Result` variant; callers can catch what they can handle and
  let the rest propagate.
- **Configurable retries and timeouts** *(design, audit)* — defaults are
  safe and documented; a `RetryPolicy` or equivalent lets advanced callers
  tune without forking.
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

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are method signatures idiomatic for the language? | Feels like a mechanical port | Restructure to language idioms |
| Are errors distinguishable by type? | Callers pattern-match on strings | Add typed exception classes |
| Can the SDK be stubbed in tests? | Tests hit the network | Add a test seam to the public API |
| Are retries configurable? | Hard-coded or undocumented | Expose a `RetryPolicy` parameter |
| Is pagination exposed as an iterator? | Callers manage cursors manually | Provide an async iterator or generator |
| Is thread-safety documented? | Users guess, concurrency bugs emerge | Add a Concurrency section to the README |

## Cross-references

- → `api.md` for the underlying HTTP/RPC contract and error envelope.
- → `errors.md` for exception message copy and recovery hints.
- → `ide.md` for autocomplete and hover-doc shape.
