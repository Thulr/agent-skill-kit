# API Playbook

## Scope

Public HTTP/RPC APIs: endpoints, request/response shapes, status codes,
versioning, pagination, idempotency, rate limits. Routes to `sdk.md` for
language-specific bindings, `errors.md` for error response copy, and
`migration.md` for breaking-change handling.

## Grounding

- **Joshua Bloch — *How to Design a Good API and Why It Matters*** —
  if-in-doubt-leave-it-out; APIs should be self-documenting; conceptual weight
  is what you avoid, not what you add.
- **Stripe API Design Guidelines** — concrete patterns for versioning, error
  shape, pagination, idempotency keys, expansion.
- **Hyrum's Law** — every observable behavior of an interface gets depended
  on. What you don't lock is what breaks integrators.

## Good signals

- Endpoint paths name resources (`/users/123/invoices`), not verbs.
- Status codes follow HTTP semantics: 2xx for success classes, 4xx for client,
  5xx for server. Never reuse 200 for errors.
- Error responses share a documented shape: code, message, fields, request_id.
- Pagination uses opaque cursors or stable offsets with explicit limits.
- Idempotency keys are accepted on every mutating endpoint that can be safely
  retried, and the keyed request is recorded before the side effect runs.
- A single machine-readable spec generates the server, the docs, and the
  client; consumer contracts are verified in CI before deploy.
- API version is explicit: in path (`/v1/`), header, or date-pinned. Deprecation
  windows are documented.
- Examples in docs are paste-runnable with one substitution.

## Common failures

- Verbs in paths (`/getUser`, `/createInvoice`) — REST resource model broken.
- 200 OK with `{"error": "..."}` body — clients can't trust status codes.
- Error responses vary by endpoint — clients write per-endpoint parsers.
- Pagination uses unstable offsets — clients miss or duplicate rows.
- No idempotency on writes — duplicate charges on retry.
- Docs and typed client are hand-maintained beside the server — they drift.
- Provider ships a breaking field change no consumer contract caught — an
  integration breaks in production with no pre-deploy signal.
- Breaking change without deprecation window — every integration breaks.
- Examples reference deleted endpoints — first-paste copy fails.

## Heuristics

- **Resource-not-verb paths** *(design, audit)* — paths name what, not how.
- **Documented error shape** *(design, audit, debug)* — one error envelope
  across the API; documented in reference docs.
- **Idempotency by default** *(design)* — every mutating endpoint accepts an
  idempotency key; safe to retry. Persist the keyed request as a durable row
  *before* the side-effecting call, so a retry that arrives mid-flight replays
  the stored result instead of re-running the effect.
- **Spec-as-source-of-truth** *(design, audit)* — one machine-readable API
  definition is authoritative; the server, the OpenAPI docs, and the typed
  client all derive from it, so they cannot drift. Hand-written docs or a
  separately-maintained client are a drift defect.
- **Consumer-driven contracts + deploy gate** *(audit, design, debug)* —
  consumers publish the request/response shape they actually depend on; the
  provider verifies against those contracts in CI. A `can-i-deploy`-style gate
  blocks a release whose deployed-together consumers have not verified the new
  contract. Operationalizes the observable-behavior assumption above.
- **Superset-compatible contract review** *(design, audit)* — when an endpoint
  claims drop-in compatibility with another API, silently accept inapplicable
  standard fields and document each ignored field inline at its endpoint (as
  vLLM notes that `user` is ignored), and route vendor-only parameters through
  one explicit escape hatch (e.g. an `extra_body` field) rather than
  overloading or rejecting the standard schema.
- **Stable pagination** *(audit, design)* — cursors or stable IDs; never raw
  offsets on mutable lists.
- **Explicit versioning** *(design, audit)* — version in path or header; never
  implicit. Deprecation window ≥ documented support period.
- **Observable-behavior contracts** *(audit, design)* — assume integrators depend on
  every observable; lock what you intend, leave room for what you don't.
- **Paste-runnable examples** *(audit)* — every example in docs runs with one
  substitution; tested in CI.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are paths resource-named, not verb-named? | REST model broken | Rename to resources |
| Do all error responses share one documented shape? | Clients re-parse per endpoint | Define one error envelope |
| Do mutating endpoints accept idempotency keys, recorded before the effect? | Retry causes duplicates | Add idempotency support; persist the request first |
| Do server, docs, and client all derive from one spec? | Surfaces drift | Make the spec authoritative; generate the rest |
| Does a deploy gate block on consumer contract verification? | Breaks hit production | Add consumer-driven contracts + a can-i-deploy gate |
| Is the API version explicit (path, header, or date)? | Breaking changes hit everyone | Add explicit versioning |
| Are deprecations documented with a window? | Integrators surprised | Publish deprecation policy |
| Do examples paste-and-run? | First-paste fails, trust dies | Test examples in CI |

## Cross-references

- → `sdk.md` for client-library shape and ergonomics.
- → `errors.md` for error message copy and recovery hints.
- → `migration.md` for breaking-change rollout and deprecation tooling.
