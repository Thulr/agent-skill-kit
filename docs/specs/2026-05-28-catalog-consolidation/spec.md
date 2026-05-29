# Spec — catalog consolidation: merge the review and research families

**Date:** 2026-05-28
**Status:** approved (maintainer chose options below on 2026-05-28)
**Triggered by:** maintainer request to evaluate the catalog and restructure it.

## Problem

A multi-agent profiling pass over all 12 published skills surfaced two
structural facts, both verified against the working tree:

1. **The review family ships one engine seven times.** Seven skills
   (`dx-heuristics`, `docs-experience-heuristics`,
   `perf-observability-heuristics`, `test-heuristics`,
   `ux-accessibility-heuristics`, `ui-design-craft`, `clean-architecture`)
   are the *same* method — `intent-router.csv → intents/<intent>.csv →
   playbooks/<surface>.md → core rubrics → lenses → modes →
   trackable-findings` — applied to seven domains. The shared machinery has
   silently drifted: 8 distinct `severity-rubric.md` hashes (15–37 lines)
   for one conceptually-identical 0–4 scale; 7 distinct
   `subagent-dispatch.md` copies; and the routing CSV header has already
   forked (`ui-design-craft` / `ux-accessibility-heuristics` use
   `intent,trigger_examples,detail_files,templates,notes`; the other six
   use `intent,name,when_to_use,registry_file,default_template`).
   `docs-experience-heuristics` carries **zero** symlinks into
   `skills/_shared/` — it re-copied even the already-shared pieces. This is
   the silent-drift class AGENTS.md Rule 2 exists to catch.

2. **The README routing table is the user-facing symptom.** Seven sibling
   skills with near-identical "Practical X review/design/debug"
   descriptions are inherently hard to disambiguate, which is why the
   README carries an 11-row "Which skill should I use?" table plus a
   five-clarifier "Ambiguous phrasings" section, and why six of seven
   descriptions spend their token budget naming siblings to push work away.

The same one-engine-many-surfaces shape exists in `topic-research` /
`opportunity-research` (both fan out by area and produce a report; they
differ only by decision-frame: open-ended report vs. go/no-go).

## Decisions

Reached with the maintainer on 2026-05-28.

- **Merge the review family** (7 → 1 `review-heuristics`). Domain becomes a
  third routing layer above the intent × surface layers the engine already
  has.
- **Merge the research family** (2 → 1 `research`), routed by decision-frame
  (`report` vs. `decide`). The FADR decision gate from `opportunity-research`
  is load-bearing and is preserved verbatim under the `decide` frame.
- **Clean break on install commands.** The repo is `0.0.1-alpha`; per-skill
  install commands for the merged skills are updated in the docs, no alias
  shims.
- **Consolidate the shared engine in `skills/_shared/`** and add a routing-CSV
  contract + static check, extending the Rule-2 schema pattern to CSV headers.
- **Do NOT split the agent-infra giants** (`project-agentification`,
  `evidence-driven-agent-rules`). The original restructuring proposal
  included splitting these on a "<800-word SKILL.md cap violation." That
  evidence does not hold: the word cap is enforced **per skill** in each
  `run-static-checks.sh`, and these skills deliberately set no cap
  (`project-agentification`, `evidence-driven-agent-rules`) or a raised one
  (`opportunity-research`: `< 1200`, currently 962). `just check` is green
  for all three. More importantly, splitting `project-agentification` (one
  engine, many surfaces) directly contradicts merging the review family
  (one engine, many surfaces) — opposite treatment of the same shape — and
  would regress its documented 90%-case (`assess × legibility`) into a
  multi-skill chore while re-duplicating its router/rubrics/lenses across
  children. They stay whole.

## Target catalog

Published, installable: `review-heuristics`, `research`,
`project-agentification`, `evidence-driven-agent-rules`, `loop-architect`.
Internal template: `example-minimal`. Repo-local: `informed-skill-curator`,
`informed-skill-reviewer`.

### `review-heuristics` layout

```
skills/review-heuristics/
  SKILL.md                      # domain router → per-domain intent/surface routing
  skill.json                    # union of the 7 skills' inspired_by (deduped)
  evals/{run-static-checks.sh,trigger-evals.json,activation-cases.md}
  references/
    domain-router.csv           # NEW: domain → references/<domain>/
    modes.md                    -> ../../_shared/modes.md
    trackable-findings.md       -> ../../_shared/trackable-findings.md
    routing-contract.md         -> ../../_shared/routing-contract.md  (from ①)
    <domain>/                   # dx, docs, perf, test, ux, ui-craft, architecture
      intent-router.csv  intents/*.csv  playbooks/*.md
      core/*  subagent-dispatch.md  starter-scenarios.csv ...
  templates/
    findings-ledger.md -> _shared ; workflow-state.json -> _shared ; ...
    <domain>/*.md               # per-domain intent output templates
```

Domain slugs: `dx` (dx-heuristics), `docs` (docs-experience-heuristics),
`perf` (perf-observability-heuristics), `test` (test-heuristics), `ux`
(ux-accessibility-heuristics), `ui-craft` (ui-design-craft), `architecture`
(clean-architecture).

### `research` layout

```
skills/research/
  SKILL.md                      # frame router → report | decide
  skill.json                    # union of topic + opportunity inspired_by
  evals/*
  references/
    frame-router.csv            # NEW: report → references/report/ ; decide → references/decide/
    modes.md -> ../../_shared/modes.md
    report/                     # from topic-research
    decide/                     # from opportunity-research (intent-router, intents, playbooks, core, FADR)
  templates/{report/,decide/}
```

## Acceptance criteria

1. `just check` is green after the change.
2. `npx skills add . --list` shows `review-heuristics`, `research`,
   `project-agentification`, `evidence-driven-agent-rules`, `loop-architect`
   (and not the 9 merged-away names).
3. `review-heuristics` routes all 7 former domains; every former playbook,
   intent CSV, rubric, and template is reachable under `references/<domain>/`
   or `templates/<domain>/`. No content is lost.
4. `research` routes `report` (former topic-research) and `decide` (former
   opportunity-research, FADR gate intact).
5. The 8 divergent severity rubrics and 7 divergent dispatch files now live
   once per surviving skill; no `references/<basename>.md` duplicates a
   top-level `_shared/*.md` as a regular file (`check-shared-content.sh`
   passes).
6. Routing CSVs across the catalog share a validated header contract
   (`scripts/check-routing-csv.sh`, wired into `just check` across all three
   install lanes per Rule 1).
7. README, AGENTS.md, `llms.txt`, `llms-full.txt`, and CODEOWNERS reflect the
   new surface; per-skill provenance (`inspired_by`) and finding-ID
   namespaces are preserved, never rewritten.
8. A reflection-log entry records the falsified-cap finding that killed the
   split, so the next person doesn't re-derive a split from the same bad
   premise.

## Out of scope

- Splitting `project-agentification` / `evidence-driven-agent-rules` (dropped,
  see Decisions).
- Changes to the `npx skills` tool.
- Re-grading activation accuracy with a live model (Stage 1.5 runner, future).
