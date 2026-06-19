# Migration Playbook

## Scope

Version upgrades, breaking changes, codemods, schema migrations, deprecation
lifecycle, and compatibility matrices. Routes to `api.md` for contract-change
rollout, `errors.md` for deprecation warning copy, and `docs.md` for upgrade
guide patterns.

## Grounding

- **Hyrum Wright — "Hyrum's Law"** — every observable behavior of an interface
  gets depended on, not just the documented surface. Integrators couple to
  timing, error text, ordering, and undocumented defaults. Migrations must
  account for that undocumented coupling, not just formal API changes.
- **Jez Humble & David Farley — *Continuous Delivery*** — release should be
  decoupled from deployment; feature flags allow behavior to ship dark and
  activate separately. The expand-contract (parallel-change) pattern makes
  migrations reversible: add new behavior alongside old, run both in parallel,
  switch reads, then remove the old path — never an atomic break.
- **Scott Ambler & Pramod Sadalage — *Refactoring Databases*** — schema
  changes follow the same incremental principle: add a new column/table
  alongside the existing one, dual-write to both, switch reads to the new
  structure, then remove the old. Each phase is independently deployable and
  independently reversible.

## Good signals

- Deprecation lifecycle is named and documented: warn → deprecated → removed,
  with a stated minimum duration at each phase.
- Codemods or upgrade scripts exist for any non-trivial breaking change;
  users run a single command, not a hand-porting guide.
- Expand-contract pattern is used: new path added first, dual-write/dual-read
  period, reads switched over, old path removed in a later release.
- A compatibility matrix documents supported version pairs (client × server,
  schema version × migration version) and is tested in CI.
- Every deprecation warning includes a "do this instead" pointer — a symbol
  name, flag, or doc URL.
- Upgrade docs include at least one complete worked example tracing old → new,
  including before/after code and any config changes.
- Breaking changes ship behind a flag first; the default-on and default-off
  transitions are each documented with a release version.
- Old paths remain functional for at least one full release after the
  deprecated warning is first emitted.
- Deprecated paths emit usage telemetry, and removal is gated on observed
  traffic dropping to near-zero rather than on a fixed sunset date alone.
- High-risk migrations ship an explicit risk note (lock behavior, backfill
  size, rollback path, blast radius) reviewed separately from the test result.

## Common failures

- Silent breaking change shipped in a minor version — semver contract violated,
  integrators discover breakage in production.
- Deprecation announced with no removal date — warnings accumulate for years
  and lose all urgency.
- No automated upgrade tool for a non-trivial change; users hand-port from a
  prose guide, introducing per-project inconsistencies.
- Integrators discover incompatibility in production rather than in staging,
  because the upgrade path was never exercised in CI.
- Deprecation warning emitted with no remediation pointer — users know
  something is wrong but not what to do about it.
- Schema migration with no rollback path — any failed deploy requires a
  manual recovery procedure.
- Compatibility matrix is missing or stale — integrators run unsupported
  version combinations without warning.
- Migration docs describe the steps but not the rationale; users can't reason
  about edge cases or non-standard environments.
- Deprecated path removed on a calendar deadline while live callers still hit
  it, because no usage signal was instrumented to prove the path was idle.
- A high-risk migration treated as safe because tests passed — no one assessed
  lock behavior, backfill size, rollback path, or blast radius before deploy.

## Heuristics

- **Named deprecation lifecycle** *(design, audit)* — every deprecation moves
  through warn → deprecated → removed, each phase with a documented minimum
  duration. Absence of a removal date is equivalent to no deprecation plan.
- **Codemod for non-trivial upgrades** *(design)* — anything more complex than
  a single rename ships with an automated migration script. Users should be
  able to run one command against their codebase.
- **Expand-contract pattern** *(design)* — add the new path, dual-write,
  switch reads, then remove the old path in a subsequent release. Never
  break and replace atomically.
- **Compatibility matrix** *(audit, design)* — supported version pairs are
  published, versioned alongside the product, and exercised in CI so stale
  entries fail fast.
- **Remediation in every deprecation warning** *(audit, design)* — every
  emitted warning names the replacement symbol, flag, or doc link. A warning
  without a fix pointer is noise, not signal.
- **Tested upgrade path** *(audit)* — a CI job exercises the full upgrade from
  the previous stable release to the current one, on both a clean install and a
  dirty state with existing data.
- **Reversible schema changes** *(design)* — every migration ships an `up` and
  a `down`; both are tested against representative data before release.
- **Deprecation period sized for undocumented coupling** *(audit, design)* —
  assume integrators depend on behaviors that were never officially documented.
  The deprecation window must be long enough for them to discover, adapt, and
  ship — not just long enough for users who read changelogs.
- **Usage-gated removal** *(audit, design)* — emit a metric or log on every
  call to a deprecated path, then gate removal on observed traffic falling to
  near-zero, not on a calendar window alone. A timer that expires while real
  callers remain is a scheduled outage. This subsumes additive-params and
  new-name migrations — both are expand-contract moves whose old path you keep
  until the meter reads empty. (Stripe gates removal of dated API versions on
  per-account usage, not a fixed sunset.)
- **Migration risk is a judgment call, not a CI result** *(audit, design)* —
  a green test suite proves the migration runs, not that it is safe to run.
  High-risk migrations — data backfills, lock-taking DDL, dependency additions
  — carry an explicit risk note covering lock behavior, backfill size, rollback
  path, and blast radius, reviewed by a human separately from the test result.
  Reviewing the risk note is a distinct gate from reading the green check.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is the deprecation lifecycle named with phase durations? | Deprecations linger indefinitely | Document warn/deprecated/removed with minimum timelines |
| Are non-trivial upgrades scripted? | Users hand-port inconsistently | Ship a codemod or upgrade script |
| Is the upgrade path exercised in CI? | Integration surprises in production | Add an upgrade test from previous stable release |
| Does every deprecation warning point to a replacement? | Users don't know what to do | Add remediation pointer to every warning |
| Is the compatibility matrix documented and tested? | Ad hoc version combinations in the wild | Publish and test supported version pairs |
| Do schema migrations include a down path? | Forward-only deploys with no rollback | Add and test down migrations |
| Is removal gated on observed deprecated-path usage? | Calendar removal may break live callers | Instrument per-call usage and remove only when traffic is near-zero |
| Do high-risk migrations carry a risk note reviewed apart from tests? | Green tests mistaken for safe-to-run | Require a lock/backfill/rollback/blast-radius note, reviewed by a human |

## Cross-references

- → `api.md` for contract-change rollout and deprecation versioning.
- → `errors.md` for deprecation warning copy and remediation pointer format.
- → `docs.md` for upgrade guide structure and worked-example patterns.
