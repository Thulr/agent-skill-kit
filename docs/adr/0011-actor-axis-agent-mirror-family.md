# ADR 0011: Actor Is the Top Axis — an Agent Mirror per Human-Experience Domain

**Status:** Accepted (2026-06-18). **Supersedes the structural claim of**
[ADR 0007](./0007-experience-disciplines-are-audience-peers.md) (UX/DX/AX as three
audience-differentiated *peers*); 0007's load-bearing result ("DX is not a subset of
UX") is preserved and re-derived under the new model. **Updates** (does not supersede)
[ADR 0005](./0005-one-engine-many-surfaces-skills-are-routed-not-split.md),
[ADR 0006](./0006-discipline-front-doors-vs-one-engine-many-surfaces.md), and
[ADR 0008](./0008-reverse-review-consolidation-split-by-domain-and-function.md). Reads
the architecture domain's singleton resolution
([ADR 0009](./0009-replace-architecture-pair-with-minimal-modular-code.md)) forward onto
the agent family.

Working design doc + evidence base:
`docs/research/agent-mirror-family-blueprint-2026-06-18.md` (since removed in a docs cleanup; see git history)
and the `agent-mirror-family-design` workflow (21 agents: map → 4 competing designs →
score → adversarial verify → synthesize). The recommended cut here is the synthesis that
survived every fatal attack that sank the alternatives.

## Context

ADR 0007 settled "isn't DX just a subset of UX?" with **audience-differentiated peers**:
UX, DX, and **AX** (agent experience) were three sibling audiences of one parent
discipline, and AX earned a single standalone skill (`design-for-agent-users`, the 0006
front-door) routing out to the agent "doing" arms (`harden-repo-for-coding-agents`,
`agent-evals`, `rules-from-coding-agent-failures`).

Living with that model surfaced a category error. "Agent" is **not a third audience next
to end-user and developer.** An agent is an *actor* that can occupy **any** role: it
reads docs (user-of-docs), builds against an SDK (developer), operates a system
(operator). Treating AX as one peer audience forced all agent-actor concerns — agent-as-
developer, agent-as-reader, agent-as-operator, agent-as-subject — into a single umbrella,
where they were either cramped together or scattered back across the human skills
(`docs-audit` still owns `llms.txt`/RAG/tool-contract surfaces; `dx` once owned
`ai-sdk`/`agent`). The model the catalog actually needs has **two orthogonal axes**, and
the catalog was only cutting on one.

A second pressure: the architecture domain already faced the "one routed skill vs an
audit/design pair" question and resolved it toward a **single skill** in
[ADR 0009](./0009-replace-architecture-pair-with-minimal-modular-code.md)
(`minimal-modular-code`, routing do/review/design internally — the shape the maintainer
endorsed). The agent family poses the same question and there was no written rule for
which way it falls.

## Decision

### 1. Actor is the top axis; agent mirrors per human-experience domain

The catalog is organized along **two orthogonal dimensions**:

