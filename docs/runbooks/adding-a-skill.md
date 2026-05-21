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
   - Alternative: copy `skills/example-minimal/` (template contract) and edit
     from there.

2. Move/ensure the directory lives under one lane:

   - `skills/<skill-name>/` for product work
   - `skills/.experimental/<skill-name>/` is reserved and should remain empty
     unless a future release explicitly reopens experimental distribution

3. Ensure required artifacts exist (per `AGENTS.md`):

   - `SKILL.md` with YAML frontmatter (`name`, `description`, `license`)
   - `skill.json` with `status: "published"`, `maintainers` (GitHub
     handles), and non-empty `inspired_by`
   - `evals/run-static-checks.sh`
   - `evals/trigger-evals.json` (canonical schema)
   - `evals/activation-cases.md`

4. Keep maturity at the repo-release level:

   - Use repository prerelease tags such as `0.0.1-alpha` for catalog-level
     caveats.
   - Do not ship installable public skills with `status: "draft"`.

5. Update any repo-level indexes that should mention the new skill:

   - `README.md` (Skills section)
   - `llms.txt` / `llms-full.txt` if agents need to discover new docs quickly

6. Run gates:

   `just check`

## Rollback

Revert the commit(s) that added the new skill directory and any index updates.
