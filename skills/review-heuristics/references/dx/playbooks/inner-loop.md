# Inner Loop Playbook

## Scope

Edit-run-test cycle: narrow vs. full test commands, watch mode, fixtures,
build/typecheck/lint paths, hot reload, and the pre-PR gate. Routes to
`setup.md` for one-time environment installation, and `contributor.md` for
the PR loop layered on top of the inner loop.

## Grounding

- **Nicole Forsgren, Jez Humble, Gene Kim — *Accelerate*** — DORA metrics
  (lead time for changes, deployment frequency, MTTR, change failure rate)
  are empirically linked to team performance; lead time in particular is a
  proxy for inner-loop quality.
- **Mary & Tom Poppendieck — *Lean Software Development*** — flow, cycle
  time, and small batch size; waste in the development loop (waiting,
  context-switching, rework) compounds directly into delivery latency.
- **Joel Spolsky — "The Joel Test"** — the 1-step test rule: anyone on the
  team should be able to run the full test suite with a single command,
  no setup ritual required.

## Good signals

- Narrow test targets (`test:unit`, `test:integration`) exist alongside a
  full-suite command (`test`); both are documented.
- Typecheck and lint complete in under 30 seconds on changed files.
- Watch mode rebuilds incrementally in seconds — not a full rebuild on every
  file save.
- Fixtures are seed-controlled and deterministic; no shared mutable state
  between test runs.
- A documented pre-PR gate exists and runs end-to-end in under 5 minutes.
- Local runs and CI produce the same results; environment drift is caught at
  setup time, not at PR time.
- Hot reload is the default dev mode for UI and server-rendered surfaces.
- One command runs the full test suite with no setup ritual.

## Common failures

- Only one slow all-in-one test command — no fast narrow target for
  focused iteration.
- Flaky local services (databases, queues) produce non-deterministic
  failures that erode trust in the test suite.
- Hidden codegen steps re-run on unrelated changes, adding rebuild latency.
- Fixtures depend on external services that flake or require network access.
- CI passes but local fails because of runtime version or config drift.
- Watch mode rebuilds the entire project on every change instead of only
  what changed.
- No documented "what to run before opening a PR" — developers guess or
  rely on Slack tribal knowledge.
- Tests touch the network, the clock, or the filesystem without isolation,
  making them environment-dependent.

## Heuristics

- **Narrow + full check commands** *(design, audit)* — both a fast focused
  target (`test:unit`) and a full-suite target (`test`) exist and are
  documented in the project README or Makefile. A developer should never
  have to run the full suite just to check one module.
- **Fast typecheck/lint** *(audit)* — typecheck and lint run in under 30
  seconds on changed files. If either exceeds that, profile and add
  incremental or cache configuration.
- **Stable fixtures** *(design, audit, debug)* — fixtures are seed-controlled
  and deterministic; no shared mutable state between runs. A flaky fixture
  is a bug in test infrastructure, not a warning to ignore.
- **Documented pre-PR gate** *(design, audit)* — one command (e.g., `make
  pre-pr`) runs the full set of checks required to land a PR: lint,
  typecheck, unit tests, and integration tests. Tribal knowledge does not
  count.
- **Watch-mode performance** *(audit, design)* — watch mode triggers
  incremental rebuild on change; a file save should not recompile the entire
  dependency graph.
- **Local-CI parity** *(audit, debug)* — local results match CI. Runtime
  version pins (`.nvmrc`, `.tool-versions`) are committed and enforced;
  env drift is surfaced at setup time.
- **Hermetic tests** *(design, audit)* — unit tests make no network calls,
  do not read the real clock, and do not share filesystem state. These
  boundaries are enforced by convention or linting rules, not just trust.
- **Lead time as a tracked metric** *(audit)* — measure how long a single
  change takes from first edit to merged. Rising lead time is an early signal
  that the inner loop is accumulating friction.
- **Incremental type-check on save** *(design, audit)* — typecheck recomputes
  only the affected files on save (TypeScript project references, mypy
  incremental, etc.); a multi-second pause on every keystroke is a
  configuration gap.
- **Watch-mode debounce** *(design, audit)* — file-system watchers debounce
  rapid changes (e.g. branch switches) so a `git checkout` does not trigger
  a hundred sequential rebuilds; a documented debounce window exists.
- **Test selection from a failing file** *(design, audit)* — a documented
  command runs only the tests affected by a given file or function (`vitest
  --related <file>`, `pytest tests/test_x.py::test_y`); developers iterate
  on one failure without rerunning the suite.
- **Monorepo task graph** *(design, audit)* — in multi-package repos, a task
  runner (Nx, Turborepo, Bazel, or equivalent) builds and tests only the
  changed packages and their dependents; full-graph rebuilds are reserved
  for release time.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are narrow + full test commands documented? | Only all-in-one slow command | Add focused targets (`test:unit`, `test:integration`) |
| Do typecheck/lint complete in <30s? | Minutes-long feedback loop | Profile; add incremental build or cache |
| Are fixtures deterministic? | Flaky runs erode trust | Seed-control everything; forbid shared mutable state |
| Is there a documented pre-PR command? | Tribal knowledge gate | Add `make pre-pr` or equivalent |
| Does watch mode rebuild incrementally? | Full rebuild on every save | Switch to incremental watcher config |
| Do local and CI results agree? | "Works on CI only" surprises | Pin runtime versions; add fresh-install CI job |

## Cross-references

- → `setup.md` for one-time environment installation.
- → `contributor.md` for the PR loop layered on top of the inner loop.
- → `perf.md` for build and test latency budgets.
