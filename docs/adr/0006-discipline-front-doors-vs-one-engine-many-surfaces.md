# ADR 0006: Discipline Front-Doors Get Their Own Skill; One-Engine-Many-Surfaces Gets Routed

**Status:** Accepted (2026-05-30). Qualifies [ADR 0005](./0005-one-engine-many-surfaces-skills-are-routed-not-split.md); does not supersede it.

> **Rename note (2026-06-17):** the agent skills were renamed by use case — `agent-experience` → `design-for-agent-users`, `agent-readiness` → `harden-repo-for-coding-agents`, `agent-rules` → `rules-from-coding-agent-failures`. This ADR keeps the original names as written; see [`CHANGELOG.md`](../../CHANGELOG.md).

## Context

ADR 0005 collapsed seven heuristics skills into one routed `review-heuristics`
because they were the *same engine* (`intent → surface → playbook → rubrics →
lenses`) applied to seven domains. Read narrowly, 0005 can be over-generalized
into "never stand up a new standalone skill again — route it." But 0005's own
§Decision bullet 4 explicitly preserves the opposite case: *"Genuinely distinct
methods still get distinct skills (`agent-readiness` vs
`agent-rules` vs `agent-evals` vs `research`): different
engines, not different surfaces of one engine."* What 0005 never wrote down was
a crisp **test** for which side of that line a candidate falls on.

A concrete candidate forced the question: **agent experience (AX)** — designing
software, repos, docs, SDKs, and feedback loops for AI agents as a first-class
consumer audience. Its content was already in the catalog but *scattered*:
review heuristics for agent-facing surfaces lived inside `review-heuristics`
(`dx/playbooks/agent.md`, `dx/playbooks/ai-sdk.md`, `docs/playbooks/ax-docs.md`),
while the *doing* lived in three separate skills (`agent-readiness`,
`agent-rules`, `agent-evals`). Two ways to consolidate it:
add an `ax` domain to `review-heuristics`, or stand up a dedicated skill. 0005
alone did not decide it.

## Decision

Ship a **standalone skill** when the candidate is a **distinct discipline /
distinct engine**. Ship a **routed domain inside an existing skill** when the
candidate is **the same engine applied to one more surface** (same rubric shape,
same lenses, same workflow, differing only in playbook data).

A candidate is a discipline front-door — and warrants its own skill — when **any**
of these hold:

1. **It routes OUT to multiple sibling skills.** Its job is orchestration /
   hand-off across top-level skills, not "load one more playbook." A
   `review-heuristics` domain *cannot* route to other top-level skills; an
   umbrella discipline must. AX routes to `agent-readiness` (harden a
   repo), `agent-rules` (promote observed failures into rules),
   and `agent-evals` (instrument the loop).
2. **Its grounding corpus and finding-ID namespace are disjoint** from the host
   engine's. AX cites the MCP spec, the AGENTS.md convention, Mündler et al.,
   and context-file evals — not Nielsen, Bloch, or Norman, which ground
   `review-heuristics`.
3. **The stance it teaches spans review AND build AND measure** — it unifies
   surfaces that today live in *different* existing skills (`dx`, `docs`, and
   the three do-skills), rather than being one intent × surface of an existing
   rubric.

`agent-experience` satisfies all three; `dx-heuristics` (and its six siblings)
satisfied **none** — they were pure intent × surface of the review engine, which
is exactly why 0005 routed them. Hence 0005 routes the seven heuristics; 0006
stands up AX.

## Consequences

- Published skills go 5 → 6. `agent-experience` is the AX umbrella: it owns the
  agent-facing review/design/debug heuristics relocated out of `review-heuristics`
  and routes to the three "doing" arms for build / promote / instrument.
- The pure-AX surfaces leave `review-heuristics` (the `dx` domain loses `agent`
  and `ai-sdk`; the `docs` domain loses `ax-docs`), with breadcrumb pointers so a
  user who lands on `dx`/`docs` is routed onward to `agent-experience`.
- Multi-audience files (`docs/core/audience-matrix.md`,
  `docs/playbooks/audience-conflicts.md`) carry load-bearing DX/UX human-audience
  content and stay **canonical in `review-heuristics`**; `agent-experience` keeps
  its own AX-focused copies. Per ADR 0004 scope discipline, divergent content is
  not forced into `_shared/`.
- Mitigating 0005's under-trigger risk: the umbrella description carries the
  relocated surfaces' keywords *and* names its three arms, so it does not
  under-trigger versus the old sharp `dx`/`docs` descriptions.
- **Risk:** a future skill that merely "cross-links to another skill" could cite
  0006 to justify fragmenting one engine. Bounded explicitly: the front-door test
  requires a *distinct discipline* (disjoint corpus + cross-skill orchestration +
  a review-build-measure stance), not mere cross-referencing. 0006 is not a
  license to split one-engine-many-surfaces skills — that remains 0005's domain.

## History

- **2026-05-30:** Original decision (this ADR). Triggered by standing up the
  `agent-experience` umbrella skill from AX content distributed across the catalog.
- **2026-05-30 (later):**
  [ADR 0008](./0008-reverse-review-consolidation-split-by-domain-and-function.md)
  reverses 0005's review-family consolidation, but this ADR is undisturbed:
  `agent-experience` remains a standalone front-door skill and the relocated AX
  surfaces do **not** return to the per-domain skills. Where this ADR refers to
  "the `dx`/`docs` domains of `review-heuristics`," read it post-0008 as the
  `dx-audit`/`dx-design`/`docs-audit`/`docs-design` skills.
- **2026-06-18:**
  [ADR 0011](./0011-actor-axis-agent-mirror-family.md) reorganizes the agent half of
  the catalog by actor. The front-door **test** here is unchanged; only its canonical
  **instance** moves — `design-for-agent-users` (was `agent-experience`) retires and
  `agent-ops` inherits the umbrella hand-off router. 0011 also corrects a 0006
  over-citation: `rules-from-coding-agent-failures` stays standalone because it is *out
  of* the agent-actor family (human-operator governance), not because it passes this
  test. `harden-repo-for-coding-agents` continues to pass independently and is kept whole.
