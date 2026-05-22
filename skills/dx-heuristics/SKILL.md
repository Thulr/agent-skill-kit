---
name: dx-heuristics
description: Use when evaluating, designing, or debugging developer experience for APIs, SDKs, CLIs, docs, examples, setup, errors, local dev, build/test workflows, migrations, package contracts, contributor workflows, auth, IDE integration, plugins, performance, or telemetry. Also trigger for DX reviews, developer onboarding friction, confusing integration steps, dev-facing interface design, or PR feedback about developer usability.
license: MIT
---

# DX Heuristics

Practical developer-experience review, design, debugging, and risk-scan for any
surface a developer has to install, call, debug, extend, test, or maintain.
Provenance and grounding sources live in `skill.json`; this file is runtime
routing only.

## Core principle

**Make the paved path obvious and failure states actionable.** If a competent
developer has to guess, hunt through source, copy from a stale example, or
debug an avoidable setup issue, that is a DX problem.

## Activation

- **Bare invocation** (`"use dx-heuristics"`, `"DX review"`, `"start"`): load
  `references/starter-scenarios.csv` and `references/intent-router.csv`,
  then show the intent menu with named starter scenarios on top and offer
  the mode choice. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with both intent and surface inferable: skip to
  step 3 of the workflow.
- **Concrete invocation with ambiguous scope**: ask one blocker question
  identifying intent or surface; do not inspect private systems first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to
   one of: `audit`, `design`, `debug`, `edge-pass`. Ambiguous → ask once.
2. **Pick surface.** Load the intent's CSV from
   `references/intents/<intent>.csv`. Match the prompt to one or more
   surfaces, or `all` (audit only) for multi-surface fan-out — see
   `references/subagent-dispatch.md`. Ambiguous → ask once with the CSV
   menu, adding `all` as an option for audit intent.
3. **Load grounded context.** Load only the files listed in the chosen CSV
   row: one playbook from `references/playbooks/<surface>.md` plus the
   `core_refs` listed. Do not load other playbooks. Skip this step when
   surface = `all` — each spawned surface agent loads its own playbook
   in step 5.
4. **Identify the target developer persona** from
   `references/core/personas.md`.
5. **Spawn sub-agents in parallel (default for `audit` and
   `edge-pass`).** Single-surface: delegate one lens per agent —
   first-time integrator, maintainer, adversarial debugger. Audit + `all`:
   delegate one surface per agent; each runs the three lenses sequentially
   inside itself. See "Subagent dispatch" below; fall back to sequential
   execution only if the host has no delegation primitive.
6. **Apply the playbook.** Use the playbook's heuristics tagged for this
   intent. For `audit`, score the surface 0–10 using
   `references/core/score-rubric.md`; for `design`, name the good-shaped
   pattern; for `debug`, rank hypotheses before naming fixes; for
   `edge-pass`, scan all categories in the playbook. If sub-agents ran,
   synthesize their findings here.
7. **Apply severity and IDs** from `references/core/severity-rubric.md`
   and `references/trackable-findings.md` to every audit/edge-pass finding
   or risk. Use stable IDs like `DX-<surface>-NNN`.
8. **Emit output.** Audit → `templates/audit-report.md` (or
   `audit-report-multi.md` for surface = `all`). Design →
   `templates/design-doc.md`. Debug → `templates/debug-runbook.md`.
   Edge-pass → `templates/edge-checklist.md`.
9. **Create, resume, or close tracking state.** For audit/edge-pass outputs
   with 7+ findings, any severity 3–4, or a save/track/closeout request, load
   `references/trackable-findings.md`. If the request names an existing
   ledger, workflow-state, PR, branch, or `DX-*` ID, read saved state first;
   update statuses only after each verification rule passes. Otherwise write
   both artifacts now at
   `docs/audits/dx-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and `docs/audits/dx-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
   Fall back to `audit-artifacts/dx-heuristics-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`
   if `docs/audits/` is unwritable. Report both paths; keep roadmaps, issues,
   and non-tracking edits opt-in.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output includes:

- Target developer persona.
- Playbook(s) applied.
- Intent-specific load-bearing section: findings (audit), acceptance criteria
  (design), prevention (debug), re-run trigger (edge-pass).
- Verification — how to prove the change worked.
- Grounding sources applied from `skill.json.inspired_by`.

## Subagent dispatch

**Default for `audit` and `edge-pass`;** preferred for `design`; optional for
`debug`; skip tiny deterministic or secret-bound work. Spawn three lenses in
parallel — **first-time integrator**, **maintainer**, **adversarial
debugger** — per `references/subagent-dispatch.md`. Without delegation, run
the lenses sequentially and preserve disagreements as open questions.

## Reference map

- `references/intent-router.csv` — level-1 router (intent).
- `references/intents/<intent>.csv` — level-2 router (surface) per intent.
- `references/playbooks/<surface>.md` — surface-specific playbooks (one per
  surface listed in the intent CSVs).
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/trackable-findings.md` — ledger, workflow-state, closeout rules.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me contract (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `references/core/{severity,score}-rubric.md` — shared 0–4 and 0–10 scales.
- `references/core/personas.md` — target developer persona list.
- `templates/*.md` — four intent-specific outputs plus tracking artifacts.
- `evals/activation-cases.md` — activation and behavioral cases (positive
  and negative).
- `evals/run-static-checks.sh` — structural and schema gates run in CI.
- `evals/trigger-evals.json` — queries for the description-optimization loop.
- `skill.json` — provenance, grounding sources, version, status.
