---
name: journey-storymapping
description: Use to shape or fix a product experience as a story — map an experience as a narrative arc with the user cast as the protagonist (concept, origin, or usage story), diagnose a flat or broken experience by finding the missing beat (no clear goal, no inciting incident, anticlimax, or the gap where users drop out), or craft a concept or origin story to align a team or pitch the experience vision. Triggers on 'map our onboarding as a story', 'our experience feels flat — diagnose the arc', 'where do users drop in the story', 'help me tell the product's concept story', 'lay this flow onto a narrative arc'. Do NOT use to heuristically audit usability or accessibility of a built interface (use ux-audit), to write a narrative as prose, a memo, or a talk (use writing-design), or to decide what to build or frame the opportunity (use product-discovery).
license: MIT
---

# Journey Storymapping

Shaping and diagnosing product experiences with narrative structure — casting the user as
the protagonist and mapping how their experience unfolds as a story arc. Provenance and
grounding sources live in `skill.json`; this file is runtime routing only.

**Produces:** a story map (arc with beats) or a concept/origin story; the
`diagnose-experience` intent returns the broken-beat diagnosis inline.

## Core principle

**The user is the protagonist; the product is the helper.** A good experience reads like a
story — a character with a goal, an event that sets them in motion, rising stakes, and a
satisfying climax near the end. Mapping an experience onto that arc shows how it *feels* to
move through it and exactly where it stalls. Use story where the experience genuinely has an
arc; a habitual or nonlinear flow may not, and forcing one onto it misleads.

## Activation

- **Bare invocation** (`"use journey-storymapping"`, `"storymap our experience"`): load
  `references/intent-router.csv` and show the intent menu (map-journey / diagnose-experience /
  narrate-concept), then offer the mode choice. Wait. No file inspection, network calls, or writes.
- **Concrete invocation** with an intent inferable: skip to Workflow step 2.
- **Ambiguous concrete invocation**: ask one question to fix the intent.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Route to one of: `map-journey`,
   `diagnose-experience`, `narrate-concept`. Ambiguous → ask once.
2. **Load only that row.** Read the chosen row's `detail_files` (one playbook) and `templates`.
   Do not load the other playbooks.
3. **Cast the protagonist.** Name the user-protagonist, their goal, and which story type applies
   (concept = the value/why, origin = how they arrive and onboard, usage = the core loop).
4. **Apply the playbook.** Lay or test the beats of the arc; produce a concrete map, diagnosis,
   or story — not generic "tell a story" advice. Watch the playbook's named common failures.
5. **Emit output.** `map-journey` → `templates/story-map.md`. `narrate-concept` →
   `templates/concept-story.md`. `diagnose-experience` returns the broken-beat diagnosis inline.
6. **Hold the boundary.** Keep the user — not the product — as the hero. If the issue is a
   usability or accessibility defect in a built screen, that is a heuristic audit (`ux-audit`),
   not a story break; say so and route it.

## Modes

Guided Draft (default — propose, then refine), Autopilot (conservative assumptions; stop only
for missing inputs), Grill Me (one question at a time when the protagonist, goal, or story type
is unclear). Offer the mode at bare invocation; default to Guided Draft otherwise.

## Output requirements

Every output names the protagonist, their goal, and the story type, lays the experience on the
arc (exposition → inciting incident → rising action → crisis → climax → resolution), and marks
where the experience peaks and where it stalls. Diagnoses name the specific missing or weak beat,
not a vague "needs more delight."

## Reference map

- `references/intent-router.csv` — one-layer router (intent → playbook + templates).
- `references/playbooks/map-journey.md` — build a story-structured journey on the arc.
- `references/playbooks/diagnose-experience.md` — find the broken or missing beat.
- `references/playbooks/narrate-concept.md` — craft concept / origin stories to align or pitch.
- `templates/story-map.md` — `map-journey` output shape.
- `templates/concept-story.md` — `narrate-concept` output shape.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
