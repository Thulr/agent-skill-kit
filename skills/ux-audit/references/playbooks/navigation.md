# Navigation Playbook

## Scope

Use for information architecture, menus, tabs, breadcrumbs, page hierarchy,
settings organization, dashboard orientation, and "users cannot find X"
problems.

## Grounding

- Nielsen: consistency, recognition, user control, and match to the real world
  are central navigation heuristics.
- Krug: users scan pages and follow scent; navigation has to orient users
  without requiring explanation.
- Accessibility guidance: navigation structure and focus order must be exposed
  semantically, not only visually.

## Good signals

- Users know where they are, what level they are in, and how to get back.
- Labels group by user goals, not internal ownership or implementation.
- Search, filters, tabs, and menus preserve state in predictable ways.
- Current page, selected tab, expanded section, and unavailable destinations
  are visible and accessible.
- Repeated navigation patterns behave consistently across the product.

## Common failures

- Multiple competing nav systems with unclear hierarchy.
- Labels use team jargon or feature names users do not know.
- Users lose context after filtering, sorting, modal actions, or route changes.
- Breadcrumbs are visual only or duplicate rather than clarify structure.
- Empty categories hide why content is missing.

## Heuristics

- **Location is visible** *(navigation-review)* - the current place and parent context are clear.
- **Goal-based labels** *(navigation-review, usability-audit)* - menu text reflects user tasks and objects.
- **Consistent controls** *(navigation-review)* - tabs, filters, and menus do not change meaning across screens.
- **State survives movement** *(navigation-review)* - sorting, filters, drafts, and selections persist or reset with clear feedback.
- **Accessible structure** *(navigation-review, accessibility-audit)* - headings, landmarks, tab state, and current page are exposed semantically.

## Quick diagnostic

Ask a user to find a target without search. Track where they hesitate, which
label they choose, and what made them think that path was right.

## Cross-references

- Use `usability.md` for page-level action clarity.
- Use `accessibility.md` for focus and semantic state.
