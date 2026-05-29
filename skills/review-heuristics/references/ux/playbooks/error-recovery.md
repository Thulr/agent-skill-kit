# Error Recovery Playbook

## Scope

Use for validation errors, failed payments, unavailable services, destructive
actions, confirmation dialogs, undo, account recovery, and support handoff.

## Grounding

- Norman: distinguish slips from mistakes; prevent likely slips and support
  recovery when mistakes happen.
- Nielsen: error prevention and recognition/recovery are core usability
  heuristics.
- WCAG: errors need identification, instructions, programmatic association, and
  accessible status updates.

## Good signals

- The message says what happened, why it matters, and what to do next.
- Recovery preserves user work and offers a safe retry or alternative.
- Destructive actions reveal consequence, scope, and reversibility.
- Status changes are announced visually and programmatically.
- Support escalation includes enough context to avoid making the user repeat
  everything.

## Common failures

- "Something went wrong" without cause, scope, or next action.
- Error text appears far from the relevant input or control.
- Retrying can duplicate charges, requests, or destructive actions.
- Confirmation dialogs ask "Are you sure?" without naming the consequence.
- Users lose drafts, carts, uploads, or form entries after failure.

## Heuristics

- **Specific next action** *(error-recovery)* - every error includes a concrete recovery path.
- **Work is preserved** *(error-recovery, form-review)* - failures do not wipe user input or progress.
- **Consequence before commitment** *(error-recovery)* - destructive actions name object, scope, and reversibility.
- **Retry is safe** *(error-recovery)* - retries avoid duplicate side effects or warn when they cannot.
- **Accessible status** *(error-recovery, accessibility-audit)* - status and error changes are exposed to assistive technology.

## Quick diagnostic

Force the likely failure. If the user cannot answer "what happened, what is
safe to try, and what data is still preserved," the recovery design is weak.

## Cross-references

- Use `forms.md` for field-level validation.
- Use `accessibility.md` for live regions, focus movement, and error
  association.
- Use `docs-experience-heuristics` when error copy is part of help-center,
  API-contract, or agent-readable documentation strategy.
