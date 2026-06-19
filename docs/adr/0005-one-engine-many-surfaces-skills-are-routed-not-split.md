# ADR 0005: One-Engine-Many-Surfaces Skills Are Routed, Not Split

**Status:** Superseded in part (2026-05-30) by
[ADR 0008](./0008-reverse-review-consolidation-split-by-domain-and-function.md),
which reverses the **review-family** consolidation (`review-heuristics` →
12 per-domain × per-function skills). What still stands: the research-frame
consolidation (`research` = one skill routed `report | opportunity`) and the
guidance against fragmenting an already-routed engine (`agent-readiness`
stays whole). 0008's `_shared/<domain>/` single-sourcing is how the split keeps
0005's anti-drift property without one skill.

> **Rename note (2026-06-17):** the agent skills were renamed by use case — `agent-experience` → `design-for-agent-users`, `agent-readiness` → `harden-repo-for-coding-agents`, `agent-rules` → `rules-from-coding-agent-failures`. This ADR keeps the original names as written; see [`CHANGELOG.md`](../../CHANGELOG.md).

## Context

The catalog grew a family of seven heuristics skills (`dx-heuristics`,
`docs-experience-heuristics`, `perf-observability-heuristics`,
`test-heuristics`, `ux-accessibility-heuristics`, `ui-design-craft`,
`clean-architecture`) that were the *same* method applied to seven domains:
an `intent-router → intents/<intent>.csv → playbooks/<surface>.md → core
rubrics → lenses → modes → trackable-findings` engine. Two-and-a-half
problems followed:

1. **Silent drift.** The shared machinery was copied per skill and diverged —
   8 distinct `severity-rubric.md` hashes for one conceptually-identical 0–4
   scale, 7 distinct `subagent-dispatch.md` copies, and a forked routing-CSV
   header (`ui-craft`/`ux` vs the other five). The exact failure class ADR 0004
   and AGENTS.md Rule 2 exist to prevent.
2. **Routing pain.** Seven near-identical "Practical X review/design/debug"
   descriptions are hard to disambiguate, which forced the README to carry an
   11-row "Which skill should I use?" table plus a clarifier section, and made
   six of seven descriptions spend budget naming siblings to push work away.
3. **A tempting but wrong fix.** A restructuring pass proposed *splitting* the
   large agent-infra skills further, justified by a "<800-word cap" that the
   gates never actually enforced (see
   `docs/reflection-log/2026-05-28-restructure-split-justified-by-unenforced-cap.md`).
   Splitting one-engine-many-surfaces skills is the opposite of what the drift
   evidence calls for.

## Decision

When several skills (or several would-be skills) are **one engine applied
across many surfaces**, ship them as **one skill that routes** — domain/frame →
intent → surface — not as sibling skills and not split per surface.

- The seven heuristics skills became one `review-heuristics` routed
  domain → intent → surface; the two research skills became one `research`
  routed by decision-frame (`report` | `opportunity`).
- The shared workflow lives **once** (`references/review-workflow.md`); each
  domain contributes only its genuinely-varying data (playbooks, routing CSVs,
  rubrics, personas, lens identities) under `references/<domain>/`.
- Conversely, a skill that is already one routed engine (e.g.
  `agent-readiness`: intent × surface across legibility/action/control)
  is **not** split into per-layer siblings. Routing depth is a feature, not a
  reason to fragment.
- Genuinely distinct *methods* still get distinct skills (e.g.
  `agent-readiness` vs `agent-rules` vs `agent-evals`
  vs `research`): different engines, not different surfaces of one engine.
- `skills/_shared/` remains the home for primitives that are *identical* across
  consumers (modes, trackable-findings, lenses, empirical-warnings W2–W10,
  templates, the routing-CSV contract). Divergent content stays local
  (ADR-0004 scope discipline); it does not get forced into `_shared/`.

## Consequences

- Fewer, higher-signal installable skills (12 → 5 published). The README's
  intra-family disambiguation table collapses into in-skill CSV routing.
- A change to the shared review workflow is one edit, not seven.
- A clean break for downstream installs: the per-skill `--skill dx-heuristics`
  (etc.) commands no longer resolve. Acceptable at `0.0.1-alpha`; the docs were
  updated in the same change. Finding-ID namespaces (`DX-*`, `CA-*`, `OR-*`,
  …) are preserved as per-domain/per-frame prefixes, never rewritten.
- A new routing-CSV well-formedness gate (`scripts/check-routing-csv.sh`) guards
  the contract across all three install lanes.
- Risk: a merged skill's umbrella description must carry every domain's trigger
  keywords or it under-triggers vs sharp sibling descriptions. Mitigated by an
  explicit seven-domain keyword list in `review-heuristics`'s description and a
  per-domain trigger-evals/activation-cases set.

## History

- **2026-05-28:** Original decision (this ADR). Triggered by a catalog-wide
  restructure; see `docs/specs/2026-05-28-catalog-consolidation/`.
- **2026-05-30:** Superseded in part by
  [ADR 0008](./0008-reverse-review-consolidation-split-by-domain-and-function.md).
  The merged `review-heuristics` name described only the critique intent while
  most intents produce artifacts; the consolidation also produced opaque/
  misleading skill names and an all-or-nothing install. 0008 splits it back into
  12 domain×function skills and keeps the anti-drift property via
  `_shared/<domain>/` single-sourcing.
- **2026-06-18:**
  [ADR 0011](./0011-actor-axis-agent-mirror-family.md) reaffirms one-engine-many-surfaces
  for the agent family: each agent mirror is a single routed skill (the ADR-0009
  singleton default), and the agent front-door (`agent-ops`) reuses the existing
  sanctioned umbrella hand-off router with **no** new CSV variant — honoring this ADR's
  anti-fork discipline.
