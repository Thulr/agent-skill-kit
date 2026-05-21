# UX Accessibility Heuristics Eval Cases

## Positive cases

- "Use ux-accessibility-heuristics." -> bare invocation; show use-case menu.
- "Our signup form has 60% drop-off." -> `form-review`; load forms + accessibility playbooks.
- "Audit our checkout page for WCAG 2.2 AA." -> `accessibility-audit`; state that this is not legal certification.
- "Users cannot find billing settings." -> `navigation-review`.
- "This failed payment message only says try again." -> `error-recovery`.

## Negative cases

- "Review my CLI help for DX." -> `dx-heuristics`.
- "Audit our SDK docs for developers." -> `dx-heuristics`.
- "Write unit tests for the signup form." -> general coding or `test-heuristics` if quality-focused.
- "Review AGENTS.md for agent readiness." -> `project-agentification`.

## Behavioral assertions

- Bare invocation loads only `references/use-case-registry.csv` and waits.
- Concrete invocation loads only the selected row's files.
- Accessibility output distinguishes likely WCAG failures from items needing
  manual or specialist confirmation.
- Findings include severity, impact, fix, verification, and grounding sources.
- For 7+ findings, any severity 3-4 finding, or save/track request, the skill
  saves both tracking artifacts and reports their paths.
