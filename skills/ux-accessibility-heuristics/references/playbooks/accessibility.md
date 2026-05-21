# Accessibility Playbook

## Scope

Use for WCAG-oriented reviews, keyboard access, focus order, screen-reader
semantics, contrast, target size, motion, error identification, and accessible
names. This is an expert triage baseline, not legal certification.

## Grounding

- WCAG 2.2: content should be perceivable, operable, understandable, and robust.
- W3C WAI guidance: WCAG is a shared standard; conformance still needs
  human judgment and assistive-technology checks.
- Inclusive design: accessibility is task success for people with real
  constraints, not a separate checklist after UX is done.

## Good signals

- All controls are keyboard reachable with visible focus.
- Semantic structure matches visual structure.
- Labels, instructions, errors, and status messages are programmatically tied
  to the controls they describe.
- Color is never the only signal; contrast is sufficient for text and UI.
- Motion, timing, and target size do not punish low-vision, motor, or cognitive
  constraints.

## Common failures

- Clickable divs without roles, states, or keyboard behavior.
- Focus is trapped, lost, hidden, or jumps unexpectedly after async updates.
- Error messages appear visually but are not associated with inputs.
- Placeholder text substitutes for persistent labels.
- Modal, toast, and route changes are invisible to assistive technology.

## Heuristics

- **Keyboard path exists** *(accessibility-audit, form-review)* - complete the core task without a mouse.
- **Focus is visible and ordered** *(accessibility-audit, navigation-review)* - focus follows task order and never disappears.
- **Semantic names and states** *(accessibility-audit)* - controls expose role, name, value, state, and relationships.
- **Error relationship** *(accessibility-audit, error-recovery)* - invalid fields expose error text, requirements, and recovery steps.
- **Contrast and non-color signal** *(accessibility-audit)* - text, icons, status, and validation survive low vision and color-blind use.
- **No checklist-only claim** *(accessibility-audit)* - separate likely WCAG failures from issues needing manual specialist confirmation.

## Quick diagnostic

Try the task with keyboard only, visible focus, zoom to 200%, reduced motion,
and a screen-reader semantics pass. Automated scanners are evidence, not proof.

## Cross-references

- Use `forms.md` for input labels, validation, and step flows.
- Use `navigation.md` for focus order across pages and menus.
- Use `error-recovery.md` for status messages and destructive actions.
