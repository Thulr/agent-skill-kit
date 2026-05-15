# Docs Playbook

## Scope

Developer documentation: quickstart guides, reference docs, tutorials,
troubleshooting, and migration guides. Routes to `setup.md` for
install-specific friction, `errors.md` for error-message-searchable
troubleshooting overlap, and `migration.md` for upgrade guide patterns.

## Grounding

- **Daniele Procida — Diátaxis framework** — four orthogonal documentation
  modes (tutorials, how-to guides, reference, explanation) that serve
  different user needs and should never be mixed on one page.
- **Steve Krug — *Don't Make Me Think*** — users scan, not read; F-pattern
  scanning means the first words of headings and bullets carry most of the
  weight; minimize cognitive load by signposting next actions visually.

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
  endpoint has a reference entry. "See source for details" is a
  documentation gap.
- **Error-message-searchable troubleshooting** *(audit, design)* —
  troubleshooting pages are indexed by the exact error string the user
  sees, not organized by theoretical cause categories.
- **Tested examples** *(audit)* — every code example in docs is run in CI;
  stale snippets fail the build before they reach users.
- **Signposted scannability** *(design, audit)* — headings are meaningful
  (not "Overview"), paragraphs are short, and the next action is visually
  distinct. Pages pass a 30-second scan test.
- **Task-before-concept** *(design)* — task docs come first; concept and
  architecture docs are linked from tasks, not the other way around.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does the quickstart end with verifiable success output? | Users can't tell if it worked | Add expected terminal output |
| Are docs split by Diátaxis mode? | Tutorial, reference, explanation mixed | Restructure information architecture |
| Are code examples tested in CI? | Stale snippets accumulate | Add example test runner to CI |
| Can users search troubleshooting by error message text? | Cause-organized only | Re-index troubleshooting by error string |
| Is every public method or endpoint documented? | Reference gaps | Generate reference from source annotations |
| Are pages scannable in 30 seconds? | Wall-of-text syndrome | Add headings, bullets, and visual hierarchy |

## Cross-references

- → `setup.md` for install-specific documentation friction.
- → `errors.md` for troubleshooting-doc and error-message UX overlap.
- → `migration.md` for upgrade guide patterns.
