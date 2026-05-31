---
name: informed-skill-reviewer
description: Use when reviewing or editing proposed or existing public skills for structure, metadata, source safety, usefulness, validation, and release readiness. Do not use for building a new skill from source material; use `informed-skill-curator` for that.
metadata:
  internal: true
---

# Skill Reviewer

**Produces:** structured review findings (issue list with severity + suggested fix per issue); for proposed skill changes with implied edit authority, also emits patched files. Long-running reviews persist `templates/workflow-state.json`.

## Overview

Review public and repo-local skills for release readiness, structure, source
safety, usefulness, progressive disclosure, templates, evals, and validation.

## Operating Contract

- Review public skills under `skills/<name>/`; also review
  `skills/.experimental/<name>/` if that reserved lane is populated.
- Review repo-local authoring/review skills under `.agents/skills/<name>/`
  when the user asks for catalog or authoring-surface review.
- Read `skill.json` first when present to confirm status and metadata.
- Installable public skills in this repo must use `skill.json.status:
  "published"`; prerelease maturity belongs to the repository release tag.
- For existing skills, produce findings unless the user explicitly asks you to
  edit them. For proposed skill changes, patch clear fixes when edit authority
  is implied.
- Keep `SKILL.md` runtime-only and move user-facing provenance to `skill.json`.
- Reject source summaries disguised as skills.
- Enforce registry-based progressive disclosure: `SKILL.md` should route, not
  carry the full knowledge base. Detailed files and templates must be mapped
  through the skill's router shape: `references/intent-router.csv` alone
  (single-axis), `references/intent-router.csv` plus
  `references/intents/*.csv` (two-axis intent × surface), or
  `references/surface-router.csv` (codebase-agent-readiness's level-2 picker).
- Check that provenance is concise and user-facing in `skill.json`, while any
  public grounding references are short, paraphrased, registry-mapped, and
  useful for execution rather than source explanation.
- Check source safety, usefulness, progressive disclosure, templates, evals, and
  validation.
- For contract-drift reviews, use `references/contract-drift-review.md` to
  trace runtime text through registries, templates, evals, static checks, and
  CI gates.
- For substantial reviews, create saved tracking artifacts by default instead
  of leaving findings only in chat.
- Run `just check` after edits.

## Activation Handshake

If the user gives a skill path, review it. If they invoke this skill without a
target, ask for the skill path or whether to review all product/repo-local
skills.

## Workflow

1. Load `references/intent-router.csv`.
2. Find the requested skill or enumerate skills across `skills/*/`,
   `skills/.experimental/*/`, and `.agents/skills/*/` as the scope requires.
3. Read `SKILL.md`, `skill.json` if present, the router files used by that
   skill, and any referenced files needed for the review.
4. Confirm every public reference/template needed by the skill is mapped from a
   router, and that selected rows load only the files needed for each intent
   or surface.
5. Apply the review rubric and assign stable IDs like `SR-<area>-NNN` to
   trackable findings using `references/trackable-findings.md`.
6. If fixes are clear and the user asked for edit authority, edit files
   directly; otherwise report findings only.
7. Run validation.
8. If all checks pass and the skill meets the rubric, update installable public
   skill manifests to `published` only when the user asked for review with edit
   authority. Use `reviewed` only for internal/template artifacts that are not
   installable product skills.
9. Report findings, edits, validation output, and remaining risks.
10. **Create tracking state.** If the review has 7+ findings, any severity
    3–4, or a save/track request, write both artifacts now: Markdown ledger at
    `docs/audits/informed-skill-reviewer-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
    and workflow state at
    `docs/audits/informed-skill-reviewer-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
    If the target is not a repo or `docs/audits/` is not writable, use
    `audit-artifacts/informed-skill-reviewer-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`.
    Populate from `templates/findings-ledger.md` and
    `templates/workflow-state.json`, report both paths, and do not merely offer
    tracking. Roadmaps, issues, and non-tracking project-file edits remain
    opt-in.

## Review Gates

Block or fix a proposed skill change when:

- `skill.json` is missing required fields or disagrees with the path
- `SKILL.md` contains source provenance, marketing, or long source summaries
- the skill would not activate on realistic prompts
- the skill is generic prompt advice rather than a durable behavior
- references are missing or not mapped from the skill's router
- router rows point to every reference for every intent instead of practicing
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
- release-contract behavior changed without an equivalent gate: required files,
  saved artifacts, symlink invariants, fallback paths, closeout rules, or CI
  workflow steps must be asserted by static checks, not only described

## Reference Map

- `references/intent-router.csv`: review modes and file routing.
- `references/review-rubric.md`: scoring and findings rubric.
- `references/source-safety-review.md`: source-inspired copyright and safety
  checks.
- `references/contract-drift-review.md`: end-to-end release-contract drift
  audit across workflow text, registries, templates, evals, static checks, and
  CI.
- `references/trackable-findings.md`: ledger, workflow-state, closeout rules.
- `templates/review-report.md`: findings report format.
- `templates/findings-ledger.md` and `templates/workflow-state.json`: saved
  tracking artifacts for substantial reviews.
