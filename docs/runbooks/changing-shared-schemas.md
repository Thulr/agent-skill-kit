# Runbook: Change a Canonical Cross-Skill Schema

## When to use

Use this when changing any schema that is intended to be shared across skills
(for example, `evals/trigger-evals.json` or required fields in `skill.json`).

## Prerequisites

- Node.js available (to run `npx skills ...`)
- `jq`, `python3`, and `python3-jsonschema` available locally
  (Debian/Ubuntu: `apt-get install python3-jsonschema`; macOS: `pip install --user --break-system-packages jsonschema`)
- `just` available

## Required environment variables

None.

## Expected duration

10–30 minutes (most of which is reviewing the affected skills, not editing).

## Procedure

The canonical schemas live in [`schemas/`](../../schemas/) as JSON Schema files.
Every skill's `run-static-checks.sh` validates against them via
[`scripts/validate-against-schema.py`](../../scripts/validate-against-schema.py),
so most schema changes only require editing the schema file itself.

1. Edit the schema file under `schemas/`:

   - `schemas/skill.schema.json` for `skill.json`.
   - `schemas/trigger-evals.schema.json` for `evals/trigger-evals.json`.

   If the change tightens an existing constraint (new required field, stricter
   `enum`, narrower `pattern`), every existing skill's affected file must be
   migrated in the same PR — drift is the failure mode (AGENTS.md Rule 2).

2. If the human-readable summary in `AGENTS.md` referenced the changed field,
   update it. Keep `AGENTS.md` short; the schema file is authoritative.

3. Run gates:

   `just check`

4. If you changed `schemas/trigger-evals.schema.json`, verify the valid and
   invalid fixture expectations directly:

   `python3 scripts/test-trigger-evals-schema.py`

5. Sanity-check installs:

   `bash scripts/list-installable-skills.sh`

## Rollback

Revert the schema change commit(s). If partial migrations landed, finish the
migration immediately rather than "rolling forward later"; drift is the failure
mode.
