---
name: example-minimal
description: >-
  Template contract for this repository: the minimum artifacts every skill must
  ship (SKILL.md, skill.json, evals/*) so static checks catch a skill templated
  from it that bypasses gates. Hidden from `npx skills add . --list` by
  `metadata.internal: true`. Do not delete.
license: MIT
metadata:
  internal: true
---

# Example minimal skill

This folder exists as the **template contract** for this repository: it carries the
minimum required artifacts (`SKILL.md`, `skill.json`, and `evals/*`) so contributors
can't accidentally template a new skill that bypasses gates.

**Produces:** nothing in production installs. New skills templated from this folder
**must** add their own `**Produces:**` callout here describing what the real skill
emits (primary artifact + any tracking files).

It is marked `metadata.internal: true`, so it is hidden from `npx skills add . --list`
unless `INSTALL_INTERNAL_SKILLS=1` is set.

## When to use

Never in production installs. Use only when validating template/gate behavior, or
as the source you copy when starting a new skill (see step 1 below).

## Steps

1. Copy this directory to `skills/my-real-skill/` and edit `SKILL.md` — rewrite the frontmatter `description` for the routing decision: intent triggers plus "Do NOT use for X — use `<sibling>`" anti-triggers (see `docs/skill-authoring-principles.md`) — or run `npx skills init my-real-skill` and move the result under `skills/`.
2. Do not delete `docs/templates/example-minimal/` — per AGENTS.md Rule 3, it is the template contract and must continue to exist so future skills can be templated from it. Living under `docs/` keeps it out of the install lanes.
