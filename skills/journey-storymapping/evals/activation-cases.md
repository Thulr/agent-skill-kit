# journey-storymapping Activation Cases

Saved at `skills/journey-storymapping/evals/activation-cases.md`. Single-layer skill (intents:
`map-journey`, `diagnose-experience`, `narrate-concept`).

## Positive

- "Map our onboarding as a story — where's the arc?" → routes to `map-journey`, emits `templates/story-map.md`.
- "Lay our signup flow onto a narrative arc with a clear climax." → routes to `map-journey`.
- "Our core experience feels flat; diagnose it using story structure." → routes to `diagnose-experience`.
- "Where do users emotionally drop in our activation story?" → routes to `diagnose-experience`.
- "Help me craft the concept story to pitch this product's vision to the team." → routes to `narrate-concept`, emits `templates/concept-story.md`.
- "Write our origin story — how a new user discovers and commits." → routes to `narrate-concept`.

## Negative

- "Audit our checkout for usability and accessibility problems." → use `ux-audit` instead — a heuristic evaluation of a built interface, not narrative experience design.
- "Write the launch blog post and conference talk narrative." → use `writing-design` instead — prose/talk craft, not structuring a product experience as a journey.
- "Should we build this feature? What's the opportunity and the riskiest assumption?" → use `product-discovery` instead — deciding what to build, not how the experience unfolds.

## Boundary / edge

- "Map our customer journey across touchpoints with emotions and KPIs." → activates for the story-arc lens, but a touchpoint/ops journey map with metrics leans toward `ux-audit` / general journey-mapping.
- "Help me tell our product's story." → activates only if it's the experience-as-story; if it's a written narrative or a talk, prefer `writing-design`.

## Notes

- Cover the dominant phrasings users try, not just the wording in `description`.
- One negative per neighbor: `ux-audit`, `writing-design`, `product-discovery`.
- Re-read after editing `trigger-evals.json` so the two artifacts agree.
