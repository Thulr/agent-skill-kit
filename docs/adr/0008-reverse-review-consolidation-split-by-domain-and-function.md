# ADR 0008: Reverse the Review Consolidation — Skills Split by Domain × Function

**Status:** Accepted (2026-05-30). Supersedes [ADR 0005](./0005-one-engine-many-surfaces-skills-are-routed-not-split.md) **for the review family only**; updates the structural claims in [ADR 0007](./0007-experience-disciplines-are-audience-peers.md). Does **not** disturb [ADR 0006](./0006-discipline-front-doors-vs-one-engine-many-surfaces.md) (`agent-experience` stays standalone).

## Context

ADR 0005 (2026-05-28) collapsed seven heuristics skills into one routed
`review-heuristics`, on the theory that they were one engine across many
surfaces and that a single installable unit prevents the copy-paste drift ADR
0004 exists to stop. Two days of living with the merged skill surfaced costs
that outweigh the benefit:

1. **The name lies.** `review-heuristics` describes only the audit/critique
   intent, but most of the skill's ~34 intents *produce an artifact* —
   `design`, `author`, `refactor`, `optimize`, `strategize`, `measure`, and the
   six `ui-craft` build intents. The shared `review-workflow.md` already forks
   on intent type at steps 4/5/6/8 (lens-dispatch → score → severity → ledger
   for critique; "name the good-shaped pattern" → emit a doc for produce). One
   name over a two-pipeline engine under-describes it and under-triggers on
   every generative ask.
2. **Names that don't say what they do.** A maintainer could not tell what the
   `ui-craft` domain was from its name. An installable skill's name is its
   primary discovery surface; an opaque or misleading name is a defect.
3. **The umbrella description is the old routing pain, relocated.** 0005 removed
   the README's "which skill?" table by forcing every domain's keywords into one
   description — the same disambiguation cost, moved, not removed.
4. **All-or-nothing install.** Installing one domain pulls in all seven.

0005's anti-drift argument is its strongest, and it is real. But it is
addressable **without** consolidation: substrate that is identical across
sibling skills can live once in `_shared/<domain>/` and be symlinked in. One
*source* does not require one *skill*.

## Decision

Split `review-heuristics` into **per-domain × per-function** skills, each named
so the name states what the skill does. A domain that is single-function is one
skill; a domain that does both critique and produce splits into a `-critique`
skill and a `-design` skill.

| Skill | Function | Intents |
|---|---|---|
| `dx-critique` | critique | audit, debug, edge-pass |
| `dx-design` | produce | design |
| `docs-critique` | critique | audit, debug |
| `docs-design` | produce | design, measure |
| `perf-critique` | critique | audit, diagnose |
| `perf-design` | produce | design, optimize, strategize |
| `test-critique` | critique | review, triage |
| `test-design` | produce | author, strategize, prune |
| `ux-critique` | critique (pure) | usability / accessibility / form / nav / error audits |
| `ui-design` | produce (pure, self-polishes) | product-ui, design-system, prototype, deck, motion, host-handoff, quality-review |
| `architecture-critique` | critique | audit |
| `architecture-design` | produce | design, refactor, explain |

- **Critique skills** run lenses → score → severity → stable finding IDs →
  ledger/workflow-state. **Design skills** load the domain heuristics, name the
  good-shaped pattern, and emit a design doc / runbook / plan.
- **Domain-shared substrate is single-sourced.** Each mixed domain's playbooks,
  lens identities/personas (`subagent-dispatch.md`, `core/personas.md`), and
  `starter-scenarios.csv` live canonically in `skills/_shared/<domain>/`; both
  the `-critique` and `-design` skills symlink them in with relative symlinks
  (`npx skills` dereferences at install, so each installs self-contained). This
  neutralizes the drift risk 0005 cited *while* delivering the split.
- **Function-specific content stays local.** Critique-only rubrics
  (`severity-rubric.md`, `score-rubric.md`, `trackable-findings.md`) and the
  audit/debug templates live in the `-critique` skill; design/runbook/plan
  templates live in the `-design` skill.
- **Scope is the review family only.** This does not reverse 0005's
  research-frame consolidation (`research` stays one skill routed
  `report | opportunity`) or its guidance against fragmenting an already-routed
  engine (`project-agentification` stays whole). `agent-experience` (0006)
  stands — AX content does not return to the per-domain skills.

The principle, stated to compete with 0005: **when a merged skill's name and
scope obscure what it does, honest naming and discoverability outweigh the
single-unit anti-drift benefit — provided the shared substrate is kept
single-sourced in `_shared/`.** Clear sibling skills + `_shared` beat one routed
mega-skill.

## Consequences

- Published skills go from one `review-heuristics` to **12** domain×function
  skills (alongside `research`, `project-agentification`,
  `evidence-driven-agent-rules`, `agent-experience`, `eval-flywheel`,
  `loop-architect`). The umbrella description's keyword pile-up collapses into
  12 sharp descriptions.
- Each new skill carries domain×function-scoped `skill.json.inspired_by`
  (partitioned from the unioned 122-source list by `playbook → function`),
  its own `evals/`, and a finding-ID namespace preserved per domain (`DX-*`,
  `CA-*`, …) — owned now by the `-critique` skill of each domain.
- `_shared/` grows a per-domain subtree. `scripts/check-shared-content.sh` and
  the routing-CSV gate now cover it; per Rule 1 every path-based gate enumerates
  the new skill set across all three install lanes.
- Catalog surface (README, `llms.txt`, `.github/CODEOWNERS`, install commands)
  is rewritten for the new set. Clean break: the `--skill review-heuristics`
  install command no longer resolves. Acceptable at `0.0.1-alpha`.
- **Risk — more surface to keep consistent.** 12 skills > 1. Mitigated by
  `_shared/<domain>/` single-sourcing and the shared schema/eval gates that
  already validate every lane.
- **Risk — seam prompts.** "Review my API *design doc*" sits between
  `dx-critique` and `dx-design`. Accepted; each pair cross-links the sibling in
  its description and `when_to_use`.
- ADR 0005 is marked Superseded-in-part. ADR 0007's *peer concept* (UX/DX/AX are
  audience-differentiated peers) stands unchanged; its structural sentence that
  0005 makes `dx`/`ux` "sibling **domains** of one review engine" is updated —
  they are now sibling **skills**.

## History

- **2026-05-30:** Original decision (this ADR). Triggered by maintainer review
  of `review-heuristics`: it housed far more than reviews, and the merged name
  hid what each part did. See
  [`docs/specs/2026-05-30-domain-function-split/`](../specs/2026-05-30-domain-function-split/).
