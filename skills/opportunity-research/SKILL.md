---
name: opportunity-research
description: Use when validating a named product, business, market, or feature opportunity and turning research into a go/no-go, pivot, or next-test decision (F/A/D/R memo). Covers 14 areas including market, customer, competitive, domain, technical, data, operational, financial, legal, channel, GTM, stakeholder, risk, and trend. Triggers on requests to validate an idea, decide whether to build or enter a market, size a market, investigate customer pain, map competitors, assess feasibility, unit economics, or legal risk, build a risk register, scope opportunity research, or produce a decision memo. Fans out subagents by area and persona. Do not use for open-ended topic research with no decision attached ("research X for me," primer, literature review — use `topic-research`), ideating candidates, red-teaming proposals or plans, critiquing research instruments/personas, comparing fixed options (use `tradeoff-analysis`), or code/DX/UX/test reviews.
license: MIT
---

# Opportunity Research

Two-level routed skill (intent × research-area) for validating a named
opportunity. Provenance lives in `skill.json`; this file is runtime
routing only.

**Produces:** intent-specific artifact — `scope-plan.md` /
`investigation-brief.md` / `cross-area-brief.md` / `fadr-memo.md` — plus
one of 14 area artifacts (e.g., `market-sizing.md`,
`competitor-map.md`, `risk-register.md`). Tracked work also emits
`opportunity-research-findings-ledger-<date>-<slug>.md` and
`opportunity-research-workflow-state-<date>-<slug>.json`.

## Core principle

**Every research branch must end in a decision, not a note.** A
branch that produces "knowns + interesting reading" without naming the
Facts, Assumptions, Decisions, and Risks (`references/core/fadr-framework.md`)
is organized procrastination. The skill exists to enforce that gate.

## Activation

- **Bare invocation** (`"opportunity research"`, `"validate this idea"`,
  `"start"`): load `references/starter-scenarios.csv` and
  `references/intent-router.csv`, show the intent menu with the named
  starter scenarios on top, offer the mode choice. Wait. No file
  inspection, no network calls, no writes.
- **Concrete invocation with intent and surface inferable**: skip to
  step 3 of the workflow.
- **Concrete invocation with ambiguous scope**: ask one blocker
  question identifying intent or surface; do not fan out sub-agents
  first.
- **Object missing** (`"research this"` with no `this`): ask for the
  one-line opportunity statement before any routing. Fanning out
  without scope produces 14 disconnected dumps — the named failure
  mode in the source.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Match the
   prompt to one of: `scope`, `investigate`, `synthesize`, `decide`.
   Ambiguous → ask once.
2. **Pick surface(s).** Load the intent's CSV from
   `references/intents/<intent>.csv`. Match the prompt to one or more
   surfaces, or `all` (scope / investigate only) for multi-surface
   fan-out — see `references/subagent-dispatch.md`. Ambiguous → ask
   once with the CSV menu.
3. **Load grounded context.** Load only the files listed in the chosen
   CSV row: the surface playbook from `references/playbooks/<surface>.md`
   plus the `core_refs` listed. Do not load other playbooks. Skip this
   step when surface = `all` — each spawned surface agent loads only
   its own playbook in step 5.
4. **Identify the target persona** from `references/core/personas.md`
   (founder / operator / investor / skeptic). For `investigate`,
   default to all four lenses in parallel; for `scope` / `decide`,
   default to founder + skeptic; for `synthesize`, the synthesizer
   collapses lenses already produced.
5. **Spawn sub-agents in parallel (default for `investigate` and for
   `scope` with surface = `all`).** Per-surface fan-out: one sub-agent
   per CSV row, each loading only its own playbook + artifact template.
   Per-persona fan-out (single surface, `investigate`): one sub-agent
   per lens, all four reading the same playbook + artifact template
   but writing distinct perspectives. See `references/subagent-dispatch.md`.
   Fall back to sequential lens-switching only if the host has no
   delegation primitive.
6. **Apply the playbook.** Use the heuristics in the loaded
   `references/playbooks/<surface>.md` tagged for the active intent.
   For `investigate`, fill the area artifact template with cited
   findings. For `scope`, produce a stage-aware shortlist of areas.
   For `synthesize`, consolidate area artifacts into the cross-area
   brief. For `decide`, fold each area's content into the F/A/D/R
   sections per `references/core/fadr-framework.md`.
7. **Apply severity and confidence** from
   `references/core/severity-rubric.md` (0–4 for risks) and
   `references/core/confidence-rubric.md` (H/M/L on every load-bearing
   claim). Auto-promote any **L** on a load-bearing claim to an
   assumption + test in the F/A/D/R fold.
8. **Emit output.** Scope → `templates/scope-plan.md`. Investigate →
   `templates/investigation-brief.md` plus the area's artifact under
   `templates/artifacts/<area>.md`. Synthesize → `templates/cross-area-brief.md`.
   Decide → `templates/fadr-memo.md`.
9. **Create, resume, or close tracking state.** For investigate /
   synthesize / decide outputs with 5+ area artifacts, any severity
   3–4 finding, or a save/track/closeout request, load
   `references/trackable-findings.md`. Write both artifacts now at
   `docs/audits/opportunity-research-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and `docs/audits/opportunity-research-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
   Fall back to `audit-artifacts/opportunity-research-{findings-ledger|workflow-state}-<YYYY-MM-DD>-<scope-slug>.{md|json}`
   if `docs/audits/` is unwritable. Report both paths; keep roadmaps,
   issues, and non-tracking edits opt-in.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/core/modes.md`](./references/core/modes.md). Offer the
mode at bare invocation; default to Guided Draft on concrete
invocations.

## Output requirements

Every output names the target persona, the playbook(s) applied, the
intent-specific load-bearing section (shortlist / artifact / cross-area
brief / F-A-D-R), the next falsifiable test (a one-week experiment
that closes the highest-leverage assumption — research without a next
test is the named failure mode), and the grounding sources from
`skill.json.inspired_by`.

## Subagent dispatch

**Default for `investigate` and for `scope` with surface = `all`;**
preferred for `synthesize` (one sub-agent per area artifact being
consolidated); optional for `decide`; skip tiny deterministic queries.
Spawn either per-surface fan-out or per-persona fan-out
(founder / operator / investor / skeptic) per
`references/subagent-dispatch.md`.

## Reference map

- `references/intent-router.csv` — level-1 router (intent).
- `references/intents/<intent>.csv` — level-2 router (surface) per intent.
- `references/playbooks/<surface>.md` — surface-specific playbooks (14
  area + 2 intent-pseudo).
- `references/subagent-dispatch.md` — per-surface + per-persona dispatch.
- `references/trackable-findings.md` — ledger, workflow-state, closeout.
- `references/starter-scenarios.csv` — worked examples for bare invocation.
- `references/core/{severity,confidence}-rubric.md` — shared scales.
- `references/core/fadr-framework.md` — Facts / Assumptions / Decisions / Risks.
- `references/core/personas.md` — founder / operator / investor / skeptic.
- `references/core/decision-gates.md` — go / no-go / pivot + kill criteria.
- `references/core/modes.md` — Guided Draft / Autopilot / Grill Me.
- `templates/{scope-plan,investigation-brief,cross-area-brief,fadr-memo}.md` — intent outputs.
- `templates/artifacts/*.md` — 14 area artifacts (one per surface).
- `templates/{findings-ledger.md,workflow-state.json}` — tracking artifacts.
- `evals/{activation-cases.md,run-static-checks.sh,trigger-evals.json}` — gates.
- `skill.json` — provenance, grounding sources, version, status.
