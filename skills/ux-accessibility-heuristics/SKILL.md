---
name: ux-accessibility-heuristics
description: Use when reviewing or designing user-facing product UX, usability, accessibility, forms, navigation, error/recovery copy, onboarding flows, checkout/sign-up friction, or WCAG-oriented accessibility basics. Trigger for heuristic evaluations, cognitive walkthroughs, form friction, IA/navigation issues, keyboard/screen-reader risks, inclusive design checks, and dark-pattern reviews. Do not use for developer-facing DX surfaces; use dx-heuristics for those.
license: MIT
---

# UX Accessibility Heuristics

Review and design user-facing interfaces so real people can complete tasks
without avoidable confusion, exclusion, or coercion. Provenance and grounding
sources live in `skill.json`; this file is runtime routing only.

## Core principle

**A usable interface makes the user's next correct action visible, reversible,
and accessible.** If people must guess, memorize hidden rules, fight a form,
or use a pointing device to recover, the product has a UX problem.

## Activation

- **Bare invocation** (`"use ux-accessibility-heuristics"`, `"UX audit"`,
  `"accessibility review"`): load `references/use-case-registry.csv`, show the
  use-case menu, wait. No file inspection, network calls, or writes.
- **Concrete invocation** with a use case inferable: skip to step 3.
- **Ambiguous concrete invocation**: ask one blocker question identifying the
  use case or target user/task before inspecting private systems.

## Workflow

1. **Pick use case.** Load `references/use-case-registry.csv`. Route to
   `usability-audit`, `accessibility-audit`, `form-review`,
   `navigation-review`, or `error-recovery`.
2. **Load context.** Load only the CSV row's `detail_files` and template.
3. **Identify task and user.** Name the primary user, their goal, constraints,
   and the interface state being reviewed.
4. **Choose lenses.** Use at least two: first-time user, returning user,
   keyboard-only user, assistive-tech user, stressed/error-state user, or
   policy/ethics reviewer.
5. **Apply the playbook.** Prefer concrete observations over generic advice.
   For accessibility, treat WCAG as the baseline and state limits: automated
   scans are not enough; keyboard, focus, semantics, contrast, and assistive
   technology behavior need human verification.
6. **Apply severity and IDs.** Use `references/core/severity-rubric.md` and
   `references/trackable-findings.md`. Use stable IDs like `UX-FORM-001` or
   `UX-A11Y-001`.
7. **Emit output.** Use `templates/audit-report.md`.
8. **Create tracking state.** For 7+ findings, any severity 3-4 finding, or a
   save/track request, write both artifacts now: Markdown ledger at
   `docs/audits/ux-accessibility-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and workflow state at
   `docs/audits/ux-accessibility-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
   If the target is not a repo or `docs/audits/` is not writable, use
   `audit-artifacts/ux-accessibility-heuristics-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`.
   Report both paths. Roadmaps, issues, and product-file edits require explicit
   confirmation.

## Output requirements

Every output includes target user, task, interface state, lenses used,
findings ordered by severity, verification steps, and grounding sources applied.
Accessibility outputs distinguish likely WCAG failures from issues that need
manual or specialist confirmation.

## Reference map

- `references/use-case-registry.csv` - use-case router.
- `references/playbooks/*.md` - use-case playbooks.
- `references/core/severity-rubric.md` - 0-4 severity scale.
- `references/trackable-findings.md` - ledger and closeout workflow.
- `templates/audit-report.md` - output shape.
- `templates/findings-ledger.md` and `templates/workflow-state.json` - tracking
  artifacts.
- `evals/*` and `skill.json` - activation/static checks and provenance.
