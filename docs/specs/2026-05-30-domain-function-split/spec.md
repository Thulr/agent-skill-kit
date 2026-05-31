# Spec: Split `review-heuristics` by domain × function

**Date:** 2026-05-30
**Status:** Active
**Decision record:** [ADR 0008](../../adr/0008-reverse-review-consolidation-split-by-domain-and-function.md)
(supersedes [ADR 0005](../../adr/0005-one-engine-many-surfaces-skills-are-routed-not-split.md) for the review family)
**Reverses:** [`docs/specs/2026-05-28-catalog-consolidation/`](../2026-05-28-catalog-consolidation/) Phase ② (the review-family merge); the AX extraction (Phase ③ → `design-for-agents`) stands.

## Problem

The 2026-05-28 consolidation collapsed seven heuristics skills into one routed
`review-heuristics`. Two days of use surfaced that the merge obscured what the
skill does:

- The name describes only the **critique** intent, but most of the ~34 intents
  **produce an artifact** (`design`, `author`, `refactor`, `optimize`,
  `strategize`, `measure`, the six `ui-craft` build intents). `review-workflow.md`
  already forks on intent type at steps 4/5/6/8.
- Skill names stopped saying what they do (a maintainer could not tell what the
  `ui-craft` domain was).
- The umbrella description must carry every domain's keywords — the old "which
  skill?" routing pain, relocated into one description.
- All-or-nothing install: one domain pulls in all seven.

## Goal

Replace `review-heuristics` with **12 per-domain × per-function skills**, named
so the name states what the skill does. Keep the anti-drift property the merge
bought by single-sourcing domain-shared substrate in `skills/_shared/<domain>/`.

## Target skills

| Skill | Function | Intents | Emits |
|---|---|---|---|
| `dx-critique` | critique | audit, debug, edge-pass | audit-report (+multi), debug-runbook, edge-checklist, ledger |
| `dx-design` | produce | design | design-doc |
| `docs-critique` | critique | audit, debug | audit-report, debug-runbook |
| `docs-design` | produce | design, measure | design-doc, measurement-plan |
| `perf-critique` | critique | audit, diagnose | audit-report (+multi), diagnose-runbook |
| `perf-design` | produce | design, optimize, strategize | design-doc, optimize-plan, strategy-doc |
| `test-critique` | critique | review, triage | review-report (+multi), triage-runbook |
| `test-design` | produce | author, strategize, prune | author-design, strategy-doc, prune-plan |
| `ux-critique` | critique (pure) | usability / accessibility / form / nav / error audits | audit-report, ledger |
| `ui-design` | produce (pure, self-polishes) | product-ui, design-system, prototype, deck, motion-scene, host-handoff, quality-review | UI artifacts, review-report |
| `architecture-critique` | critique | audit | audit-report (+multi), ledger |
| `architecture-design` | produce | design, refactor, explain | design-doc, refactor-runbook, explanation |

`ux` (pure critique) and `ui-craft` (pure produce) are single-skill renames.
The five mixed domains split into a `-critique` and a `-design` skill.

## Shared vs. local split (per mixed domain `D`)

Each new skill is flat (`references/playbooks/…`, not `references/D/…`) — i.e.
the pre-consolidation layout. The `references/D/` → `references/` path rewrite is
the inverse of the consolidation's `references/` → `references/D/` rewrite.

**Canonical in `skills/_shared/<D>/`, symlinked by BOTH skills** (relative
symlinks; `npx skills` dereferences at install → self-contained installs, one
maintenance source, no drift):

- `playbooks/*.md` — heuristic content is intent-tagged (`*(audit, design)*`),
  so the same file serves critique and design.
- `core/personas.md` (and lens identities in `subagent-dispatch.md`).
- `first-impressions-checklist.md` and any other content both functions load.

**Local to `<D>-critique`:** `intent-router.csv` (critique intents only),
`intents/{audit,debug,…}.csv`, `core/severity-rubric.md`, `core/score-rubric.md`,
`trackable-findings.md`, `starter-scenarios.csv` (critique rows), critique
templates (`audit-report.md`, `debug-runbook.md`, `edge-checklist.md`,
`findings-ledger.md`, `workflow-state.json`), `modes.md` (symlink to
`_shared/modes.md`).

