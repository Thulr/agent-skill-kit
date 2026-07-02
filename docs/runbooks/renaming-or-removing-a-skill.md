# Runbook: Rename or Remove a Skill

## When to use

Use this when renaming an installable skill (`skills/<old>` → `skills/<new>`) or
removing one. Both change the published install surface, so they are release
artifacts: every reference across the catalog must move with the skill, and the
change must be recorded for downstream installers whose `--skill <old>` command
will stop resolving.

## Prerequisites

- `just` and `git` available; `gh` for the PR.
- A clear new name (for renames). Names should state what the skill *does*; see
  the `dx`/`ux` skill names for the function-first convention.

## Required environment variables

None.

## Expected duration

30–60 minutes (a rename touches many cross-references; the sweep is the bulk).

## Procedure — rename `<old>` → `<new>`

1. `git mv skills/<old> skills/<new>` (preserves history).
2. **Sweep the hyphenated identifier** `<old>` → `<new>` across **live** files
   only — `skills/`, `catalog/catalog.json`, `llms-full.txt`, `AGENTS.md`,
   `docs/adr/`, `docs/runbooks/`, `skills/_shared/`, `.agents/skills/`,
   `.claude/skills/`, `scripts/` — then run
   `python3 scripts/build-catalog.py --write` (regenerates the README
   §Pick a skill block and `CATALOG.md`; never hand-edit those).
   **Do not** rewrite dated historical records
   (`docs/reflection-log/[0-9]*.md`, prior
   dated `docs/specs/`, `.agents/state/`) — they are point-in-time records and
   rewriting them falsifies history.
3. The sweep updates, inside `skills/<new>/`: `SKILL.md` `name:`, `skill.json`
   `name`, `evals/run-static-checks.sh` (`SKILL_NAME` + name assertions +
   `<old>-findings-ledger-`/`-workflow-state-` **ledger filename prefixes**), and
   `evals/trigger-evals.json` `skill`. Confirm the description still leads with
   what the skill does.
4. **Watch identifier-vs-concept.** A hyphenated token (`design-for-agent-users`) is
   the *skill id* and should change; a spaced/Title phrase (`agent experience
   (AX)`) may be a *discipline concept* that should stay. Review prose hits, do
   not blanket-replace the spaced form.
5. Record it in [`CHANGELOG.md`](../../CHANGELOG.md): a `Changed` entry naming
   the rename and the dropped `--skill <old>` install command.
6. If `<old>` is named in an ADR's decision, add a one-line rename note to that
   ADR — do not rewrite the decision narrative.
7. `just check` (includes the doc-link gate, which catches orphaned links from
   the rename) → green. Open a PR; merge once the `static-checks` CI check is
   green (no approving review required — single-maintainer ruleset; see
   AGENTS.md §Ownership and review).

## Procedure — remove `<old>`

1. `git rm -r skills/<old>`.
2. Remove the skill's routing-matrix row (and its family entry, if it was the
   family's last skill — empty families fail validation) from
   `catalog/catalog.json`, run `python3 scripts/build-catalog.py --write`
   (regenerates the README §Pick a skill block and `CATALOG.md` — never
   hand-edit them), then remove remaining cross-references: `llms-full.txt`,
   `AGENTS.md`, other skills' "use `<old>`" pointers, and `skills/_shared/`
   mentions. `.github/CODEOWNERS` is glob-based — no change.
3. Record a `Removed` entry in `CHANGELOG.md` with the dropped `--skill <old>`.
4. If the removal is structural (e.g. a consolidation/split), supersede the
   relevant ADR with a new one that links back — do not delete the old ADR.
5. `just check` green; PR; merge.

## Verify

- `bash scripts/list-installable-skills.sh` (or `npx skills add . --list`) shows
  the new/remaining set and no `<old>`.
- `python3 scripts/check-doc-links.py` passes (no orphaned relative links).
- `git grep -n '<old>'` returns only intentional historical records.

## Rollback

Renames/removals are plain `git` history — revert the merge commit (or
`git mv`/`git restore` the dir back) and re-run `just check`. Restore the
`CHANGELOG.md` entry's state to match.
