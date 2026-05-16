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
- **Activation-case sections are unambiguous.** Items in "should activate"
  do not carry "may not activate" hedges; items in "should NOT activate" do
  not carry "may activate" caveats. Hedged cases belong in a boundary /
  ambiguous section with explicit clarifying-question guidance, not in the
  binary positive/negative lists. A static check can grep for hedge words
  inside the wrong-polarity section.
- **Validation regexes are specific to their target syntax.** A static check
  that asserts "every X must appear" should match only the canonical
  syntax it's looking for, not loosely-similar substrings. A regex like
  `\($mode\)` or `\(.*\b$mode\b` will match prose parentheses elsewhere
  in the file and silently pass when the actual tag is missing. Tighten
  detection to the tag's specific form (e.g., italic-parenthesized
  comma-separated tokens within a named section) and parse structurally
  with awk when grep gets ambiguous.

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
- **Special meta-values are documented per parent scope.** When a registry
  CSV contains a meta-value row (e.g., layer = `all`, surface = `any`,
  mode = `auto`), the workflow text says *which parent activities/intents
  support that meta-value* and *what semantics each one applies* — single
  integrative pass, fan-out, etc. A workflow that says "`all` is review
  only" while another activity's CSV also has an `all` row creates a
  silent gap: the agent reads the workflow literally and never offers
  the `all` path for the other activity. Walk every CSV row that uses a
  meta-value and confirm the SKILL.md workflow names both the activity
  and its semantics.
- **Multi-playbook rows are honored downstream.** If any registry CSV row
  references multiple playbook files (semicolon-separated), the
  context-loading step in the workflow describes how multi-playbook rows
  are loaded (single pass vs. fan-out per playbook). A workflow that says
  "load *one* `playbook.md`" silently breaks the multi-playbook case.
- **Template inputs are sourced by the workflow.** Every named field a
  template asks for (Persona, Purpose, Score, Severity, Failure mode,
  Layer, …) has a workflow step that elicits, computes, or explicitly
  skips it for every activity that emits that template. A template with a
  "Purpose-by-purpose coverage" table is incoherent if the workflow
  never elicits purpose for that activity *and* never says "this
  template covers all purposes." Either the workflow gathers the input
  or the workflow says where the template gets it.
- **Template enums match the registry (or are explicitly abbreviated).**
  When a template enumerates values for a routing field (e.g.,
  `Layer: [unit | integration | snapshot]`), the set must either equal
  the corresponding registry CSV's layer set OR include an ellipsis
  (`…` / `...`) signalling non-exhaustive. An exhaustive-looking enum
  that silently drifts from the CSV (e.g., CSV gains a `mutation` row
  but the template still lists 7 layers without it) lets the agent
  fill in the wrong value or omit the routed layer entirely. CI can
  detect this by parsing the enum bracket and comparing against the
  CSV's first column for the activity bound to that template by the
  router's `default_template` column.
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
- **Description claims match the registry (verb × noun cross-product).**
  When the frontmatter `description` lists a verb-set ("reviewing,
  designing, triaging, …") × a noun-set ("unit, integration, …, mutation"),
  a reader infers each pair as supported. Every such pair must be either
  wired in the corresponding activity/intent CSV or *explicitly omitted*
  via an in-CSV comment of the form `# omits: <layers>` (with a
  `# rationale:` line). A description that promises triage of mutation
  tests while `triage.csv` omits the row creates a routing gap users
  will hit; the same is true for design-of-mutation, prune-of-property-
  based, etc. A static gate that parses the description verb/noun
  vocabulary and verifies each pair is wired or explicitly omitted is
  feasible — recommend adding it.

## Status Decision

- **Block**: unsafe, source-reproducing, structurally invalid, or not a skill.
- **Fix**: clear issues can be patched while status is draft.
- **Reviewed**: structure, behavior, progressive disclosure, metadata, source
  safety, and validation pass.
