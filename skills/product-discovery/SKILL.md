---
name: product-discovery
description: Use to decide what to build and why before building it — reframe a feature/output request as a measurable outcome and diagnose feature-factory risk, map an opportunity solution tree from a desired outcome down to opportunities and assumption tests, define the customer's job-to-be-done and rank underserved needs, surface and test the riskiest desirability/viability/feasibility assumptions behind a bet, or scope an MVP toward product-market fit. Triggers on 'reframe this roadmap around outcomes', 'build an opportunity solution tree', 'what job are customers hiring us for', 'what is our riskiest assumption and how do we test it', 'scope an MVP', 'are we a feature factory'. Do NOT use to run or synthesize the customer interviews that feed discovery (use customer-interviewing), to do sourced desk/market validation ending in a go/no-go memo (use research), or to audit a built interface (use ux-audit).
license: MIT
---

# Product Discovery

Deciding *what to build and why* before building it — framing outcomes, mapping
opportunities, defining the customer's job, testing the riskiest assumptions, and
scoping an MVP. Provenance and grounding sources live in `skill.json`; this file is
runtime routing only.

**Produces:** an opportunity solution tree, a job map with desired-outcome statements,
an assumption test plan, or an MVP definition; the `frame-outcomes` intent reframes the
request in place.

## Core principle

**Reduce the risk of building the wrong thing; do not pretend to remove it.** Discovery
turns a request into a measurable outcome, the opportunities under it, the customer's
job, the assumptions a bet rests on, and the smallest test of value. These frameworks
are scaffolding for judgment — they cut the odds of shipping on faith, but they cannot
manufacture strategy or substitute for real customer evidence.

## Activation

- **Bare invocation** (`"use product-discovery"`, `"help with product discovery"`): load
  `references/intent-router.csv` and show the intent menu (frame-outcomes /
  map-opportunities / define-jobs / test-assumptions / scope-mvp), then offer the mode
  choice. Wait. No file inspection, network calls, or writes.
- **Concrete invocation** with an intent inferable: skip to Workflow step 2.
- **Ambiguous concrete invocation**: ask one question to fix the intent.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Route to one of: `frame-outcomes`,
   `map-opportunities`, `define-jobs`, `test-assumptions`, `scope-mvp`. Ambiguous → ask once.
2. **Load only that row.** Read the chosen row's `detail_files` (one playbook) and
   `templates`. Do not load the other playbooks.
3. **Anchor on the outcome.** Name the desired outcome (the business/customer result) and
   the segment. Most intents are weaker without one — if it is missing, establish it first.
4. **Apply the playbook.** Use its heuristics; produce a concrete artifact or reframing,
   not a lecture. Watch the playbook's named common failures.
5. **Emit output.** `map-opportunities` → `templates/opportunity-solution-tree.md`.
   `define-jobs` → `templates/jtbd-job-map.md`. `test-assumptions` →
   `templates/assumption-test-plan.md`. `scope-mvp` → `templates/mvp-definition.md`.
   `frame-outcomes` returns the reframed outcome and risk read inline.
6. **Hold two boundaries.** Separate evidence from assumption — never call a survey or a
   single interview "validation" when the assumption needed a behavioral test. And avoid
   outcome dogma: some work (compliance, platform, table-stakes) is legitimately
   output-shaped; say so rather than shaming it.

## Modes

Guided Draft (default — propose, then refine), Autopilot (conservative assumptions; stop
only for missing inputs), Grill Me (one question at a time when the outcome or segment is
unclear). Offer the mode at bare invocation; default to Guided Draft otherwise.

## Output requirements

Every output names the desired outcome and the segment, traces solutions back to an
opportunity or job (not to an opinion), and marks each load-bearing claim as evidence or
assumption. Assumption work ranks by risk and least evidence first. MVP work states the
value hypothesis the MVP tests and the signal that would show fit.

## Reference map

- `references/intent-router.csv` — one-layer router (intent → playbook + templates).
- `references/playbooks/frame-outcomes.md` — outcome-over-output, four product risks, build-trap diagnosis.
- `references/playbooks/map-opportunities.md` — opportunity solution tree.
- `references/playbooks/define-jobs.md` — jobs-to-be-done, job map, desired-outcome statements.
- `references/playbooks/test-assumptions.md` — assumption mapping and experiment selection.
- `references/playbooks/scope-mvp.md` — lean product process, MVP, product-market fit.
- `templates/` — opportunity-solution-tree, jtbd-job-map, assumption-test-plan, mvp-definition.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
