# product-discovery Activation Cases

Saved at `skills/product-discovery/evals/activation-cases.md`. Single-layer skill (intents:
`frame-outcomes`, `map-opportunities`, `define-jobs`, `test-assumptions`, `scope-mvp`).

## Positive

- "We keep shipping features but nothing moves — reframe this roadmap around outcomes." → routes to `frame-outcomes`.
- "Are we a feature factory? Help me turn these outputs into outcomes." → routes to `frame-outcomes`.
- "Help me build an opportunity solution tree for our activation outcome." → routes to `map-opportunities`, emits `templates/opportunity-solution-tree.md`.
- "What job are customers hiring our product for, and which needs are underserved?" → routes to `define-jobs`, emits `templates/jtbd-job-map.md`.
- "What's the riskiest assumption behind this bet and how do I test it cheaply?" → routes to `test-assumptions`, emits `templates/assumption-test-plan.md`.
- "Scope an MVP that actually tests whether people want this." → routes to `scope-mvp`, emits `templates/mvp-definition.md`.

## Negative

- "Validate the market size and give me a go/no-go on this opportunity." → use `research` instead — sourced desk validation to an F/A/D/R memo, not the team's own discovery reasoning.
- "Help me write and run the actual customer interview for this." → use `customer-interviewing` instead — live conversation craft, not opportunity/assumption framing.
- "Audit our checkout flow for usability problems." → use `ux-audit` instead — evaluating a built interface, not deciding what to build.
- "Make our dashboard look modern — pick a color system and component library." → use `ui-design` instead — visual UI craft, not product discovery.

## Boundary / edge

- "Turn our discovery into a roadmap we can commit to." → activates for the outcome/opportunity framing, but release sequencing is general PM, not this skill.
- "Is this a good idea?" → activates only if reframed into a desired outcome plus the assumptions to test; otherwise too vague to route.

## Notes

- Cover the dominant phrasings users try, not just the wording in `description`.
- One negative per neighbor: `research`, `customer-interviewing`, `ux-audit` (plus `ui-design`).
- Re-read after editing `trigger-evals.json` so the two artifacts agree.
