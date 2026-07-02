# ADR 0009: Replace the clean-architecture pair with a single `minimal-modular-code` skill

**Status:** Accepted (2026-06-18). Supersedes [ADR 0008](./0008-reverse-review-consolidation-split-by-domain-and-function.md) **for the architecture domain only** — it removes the `architecture-audit` / `architecture-design` pair from 0008's table. The other domain pairs (`dx`, `docs`, `perf`, `test`, `writing`) and the single-function `ux-audit` / `ui-design` stand unchanged.

## Context

ADR 0008 split the clean-architecture domain into `architecture-audit` (critique) and `architecture-design` (produce), grounded in the clean-architecture / DDD canon (Martin, Evans, Cockburn, Palermo). Two problems surfaced once the catalog's center of gravity moved toward *minimal, right-sized code for AI coding agents*:

1. **Philosophical conflict.** Classic clean-architecture and DDD, applied as a target, push *toward* more structure — layers, ports/adapters, aggregates, value objects, bounded contexts. That is precisely the speculative structure coding agents already over-produce. The architecture pair had no subtraction or right-sizing lens; shipped next to a minimalism skill, the catalog would give push-pull advice on the same code.
2. **The evidenced, valuable part lived elsewhere.** The agent-parallelism backbone (Conway's Law, the mirroring hypothesis, Baldwin & Clark design rules, Wong & Cai same-layer parallelism, Herbsleb & Grinter integration) was split between `harden-repo-for-coding-agents`'s `inspired_by` and a pointer to the architecture pair. No skill owned the reconciliation between staying minimal and investing in modular boundaries.

A source-grounded research pass (`docs/research/research-report-2026-06-17-minimal-code-and-agent-slop.md`, since removed in a docs cleanup; see git history) established a unifying thesis: **invest in interfaces, not implementations; enforce with gates, not prose; the scarce resource is accountable review, not code generation.** That thesis spans review *and* design — so the audit/design split is the wrong cut for this domain.

## Decision

Delete `architecture-audit` and `architecture-design`. Replace them with one skill, **`minimal-modular-code`** — a `singleton` in the `heuristics` family, two-level routing (intent `do` / `review` / `design` × surface `minimalism` / `legibility` / `boundaries` / `parallel-readiness` / `enforcement`).

- **Absorb the minimalism-compatible substance:** dependency *direction* as a right-sizing/decoupling tool, deep modules, information hiding, and the reusable audit machinery (severity 0–4, score 0–10, project-scale calibration, findings-ledger + workflow-state tracking, three-lens subagent dispatch). The shared agent-architecture note (`skills/_shared/agent-friendly-architecture.md`) is repointed to this skill as the boundary-model owner; `harden-repo-for-coding-agents` keeps the enforcement-wiring surface.
- **Drop the clean-architecture / DDD maximalism:** aggregates, entities, value objects, bounded-context modeling, prescriptive hexagon/onion/ports-as-default, anemic-domain "fix by adding objects", strangler-fig. The orphaned `skills/_shared/architecture/` substrate (used only by the deleted pair) is removed.
- **Finding-ID namespace** moves from `CA-*` to `MM-*` (`MM-MIN`, `MM-LEG`, `MM-BND`, `MM-PAR`, `MM-ENF`). Historical `docs/audits/` artifacts keep their `CA-*` IDs as an immutable record.

The principle, stated to compete with 0008's per-domain × per-function rule: **for the architecture domain the load-bearing distinction is not review-vs-build but minimal-vs-bloated, and that thesis spans both review and design — so a single skill that holds the reconciliation beats a pair that, as classic clean-architecture/DDD, would advise the over-structure we exist to prevent.** A singleton is the right shape here; precedent is `harden-repo-for-coding-agents` (a multi-intent singleton).

## Consequences

- Published catalog skills go from 22 to **21**: `architecture-audit` + `architecture-design` removed, `minimal-modular-code` added.
- The `heuristics` family now holds one singleton alongside the `-audit`/`-design` pairs; the family intro and `docs/architecture/README.md` taxonomy note this.
- `--skill architecture-audit` and `--skill architecture-design` install commands no longer resolve. Install `minimal-modular-code` instead. Acceptable at `0.0.1-alpha`.
- Cross-references repointed to `minimal-modular-code` in `research`, `harden-repo-for-coding-agents`, `rules-from-coding-agent-failures`, and the `_shared` notes (`agent-friendly-architecture.md`, `trackable-findings.md`).
- The agent-parallelism research (Conway, mirroring, design rules, Wong & Cai, Herbsleb & Grinter, Parnas, Meng & Jackson, RIG, CodePlan) is now owned and cited by this skill's `inspired_by`, not stranded.
- **Risk — broader single skill.** One multi-intent skill is more surface to keep coherent than a pair. Mitigated by two-level routing, the per-skill static check, and the shared schema/eval gates.
- **Risk — seam with `harden-repo-for-coding-agents`.** "Enforce this boundary" sits between the two. Accepted: `minimal-modular-code` says *what* to enforce and *why*; `harden-repo-for-coding-agents` owns the hook/CI/AGENTS.md wiring. Each cross-links the other.

## History

- **2026-06-18:** Original decision (this ADR). Triggered by maintainer review while scoping a minimalism/anti-slop skill: the clean-architecture pair conflicted with the minimalism thesis and the evidenced parallelism material had no home. Grounded in `docs/research/research-report-2026-06-17-minimal-code-and-agent-slop.md` (since removed; see git history).
