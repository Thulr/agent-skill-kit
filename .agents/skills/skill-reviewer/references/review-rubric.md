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

## Internal Consistency

Cross-check that runtime instructions, registries, templates, and load-bearing
markers stay aligned as the skill evolves. Catches drift introduced by partial
edits — the most common failure mode when a skill adds a new mode or refactors
a template.

- **Workflow paths are wired end-to-end.** Every routing branch (intent,
  surface, mode, special meta-values like `all`) is honored by every
  downstream step that varies on it — grounding/context loading, dispatch,
  output template. A new mode that updates one step but not the others
  creates a silent gap: the workflow accepts `surface=all`, a later step
  says "load the chosen CSV row" with no `all` branch, and the agent
  improvises or emits the wrong template. Walk every workflow step and
  confirm each routing branch is handled.
- **Menu options match the registry.** When the workflow says "ask with the
  menu from `<registry>.csv`," every option the workflow accepts (including
  special meta-values like `all`) is either a row in that CSV or explicitly
  added to the menu instructions.
- **Load-bearing markers match section headers.** A `<!-- Load-bearing
  section: X -->` comment in a template names a real `## X` heading in that
  same file. Renaming the heading without updating the marker (or vice
  versa) breaks downstream parsing.
- **No hardcoded counts or item lists derived from registries.** References,
  dispatch docs, and templates iterate the CSV/registry rather than naming a
  fixed count ("all 14 surfaces") or inline list ("api, sdk, cli, ..."). These
  drift the next time a row is added or renamed.
- **Descriptive intros survive structural refactors.** After a refactor
  (e.g., tables → blocks, renamed sections, removed columns), intro
  sentences and inline references describe the new structure. "Each row gets
  a severity…" must not survive a row-to-block conversion.
- **Description claims match the registry.** Every routable concept the
  frontmatter `description` advertises (surface, layer, activity, intent,
  mode) is reachable from at least one registry row. Stronger form: when
  the description lists a verb-set × noun-set (e.g., "reviewing, designing,
  triaging X, Y, Z tests"), each (verb, noun) pair the reader will infer
  must be routable. A description that promises triage of mutation tests
  while `triage.csv` omits the mutation row creates a routing gap users
  will hit. Either wire it or narrow the description's claim.

## Status Decision

- **Block**: unsafe, source-reproducing, structurally invalid, or not a skill.
- **Fix**: clear issues can be patched while status is draft.
- **Reviewed**: structure, behavior, progressive disclosure, metadata, source
  safety, and validation pass.
