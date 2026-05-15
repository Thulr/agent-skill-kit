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
  `references/intent-router.csv`, show the intent menu, wait. No file
  inspection, no network calls, no writes.
- **Concrete invocation** with both intent and surface inferable: skip to
  step 3 of the workflow.
- **Concrete invocation with ambiguous scope**: ask one blocker question
  identifying intent or surface; do not inspect private systems first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the prompt to
   one of: `audit`, `design`, `debug`, `edge-pass`. Ambiguous → ask once.
2. **Pick surface.** Load the intent's CSV from
   `references/intents/<intent>.csv`. Match the prompt to one or more
   surfaces. Ambiguous → ask once with the surface menu from the CSV.
3. **Load grounded context.** Load only the files listed in the chosen CSV
   row: one playbook from `references/playbooks/<surface>.md` plus the
   `core_refs` listed. Do not load other playbooks.
4. **Identify the target developer persona** from
   `references/core/personas.md`: first-time user, integrator, contributor,
   maintainer, operator, migration user.
5. **Apply the playbook.** Use the playbook's heuristics tagged for this
   intent. For `audit`, score the surface 0–10 using
   `references/core/score-rubric.md`; for `design`, name the good-shaped
   pattern; for `debug`, rank hypotheses before naming fixes; for
   `edge-pass`, scan all categories in the playbook.
6. **Apply severity** from `references/core/severity-rubric.md` (0–4) to
   every finding or risk.
7. **Emit output** in the intent's `default_template` from the intent
   router row. Audit → `templates/audit-report.md`. Design →
   `templates/design-doc.md`. Debug → `templates/debug-runbook.md`.
   Edge-pass → `templates/edge-checklist.md`.

## Modes

- **Guided Draft (default):** ask only the questions needed to define
  audience, surface, and success criteria. One optionized question at a time,
  3–4 likely choices plus a freeform path. Record the decision, then proceed.
- **Autopilot:** proceed from available context and state assumptions when
  the task is clear and low-risk.
- **Grill Me:** open-ended questions, one at a time, when audience,
  constraints, rollout, or compatibility trade-offs materially change the
  result.

## Output requirements

Every output includes:

- Target developer persona.
- Playbook(s) applied (for traceability to grounded sources).
- Intent-specific load-bearing section: findings (audit), acceptance criteria
  (design), prevention (debug), re-run trigger (edge-pass).
- Verification — how to prove the recommended change had the intended effect.

## Subagent suitability

Use subagents only when permitted and useful for independent perspectives:

- **First-time integrator:** follows only public docs/examples and reports
  unclear steps.
- **Maintainer:** checks compatibility, package boundaries, migration cost,
  and long-term support burden.
- **Adversarial debugger:** starts from likely failures and checks whether
  errors, logs, and docs lead to recovery.

Fallback: run the same three lenses sequentially.

Do not use subagents for tiny copy edits, deterministic command checks, or
tasks requiring secrets/live production access.

## Memory

This skill does not store user identity facts. If repeated operational memory
would help, store only non-secret local defaults (last reviewed surface,
preferred report format) in `~/.local/share/dx-heuristics/memory.md`.

## Reference map

- `references/intent-router.csv` — level-1 router (intent).
- `references/intents/<intent>.csv` — level-2 router (surface) per intent.
- `references/playbooks/<surface>.md` — 14 cited, surface-specific playbooks.
- `references/core/severity-rubric.md` — shared severity scale (0–4).
- `references/core/score-rubric.md` — shared DX score (0–10).
- `references/core/personas.md` — target developer persona list.
- `templates/*.md` — four intent-specific output templates.
- `evals/activation-cases.md` — activation and scenario eval cases.
- `skill.json` — provenance, grounding sources, version, status.
