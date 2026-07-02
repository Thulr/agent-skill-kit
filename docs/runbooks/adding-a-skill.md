# Runbook: Add a Skill

## When to use

Use this when creating a new installable skill under `skills/`. The
`skills/.experimental/` lane remains reserved for future caveat-heavy work, but
current product skills live in `skills/<name>/`.

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
   - Alternative: copy `docs/templates/example-minimal/` (template contract) and edit
     from there.

2. Move/ensure the directory lives under `skills/<skill-name>/` (see §When to
   use for the reserved `.experimental/` lane).

3. Write the content against
   [`docs/skill-authoring-principles.md`](../skill-authoring-principles.md):
   description written for the routing decision (triggers + anti-triggers
   naming sibling skills), must-not-miss invariants inlined in `SKILL.md`
   (never only behind a router row), gotchas and opinions rather than
   pasted external docs, explicit stop conditions + iteration caps for any
   looping workflow.

4. Ensure required artifacts exist (per `AGENTS.md`):

   - `SKILL.md` with YAML frontmatter (`name`, `description`, `license`)
   - `skill.json` with `status: "published"`, `maintainers` (GitHub
     handles), and optionally `inspired_by` (encouraged for
     literature-derived skills; may be absent or empty)
   - `evals/run-static-checks.sh`
   - `evals/trigger-evals.json` (canonical schema)
   - `evals/activation-cases.md`

5. Keep maturity at the repo-release level:

   - Use repository prerelease tags such as `0.0.1-alpha` for catalog-level
     caveats.
   - Do not ship installable public skills with `status: "draft"`.

6. Update any repo-level indexes that should mention the new skill:

   - `skill.json` `metadata` catalog fields (`family`, `function`,
     `catalog_summary` — required on every published skill; `just check`
     fails without them), plus a routing-matrix row in `catalog/catalog.json`
     if the skill should appear in §Pick a skill; then run
     `python3 scripts/build-catalog.py --write` (regenerates the README
     §Pick a skill block and `CATALOG.md` — never hand-edit them)
   - `llms.txt` / `llms-full.txt` if agents need to discover new docs quickly

7. Run gates:

   `just check`

## Rollback

Revert the commit(s) that added the new skill directory and any index updates.