**Local to `<D>-design`:** `intent-router.csv` (design intents only),
`intents/{design,…}.csv`, `starter-scenarios.csv` (design rows), design
templates (`design-doc.md`, runbooks, plans), `modes.md` (symlink).

`ux-critique` and `ui-design` keep their existing one-layer (`detail_files`/
`templates`) routers; nothing to share between siblings, so no `_shared/ux` or
`_shared/ui` subtree is required (keep their content local).

## Provenance partitioning

Each new skill's `skill.json.inspired_by` is the subset of the unioned
122-source list whose `playbooks` tags map to that skill's surfaces **and**
function. A source that grounds both critique and design of a surface (e.g.
Bloch on `api`) appears in **both** `dx-critique` and `dx-design`. The recovered
pre-consolidation per-domain `skill.json` files (`git show c21b802^:skills/<old>/skill.json`)
are the partitioning reference; drop AX-only sources (`ai-sdk`/`agent` playbooks
left for `design-for-agents`). The `inspired_by.playbooks` static gate validates
each value against on-disk playbooks + intent markers, so design skills tag
`design`/`design-intent`/`all`, critique skills tag `audit`/`audit-intent`/etc.

## Per-skill eval contract

Recover each old skill's `run-static-checks.sh` (`git show c21b802^:…`) as the
base, then specialize:

- **Critique skills** keep the tracking gates (ledger/workflow-state filename
  prefixes, `trackable-findings.md`, severity/score rubric presence), the
  registry CSV→file integrity check, the orphan-playbook check (against
  `_shared/<D>/playbooks` via the symlinked path), and the SKILL.md source-leak
  + word-count (<800) gates.
- **Design skills** drop the severity/score/tracking gates (design doesn't score
  or rate findings); keep frontmatter, source-leak, word-count, intent-router
  shape, and registry integrity.
- `trigger-evals.json` + `activation-cases.md`: split each old skill's curated
  set by route — critique routes to the `-critique` skill, design routes to the
  `-design` skill. Each set keeps negatives; cross-sibling cases that were once
  intra-skill become cross-skill negatives (e.g. a `design/*` query is a
  negative for `<D>-critique`).
- Finding-ID namespace (`DX-*`, `CA-*`, …) is owned by the `<D>-critique` skill
  (only critique emits findings).

## Catalog surface + gates (Rule 1: all three install lanes)

- Delete `skills/review-heuristics/`.
- `README.md` Layout table + any "which skill?" guidance → the 12 skills.
- `llms.txt` / catalog listing, `.github/CODEOWNERS` globs, install commands.
- `check-shared-content.sh` and `check-routing-csv.sh` already enumerate all
  lanes; they pick up `_shared/<D>/` and the new skills automatically. Verify.
- `check-release-contract.py` and `list-installable-skills.sh`: confirm the 12
  show up; `example-minimal` stays hidden (`metadata.internal: true`).
- `AGENTS.md` references to `review-heuristics` paths (audience-matrix canonical
  home, empirical-warnings links) → repoint to the new owning skill.

## Execution order

1. ✅ ADR 0008 + supersede 0005 / reconcile 0006-0007 (done).
2. ✅ This spec.
3. Build `dx-critique` + `dx-design` as the proven template; `just check` green
   on the pair (and `_shared/dx/`).
4. Fan out `docs` / `perf` / `test` / `architecture` pairs (parallel subagents
   following this recipe once dx is proven).
5. `ux` → `ux-critique`; `ui-craft` → `ui-design` (renames).
6. Delete `review-heuristics`; rewrite catalog surface + repoint AGENTS.md refs.
7. `just check` green across all lanes; confirm `npx skills add . --list`.

## Risks

- **More surface (12 > 1).** Mitigated by `_shared/<D>/` single-sourcing + the
  shared schema/eval gates.
- **Seam prompts** ("review my API *design doc*") land between `<D>-critique`
  and `<D>-design`. Each pair cross-links the sibling in its description.
- **Clean break:** `--skill review-heuristics` stops resolving. Acceptable at
  `0.0.1-alpha`; docs updated in the same change.
