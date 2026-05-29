# End-User Help Playbook

## Scope

Covers documentation inside and around a product for end users: labels,
microcopy, contextual help, onboarding, empty states, tooltips, help centers,
plain-language errors, accessibility of help content, and support deflection.
Use when the person reading is trying to learn or recover inside the product,
not integrate an API.

- In: help-in-the-moment, onboarding guidance, empty-state teaching, tooltips,
  walkthroughs, help-center IA/search, plain language, accessible help media,
  article feedback, and support-ticket loops.
- Out: visual redesign without documentation/help concerns (use a UI craft
  skill) and field-by-field accessibility audits of the product itself (use a UX
  accessibility skill).
- Intents this surface answers: audit, design, debug, measure.

## Grounding

- Research Report — Effective Documentation Patterns and Practices for DX, AX,
  and UX (Informed Skills research synthesis, 2026) — summarizes UX help,
  onboarding, microcopy, error, and feedback patterns.
- Help and Documentation (Nielsen Norman Group) — grounds contextual help and
  search/browse help behavior.
- Web Content Accessibility Guidelines 2.2 (World Wide Web Consortium, 2023) —
  sets requirements for focus, target size, media alternatives, and consistent
  help placement.
- Information Architecture: For the Web and Beyond (Rosenfeld, Morville, and
  Arango, 2015) — grounds help-center organization and labeling.
- The Documentation System (Procida) — maps end-user help into learning,
  task, reference, and explanation modes.

## Good signals

- Essential instructions are visible in the task flow, not hidden in a help
  destination.
- Empty states explain status, teach the concept, and offer the first action.
- Error copy says what happened, what to do next, and preserves user work.
- Help center supports both search-first urgent users and browse-first learners.
- Help articles and media are accessible: headings, captions, transcripts,
  keyboard paths, focus, contrast, and descriptive links.

## Common failures

- Tooltip dependency — critical information is hidden behind hover, unavailable
  to touch/keyboard users and invisible to agents.
- Modal-carousel teaching — users click through passive onboarding slides before
  performing a real task, then forget the instruction.
- Empty blankness — the product shows an empty table or dashboard without
  explaining whether the state is new, filtered, failed, or permission-bound.
- Blame-language errors — copy says invalid, illegal, or failed without naming
  recovery in the user's terms.
- Deflection theater — article ratings are tracked, but no one joins them to
  tickets or turns gaps into product/help changes.

## Heuristics

- (audit, design) Moment-of-need placement — put the first layer of help where
  the decision happens: labels, hints, empty states, inline validation, or
  contextual sidebars before external articles.
- (audit, design) Hidden-help test — if completing the task requires a tooltip,
  move the instruction onto the page or add an accessible persistent affordance.
- (audit, design) Empty-state triple — every empty state should state status,
  teach what belongs here, and provide a direct path to the first useful action.
- (audit, debug) Recovery copy shape — describe what happened in user language,
  name the next step, preserve work, and avoid blame.
- (design, debug) Walkthrough does real work — guided onboarding should help the
  user complete one real task, not consume a generic tour.
- (audit, measure) Help-center gap loop — review zero-result searches, low-rated
  articles, and tickets opened after article views as one backlog, not separate
  dashboards.
- (measure) Activation tie-in — if an article appears repeatedly before first
  key action, consider moving the content into product help.
- (audit, design) Accessible help media — screenshots need meaningful alt text;
  videos need captions and transcripts; interactive demos need keyboard paths.

## Quick diagnostic

- If the help article vanished, could the user still complete the core task?
  yes → article can stay supplemental; no → promote help into the product flow.
- Does the empty state have a primary next action? yes → verify it is correct;
  no → design first-action guidance.
- Are users opening tickets after reading the same article? yes → debug the
  article/task mismatch; no → inspect top zero-result searches.
- Is essential copy hidden in hover-only UI? yes → escalate as accessibility and
  AX risk; no → inspect clarity.

## Cross-references

- `references/docs/playbooks/foundations.md` — shared IA, accessibility, and feedback
  loops.
- `references/docs/playbooks/audience-conflicts.md` — when helpful human UI hides
  load-bearing text from agents.
- `references/docs/playbooks/dx-docs.md` — developer docs; do not route end-user help
  through developer-facing patterns.
- `references/docs/core/personas.md` — end-user recovery and exploratory personas.
