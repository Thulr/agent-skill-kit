---
name: example-minimal
description: >-
  Template skill demonstrating this repository layout. Copy or delete after
  adding real skills; run `npx skills init <name>` for a fresh starter.
license: MIT
metadata:
  internal: true
---

# Example minimal skill

This folder exists as the **template contract** for this repository: it carries the
minimum required artifacts (`SKILL.md`, `skill.json`, and `evals/*`) so contributors
can't accidentally template a new skill that bypasses gates.

It is marked `metadata.internal: true`, so it is hidden from `npx skills add . --list`
unless `INSTALL_INTERNAL_SKILLS=1` is set.

## When to use

Never in production installs. Use only when validating template/gate behavior.

## Steps

1. Copy this directory to `skills/my-real-skill/` and edit `SKILL.md`, or run `npx skills init my-real-skill` and move the result under `skills/`.
2. Delete `skills/example-minimal/` if you do not want a sample in the repository.
