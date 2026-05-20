---
name: skill-reviewer
description: Use when reviewing or editing draft public skills for structure, metadata, source safety, usefulness, validation, and readiness before they become reviewed or published.
metadata:
  internal: true
---

# Skill Reviewer

## Overview

Review draft public skills before they leave `draft` status. You may edit draft
skill files directly, but only when `skill.json.status` is `draft`.

## Operating Contract

- Review public skills under `skills/<pack>/<skill>/`.
- Read `skill.json` first to confirm status and metadata.
- If status is `draft`, you may patch files directly.
- If status is `reviewed` or `published`, produce findings unless the user
  explicitly asks you to edit that skill.
- Keep `SKILL.md` runtime-only and move user-facing provenance to `skill.json`.
- Reject source summaries disguised as skills.
- Enforce registry-based progressive disclosure: `SKILL.md` should route, not
  carry the full knowledge base; detailed files and templates must be mapped
  through `references/use-case-registry.csv`.
- Check that provenance is concise and user-facing in `skill.json`, while any
  public grounding references are short, paraphrased, registry-mapped, and
  useful for execution rather than source explanation.
- Check source safety, usefulness, progressive disclosure, templates, evals, and
  validation.
- For substantial reviews, create saved tracking artifacts by default instead
  of leaving findings only in chat.
- Run `just check` after edits.

## Activation Handshake

If the user gives a draft skill path, review it. If they invoke this skill
without a target, ask for the skill path or whether to review all draft skills.

## Workflow

1. Load `references/use-case-registry.csv`.
2. Find the requested draft skill or enumerate draft skills from `skill.json`.
3. Read `SKILL.md`, `skill.json`, `references/use-case-registry.csv`, and any
   referenced files needed for the review.
4. Confirm every public reference/template needed by the skill is mapped from
   `references/use-case-registry.csv`, and that the selected rows load only the
   files needed for each use case.
5. Apply the review rubric and assign stable IDs like `SR-<area>-NNN` to
   trackable findings using `references/trackable-findings.md`.
6. If the skill is draft and fixes are clear, edit files directly.
7. Run validation.
8. If all checks pass and the skill meets the rubric, update
   `skill.json.status` to `reviewed` only when the user asked for review with
   edit authority.
9. Report findings, edits, validation output, and remaining risks.
10. **Create tracking state.** If the review has 7+ findings, any severity
    3–4, or a save/track request, write both artifacts now: Markdown ledger at
    `docs/audits/skill-reviewer-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
    and workflow state at
    `docs/audits/skill-reviewer-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
    If the target is not a repo or `docs/audits/` is not writable, use
    `audit-artifacts/skill-reviewer-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`.
    Populate from `templates/findings-ledger.md` and
    `templates/workflow-state.json`, report both paths, and do not merely offer
    tracking. Roadmaps, issues, and non-tracking project-file edits remain
    opt-in.

## Review Gates

Block or fix a draft when:

- `skill.json` is missing required fields or disagrees with the path
- `SKILL.md` contains source provenance, marketing, or long source summaries
- the skill would not activate on realistic prompts
- the skill is generic prompt advice rather than a durable behavior
- references are missing or not mapped from the registry
- registry rows point to every reference for every use case instead of practicing
  progressive disclosure
- public grounding references are long bibliographies, source explainers, author
  biographies, or substitute summaries instead of concise operational maps
- artifact-producing workflows lack templates
- risky workflows lack evals or safety boundaries
- sensitive domains overclaim expertise or omit escalation boundaries
- copyrighted source material is reproduced or closely paraphrased
- workflow, registries, templates, or load-bearing markers have drifted out
  of sync (see Internal Consistency in the rubric) — e.g., a new mode/branch
  in the workflow with no matching downstream wiring (context loading,
  dispatch, or template selection), a menu that lists options not in the
  CSV, a load-bearing comment naming a heading that no longer exists, or a
  doc hardcoding a count/list that should iterate a registry

## Reference Map

- `references/use-case-registry.csv`: review modes and file routing.
- `references/review-rubric.md`: scoring and findings rubric.
- `references/source-safety-review.md`: source-inspired copyright and safety
  checks.
- `references/trackable-findings.md`: ledger, workflow-state, closeout rules.
- `templates/review-report.md`: findings report format.
- `templates/findings-ledger.md` and `templates/workflow-state.json`: saved
  tracking artifacts for substantial reviews.
