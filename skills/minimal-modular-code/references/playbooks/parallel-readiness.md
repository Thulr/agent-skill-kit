# Parallel-Readiness Playbook

## Scope

Repo-scale structure that lets many coding agents work concurrently without colliding:
stable contracts ("design rules"), work-partitioning by dependency layer, blast-radius
awareness, ownership, and isolation. The "modular in the large" counterpart to
`boundaries.md`.

- **In:** design rules as contracts, same-layer parallelization, mirroring, blast-radius
  and impact, run isolation (worktrees/branches), machine-queryable structure for
  partitioning.
- **Out:** the single-module seam (see `boundaries.md`); how invariants are mechanically
  held (see `enforcement.md`).
- **Intents this surface answers:** do, review, design.

## Grounding

- **Melvin Conway (1968)** — a system mirrors the communication structure that built it.
- **MacCormack, Baldwin & Rusnak (2012)** — loosely-coupled organizations produce more
  modular products; an agent fleet is such an organization.
- **Baldwin & Clark, Design Rules (2000)** — freeze stable design rules; hidden modules
  evolve independently beneath them.
- **Wong, Cai et al. (2009)** — modules in the same design-rule layer are independent and
  parallelizable; cross-layer dependencies need coordination.
- **Herbsleb & Grinter (1999)** — modularity is necessary but not sufficient; without
  explicit interfaces the collision moves to integration.
- **Bairi et al., CodePlan (2024)** — sequence repo-scale edits with dependency and
  change-impact analysis.
- **Cherny-Shahar & Yehudai, RIG (2026)** — a deterministic structure map both helps an
  agent and reveals when two agents' modules touch.

## Good signals

- A small set of stable, documented contracts (interfaces, schemas, dependency direction)
  is named and owned; everything behind them is free to change.
- The modules handed to concurrent agents sit in the same dependency layer — they do not
  depend on each other.
- Each parallel run is isolated (its own worktree/branch/workspace); runs do not edit the
  same files.
- A change's blast radius is known before it is dispatched.
- A machine-queryable structure map exists, so "what touches what" is queryable, not
  guessed.

## Common failures

- **Implicit or unstable interfaces** — contracts that live only in code shape and change
  freely; N agents then collide at integration, more expensively than if serialized.
- **Shared mutable state across modules** — two modules read/write the same store; a change
  to one ripples into the other, so they cannot be worked in parallel.
- **Cross-layer chains** — modules in different layers handed to parallel agents; each
  waits on the other, and edits conflict.
- **No ownership** — a contract owned by no one drifts; every agent edits it, maximizing
  collisions on the highest-blast-radius artifact.
- **Big-ball-of-mud** — no stable seams at all; the only safe concurrency is one agent.

## Heuristics

- **(design) Freeze a thin set of design rules.** Identify the stable contracts (interfaces,
  schemas, dependency direction, core standards), document and own them, and let modules
  evolve independently underneath. Invest in the interface; keep the implementation cheap to
  replace.
- **(design) Partition work by dependency layer.** Hand same-layer modules to different
  agents; serialize across layers. Same-layer modules are predicted independent and collide
  least.
- **(review, design) Treat contracts as high-blast-radius artifacts.** Put ownership and
  gates around the few shared contracts; assign agents to independent modules *under* them
  and rely on integration tests to catch drift.
- **(review) Confirm interfaces are explicit and stable, not implicit.** Modularity alone is
  not enough; if the contract is not written down and frozen, parallel work just defers the
  conflict to merge/integration.
- **(do) Compute blast radius before editing.** Before changing code, identify which modules
  and contracts the change touches; a change that touches a shared contract is a serialize-or
  -coordinate signal, not a parallel one.
- **(design) Shape the topology deliberately.** A loosely-coupled agent fleet will produce
  loosely-coupled code; design the module and ownership map so the structure you want is the
  one that emerges, rather than letting it fall out of who-edited-what.
- **(do, design) Isolate each run.** Give each parallel agent its own worktree/branch/
  workspace so edits do not stomp each other; prompt-only "stay in your lane" scoping leaks
  on long runs and weaker models — isolate structurally.
- **(review, design) Provide a machine-queryable structure map.** A build/test/dependency
  graph both grounds each agent and exposes where two agents' modules intersect, so you can
  partition before dispatch.

## Quick diagnostic

- Is there a written, owned contract for each seam two agents would work across? — no → make
  it explicit before parallelizing.
- Do the modules you want to parallelize depend on each other? — yes → they are not
  same-layer; serialize or re-cut the boundary.
- Do you know what a change touches before dispatching it? — no → compute blast radius
  first.
- Are parallel runs isolated at the filesystem level, or only by instruction? — instruction
  → expect leaks; isolate structurally.

## Cross-references

- `boundaries.md` — the single-module seam these contracts are made of.
- `enforcement.md` — how the contracts and dependency direction are held mechanically.
- `minimalism.md` — contracts are a present-need investment (malleability), not speculative
  generality.
- `references/intents/{do,review,design}.csv` row `parallel-readiness` — the entry points.
