# Contract Drift Review

Use this reference when the review target is a skill or shared workflow whose
behavior is supposed to be load-bearing for downstream agents. The goal is to
find mismatches between what the skill promises, what it loads, what it emits,
and what CI actually prevents from regressing.

## Evidence To Collect

- **Runtime contract:** `SKILL.md` activation, workflow steps, side-effect
  rules, output requirements, and reference map.
- **Routing contract:** `references/use-case-registry.csv`, intent/activity
  CSVs, router `default_template` columns, and any special meta-values such as
  `all`, `auto`, `tracking`, or `closeout`.
- **Artifact contract:** templates named by the workflow, required saved-file
  paths, fallback paths, workflow-state shape, ledger status taxonomy, and
  load-bearing section markers.
- **Validation contract:** `evals/run-static-checks.sh`, activation cases,
  trigger evals, repo-level scripts, Justfile entries, and CI workflow steps.
- **Shared-content contract:** symlinks into `skills/_shared/`, canonical
  basename mapping, relative-link portability, and all three install lanes:
  `skills/*`, `skills/.experimental/*`, `.agents/skills/*`.

## Drift Checks

1. **Workflow path coverage.** For every branch accepted by `SKILL.md`, confirm
   downstream steps load the needed rows/files, choose a real template, and
   say what to do for special values like `all` or `closeout`.
2. **Template resolution.** Template names in dispatch docs and synthesis steps
   must be real filenames or come from a router column that static checks
   validate.
3. **Registry-derived lists.** Any hardcoded count or item list that mirrors a
   CSV must either iterate the CSV or be explicitly marked non-exhaustive.
4. **Required artifact gates.** Every required `SKILL.md`, `skill.json`,
   eval file, template, reference, saved ledger/state file, and fallback path
   must have a presence or pattern gate.
5. **Status taxonomy parity.** Statuses in shared workflow docs must appear in
   ledger summaries, closeout rules, and workflow-state templates.
6. **Side-effect boundaries.** Default writes must be limited to the declared
   tracking artifacts; roadmaps, GitHub issues, external closures, and
   non-tracking project edits require explicit confirmation.
7. **CI parity.** A gate added to `just check` must also run in the required CI
   path, unless the PR explicitly documents why local-only enforcement is
   intentional.
8. **Symlink integrity.** Shared references must be relative symlinks to the
   matching basename under `skills/_shared/`; absolute links and basename
   mismatches are release bugs.

## Finding Shape

Use stable IDs by area:

- `SR-CONTRACT-###` for workflow/template/registry drift.
- `SR-GATE-###` for missing static or CI enforcement.
- `SR-SHARED-###` for shared-content and symlink drift.
- `SR-STATE-###` for ledger, workflow-state, status, or closeout drift.

Each finding should name the promised behavior, the artifact that contradicts
or fails to enforce it, the smallest gate or text change that closes the gap,
and the regression case that would have caught it.
