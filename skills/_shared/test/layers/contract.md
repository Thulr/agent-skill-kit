# Contract Test Playbook

## Scope

Tests that verify the *contract* between a consumer and a provider — usually two services communicating over HTTP, gRPC, or a message queue. Distinct from integration tests, which test the consumer against a real provider. Routes to `integration.md` when you actually need to verify the integration. Routes to `e2e-ui.md` when the consumer-provider interaction has to be exercised through the full stack.

## Grounding

- **Ian Robinson — "Consumer-Driven Contracts: A Service Evolution Pattern"** — the CDC pattern: consumers state what they actually use, providers verify that subset. The foundation of modern contract testing.
- **Pact Foundation documentation** — the de-facto practical implementation; broker-published pacts, provider-side verification, integration into CI for both sides.
- **Sam Newman — *Building Microservices*** — contract testing as the layer that replaces many cross-service e2e tests; the relationship between contracts and service evolution.

## Good signals

- The consumer writes the contract describing the responses it actually relies on (fields, types, status codes). The provider verifies it can satisfy the contract.
- Contracts are versioned and published to a shared mechanism (a broker, a file in a known repo, an OCI registry).
- Provider verification runs in the *provider's* CI, gating provider releases. Without this, contracts are documentation, not protection.
- Setup states are explicit and named: "given an active user exists with id=42", not implicit DB state.
- The contract describes the wire shape (JSON structure, headers, status codes), not the internal implementation types of either side.
- Contract suite replaces (rather than supplements) most cross-service e2e tests; the team trusts the contracts enough to delete the duplicate e2e coverage.

## Common failures

- Provider-written contracts: the provider declares what *it* returns, not what the consumer uses. Drift goes undetected because the contract isn't anchored in real consumer behavior.
- Contracts asserting on internal types (`User.firstName` matches a Java field exactly) — refactoring breaks the contract for no observable reason.
- Provider verification runs only on consumer CI, not provider CI — provider ships a breaking change and the consumer's next build catches it (too late).
- Implicit setup: the contract says "GET /users/42 returns a User", but doesn't state that User 42 must exist. The provider implementation under test happens to have a seeded User 42 — false-pass.
- Contracts and e2e tests both maintained for the same interaction — double cost, no extra signal.
- Contracts aren't versioned; updating breaks consumers silently.

## Heuristics

- **Consumer-driven, not provider-driven** *(audit, author)* *(gap)* — the consumer states what it actually uses; the provider verifies that subset. Provider-driven contracts overspecify (the provider declares everything it returns, most of which no consumer reads) and underspecify (they miss what the consumer expects but the provider doesn't think to declare).
- **Tests the wire shape, not the impl** *(audit)* *(brittleness)* — JSON structure, headers, status codes — not internal class names or field types. An internal rename in either service should not require a contract change.
- **Versioned and broker-published** *(audit)* *(gap)* — pacts shared via a known mechanism (broker, repo, registry); both sides know which version is canonical. Without versioning, evolution becomes a coordination nightmare.
- **Provider verification runs in provider's CI** *(audit)* *(gap)* — the provider cannot ship a breaking change without seeing it. Verification only on the consumer side means the consumer catches the break after the fact, in production or in the next consumer build.
- **States are explicit** *(audit, author)* *(false-pass)* — "given an active user exists with id=42" is part of the contract; implicit setup hides the assumptions and lets the test pass for the wrong reasons.
- **Decoupled from end-to-end** *(strategize)* *(cost)* — contract tests *replace* most cross-service e2e tests; running both is duplication. The whole value of contract testing is the dramatic reduction in expensive cross-service e2e coverage.
- **Backward compatibility checked** *(audit, author)* *(gap, brittleness)* — new contract versions should be additive when possible; breaking changes flagged explicitly and coordinated with consumer rollout. The contract suite is the early-warning system for SemVer commitments.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is the contract consumer-driven? | Drift goes undetected | Have the consumer write the contract from real usage |
| Does it describe the wire shape only? | Brittle on internal refactor | Strip internal type references; assert on JSON structure |
| Is it versioned and broker-published? | Coordination breaks down | Adopt a broker or repo-based pact-sharing mechanism |
| Does provider CI run verification? | Provider ships breaks blindly | Add the contract-verification step to provider CI |
| Are setup states explicit? | False-pass on accidental seed state | Name and seed states explicitly per contract scenario |
| Have you removed duplicate e2e coverage? | Cost without extra signal | Audit e2e suite; delete what the contracts now cover |

## Cross-references

- → `integration.md` when you actually need to verify the live integration
- → `e2e-ui.md` when consumer-provider interaction must run through the full stack
- → `core/failure-modes.md` — gap (provider ships untested breakages) is the headline mode at this layer
- → `core/personas.md` — persona 3 (suite operator) sees the cost reduction; persona 2 (on-call) sees the catches
