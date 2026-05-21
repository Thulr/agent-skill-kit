# Forms Playbook

## Scope

Use for sign-up, checkout, onboarding, settings, support, survey, and data-entry
flows where users provide information or make choices.

## Grounding

- Form design research: ask only what the task needs; make labels, examples,
  constraints, and confirmation explicit.
- Norman: many form errors are slips caused by bad mapping, weak feedback, or
  mode confusion.
- WCAG: labels, instructions, error identification, and target behavior affect
  accessibility as well as usability.

## Good signals

- The form asks for the minimum necessary information in a sensible order.
- Labels persist and examples clarify format without becoming the only label.
- Validation happens when it helps, not after avoidable rework.
- Errors preserve entered data and tell users exactly what to change.
- Required, optional, disabled, and read-only states are unambiguous.

## Common failures

- Placeholder-only labels disappear during entry.
- Error messages are generic, late, or detached from the field.
- Field order follows database schema instead of user reasoning.
- Users cannot tell what will happen after submit.
- The flow blocks progress for optional or irrelevant details.

## Heuristics

- **Ask less** *(form-review)* - remove fields that are not required for the current decision.
- **Persistent labels** *(form-review, accessibility-audit)* - every input has a visible and programmatically associated label.
- **Helpful examples** *(form-review)* - examples clarify format without replacing instructions.
- **Inline recovery** *(form-review, error-recovery)* - validation names the bad value, expected format, and next action.
- **Submission confidence** *(form-review)* - the user knows cost, timing, reversibility, and confirmation before submit.

## Quick diagnostic

For each field, ask: "Why is this needed now, how does the user know the right
answer, and what happens if they get it wrong?"

## Cross-references

- Use `accessibility.md` for labels, focus, and error association.
- Use `error-recovery.md` for failed payments, destructive submits, and undo.
