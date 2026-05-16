# Runbook: Add a Skill

## When to use

Use this when creating a new installable skill under `skills/` or
`skills/.experimental/`.

## Prerequisites

- Node.js available (to run `npx skills ...`)
- `just` available

## Required environment variables

None.

## Expected duration

30–90 minutes, depending on how much reference material the skill includes.

## Procedure

1. Create a starter:

   - Preferred: `npx skills init <skill-name>`
   - Alternative: copy `skills/example-minimal/` (template contract) and edit
     from there.

2. Move/ensure the directory lives under one lane:

   - `skills/<skill-name>/` (default)
   - `skills/.experimental/<skill-name>/` (caveat-heavy / WIP, but installable)

3. Ensure required artifacts exist (per `AGENTS.md`):

   - `SKILL.md` with YAML frontmatter (`name`, `description`, `license`)
   - `skill.json` with `status` (`draft|reviewed|published`), `maintainers`
     (GitHub handles), and non-empty `inspired_by`
   - `evals/run-static-checks.sh`
   - `evals/trigger-evals.json` (canonical schema)
   - `evals/activation-cases.md`

4. Update any repo-level indexes that should mention the new skill:

   - `README.md` (Skills section)
   - `llms.txt` / `llms-full.txt` if agents need to discover new docs quickly

5. Run gates:

   `just check`

## Rollback

Revert the commit(s) that added the new skill directory and any index updates.

