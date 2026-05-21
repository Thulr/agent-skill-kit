# Activation Cases

## Positive

- "Use ui-design-craft to make this dashboard look less generic." Activates,
  routes to `product-ui` plus `quality-review`, inspects the existing UI, and
  emits a concrete plan before edits.
- "Prototype this onboarding flow with a few tweakable variants." Activates,
  routes to `prototype`, loads host/tweak guidance, and maps variation axes.
- "Make a presentation deck from these notes." Activates, routes to `deck`,
  chooses a slide system, and asks only if audience or export target is unknown.
- "Author a small design system for this app." Activates, routes to
  `design-system`, and produces token/component/preview requirements.
- "Review this UI for AI slop." Activates, routes to `quality-review`, applies
  visual, task, and handoff lenses.
- "Add subtle animated depth to this hero." Activates, routes to
  `motion-scene`, checks reduced motion and intensity.
- "Package this prototype for handoff." Activates, routes to `host-handoff`,
  checks bundling, direct edit, export, and limitations.

## Negative

- "Run a formal WCAG audit of this checkout." Prefer
  `ux-accessibility-heuristics` unless the prompt also asks for visual redesign.
- "Review this API onboarding guide." Prefer `dx-heuristics`.
- "Refactor the repository architecture." Prefer `clean-architecture` or
  `project-agentification` depending on scope.
- "Write unit tests for this component." Prefer normal coding/test workflow,
  not this skill.

## Edge

- Bare "UI designer" invocation shows modes and use cases, then waits.
- If a design system is named but unavailable, ask for it or state the
  from-scratch fallback before inventing visuals.
- If the user asks to copy a third-party product's distinctive UI without
  evidence of ownership, refuse that copy and offer an original adjacent style.
- If host protocol files are not relevant to the target environment, skip them
  and document the portability assumption.
