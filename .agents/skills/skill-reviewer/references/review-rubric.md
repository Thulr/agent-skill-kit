# Skill Review Rubric

Score each category as pass, fix, or block.

## Structure

- Path is `skills/<pack>/<skill>/`.
- `SKILL.md`, `skill.json`, and `references/use-case-registry.csv` exist.
- `skill.json.name` matches frontmatter `name`.
- `skill.json.pack` matches the path pack.
- `skill.json.status` is `draft`, `reviewed`, or `published`.
- Every public reference file and artifact template needed by the skill is
  mapped from `references/use-case-registry.csv`.

## Runtime Quality

- `SKILL.md` has concrete activation criteria.
- Bare activation is interactive and non-side-effectful.
- Workflows are specific enough for another agent to run.
- Heavy knowledge lives in references, not only in `SKILL.md`.
- Registry rows load only the detail files and templates needed for the matched
  use case; rows should not point to the whole knowledge base by default.
- The skill can be useful to a user who has not read or watched the source.

## Grounding And Provenance

- `skill.json.inspired_by` carries concise user-facing provenance.
- `SKILL.md` does not contain author biographies, further-reading sections,
  source marketing, long bibliographies, or source summaries.
- Public grounding references, when present, are concise operational maps:
  source family, derived heuristic, caveat, and relevant use case.
- Detailed research trails, notes, and source URLs belong in local dossiers or
  user-provided notes, not in runtime instructions.

## Pack Fit

- Pack describes a capability domain.
- Skill name describes the agent behavior.
- Source title, creator, character, or franchise is not used as the pack.
- The candidate should not be a reference addition to an existing skill instead.

## Artifact And Eval Quality

- Artifact-producing workflows have templates.
- Reused or risky behavior has activation and scenario evals.
- Validation instructions are realistic and runnable.
- Templates do not contain unresolved placeholders in published/reviewed status.

## Status Decision

- **Block**: unsafe, source-reproducing, structurally invalid, or not a skill.
- **Fix**: clear issues can be patched while status is draft.
- **Reviewed**: structure, behavior, progressive disclosure, metadata, source
  safety, and validation pass.
