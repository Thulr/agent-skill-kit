# <Skill Title>

Frontmatter (in the generated `SKILL.md`):

```yaml
---
name: <skill-slug>
description: Use when <one-sentence trigger>. Also use when <secondary trigger>. Do not use when <boundary>.
license: MIT
---
```

For a flat skill, **the entire skill is the `SKILL.md` body**. Use this
skeleton to draft the body before scaffolding so every required
section exists from the start.

## Overview / core principle

3–5 lines on the single procedure or technique the skill embodies.
This is what activates in the agent's mind when the skill triggers.

## When to use

- Specific situation 1
- Specific situation 2
- Specific situation 3
- (When **not** to use — point to a neighbor skill if applicable)

## The procedure

Either numbered steps or a single named pattern. Keep operational:
the agent should be able to execute, not just understand.

1. Step 1 — what to do, with the observable signal that you're done
2. Step 2 —
3. Step 3 —

## Output requirements

What the skill must produce. If it's a critique / report / decision,
say what shape it takes. If there's no artifact, say so.

## Grounding

A short bullet list mapping each load-bearing claim to its
`skill.json.inspired_by` source. Example:

- "Surface defaults are the dominant lever" — Norman 1988
- "Five-minute fix rule for friction" — <source>

Keep this concise: detail belongs in the dossier, attribution belongs
in `skill.json`. Two or three named sources is plenty for a flat skill.

## Common mistakes / red flags

What goes wrong when this skill is applied carelessly. Include the
anti-pattern the user is most likely to fall into.

- Red flag 1
- Red flag 2

## Word budget

Target <500 words across the whole SKILL.md. If you push past 800,
the skill should escalate to single-layer (see `references/shapes/single-layer.md`).
