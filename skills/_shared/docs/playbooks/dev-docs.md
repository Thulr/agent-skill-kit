# Developer Docs Playbook

## Scope

Developer documentation as a reading surface: quickstart guides, reference
docs, tutorials, troubleshooting, and the doc-site information architecture.
Use this when the primary audience is a developer reading docs to build,
debug, or upgrade.

- In: time-to-first-success, quickstarts, reference completeness, tutorials,
  troubleshooting, doc-site IA, search labels and findability, developer doc
  telemetry.
- Out: install/API/error friction experienced while *running* the product
  (the `dx-audit` / `dx-design` skills), end-user product help
  (`ux-help.md`), schema/tool description quality (`api-contracts.md`), and
  front-door/release surfaces with their own playbooks here (`readme.md`,
  `changelog.md`, `examples.md`, `contributor.md`).
- Intents this surface answers: audit, debug, design, measure.

## Grounding

- **Daniele Procida — Diátaxis framework / The Documentation System** — four
  orthogonal documentation modes (tutorials, how-to guides, reference,
  explanation) that serve different user needs and should never be mixed on
  one page.
- **Steve Krug — *Don't Make Me Think*** — users scan, not read; F-pattern
  scanning means the first words of headings and bullets carry most of the
  weight; minimize cognitive load by signposting next actions visually.
- Research Report — Effective Documentation Patterns and Practices for DX,
  AX, and UX (Informed Skills research synthesis, 2026) — collects README,
  quickstart, example, reference, error, changelog, and search patterns.
- Improving API Usability (Myers and Stylos, 2016) — grounds examples as the
  primary developer learning surface.
- How to Design a Good API and Why It Matters (Bloch, 2006) — frames APIs
  and type surfaces as documentation.

## Good signals

- One quickstart that ends with a visible, verifiable "it worked" output
  — not "see the reference docs for what to try next."
- Reference docs cover every public method or endpoint; mechanically
  generated from source where possible so they stay in sync.
- Tutorials follow a single thread — no branch points or "alternatively"
  detours that force the reader to choose.
- Troubleshooting docs are indexed by the exact error message text the
  user sees in their terminal or browser, not by theoretical root cause.
- Diátaxis modes are visible in the information architecture: tutorials,
  how-to guides, reference, and explanation live in distinct sections.
- Pages are F-pattern friendly: meaningful headings, short paragraphs,
  code in code blocks, and the next action visually distinct.
- Every code example runs in CI; stale snippets fail the build.

## Common failures

- Tutorial-only docs with no reference: users finish the tutorial, then
  stall when the tutorial's scope runs out.
- Reference-only docs with no tutorial: users have to already know what
  they're looking for before the docs are useful.
- Quickstart that bottoms out at "see the reference docs" — users can't
  verify the tool works at all before going deeper.
- Troubleshooting that explains root causes without saying what to do
  next — diagnosis without a fix is frustration.
- Concept and task content mixed on one page — users searching for
  "how do I do X" wade through architecture before they find the steps.
- Stale code snippets that fail on first paste, breaking trust
  immediately.
- Docs that front-load architecture before the task — users want to
  accomplish something first and understand it second.

## Heuristics

- **Diátaxis-mode purity** *(design, audit)* — each page is one mode:
  tutorial, how-to, reference, or explanation. Mixing modes on one page
  means neither goal is well served.
- **Verifiable-output quickstart** *(design, audit)* — the quickstart ends
  with a visible "it worked" signal the user can check. Bad: ends at
  "you're all set." Good: shows expected terminal output.
- **Per-method reference completeness** *(audit)* — every public method or
  endpoint has a reference entry covering parameters, defaults, examples,
  errors, and version notes. "See source for details" is a documentation gap.
- **Error-message-searchable troubleshooting** *(audit, design)* —
  troubleshooting pages are indexed by the exact error string the user
  sees, not organized by theoretical cause categories.
- **Copy-paste proof** *(audit, debug)* — run the first example from a clean
  machine or container; every unstated prerequisite is a finding. Every code
  example in docs runs in CI; stale snippets fail the build before they
  reach users.
- **Example ecosystem** *(audit, design)* — inline snippets show local
  context; sample repos or sandboxes show complete apps. Do not ask one
  artifact to do both jobs (see `examples.md`).
- **Signposted scannability** *(design, audit)* — headings are meaningful
  (not "Overview"), paragraphs are short, and the next action is visually
  distinct. Pages pass a 30-second scan test.
- **Task-before-concept** *(design)* — task docs come first; concept and
  architecture docs are linked from tasks, not the other way around.
- **Copy-button on code blocks** *(design, audit)* — every code block in the
  docs has a one-click copy affordance; the developer never has to
  hand-select the text to paste-and-run.
- **Version selector** *(design, audit)* — when the docs cover more than one
  released version, a visible selector switches between them and persists
  across navigation; users on an older version are not silently served the
  latest docs.
- **Broken-link CI** *(audit)* — internal links and external references are
  exercised in CI; broken links fail the build before they reach users.
- **Retrieval-friendly headings** *(design)* — headings are specific
  ("Configuring retry backoff" beats "Configuration") so chunks retrieved
  by search or by agents make sense on their own. Wide nav with shallow
  pages beats deep pages with everything dumped in.
- **Search-query replay** *(debug)* — reproduce the developer's likely
  search terms; if the right page ranks low or uses internal vocabulary,
  fix labels and synonyms before writing more prose.
- **TTFHW metric** *(measure)* — measure time from landing on docs to a
  verified result, not page views. Segment by language and environment.
- **Sample freshness gate** *(measure)* — examples should build or execute
  in CI, or the docs must mark them illustrative rather than
  copy-pasteable.
- **Edit-on-GitHub footer** *(design, audit)* — every page links to its
  source for direct contribution; small fixes flow back as PRs without the
  contributor learning the docs build first.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does the quickstart end with verifiable success output? | Users can't tell if it worked | Add expected terminal output |
| Are docs split by Diátaxis mode? | Tutorial, reference, explanation mixed | Restructure information architecture |
| Are code examples tested in CI? | Stale snippets accumulate | Add example test runner to CI |
| Can users search troubleshooting by error message text? | Cause-organized only | Re-index troubleshooting by error string |
| Is every public method or endpoint documented? | Reference gaps | Generate reference from source annotations |
| Are pages scannable in 30 seconds? | Wall-of-text syndrome | Add headings, bullets, and visual hierarchy |
| Does a likely search query land on the right page? | Findability gap | Fix labels and synonyms before writing more prose |

## Cross-references

- → `readme.md` for the front-door README that funnels evaluators into the
  docs site.
- → `examples.md` for the runnable samples the docs link out to.
- → `changelog.md` for release notes and upgrade communication.
- → `contributor.md` for contributor onboarding documentation.
- → `foundations.md` for shared IA, versioning, and feedback loops.
- → `api-contracts.md` for schema descriptions, tool contracts, errors,
  retries, and examples-as-contract.
- → `audience-conflicts.md` for when developer terminology and
  plain-language or agent-readable needs conflict.
- → the `dx-audit` / `dx-design` skills for install, error-message, and
  upgrade friction experienced while running the product (their `setup`,
  `errors`, and `migration` playbooks).
- → the `agent-docs` skill for retrieval-friendly structuring optimized for
  AI agents.
