# Candidate Skill Plan: journey-storymapping

Phase 3 artifact.

## Back-links

- Intake brief: `.agents/state/intake-briefs/journey-storymapping.md`
- Source dossier: `.agents/state/source-dossiers/journey-storymapping.md`

## Source

- *The User's Journey* (Donna Lichaw, 2016). Why now: the narrative-experience lens of the
  `discovery` family.

## Recommended Pack Decisions

- Pack tag(s): `discovery` (tags also: storymapping, user-journey, narrative, experience-design).
  Existing pack; extends the family.

## Draft Skill Candidates

```text
candidate:                  journey-storymapping
pack:                       discovery
shape:                      single-layer
depth:                      1
action:                     create
public_path:                skills/journey-storymapping/
dossier_ref:                journey-storymapping
audience_ref:               journey-storymapping
shape_decision:
  rubric_evidence:          Q1 = 3 distinct invocations (3–8 → single-layer; >2 so not flat). Q2 = 1 axis (narrative activity); no orthogonal 2nd axis. Q3 = each leaf 250–450 words. Q4 = shared arc vocabulary (protagonist, beats, climax, the three story types) → centralize via one router.
  promotion_path:           Promote only if a second axis appears — e.g. story-type (concept/origin/usage) × activity each needing distinct content, or a per-platform variant.
  axes:                     intent  (map-journey | diagnose-experience | narrate-concept)
anti_pattern_check:
  - one_dim_collapsed:      yes  (exactly 3 differentiated rows — meets the ≥3 floor)
  - registry_routes:        yes  (3 distinct playbooks; templates differ — diagnose-experience carries none)
  - cargo_culting:          yes  (single-layer on content; not flat because 3 invocations + shared rubric)
  - bloat_check:            yes  (SKILL.md <800; each playbook 250–450 < 1500)
  - depth_orthogonality:    N/A  (depth 1)
playbook_outline:
  - map-journey:
      heuristic_seeds:
        - Cast the user as the protagonist with a concrete goal; the product is the helper, not the hero.
        - Lay the chosen story type (concept / origin / usage) onto the arc — exposition, inciting incident, rising action, crisis, climax, resolution — beat by beat.
      common_failure_seeds:
        - Making the product the hero instead of the user.
        - A flat list of steps with no inciting incident, stakes, or climax.
  - diagnose-experience:
      heuristic_seeds:
        - Walk the existing experience against the arc and find the missing or weak beat (no clear goal, no inciting incident, anticlimax, dead cliffhanger).
        - Locate where users emotionally drop — the gap between beats — and name the specific missing beat.
      common_failure_seeds:
        - Confusing a usability nit with a story break (route usability to ux-audit).
        - Over-dramatizing a habitual/nonlinear flow that has no real arc.
  - narrate-concept:
      heuristic_seeds:
        - Write the concept story (what the product makes possible) or origin story (how they arrive) as a short arc to align a team or pitch the vision.
        - Anchor the narrative in the protagonist's want and the change they experience, not a feature list.
      common_failure_seeds:
        - A feature tour dressed up as a story.
        - A narrative with no stakes or transformation, so nothing lands.
registry_sketch:
  layers:
    - layer: intent-router
      rows:
        - row: map-journey
          loads: references/playbooks/map-journey.md ; templates/story-map.md
          notes: Build a story-structured journey. Carries the story-map template.
        - row: diagnose-experience
          loads: references/playbooks/diagnose-experience.md
          notes: Diagnose a broken/flat experience via the arc. No template (diagnosis in place).
        - row: narrate-concept
          loads: references/playbooks/narrate-concept.md ; templates/concept-story.md
          notes: Craft concept/origin story to align or pitch. Carries the concept-story template.
activation_case_seeds:
  positive:
    - prompt: "Map our onboarding as a story — where's the arc?" -> route: map-journey
    - prompt: "Our core experience feels flat; diagnose it using story structure." -> route: diagnose-experience
    - prompt: "Help me craft the concept story to pitch this product's vision to the team." -> route: narrate-concept
    - prompt: "Lay our signup flow onto a narrative arc with a clear climax." -> route: map-journey
  negative:
    - prompt: "Audit our checkout for usability and accessibility problems." -> use ux-audit because that's a heuristic evaluation of a built interface, not narrative experience design.
    - prompt: "Write the launch blog post / conference talk narrative." -> use writing-design because that's prose/talk craft, not structuring a product experience as a journey.
    - prompt: "Should we build this feature? What's the opportunity?" -> use product-discovery because that decides what to build, not how the experience unfolds.
  edge:
    - prompt: "Map our customer journey across touchpoints with emotions and KPIs." -> activates for the story-arc lens, but a touchpoint/ops journey map with metrics leans toward ux-audit / general journey-mapping.
    - prompt: "Help me tell our product's story." -> activates only if it's the experience-as-story; if it's a written narrative or talk, prefer writing-design.
grounding_map:
  - source: The User's Journey, year: 2016
    playbooks: [map-journey, diagnose-experience, narrate-concept]
    contribution: Storymapping — user as protagonist; concept/origin/usage story types; the narrative arc used to design, diagnose, and pitch product experiences.
reason:                     Distinct narrative-experience lens completing the discovery family; well-bounded single source; fenced against ux-audit and writing-design.
inspired_by:                [the-users-journey]
```

## Anti-pattern self-check (rubric walk)

- [x] No CSV layer has fewer than 3 differentiated rows. (exactly 3 — meets floor)
- [x] No registry layer whose rows all load the same files. (3 distinct playbooks; 2 templates + 1 none)
- [x] SKILL.md projected <800; no playbook projected >1500. (250–450 each)
- [x] Depth ≥2 orthogonality — N/A.
- [x] Every `grounding_map.playbooks` non-empty. (the single source → all 3 intents)
- [x] Every negative names a sibling skill. (ux-audit, writing-design, product-discovery)
- [x] Every playbook has ≥2 heuristic seeds and ≥1 common-failure seed.

## Review Handoff (filled at end of Phase 5)

- Draft paths: `skills/journey-storymapping/` (SKILL.md, skill.json, references/intent-router.csv, 3 playbooks, 2 templates, evals/*); README regenerated.
- Known risks: (1) single source (one book) — `inspired_by` has one entry (schema-valid); grounding leans entirely on it. (2) Boundary with `ux-audit` (journeys/flows) and `writing-design` (narrative) relies on description fencing + negative cases; the "customer journey map with KPIs" edge case is the most likely mis-fire. (3) Anti-over-dramatization heuristic added so the skill doesn't force an arc onto nonlinear flows.
- Suggested reviewer focus: fencing vs `ux-audit`/`writing-design`; that no book diagrams/exercises were reproduced; whether 3 intents is the right granularity.
- Validation report: `.agents/state/validation-reports/journey-storymapping-phase5.md` (validator exit 0; static check pass; `just check` exit 0).
