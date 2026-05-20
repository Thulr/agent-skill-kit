---
name: test-heuristics
description: Use when reviewing, designing, triaging, or rationalizing test suites — unit, integration, e2e/UI, exploratory, property-based, contract, snapshot, mutation, or performance tests. Trigger for flakiness triage, false-pass risk, brittleness on refactor, suite pruning, test-pyramid/trophy decisions, exploratory charters, and snapshot review. Routes by activity (triage / review / author / strategize / prune) and layer.
license: MIT
---

# Test Heuristics

Practical test-suite review, design, triage, strategy, and pruning for any
testing layer a developer writes, runs, debugs, or maintains. Provenance and
grounding sources live in `skill.json`; this file is runtime routing only.

## Core principle

**A test exists to catch the bugs that ship in this code class — and to be
diagnosable when it fails.** A test that passes regardless of bug presence,
breaks on legitimate refactor, or fails uninformatively is failing at its job.

## Activation

- **Bare invocation** (`"use test-heuristics"`, `"test review"`, `"start"`):
  load `references/activity-router.csv`, show the activity menu, wait. No
  file inspection, no network calls, no writes.
- **Concrete invocation** with both activity and layer inferable: skip to
  step 3 of the workflow.
- **Concrete invocation with ambiguous scope**: ask one blocker question
  identifying activity or layer; do not inspect private systems first.

## Workflow

1. **Pick activity.** Load `references/activity-router.csv`. Match the
   prompt to: `triage`, `review`, `author`, `strategize`, `prune`.
   Ambiguous → ask once.
2. **Pick layer.** Load `references/activities/<activity>.csv`. Match to
   one or more layers, or `all` for cross-layer treatment (`review`
   fan-out, `strategize` integrative pass). Ambiguous → ask with the
   menu.
3. **Load grounded context.** Load the files in the chosen row's
   `playbook` column — most rows reference one playbook; cross-layer
   rows list many — plus the listed `core_refs`. For `review/all`,
   skip: each spawned layer agent loads its own.
4. **Identify the target persona** from `references/core/personas.md`.
5. **Handle purpose** (`spec`, `regression`, `characterization`,
   `exploration`, `gate`). For `review`/`author`/`triage`/`prune`, ask
   which applies (multiple can); heuristics for that purpose apply
   first. For `strategize`, skip — the strategy template covers all
   purposes via its purpose-by-purpose table.
6. **Spawn sub-agents in parallel** (default for `review` and `prune`).
   Single-layer: one lens per agent. `review/all`: one layer per agent;
   each runs the three lenses sequentially inside itself.
   `strategize/all`: single integrative pass — no fan-out. See
   `references/subagent-dispatch.md`. Fall back to sequential lenses
   only if the host has no delegation primitive.
7. **Apply the playbook.** Use heuristics tagged for this activity. For
   `review`, score 0–10 using `references/core/score-rubric.md`. For
   `author`, name the good-shaped pattern. For `triage`, rank hypotheses
   before fixes. For `strategize`, produce a per-layer investment
   recommendation. For `prune`, produce a deletion list with rationale.
   Synthesize sub-agent findings here.
8. **Apply severity, IDs, and failure modes** from
   `references/core/severity-rubric.md`, `references/trackable-findings.md`,
   and `references/core/failure-modes.md` to every review/prune finding. Use
   stable IDs like `TEST-<layer>-NNN`.
9. **Emit output** per the default template in the activity router row.
10. **Create, resume, or close tracking state.** For review/prune outputs with
   7+ findings or candidates, any severity 3–4, or a save/track/closeout
   request, load `references/trackable-findings.md`. If the request names an
   existing ledger, workflow-state file, PR, diff, branch, or `TEST-*` ID, read
   saved state first and update statuses only after each verification rule
   passes. Otherwise write both artifacts now: Markdown ledger at
   `docs/audits/test-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and workflow state at
   `docs/audits/test-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
   If the target is not a repo or `docs/audits/` is not writable, use
   `audit-artifacts/test-heuristics-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`.
   Populate/update `templates/findings-ledger.md` and
   `templates/workflow-state.json`, report both paths, and keep roadmaps,
   issues, and non-tracking edits opt-in.

## Modes

- **Guided Draft (default):** one optionized question at a time.
- **Autopilot:** proceed from clear, low-risk context; state assumptions.
- **Grill Me:** one open-ended question at a time when trade-offs matter.

## Output requirements

Every output includes target persona, layer/purpose, the template's
load-bearing section, failure modes on findings, and verification.

## Subagent dispatch

Independent perspectives catch issues a single pass misses. **Default for
`review` and `prune`;** preferred for `author`; optional for `triage`; skip tiny
deterministic work or secret-bound tasks. Spawn three agents in parallel —
**intent reader**, **refactor adversary**, **bug-shape hunter** — and load
`references/subagent-dispatch.md` for prompts and synthesis. If the host lacks
delegation, run the lenses sequentially and still preserve disagreements as
open questions.

## Reference map

- `references/activity-router.csv` — level-1 router (activity).
- `references/activities/<activity>.csv` — level-2 router (layer) per activity.
- `references/layers/<layer>.md` — layer-specific playbooks (one per layer
  listed in the activity CSVs).
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/trackable-findings.md` — ledger, workflow-state, closeout rules.
- `references/core/severity-rubric.md` — 0–4 severity scale.
- `references/core/score-rubric.md` — 0–10 test-quality scale.
- `references/core/personas.md` — target persona list.
- `references/core/failure-modes.md` — six-mode test failure taxonomy.
- `references/core/oracles.md` — test oracles for exploratory work and the
  bug-shape hunter lens.
- `templates/*.md` — five activity outputs plus tracking artifacts.
- `evals/activation-cases.md` — activation and behavioral cases (positive
  and negative).
- `evals/run-static-checks.sh` — structural and schema gates run in CI.
- `evals/trigger-evals.json` — queries for the description-optimization loop.
- `skill.json` — provenance, grounding sources, version, status.
