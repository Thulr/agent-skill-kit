# Runbook: Change a Canonical Cross-Skill Schema

## When to use

Use this when changing any schema that is intended to be shared across skills
(for example, `evals/trigger-evals.json` or required fields in `skill.json`).

## Prerequisites

- Node.js available (to run `npx skills ...`)
- `jq` and `python3` available (used by existing static checks)
- `just` available

## Required environment variables

None.

## Expected duration

30–120 minutes, depending on how many skills are affected.

## Procedure

1. Update the documented contract:

   - Update the canonical schema description in `AGENTS.md` (keep it short; it is
     a table of contents, not a full spec).
   - If this is the second time a schema has drifted, consider promoting the
     contract to a single shared schema file under `schemas/` and validating
     every skill against it.

2. Migrate every skill in the same PR:

   - Update each skill's `evals/run-static-checks.sh` to validate the new shape.
   - Update every affected file (`trigger-evals.json`, etc.) in every skill.

3. Run gates:

   `just check`

4. Sanity-check installs:

   `npx skills add . --list`

## Rollback

Revert the schema change commit(s). If partial migrations landed, finish the
migration immediately rather than “rolling forward later”; drift is the failure
mode.

