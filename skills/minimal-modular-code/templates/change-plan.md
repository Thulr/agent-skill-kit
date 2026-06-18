# Change Plan — <what you are changing>

**Target persona:** <from references/core/personas.md> (usually Persona A)
**Surfaces in scope:** <minimalism | legibility | boundaries | parallel-readiness>
**Date:** <YYYY-MM-DD>

A pre-flight plan for keeping an in-progress change minimal. Fill it before writing much code;
it is a thinking tool, not a deliverable to track.

## What already exists

<What you searched for and found before writing. The function, module, or pattern you will
reuse instead of rebuilding. If you genuinely found nothing reusable, say so and how you
checked.>

## The minimal change

- **Reuse:** <existing code this change builds on>
- **Add:** <the smallest new code the present requirement forces>
- **Remove:** <what this change lets you delete — answer even if the answer is "nothing", to
  force the subtractive option to surface>

## Seams I am deliberately NOT adding

<The abstractions, parameters, config hooks, or layers you considered and are leaving out
because no present need forces them (YAGNI). Naming them is the point — it documents the
restraint.>

## Blast radius

<Which modules and contracts this change touches. If it touches a shared/owned contract, note
that it is a coordinate-or-serialize change, not a free parallel one.>

## Routing

- **Mechanical** (format, types, lint, tests): handled by <gate / will run locally>.
- **Judgment call to flag to a human:** <migration, permission, new dependency, reliability
  choice, or boundary change — or "none">.

## Grounding sources applied

- <skill.json inspired_by entry> — <how it shaped this plan>
