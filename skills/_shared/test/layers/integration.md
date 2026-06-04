# Integration Test Playbook

## Scope

Tests that exercise the SUT against real collaborators across one boundary at a time — the database, a queue, an HTTP service, the file system. Routes to `unit.md` when the test could be done in isolation. Routes to `e2e-ui.md` when crossing multiple boundaries through the UI. Routes to `contract.md` when verifying a service-to-service contract.

## Grounding

- **Gerard Meszaros — *xUnit Test Patterns: Refactoring Test Code*** — fixture-management patterns (transient / persistent / shared), test-data builders, and the anti-pattern catalog for shared-state coupling between integration tests.
- **Jez Humble & David Farley — *Continuous Delivery*** — environment parity, the deployment pipeline as the integration-test runner, and the role of integration tests in detecting drift between dev and prod.
- **Sam Newman — *Building Microservices*** — the integration boundary as a contract; how to test against real infrastructure without brittleness; testcontainers/localstack-style real-but-controlled dependencies.

## Good signals

- Tests use the real DB / queue / HTTP collaborator — or a high-fidelity emulator (e.g., a containerized real service), not an in-process fake.
- Each test owns its data lifecycle: creates the rows it needs, deletes them in teardown — or runs in a transaction that's rolled back.
- A test that fails fails for one reason: it crosses one boundary, not three.
- Real error shapes are exercised: connection drop, timeout, partial write, retry-creates-duplicate.
- The same test passes locally (Linux, macOS) and in CI; passes alone and in the full suite; passes on a clean DB and a re-seeded one.
- Integration suite is opt-in (`--integration`, `make integration`, separate CI job) so the unit suite stays fast.
- Tests are idempotent or transactional — rerunning leaves no detritus.

## Common failures

- Test depends on a row that was created by another test — when run alone, it fails.
- Hard-codes IDs (`user_id=1`) that match a seed file but break when the seed changes.
- Mixes three boundaries in one test (HTTP → DB → external API). When it fails, you don't know which broke.
- Uses an in-process fake to "test the integration" — that's a unit test in disguise. False-pass risk.
- Real network calls to third parties → flake when the third party hiccups, slow when the third party is slow.
- Cleanup in `tearDown` only — when the test crashes mid-run, the next run is poisoned.
- Runs alongside unit tests in the same `make test` — slows the inner loop, encourages people to skip tests.

## Heuristics

- **Real I/O at the boundary** *(audit, author)* *(false-pass)* — uses the real DB / queue / HTTP collaborator (or a high-fidelity emulator like testcontainers), not an in-process fake. If you're stubbing the thing the integration test is supposed to integrate with, it's a unit test pretending.
- **Owns its data lifecycle** *(audit, author)* *(flakiness, brittleness)* — creates the fixtures it needs and removes them; doesn't depend on database seed order or another test's leftover rows. Transaction-rollback or unique-per-run identifiers both work.
- **Single failure surface per test** *(audit, author)* *(confusion)* — exercises one boundary at a time. A test that crosses three boundaries fails ambiguously and triages slowly.
- **Replays real error shapes** *(audit, author)* *(gap)* — connection drop, timeout, partial write, retry-creates-duplicate, deadlock. Happy-path-only integration tests are gap factories.
- **Environment-independent** *(audit)* *(flakiness)* — passes when run alone and in the full suite; on Linux and macOS; in CI and locally; on a fresh DB and a re-seeded one. Differences here are bugs in the test, not bugs in the runner.
- **Tagged & isolated from unit run** *(audit, strategize)* *(cost)* — opt-in via flag (`--integration`, `pytest -m integration`, separate CI job) so the unit suite stays fast. The fast-feedback loop is the most valuable property of the test suite.
- **Idempotent or transactional** *(audit, author)* *(flakiness)* — rerunnable without manual cleanup. Either wrap each test in a rolled-back transaction, or use unique-per-run identifiers (UUIDs, timestamped names) so the test can be re-run after a crash.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does the test use the real collaborator? | False-pass risk | Replace in-process fake with a containerized real service |
| Does the test own its data? | Flake when run alone or in CI | Add setup creates / teardown deletes; or use transaction rollback |
| Does it cross one boundary or many? | Diagnostic ambiguity on failure | Split into per-boundary tests |
| Are error paths exercised? | Gap on real-world failures | Add tests for the canonical error shapes for this boundary |
| Does it run alongside unit tests? | Suite slows; people skip | Tag and run separately |
| Is teardown crash-safe? | Test poisons the next run | Move cleanup before setup, or use transactional fixtures |

## Cross-references

- → `unit.md` when the test could be done in isolation
- → `e2e-ui.md` when crossing multiple boundaries through the UI
- → `contract.md` when verifying a service-to-service contract
- → `core/failure-modes.md` — flakiness and false-pass are the two highest-frequency modes at this layer
- → `core/personas.md` — persona 2 (on-call) is the right lens; integration test failures are usually what wakes them up
