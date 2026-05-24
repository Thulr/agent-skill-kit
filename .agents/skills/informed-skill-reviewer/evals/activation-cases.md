# Activation Cases

Behavioral cases for the repo-local `skill-reviewer` skill.

## Positive

- "Review this draft skill before publishing" with a draft skill path -> loads the registry and review rubric, checks metadata/source safety/templates/evals, and emits `templates/review-report.md`.
- "Audit all draft skills for source-safety issues" -> routes through the `source-safety-audit` registry row and reports findings per skill.
- "Check this skill for contract drift between SKILL.md, registries, templates, evals, and CI" -> routes through `contract-drift-audit`, follows runtime text through every release-contract artifact, and flags missing static/CI gates.
- "Review this draft and save a ledger for follow-up" -> assigns stable `SR-<area>-NNN` finding IDs and saves both `skill-reviewer-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and `skill-reviewer-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.

## Negative

- "Review this application code for bugs" -> not a skill-review task.
- "Publish this reviewed skill" with no review request -> not a reviewer workflow.

## Artifact/State Regression

- Reviews with 7+ findings or any severity 3-4 finding save both tracking artifacts under `docs/audits/`, or use the matching `audit-artifacts/skill-reviewer-...` fallback.
- The response reports both saved paths and does not merely offer to create them.
- Roadmaps, GitHub issues, and non-tracking project-file edits require explicit confirmation.