- **Actor** — `human | agent`. An agent is an actor **type**, not an audience peer.
- **Role / relationship to the software** — `user` (ux), `developer` (dx),
  `operator` (ops). Roles are **non-nesting peers** (0007's result, re-derived: "DX is
  not a subset of UX" becomes "the roles do not nest *within* an actor column").

The operative test for which side of the actor axis a surface sits on:

> A surface that exists **only because agents exist** — MCP, tool schemas, `llms.txt`,
> `AGENTS.md`, agent loops, eval harnesses, RAG/context budgets — is **agent-family**. A
> surface an agent merely *consumes* but that has a human analog (a generic API, SDK,
> CLI, doc, or test) stays **human** unless the artifact is machine-first.

Because the agent is a *column* of the actor × role grid rather than a single peer cell,
it **mirrors per human-experience domain** wherever the agent-actor content is real:

| Role / domain | Human skill(s) | Agent mirror |
|---|---|---|
| developer (dx) | `dx-audit` / `dx-design` | **`agent-dx`** |
| reader (docs) | `docs-audit` / `docs-design` | **`agent-docs`** (narrowed) |
| user (ux) | `ux-audit` / `ui-design` | **`agent-ux`** (net-new) |
| operator (ops/perf) | `perf-audit` / `perf-design` | **`agent-ops`** (family front-door) |
| subject-under-test | `test-audit` / `test-design` | **`agent-test`** |

No mirror for `research`, the discovery family, or `writing` (no real agent-actor
column, and the maintainer scoped writing out). `minimal-modular-code` is already
agent-oriented; there is no separate `agent-code`.

### 2. Single skill per domain, not an audit/design pair (resolving 0005 vs 0008)

Each agent mirror is **one skill routing do/review/design internally** via the proven
`minimal-modular-code` two-layer CSV shape — **not** an `-audit`/`-design` pair.

The rule, stated so it is not re-litigated: **split a domain into audit/design pairs
only when *both* of ADR-0008's pathologies hold** — (1) a single skill *name would lie*
over the engine (a review-only name hiding a build pipeline), **and** (2) install is
*all-or-nothing across multiple domains* packed into one skill. The human review family
had both (seven domains in one `review-heuristics`; a name that said "review" over a two-
pipeline engine). The agent family has **neither**: each agent skill is exactly one
actor-role domain, and an intent-router whose top routes are named per function
(`do`/`review`/`design`) does not lie. This is ADR-0009's reasoning ("the thesis spans
review *and* build, so a single skill beats a pair") applied to the agent column. What
carries over from 0008 is only its **`_shared/<domain>/` anti-drift mechanism**, reused
verbatim as **`_shared/agent/<domain>/`**.

### 3. Disposition of the four existing agent skills

| Skill | Disposition | Becomes |
|---|---|---|
| `design-for-agent-users` | **retire & decompose** | `ai-sdk` → `agent-dx`; `ax-docs` → `agent-docs` (narrowed); `audience-conflicts` → `agent-ux`; repo-readiness review heuristics → `agent-ops`. Its **umbrella front-door role and sanctioned hand-off router are inherited by `agent-ops`.** Removed via the removal runbook — **no breadcrumb stub** (a stub under `skills/` must itself pass the full per-skill artifact contract, so it is not "thin"). |
| `harden-repo-for-coding-agents` | **keep standalone, unchanged name** | The repo/infra **do/scaffold engine** (`assess`/`harden`/`scaffold`/`diagnose` × 11 surfaces, raised 900–3200 word cap, `AG-<SURFACE>-NNN`). It independently passes the 0006 front-door test. `agent-ops` **routes out to it** and does **not** stand up a competing repo-readiness review surface — harden-repo already owns `assess`. |
| `agent-evals` | **retire & decompose** | eval/judge/trajectory/benchmark **design** → `agent-test`; optimization-loop / observability / autonomous-improvement-controller **lifecycle** → `agent-ops`. The level-N + loop templates move to `_shared/agent/templates/`; the self-test harness is re-homed to `agent-test/evals/` with its hardcoded constants rewritten, plus one repo-level integration test for the cross-skill arc. |
| `rules-from-coding-agent-failures` | **stays standalone, unchanged** | The W1≥3 evidence-driven failure→rule governance engine. Kept standalone **not** on a front-door test (correcting a 0006 over-citation) but because it is **out of the agent-actor experience family** — a *human-operator* governance discipline that curates the `AGENTS.md` agents later read. Becomes the **sole canonical** `empirical-warnings-w1.md`. `agent-ops` and `harden-repo` route out to it. |

The final agent family is **five mirrors** (`agent-dx`, `agent-docs`, `agent-ux`,
`agent-ops`, `agent-test`) **plus two retained arms** (`harden-repo-for-coding-agents`,
`rules-from-coding-agent-failures`). `agent-ux` ships with an explicit **0.0.2 kill-
criterion**: if it still carries only the single `audience-conflicts` playbook with no
disjoint corpus, it folds into `agent-docs`/`agent-dx` rather than ship hollow.

### 4. Topology, `_shared` backing, and trigger disambiguation

- **Topology.** Every mirror uses the identical two-layer flat-CSV shape
  `minimal-modular-code` ships and `routing-contract.md` already sanctions: Layer-1
  `references/intent-router.csv` (rows `do`/`review`/`design`) → Layer-2
  `references/intents/<intent>.csv` (surface playbook). **No Layer-0 `actor:agent` gate
  row** — that forks the CSV contract (the `ui-craft`/`ux` 5-column divergence class
  ADR 0005 warns against). The two retained arms keep their **existing** routers
  unchanged.
- **Front-door.** `agent-ops` **alone** carries umbrella hand-off rows, inheriting the
  **existing sanctioned** hand-off variant (empty `detail_files`, `notes` names the
  target) **verbatim** from the retiring `design-for-agent-users` — routing out to
  `agent-dx`, `agent-docs`, `agent-test`, `harden-repo-for-coding-agents`, and
  `rules-from-coding-agent-failures`. No new router primitive is invented.
- **Backing.** `skills/_shared/agent/<domain>/` holds each domain's
  playbooks/surface-registry/personas/severity, plus the partition genuinely shared by
  2+ agent skills (agent lenses; severity rubric with agent escalators; retry/
  structured-output/error-envelope rubrics; `AGENTS.md`/`llms.txt`/MCP primitive
  definitions; the level-N/loop templates). Cross-catalog substrate (modes,
  empirical-warnings W2–W10, trackable-findings, tracking templates) stays at
  `_shared/` root and is symlinked in. W1 stays **sole-tenant** in
  `rules-from-coding-agent-failures`.
- **Disambiguation** (e.g. human "review my API design" vs agent "review my MCP tool
  surface"). Two layers, because the per-skill `trigger-evals.json` cannot yet *enforce*
  which sibling wins a prompt (the cross-skill activation grader is the unbuilt
  Stage 1.5): (1) every agent-* description **leads with the actor frame** ("Use when an
  AI **agent** is the {developer | reader | user | operator | subject}…") and the
  "exists only because agents exist" test; (2) **reciprocal Do-NOT clauses** are
  repointed in the same PR from the retiring `design-for-agent-users` to the specific
  agent-* skill across the nine inbound human `SKILL.md` files.
- **The `agent-docs` collision is resolved by explicit corpus surrender.**
  `docs-audit`/`docs-design` today own `llms.txt`/agent-context-files/RAG/tool-contract
  descriptions and fire on "why does the agent call the wrong tool." `agent-docs` is
  **narrowed to agent-native-only** artifacts (`AGENTS.md` as a portable instruction-
  surface contract, MCP/tool-as-API discovery, `llms.txt` curation, machine-readable
  reference, chunk survivability). In the **same PR**, `docs-audit`/`docs-design`
  **surrender** those tokens (descriptions, activation-cases, trigger-evals, the
  `agent-retrieval` lens). Generic "audit our docs/README" stays human;
  "audit our `llms.txt`/`AGENTS.md`/tool schema for an agent" routes `agent-docs`.
  `perf-audit`/`perf-design` get an agent-observability Do-NOT clause (agent
  traces/observability → `agent-ops`).

## Consequences

- **Published agent surface goes from 4 → 7 skills:** five `agent-*` mirrors + the two
  retained arms. Two skills retire (`design-for-agent-users`, `agent-evals`); their
  install commands stop resolving (clean break, acceptable at `0.0.1-alpha`).
- **0007's result is preserved, its structure retired.** "DX is not a subset of UX" and
  the "do not staff/measure agent surfaces as a branch of human UX" rule carry forward,
  re-derived as "roles are non-nesting peers within each actor column." Only 0007's
  three-peer enumeration and its "AX is one peer discipline" framing are dropped.
- **The ADR-0006 front-door *test* is unchanged**; only its canonical *instance* moves
  — `design-for-agent-users` retires and `agent-ops` inherits the role. The 0006 over-
  citation for `rules-from-coding-agent-failures` is corrected (kept standalone because
  it is out of the agent-actor family, not because it passes the test).
- **ADR-0008's pair-split stands for the human review family and is explicitly *not*
  lifted** to the agent family; its `_shared/<domain>/` mechanism is reused. 0008's "AX
  content does not return to the per-domain skills" clause is updated: the audience-
  conflict excerpt moves to `agent-ux`, while the canonical docs `audience-matrix.md`
  (the 3240b `_shared/docs` copy) is **rewritten to the actor-axis framing** and stays
  canonical in the review family. The divergent 3415b peer-model copy in
  `design-for-agent-users` is **deleted** — no double ownership.
- **Two pre-existing silent drifts are reconciled as binding same-PR steps:** the
  divergent `empirical-warnings-w1.md` (delete the 1129b `design-for-agent-users` copy;
  the 2313b `rules-from-coding-agent-failures` copy becomes sole-tenant) and the four-
  copy `audience-matrix.md`.
- **Finding-ID namespaces are re-keyed, never dropped:** `AX-NNN` → `agent-ux`
  (human-vs-agent tension); the other mirrors get `AGENT-DX/DOC/OPS/TEST-NNN`. Historical
  `AX-NNN` references stay immutable (as 0009 did for `CA-*` → `MM-*`).
- **`scripts/catalog_taxonomy.py` is extended** to classify the agent singletons
  (`FUNCTIONS` already carries `singleton`; the `FAMILIES` scheme for the agent column is
  finalized at the catalog-rewire step). Because the mirrors are singletons, they do
  **not** register under `heuristic_pairs()` completeness validation — a concrete
  advantage of the singleton shape over a pair-split.
- **Per Rule 1, every path-based gate** (`check-shared-content.py`, the routing-CSV gate,
  the orphan check, CI matrices) is extended to enumerate `_shared/agent/**` across all
  three install lanes.

### Risks (recorded, accepted)

- **Dual-audience seam prompts mis-route, ungated.** "Review our SDK that both humans and
  agents call" / bare "docs review" route imperfectly until the Stage 1.5 cross-skill
  activation grader exists. Narrowing + corpus surrender + Do-NOT clauses *reduce* but do
  not *eliminate* this; the collision rate is asserted, not measured.
- **`agent-ux` launches thinnest** and may under-trigger; the 0.0.2 kill-criterion is the
  mitigation.
- **`agent-ops` is the heaviest mirror** (operator review + optimization/observability
  slice + front-door); a future thin-front-door split is foreseeable.
- **Retiring the named `design-for-agent-users` umbrella is a discoverability
  regression** — a reader searching "make this agent-friendly" lands on `agent-ops` as
  the de-facto hub, not a skill literally named for the generic ask. Mitigated by
  `agent-ops`' keyword-rich front-door description.
- **Naming asymmetry persists** (`harden-repo`/`rules` keep non-`agent-*` names beside
  five prefixed siblings). The "arm, not mirror" rationale must stay load-bearing here or
  it gets re-litigated.
- **Splitting `agent-evals`' validated diagnostic arc** across `agent-test` and
  `agent-ops` raises eval-maintenance cost; the repo-level integration test must actually
  be authored.
- **Migration blast radius is the largest in repo history** (nine Do-NOT clauses,
  routing-contract + empirical-warnings prose, `catalog_taxonomy` + `catalog.json` +
  generated README, two drift reconciliations, the harness re-home, new `_shared/agent`
  gate coverage). All gated by `just check`, so a miss fails CI — but it **warrants
  phasing**, below.

## Migration / sequencing

Phased so each PR is independently green under `just check`:

0. **Land the contract** (this PR + reconciliations): ADR-0011; reconcile the two W1
   copies and `audience-matrix` to the actor-axis framing; extend `catalog_taxonomy`
   FAMILIES; record in `routing-contract.md` that `agent-ops` reuses the existing
   umbrella hand-off variant.
1. **Stand up the `_shared/agent/` backbone** and extend every path-gate + CI matrix to
   cover `_shared/agent/**` across all three lanes (verify ≥1 symlink consumer per lane).
2. **Build the two highest-corpus mirrors first** to validate the mmc shape end-to-end:
   `agent-dx` and `agent-ops` (front-door, with the inherited hand-off router wired out
   to `harden-repo` + `rules`; repoint harden-repo's "arm of design-for-agent-users"
   prose to `agent-ops`).
3. **Build `agent-test` + `agent-docs`**, and in the same commit execute the
   `docs-audit`/`docs-design` corpus surrender + the `perf` agent-observability Do-NOT
   clause.
4. **Build `agent-ux`** (with its kill-criterion); repoint all nine inbound human Do-NOT
   clauses; re-home the `AX-NNN` namespace.
5. **Retire + regenerate:** `git rm` `design-for-agent-users` and `agent-evals` per the
   removal runbook; CHANGELOG Removed/Changed entries; `build-catalog.py --write`; full
   `just check`; `check-doc-links` clean. Extend the runbook with a
   "decompose one skill into a role-mirror" procedure (the existing runbook covers
   rename or remove, not fan-out).

## History

- **2026-06-18:** Original decision (this ADR). Triggered by the maintainer reframing the
  catalog around actor (human vs agent) after the human-DX de-scoping (PR #56) parked the
  agent-error/telemetry heuristics for an `agent-dx` mirror. Recommended cut produced by
  the `agent-mirror-family-design` workflow and the blueprint it formalizes.

> **Update (2026-07-02):** the human `test-audit` / `test-design` pair was
> removed from the catalog; `agent-test` remains. See CHANGELOG.
