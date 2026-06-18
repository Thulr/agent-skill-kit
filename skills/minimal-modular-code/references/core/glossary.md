# Glossary

Terms used across the playbooks. Definitions are operational, not exhaustive.

- **Slop** — code that consumes review attention without earning it: duplication, dead code,
  speculative generality, needless verbosity, over-abstraction.
- **Right-sizing** — matching the amount of code and structure to the present need and the
  project's scale (see `calibration.md`), not to an imagined future.
- **Minimal** — nothing left to take away: powerful behavior behind a simple interface, not
  fewest lines or smallest units.
- **The wrong abstraction** — a shared abstraction that does not actually fit, kept alive with
  parameters and conditionals; costlier than the duplication it replaced.
- **YAGNI** — "you aren't gonna need it": build for the requirement you have, not one you
  foresee. Applies to features, not to keeping code malleable.
- **Rule of three** — wait until the third occurrence before abstracting; two look-alikes may
  encode different decisions.
- **Deep / shallow module** — deep: a small interface over substantial behavior (good);
  shallow: a large interface over little behavior (a smell).
- **Information hiding** — hide the decision most likely to change behind the interface, so
  callers do not break when it changes.
- **Dependency direction** — which way source-code dependencies point; they should point
  toward the more stable, more abstract code.
- **Complecting** — braiding independent concerns into one unit so they can no longer be
  reasoned about separately.
- **Design rule** — a stable, owned decision (an interface, schema, or standard) that lets the
  modules beneath it change independently.
- **Hidden module** — a unit free to change behind a design rule; cheap to build, replace, or
  delete.
- **Blast radius** — the set of modules and contracts a change can affect; large blast radius
  means coordinate or serialize rather than parallelize.
- **Mirroring** — a system tends to mirror the structure of the organization (or agent fleet)
  that builds it; loosely-coupled builders produce more modular code.
- **Parallel-readiness** — the property that several agents can work concurrently without
  colliding: stable contracts, same-layer partitioning, isolation, known blast radius.
- **Legibility** — behavior readable from the unit, by a human or a context-bound agent,
  without tracing hidden magic.
- **Gate (vs prose)** — a mechanical check (lint, arch-test, CI-required) that fails the build
  on violation, as opposed to an instruction that merely asks.
- **Mechanical vs judgment** — mechanical defects (format, types, forbidden imports, missing
  tests) route back to the agent; judgment calls (migrations, permissions, dependencies,
  reliability, boundary changes) route to a human.
- **Parallel-change (expand-contract)** — introduce the new shape alongside the old, migrate
  callers, then remove the old — so every step is shippable.
- **Branch-by-abstraction** — put an abstraction over the thing being replaced, swap
  implementations behind it, remove the old one when no callers remain.
- **Characterization test** — a test that pins current behavior before a refactor, as a safety
  net.
- **Chesterton's fence** — do not remove something until you understand why it is there.
