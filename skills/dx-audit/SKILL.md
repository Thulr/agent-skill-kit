---
name: dx-audit
description: Use to AUDIT an existing developer-experience surface — audit it for friction and score it, debug a reported developer-facing issue, or run a pre-ship edge-case risk pass. Covers APIs, SDKs, CLIs, developer docs, examples, errors, setup, local inner-loop, migrations, package contracts, contributor flows, auth, IDE, plugins, perf, telemetry, README/first-impressions, logging, config, and changelogs. Triggers on "DX review", "audit our API/SDK/CLI", "is this error message OK", "why do users hit this", "pre-1.0 risk pass". Do NOT use to DESIGN a new surface from scratch (use dx-design), to audit documentation as a reading surface (use docs-audit), to only tighten one piece's prose (use writing-audit), for end-user product UX/accessibility (use ux-audit), or for AI-agent-facing surfaces, AGENTS.md, or AI/Agent SDK design (use agent-experience).
license: MIT
---

# DX Critique

Developer-experience audit, debugging, and edge-case risk-scan for any surface
a developer installs, calls, or extends. Provenance lives in `skill.json`; this
file is runtime routing only.

**Produces:** an intent-specific report — `audit-report.md` (or
`audit-report-multi.md` for `all`) / `debug-runbook.md` / `edge-checklist.md`;
tracked audits also emit a findings-ledger + workflow-state file.

## Core principle

**Make the paved path obvious and failure states actionable.** If a competent
developer must guess, hunt through source, copy a stale example, or debug
avoidable setup, that is a DX problem worth a finding.

## Activation

- **Bare invocation** (`"use dx-audit"`, `"DX review"`, `"start"`): load
  `references/starter-scenarios.csv` and `references/intent-router.csv`, then
  show the intent menu with named starter scenarios on top and offer the mode
  choice. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with both intent and surface inferable: skip to step 3.
- **Concrete invocation with ambiguous scope**: ask one blocker question
  identifying intent or surface; do not inspect private systems first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to one
   of: `audit`, `debug`, `edge-pass`. Ambiguous → ask once. (Designing a new
   surface instead? That is `dx-design`.)
2. **Pick surface.** Load the intent's CSV from
   `references/intents/<intent>.csv`. Match to one or more surfaces, or `all`
   (audit only) for a multi-surface fan-out — see `references/subagent-dispatch.md`.
   Ambiguous → ask once with the CSV menu.
3. **Load grounded context.** Load only the chosen CSV row's files: one playbook
   from `references/playbooks/<surface>.md` plus its `core_refs`. Do not load
   other playbooks. Skip for `all` — each surface agent loads its own playbook.
4. **Identify the target developer persona** from `references/core/personas.md`.
   Then **calibrate to project scale** per `references/calibration.md` —
   tier-gate scope, collapse same-mechanism gaps, split fixes Now vs Later.
5. **Spawn sub-agents in parallel (default for `audit` and `edge-pass`).**
   Single-surface: one lens per agent; audit + `all`: one surface per agent
   running the three lenses sequentially. See "Subagent dispatch"; fall back to
   sequential only if the host lacks a delegation primitive.
6. **Apply the playbook.** Use the heuristics tagged for this intent. For
   `audit`, score 0–10 using `references/core/score-rubric.md`; for `debug`, rank
   hypotheses before naming fixes; for `edge-pass`, scan every playbook category.
   If sub-agents ran, synthesize their findings here.
7. **Apply severity and IDs** from `references/core/severity-rubric.md` and
   `references/trackable-findings.md` to every audit/edge-pass finding or risk.
   Use stable IDs like `DX-<surface>-NNN`.
8. **Emit output.** Audit → `templates/audit-report.md` (or
   `audit-report-multi.md` for `all`). Debug → `templates/debug-runbook.md`.
   Edge-pass → `templates/edge-checklist.md`.
9. **Create, resume, or close tracking state.** For audit/edge-pass outputs with
   7+ findings, any severity 3–4, or a save/track/closeout request, load
   `references/trackable-findings.md`. If the request names an existing ledger,
   workflow-state, PR, branch, or `DX-*` ID, read saved state first; update
   statuses only after each verification rule passes. Otherwise write both
   artifacts now at
   `docs/audits/dx-audit-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and `docs/audits/dx-audit-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
   Fall back to `audit-artifacts/dx-audit-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`
   if `docs/audits/` is unwritable. Report both paths; keep roadmaps, issues,
   and non-tracking edits opt-in.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the target developer persona, the playbook(s) applied, the
intent-specific load-bearing section, verification per finding, and the
grounding sources from `skill.json.inspired_by`.

## Subagent dispatch

**Default for `audit` and `edge-pass`;** optional for `debug`; skip tiny
deterministic or secret-bound work. Spawn three lenses in parallel —
**first-time integrator**, **maintainer**, **adversarial debugger** — per
`references/subagent-dispatch.md`.

## Reference map

- `references/intent-router.csv` — level-1 router (audit / debug / edge-pass).
- `references/intents/<intent>.csv` — level-2 router (surface) per intent.
- `references/playbooks/<surface>.md` — surface playbooks (shared with dx-design).
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/trackable-findings.md` — ledger, workflow-state, closeout rules.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/calibration.md` — project-scale tiers + every-X collapse rule (shared).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `references/core/{severity,score}-rubric.md` — the 0–4 and 0–10 scales.
- `references/core/personas.md` — target developer persona list.
- `templates/*.md` — audit / debug / edge-pass outputs plus tracking artifacts.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
