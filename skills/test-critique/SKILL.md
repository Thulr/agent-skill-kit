---
name: test-critique
description: Use to CRITIQUE an existing test suite — review tests for smells, redundancy, false-pass risk, brittleness, and flakiness and score them, or triage one specific test that is failing, flaky, or unacceptably slow. Covers unit, integration, e2e/UI, exploratory, property-based, contract, snapshot, mutation, and performance tests. Triggers on "review these tests", "are these tests any good", "this test is flaky", "why does CI fail intermittently", "triage this failing test", "do our tests actually catch bugs". Do NOT use to AUTHOR new tests, shape suite strategy, or pick tests to delete (use test-design), or for production-system performance/SLOs (use perf-critique).
license: MIT
---

# Test Critique

Test-suite audit and triage for any layer a team relies on to catch regressions.
Provenance lives in `skill.json`; this file is runtime routing only.

**Produces:** an intent-specific report — `review-report.md` (or
`review-report-multi.md` for a cross-layer review) / `triage-runbook.md`;
tracked reviews also emit `test-critique-findings-ledger-<date>-<slug>.md` +
`test-critique-workflow-state-<date>-<slug>.json`.

## Core principle

**A test earns its place by failing when behavior breaks and only then.** If a
test passes while the code is wrong, breaks on a harmless refactor, flakes, or
nobody can tell what behavior it pins, that is a finding worth recording.

## Activation

- **Bare invocation** (`"use test-critique"`, `"test review"`, `"start"`): load
  `references/starter-scenarios.csv` and `references/intent-router.csv`, then
  show the intent menu with named starter scenarios on top and offer the mode
  choice. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with both intent and layer inferable: skip to step 3.
- **Concrete invocation with ambiguous scope**: ask one blocker question
  identifying intent or layer; do not inspect private systems first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to
   `review` or `triage`. Ambiguous → ask once. (Authoring, strategizing, or
   pruning instead? That is `test-design`.)
2. **Pick layer.** Load the intent's CSV from `references/intents/<intent>.csv`.
   Match to one layer (unit, integration, e2e-ui, exploratory, property-based,
   contract, snapshot, mutation, performance). Ambiguous → ask once with the
   CSV menu.
3. **Load grounded context.** Load only the chosen CSV row's files: one layer
   reference from `references/layers/<layer>.md` plus its `core_refs`. Do not
   load other layer references.
4. **Identify the target persona** from `references/core/personas.md`.
5. **Spawn sub-agents in parallel (default for `review`).** One lens per agent —
   intent reader, refactor adversary, bug-shape hunter. See "Subagent dispatch";
   fall back to sequential only if the host has no delegation primitive. Triage
   is usually single-agent.
6. **Apply the layer reference.** Use the heuristics tagged for this intent. For
   `review`, score the suite 0–10 using `references/core/score-rubric.md`; for
   `triage`, rank hypotheses before naming a fix. If sub-agents ran, synthesize
   their findings here.
7. **Apply severity and IDs** from `references/core/severity-rubric.md` and
   `references/trackable-findings.md` to every review finding or triage cause.
   Use stable IDs like `TEST-<layer>-NNN`.
8. **Emit output.** Review → `templates/review-report.md` (or
   `review-report-multi.md` for a cross-layer review). Triage →
   `templates/triage-runbook.md`.
9. **Create, resume, or close tracking state.** For review outputs with 7+
   findings, any severity 3–4, or a save/track/closeout request, load
   `references/trackable-findings.md`. If the request names an existing ledger,
   workflow-state, PR, branch, or `TEST-*` ID, read saved state first; update
   statuses only after each verification rule passes. Otherwise write both
   artifacts now at
   `docs/audits/test-critique-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and `docs/audits/test-critique-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
   Fall back to `audit-artifacts/test-critique-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`
   if `docs/audits/` is unwritable. Report both paths; keep roadmaps, issues,
   and non-tracking edits opt-in.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the target persona, the layer reference(s) applied, the
intent-specific load-bearing section (findings / hypotheses / prevention),
verification per finding, and the grounding sources from `skill.json.inspired_by`.

## Subagent dispatch

**Default for `review`;** optional for `triage`; skip tiny deterministic or
secret-bound work. Spawn three lenses in parallel — **intent reader**,
**refactor adversary**, **bug-shape hunter** — per
`references/subagent-dispatch.md`.

## Reference map

- `references/intent-router.csv` — level-1 router (review / triage).
- `references/intents/<intent>.csv` — level-2 router (layer) per intent.
- `references/layers/<layer>.md` — layer references (shared with test-design).
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/trackable-findings.md` — ledger, workflow-state, closeout rules.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `references/core/{severity,score}-rubric.md` — the 0–4 and 0–10 scales.
- `references/core/{personas,failure-modes,oracles}.md` — personas, failure
  taxonomy, and consistency oracles.
- `templates/*.md` — review / triage outputs plus tracking artifacts.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
