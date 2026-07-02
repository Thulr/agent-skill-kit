---
name: test-audit
description: "Audit an existing test suite for smells, redundancy, false-pass risk, brittleness, and flakiness. Triage failing, flaky, or slow tests. Triggers: 'review these tests', 'this test is flaky', 'do our tests actually catch bugs'. Do NOT use to author tests, shape suite strategy, or pick tests to delete (use test-design)."
license: MIT
---

# Test Audit

Test-suite audit and triage for any layer a team relies on to catch regressions.
Provenance lives in `skill.json`; this file is runtime routing only.

**Produces:** an intent-specific report — `audit-report.md` (or
`audit-report-multi.md` for a cross-layer audit) / `triage-runbook.md`;
tracked audits also emit `test-audit-findings-ledger-<date>-<slug>.md` +
`test-audit-workflow-state-<date>-<slug>.json`.

## Core principle

**A test earns its place by failing when behavior breaks and only then.** If a
test passes while the code is wrong, breaks on a harmless refactor, flakes, or
nobody can tell what behavior it pins, that is a finding worth recording.

## Activation

- **Bare invocation** (`"use test-audit"`, `"test audit"`, `"start"`): show a compact menu: mode choice (guided / autopilot / grill me?) and numbered intents from the router. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with both intent and layer inferable: skip to step 3.
- **Concrete invocation with ambiguous scope**: ask one — e.g., *"Are you auditing unit tests, integration tests, or e2e/UI tests?"* or *"Is this a full-suite review or a single flaky-test triage?"*

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to
   `audit` or `triage`. Ambiguous → ask once. (Authoring, strategizing, or
   pruning instead? That is `test-design`.)
2. **Pick layer.** Load the intent's CSV from `references/intents/<intent>.csv`.
   Match to one layer (unit, integration, e2e-ui, exploratory, property-based,
   contract, snapshot, mutation, performance). Ambiguous → ask once with the
   CSV menu. Whole-suite request → route `all`: fan out per §Subagent
   dispatch and emit `templates/audit-report-multi.md`.
3. **Load grounded context.** Load only the chosen CSV row's files: one layer
   reference from `references/layers/<layer>.md` plus its `core_refs`. Do not
   load other layer references.
4. **Identify the target persona** from `references/core/personas.md`.
   Then **calibrate to project scale** per `references/calibration.md`: infer the
   tier (Prototype / Growing / Load-bearing) — ask once only if unclear. Below
   Load-bearing, narrow scope and collapse same-mechanism gaps into one systemic
   finding at max severity, and split fixes Now vs Later; tier reshapes emission,
   not the severity rubric.
5. **Spawn sub-agents in parallel (default for `audit`).** One lens per agent —
   intent reader, refactor adversary, bug-shape hunter. See "Subagent dispatch";
   fall back to sequential only if the host has no delegation primitive. Triage
   is usually single-agent.
6. **Apply the layer reference.** Use the heuristics tagged for this intent. For
   `audit`, score the suite 0–10 using `references/core/score-rubric.md`; for
   `triage`, rank hypotheses before naming a fix. If sub-agents ran, synthesize
   their findings here.
7. **Apply severity and IDs** from `references/core/severity-rubric.md` and
   `references/trackable-findings.md` to every audit finding or triage cause.
   Use stable IDs like `TEST-<layer>-NNN`.
8. **Emit output.** Audit → `templates/audit-report.md` (or
   `audit-report-multi.md` for a cross-layer audit). Triage →
   `templates/triage-runbook.md`.
9. **Create, resume, or close tracking state.** For audit outputs with 7+
   findings, any severity 3–4, or a save/track/closeout request, load
   `references/trackable-findings.md`. If the request names an existing ledger,
   workflow-state, PR, branch, or `TEST-*` ID, read saved state first; update
   statuses only after each verification rule passes. Otherwise write both
   artifacts now at
   `docs/audits/test-audit-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and `docs/audits/test-audit-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
   Fall back to `audit-artifacts/test-audit-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`
   if `docs/audits/` is unwritable. Report both paths; keep roadmaps, issues,
   and non-tracking edits opt-in.

> **Wrong direction?** If the user says this is not what they meant, go back to step 1 (Pick intent) - do not patch in the wrong direction. Restate the corrected understanding and re-plan.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the target persona, the layer reference(s) applied, the
intent-specific load-bearing section (findings / hypotheses / prevention),
verification per finding, and the grounding sources from `skill.json.inspired_by`.

## Subagent dispatch

**Default for `audit`;** optional for `triage`; skip tiny deterministic or
secret-bound work. Spawn three lenses in parallel — **intent reader**,
**refactor adversary**, **bug-shape hunter** — per
`references/subagent-dispatch.md`.

## Reference map

- `references/intent-router.csv` — level-1 router (audit / triage).
- `references/intents/<intent>.csv` — level-2 router (layer) per intent.
- `references/layers/<layer>.md` — layer references (shared with test-design).
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/trackable-findings.md` — ledger, workflow-state, closeout rules.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/calibration.md` — project-scale tiers + every-X collapse rule (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `references/core/{severity,score}-rubric.md` — the 0–4 and 0–10 scales.
- `references/core/{personas,failure-modes,oracles}.md` — personas, failure
  taxonomy, and consistency oracles.
- `templates/*.md` — audit / triage outputs plus tracking artifacts.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
