# Core Workflow

## Operating Rules

Run UI work as a visible design loop, not a hidden reveal. The workflow has
seven stages:

1. **Understand.** Re-read the user request. Name output format, audience,
   timebox, and whether the brief asks for a polish pass, variations, brand
   matching, or a new artifact.
2. **Explore.** Inspect every relevant file, screenshot, token file, component,
   existing view, image, deck, or design-system guide. Prefer source files over
   screenshots when both exist.
3. **Ask.** Use one focused round only when the answer changes the direction:
   audience, format, design-system binding, novelty appetite, variation count,
   tweak surface, or missing assets.
4. **Plan.** Produce a short todo list and a stated design direction. This lets
   the user correct assumptions before implementation cost piles up.
5. **Show early.** Surface a running artifact once the skeleton communicates
   hierarchy and direction, even before final copy and polish.
6. **Build.** Work in order: layout skeleton, type and color, real content,
   component states, then polish and motion.
7. **Verify.** Check that the artifact loads, the requested thing is visibly
   present, states work, text does not overflow, and system tokens are honored.

## Grounding Checklist

Extract these before designing:

- Color palette and semantic roles.
- Type family, scale, weight, and casing rules.
- Spacing, radius, and density scale.
- Component idioms for buttons, rows, forms, cards, nav, modals, and tables.
- Existing product vocabulary and voice samples.
- Real content or honest placeholders.

If no system exists, state that the work is from-scratch and choose explicit
commitments for material, type, accent, radius, and density.

## Re-Entry Rules

Go back to Understand when the user says the direction is wrong, not merely
when they request a small tweak. Do not salvage a misread direction with local
patches; ask one focused question, restate the new understanding, and re-plan.

## Verification Floor

**For code-backed artifacts, you MUST visually inspect the rendered page — reading
source code is not sufficient.** Load `references/browser-verification.md` and use the session's browser tools
(example names there — map to whatever the session exposes).

For non-code artifacts, verify dimensions, export format, editability, and that
the deliverable can be opened by the intended recipient.
