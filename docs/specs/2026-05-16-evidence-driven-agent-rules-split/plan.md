# Plan — execute the split

**Spec:** [spec.md](./spec.md)
**Sequencing:** vertical slices, not horizontal phases (per `docs/specs/README.md`).

## Pre-execution gate

Plan execution **blocks on reviewer answers** to spec.md §Open questions
Q1–Q6. Each open question maps to an irreversible decision in the
migration map below; resolving them after files move is more expensive
than resolving them now.

## Slices

Each slice is independently mergeable and leaves the repo in a working
state. `just check` passes after each.

### Slice 1 — shared-content scaffold (PR #12)

**Goal:** establish the `_shared/` directory and the lint pattern, with
no functional skill changes yet. Validates the chosen Q1 mechanic before
either skill depends on it.

- Create `skills/_shared/` (or whatever Q1 resolves to).
- Move `references/lenses.md` from `project-agentification` to
  `_shared/lenses.md` (single canonical source).
- Embed copy back into `project-agentification/references/lenses.md`
  (per Q1's recommended option (c)) **or** symlink (per option (a)) —
  pending Q1 answer.
- Add `scripts/check-shared-content.sh` invoked by `just check`: asserts
  embedded copies match canonical `_shared/` sources.
- Update `Justfile` to include the new check.
- Update `.github/workflows/ci.yml` if needed.
- Acceptance: `just check` green; no behavioral change to
  `project-agentification`.

### Slice 2 — empirical-warnings split (PR #13)

**Goal:** move shared warnings to `_shared/`, scope per-skill warnings
to their owning skills.

- Move W2/W3/W4/W5/W6/W7/W8/W9/W10 from
  `project-agentification/references/empirical-warnings.md` to
  `_shared/empirical-warnings.md` (pending Q3 answer).
- Leave W1 in `project-agentification` temporarily — Slice 4 moves it
  with the rest of the failure-driven content.
- Update every backlink in playbooks (search for `W1`–`W10` and
  `empirical-warnings.md#W` patterns).
- Acceptance: `just check` green; all warning citations resolve.

### Slice 3 — maturity rubric split (PR #14)

**Goal:** scope the rubric to what each audience can score against
(pending Q2 answer).

- Move Levels 4–5 content out of
  `project-agentification/references/core/maturity-rubric.md` into a
  draft file at `docs/specs/2026-05-16-evidence-driven-agent-rules-split/maturity-rubric-l4-l5.md`
  for Slice 4 to consume.
- Update `project-agentification`'s rubric to cap at Level 3 with a
  pointer to `evidence-driven-agent-rules` for Levels 4–5.
- Acceptance: `just check` green; `assess` intent on
  `project-agentification` no longer claims to score Levels 4–5.

### Slice 4 — new skill scaffold (PR #15)

**Goal:** stand up `evidence-driven-agent-rules` with the
reflection-log workflow + W1 + Levels 4–5 + Mündler citations.

- Create `skills/.experimental/evidence-driven-agent-rules/` with:
  - `SKILL.md` (frontmatter + bootstrap order + workflow steps for the
    evidence-driven scaffolding mode)
  - `skill.json` (provenance, inspired_by: Engineering Agents, Mündler
    et al., the cross-link to `project-agentification`)
  - `references/empirical-warnings.md` (W1 only; cross-links to
    `_shared/empirical-warnings.md` for the rest)
  - `references/core/maturity-rubric.md` (Levels 4–5; cross-links to
    `project-agentification` for Levels 1–3)
  - `references/playbooks/reflection-log.md` (new playbook for the
    sub-surface, lifted from `project-agentification`'s mentions)
  - `templates/artifacts/reflection-log/` (moved from
    `project-agentification`)
  - `evals/run-static-checks.sh`, `evals/trigger-evals.json`,
    `evals/activation-cases.md`
- The new skill's `scaffold` intent owns the ≥3 floor and the Stage 0/1/2
  bootstrap order.
- Acceptance: `npx skills add . --list` lists both skills; the new
  skill's static checks pass.

### Slice 5 — `project-agentification` reframe (PR #16)

**Goal:** strip the failure-driven gating from `project-agentification`;
update its scaffold to project-context-first.

- SKILL.md:
  - Delete §Bootstrap order section entirely.
  - Workflow step 4: rewrite — no longer "collect 3–5 observed failures
    or refuse"; instead "collect project knowledge (stack, layout,
    monorepo scope, build/test commands, top-level invariants)."
  - Reference map: remove `reflection-log` sub-surface entries; add a
    "see also: `evidence-driven-agent-rules`" line.
- `references/playbooks/instruction-surface.md`: scaffold heuristics no
  longer require "every section traces to a failure"; rationale shifts
  to content-quality / project-specificity.
- `references/playbooks/governance.md`: trim the reflection-log
  references (governance H4/H5 mentioning the log) to "see
  `evidence-driven-agent-rules` for the reflection-log workflow."
- `references/layer-router.csv`: remove the `reflection-log` sub-surface
  row if it has one.
- `templates/artifacts/instruction-surface/AGENTS.md` (the template
  this skill scaffolds for target repos):
  - Remove "every rule must cite a reflection-log entry" requirement.
  - Rule format reverts to `### Rule N — <title>` (no log-entry
    citation in heading).
  - §Reflection-log workflow section becomes a one-line "see also" if
    kept at all, or is deleted (decision per Q4).
- `templates/artifacts/reflection-log/` — delete (moved to new skill in
  Slice 4).
- `templates/artifacts/instruction-surface/README-agents-section.md`:
  remove the reflection-log pointer prose; replace with optional "if
  this repo has an evidence-driven workflow, see
  `evidence-driven-agent-rules`."
- `templates/scaffold-bundle.md`: remove the reflection-log rows.
- `evals/trigger-evals.json` + `evals/activation-cases.md`: prune queries
  that route to reflection-log scaffolding.
- Acceptance: `just check` green; scaffold intent no longer refuses on
  missing failures.

### Slice 6 — this repo's own surface (PR #17)

**Goal:** update this repo (which is a consumer of both skills) so its
cross-references point to the right skill.

- `AGENTS.md`: the §Reflection-log workflow section continues to point
  at `docs/reflection-log/` but its W1 citation now references
  `evidence-driven-agent-rules` instead of `project-agentification`.
- `README.md`: skills table adds `evidence-driven-agent-rules` row;
  description copy updated.
- `llms.txt` / `llms-full.txt`: add the new skill entry; update
  reflection-log description if needed.
- `docs/reflection-log/README.md`: its W1 footnote points at
  `evidence-driven-agent-rules`.
- `docs/reflection-log/<entries>.md`: entries that mention W1 update
  their citation paths. Use a script if there are many.
- `constitution.md`: §Architecture principles entry 3 (Evidence before
  scaffolding) updates its W1 citation.
- Acceptance: `grep -r 'project-agentification.*reflection-log\|reflection-log.*project-agentification'`
  returns no false coupling.

## Rollback

If a slice fails review or surfaces an unanticipated problem:

- **Slice 1 (shared-content scaffold):** revert; no skill behavior
  changed.
- **Slice 2 (warnings split):** revert; W references in playbooks
  re-resolve to the un-split file.
- **Slice 3 (rubric split):** revert; rubric reunifies under
  `project-agentification`.
- **Slice 4 (new skill scaffold):** if the skill scaffolds successfully
  but downstream feedback says it's wrong-shaped, iterate inside the
  skill without reverting the whole split.
- **Slice 5 (reframe):** the riskiest revert because it changes the
  scaffold contract. Keep Slice 5 as a single commit so it's revertable.
- **Slice 6 (this repo's surface):** small, easy to revert.

## Out of scope

- Clean-architecture skill overlap (flagged by maintainer as future
  consideration, but not in this spec's scope).
- Building a "core" directory for cross-skill shared content beyond what
  the two skills in scope need (the `_shared/` directory is a means, not
  an end — it grows only as new shared primitives surface).
- Changes to the `npx skills add` tool itself. If Q1 resolves to (b)
  (copy-at-install), that becomes a separate spec for the tool
  maintainer.
- Mündler-style benchmarking infrastructure inside this repo.
- Cross-skill schema for `inspired_by` cycles (e.g., what happens if
  skill A's `inspired_by` lists skill B); not a problem yet.

## Tracking

- Spec: this file.
- Open questions to resolve before execution: Q1–Q6 in `spec.md`.
- Reflection-log entry for this reframe: will be added under
  `docs/reflection-log/` once the split lands, documenting the layer
  mismatch that motivated it (separate from the recording-bar entry
  already there).
