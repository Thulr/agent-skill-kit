# Developer Documentation Playbook

## Scope

Covers documentation for humans integrating or maintaining software: README,
quickstarts, tutorials, API reference, code samples, examples, changelogs,
troubleshooting, search, and findability. Use this when the primary audience is
a developer reading docs to build, debug, or upgrade.

- In: time-to-first-success, install instructions, minimal working examples,
  reference completeness, examples ecosystem, error-doc links, migration docs,
  changelogs, search labels, and developer doc telemetry.
- Out: pure API design outside docs (use a DX skill), end-user product help
  (use `ux-help.md`), and schema/tool description quality (use
  `api-contracts.md`).
- Intents this surface answers: audit, design, debug, measure.

## Grounding

- Research Report — Effective Documentation Patterns and Practices for DX, AX,
  and UX (Informed Skills research synthesis, 2026) — collects README,
  quickstart, example, reference, error, changelog, and search patterns.
- Improving API Usability (Myers and Stylos, 2016) — grounds examples as the
  primary developer learning surface.
- How to Design a Good API and Why It Matters (Bloch, 2006) — frames APIs and
  type surfaces as documentation.
- Stripe API Errors reference (Stripe) — provides the structured error-plus-doc
  link pattern.
- The Documentation System (Procida) — separates tutorials, how-to guides,
  reference, and explanation for developer docs.

## Good signals

- README opens with what this is, install, and a paste-runnable first example.
- The quickstart ends in a visible success state and does not branch into full
  reference.
- Reference covers every public method, endpoint, parameter, response, error,
  and version caveat.
- Examples are runnable, minimal, idiomatic per language, and tested against the
  current product.
- Changelogs and migration docs tell maintainers what broke, what to do, and by
  when.

## Common failures

- Badge-and-marketing front door — evaluators see status badges and slogans
  before they see the install or first result.
- Reference disguised as tutorial — beginners are forced through parameter
  exhaustiveness before they can succeed once.
- Tutorial disguised as reference — working developers must search narrative
  prose to find a field, flag, or return type.
- Snippet rot — inline examples omit imports, credentials, or error handling and
  are never executed in CI.
- Upgrade fog — release notes announce changes but do not name affected users,
  replacement APIs, codemods, or deprecation dates.

## Heuristics

- (audit, design) First-success ladder — above the fold: one-line purpose,
  prerequisites, install, minimal working example, expected output, and next
  link. Move badges and feature tours below that ladder.
- (audit, design) Mode split — quickstart teaches one golden path; how-to pages
  solve named tasks; reference answers lookup; explanation covers concepts.
- (audit, debug) Copy-paste proof — run the first example from a clean machine
  or container; every unstated prerequisite is a finding.
- (audit, design) Reference coverage map — compare public surface to docs; every
  method/endpoint/flag needs parameters, defaults, examples, errors, and version
  notes.
- (audit, design) Example ecosystem — inline snippets show local context;
  sample repos or sandboxes show complete apps. Do not ask one artifact to do
  both jobs.
- (debug) Search-query replay — reproduce the developer's likely search terms;
  if the right page ranks low or uses internal vocabulary, fix labels and
  synonyms before writing more prose.
- (measure) TTFHW metric — measure time from landing on docs to verified result,
  not page views. Segment by language and environment.
- (measure) Sample freshness gate — examples should build or execute in CI, or
  the docs must mark them illustrative rather than copy-pasteable.

## Quick diagnostic

- Does the first code block produce a useful result after credentials are
  filled? yes → inspect edge cases; no → fix first-success ladder.
- Can a maintainer find a parameter or error without reading tutorial prose?
  yes → reference is doing its job; no → split reference from learning content.
- Are examples tested against the current release? yes → inspect coverage; no →
  add CI or narrow the promise.
- Do support tickets quote exact docs text? yes → debug ambiguity/staleness; no
  → inspect findability.

## Cross-references

- `references/playbooks/foundations.md` — shared IA, versioning, and feedback
  loops.
- `references/playbooks/api-contracts.md` — schema descriptions, tool contracts,
  errors, retries, and examples-as-contract.
- the `design-for-agent-users` skill (ax-docs surface) — when developer docs are also
  consumed by agents.
- `references/playbooks/audience-conflicts.md` — when developer terminology and
  plain-language or agent-readable needs conflict.
