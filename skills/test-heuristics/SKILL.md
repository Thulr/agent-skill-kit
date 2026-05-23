---
name: test-heuristics
description: Use when reviewing, designing, triaging, or rationalizing test suites — unit, integration, e2e/UI, exploratory, property-based, contract, snapshot, mutation, or performance tests. Trigger for flakiness triage, false-pass risk, brittleness on refactor, suite pruning, test-pyramid/trophy decisions, exploratory charters, and snapshot review. Routes by intent (triage / review / author / strategize / prune) and surface. Do not use for production-system performance / SLOs (use `perf-observability-heuristics`).
license: MIT
---

# Test Heuristics

Test-suite review, design, triage, strategy, and pruning for any testing
layer a developer writes, runs, debugs, or maintains. Provenance and
grounding sources live in `skill.json`; this file is runtime routing only.

## Core principle

**A test exists to catch the bugs that ship in this code class — and to be
diagnosable when it fails.** A test that passes regardless of bug presence,
breaks on legitimate refactor, or fails uninformatively is failing at its job.

## Activation

- **Bare invocation** (`"use test-heuristics"`, `"test review"`, `"start"`):
  load `references/starter-scenarios.csv` and `references/intent-router.csv`,
  then show the intent menu with named starter scenarios on top and offer
  the mode choice. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with both intent and surface inferable: skip to
  step 3 of the workflow.
- **Concrete invocation with ambiguous scope**: ask one blocker question
  identifying intent or surface; do not inspect private systems first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match to:
   `triage`, `review`, `author`, `strategize`, `prune`. Ambiguous → ask once.
2. **Pick surface.** Load `references/intents/<intent>.csv`. Match to
   one or more surfaces, or `all` for cross-layer treatment (`review`
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
7. **Apply the playbook.** Use heuristics tagged for this intent. For
   `review`, score 0–10 using `references/core/score-rubric.md`. For
   `author`, name the good-shaped pattern. For `triage`, rank hypotheses
   before fixes. For `strategize`, produce a per-layer investment
   recommendation. For `prune`, produce a deletion list with rationale.
   Synthesize sub-agent findings here.
8. **Apply severity, IDs, and failure modes** from
   `references/core/severity-rubric.md`, `references/trackable-findings.md`,
   and `references/core/failure-modes.md` to every review/prune finding. Use
   stable IDs like `TEST-<layer>-NNN`.
9. **Emit output** per the default template in the intent router row.
10. **Create, resume, or close tracking state.** For review/prune outputs with
   7+ findings, any severity 3–4, or a save/track/closeout request, load
   `references/trackable-findings.md`. If the request names an existing
   ledger, workflow-state, PR, branch, or `TEST-*` ID, read saved state first;
   update statuses only after each verification rule passes. Otherwise write
   both artifacts now at
   `docs/audits/test-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and `docs/audits/test-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
   Fall back to `audit-artifacts/test-heuristics-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`
   if `docs/audits/` is unwritable. Report both paths; keep roadmaps, issues,
   and non-tracking edits opt-in.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output includes target persona, layer/purpose, the template's
load-bearing section, failure modes on findings, verification, and grounding
sources applied from `skill.json.inspired_by`.

## Subagent dispatch

**Default for `review` and `prune`;** preferred for `author`; optional for
`triage`; skip tiny deterministic or secret-bound tasks. Spawn three lenses
in parallel — **intent reader**, **refactor adversary**, **bug-shape
hunter** — per `references/subagent-dispatch.md`. If the host lacks
delegation, run the lenses sequentially and still preserve disagreements as
open questions.

## Reference map

- `references/intent-router.csv` — level-1 router (intent).
- `references/intents/<intent>.csv` — level-2 router (surface) per intent.
- `references/layers/<layer>.md` — test-pyramid-layer playbooks (one per
  layer listed in the intent CSVs).
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/trackable-findings.md` — ledger, workflow-state, closeout rules.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me contract (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `references/core/severity-rubric.md` — 0–4 severity scale.
- `references/core/score-rubric.md` — 0–10 test-quality scale.
- `references/core/personas.md` — target persona list.
- `references/core/failure-modes.md` — six-mode test failure taxonomy.
- `references/core/oracles.md` — test oracles for exploratory work and the
  bug-shape hunter lens.
- `templates/*.md` — five intent outputs plus tracking artifacts.
- `evals/activation-cases.md` — activation and behavioral cases (positive
  and negative).
- `evals/run-static-checks.sh` — structural and schema gates run in CI.
- `evals/trigger-evals.json` — queries for the description-optimization loop.
- `skill.json` — provenance, grounding sources, version, status.
