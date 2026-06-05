---
name: ux-audit
description: Use to AUDIT an existing end-user product UX or accessibility surface — audit a usability flow for confusion, review a form for friction, inspect navigation / information architecture, sweep error and recovery copy, or run a WCAG / keyboard / screen-reader / contrast / focus accessibility pass. Triggers on "UX audit", "heuristic evaluation", "users are confused", "signup/checkout drop-off", "IA review", "accessibility/WCAG review", "is this form usable". Do NOT use to AUDIT developer-facing surfaces such as APIs, SDKs, CLIs, or dev docs (use dx-audit), to BUILD or visually polish UI, design systems, or prototypes (use ui-design), or for AI-agent-facing surfaces and AGENTS.md (use agent-experience).
license: MIT
---

# UX Critique

End-user usability and accessibility audit for any interface real people use —
flows, forms, navigation, error states, and assistive-technology paths.
Provenance and grounding sources live in `skill.json`; this file is runtime
routing only.

**Produces:** `audit-report.md` per use case (usability / accessibility / form /
navigation / error-recovery); tracked reviews also emit
`ux-audit-findings-ledger-<date>-<slug>.md` +
`ux-audit-workflow-state-<date>-<slug>.json`.

## Core principle

**A usable interface makes the user's next correct action visible, reversible,
and accessible.** If people must guess, memorize hidden rules, fight a form, or
reach for a pointing device to recover, that is a UX problem worth a finding.

## Activation

- **Bare invocation** (`"use ux-audit"`, `"UX audit"`, `"accessibility
  review"`): load `references/starter-scenarios.csv` and
  `references/intent-router.csv`, then show the intent menu with the named
  starter scenarios on top (each pre-routes intent + persona) and offer the mode
  choice. Wait. No file inspection, network calls, or writes.
- **Concrete invocation** with an intent inferable: skip to step 3.
- **Ambiguous concrete invocation**: ask one blocker question identifying the
  intent or the target user/task before inspecting private systems.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Route the prompt to one
   of: `usability-audit`, `accessibility-audit`, `form-review`,
   `navigation-review`, `error-recovery`. Ambiguous → ask once. (Building or
   polishing the UI instead? That is `ui-design`.)
2. **Load grounded context.** Load only the chosen row's `detail_files` (one
   playbook plus its core refs) and `templates`. Do not load other playbooks.
3. **Identify task and user.** Name the primary user, their goal, constraints,
   and the interface state being reviewed.
4. **Choose lenses.** Use at least two: first-time user, returning user,
   keyboard-only user, assistive-tech user, stressed/error-state user, or
   policy/ethics reviewer.
   Then **calibrate to project scale** per `references/calibration.md`: infer the
   tier (Prototype / Growing / Load-bearing) — ask once only if unclear. Below
   Load-bearing, narrow scope and collapse same-mechanism gaps into one systemic
   finding at max severity, and split fixes Now vs Later; tier reshapes emission,
   not the severity rubric.
5. **Apply the playbook.** Prefer concrete observations over generic advice. For
   accessibility, treat the WCAG baseline as a floor and state its limits:
   automated scans are not enough — keyboard, focus, semantics, contrast, and
   assistive-technology behavior need human verification.
6. **Apply severity and IDs** from `references/core/severity-rubric.md` and
   `references/trackable-findings.md` to every finding. Use stable IDs like
   `UX-FORM-001` or `UX-A11Y-001`.
7. **Emit output.** Use `templates/audit-report.md`.
8. **Create, resume, or close tracking state.** For outputs with 7+ findings,
   any severity 3–4 finding, or a save/track/closeout request, load
   `references/trackable-findings.md`. If the request names an existing ledger,
   workflow-state, PR, branch, or `UX-*` ID, read saved state first; update
   statuses only after each verification rule passes. Otherwise write both
   artifacts now at
   `docs/audits/ux-audit-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and `docs/audits/ux-audit-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
   Fall back to
   `audit-artifacts/ux-audit-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`
   if `docs/audits/` is unwritable. Report both paths; keep roadmaps, issues,
   and product-file edits opt-in.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare
invocation, before loading the intent router; default to Guided Draft on
concrete invocations.

## Output requirements

Every output names the target user, the task, the interface state, the lenses
used, findings ordered by severity, verification per finding, and the grounding
sources from `skill.json.inspired_by`. Accessibility outputs distinguish likely
WCAG failures from issues that need manual or specialist confirmation.

## Reference map

- `references/intent-router.csv` — one-layer router (intent → detail files +
  templates).
- `references/starter-scenarios.csv` — named worked examples for bare invocation.
- `references/playbooks/*.md` — per-intent playbooks.
- `references/core/severity-rubric.md` — the 0–4 severity scale.
- `references/trackable-findings.md` — ledger, workflow-state, closeout rules.
- `references/modes.md` — Guided Draft / Autopilot / Grill Me (shared).
- `references/calibration.md` — project-scale tiers + every-X collapse rule (shared).
- `templates/audit-report.md` — output shape.
- `templates/findings-ledger.md` and `templates/workflow-state.json` — tracking
  artifacts.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
