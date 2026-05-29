# Opportunity frame — workflow

Two-level routed (intent × research-area) validation of a named opportunity.

**Produces:** intent-specific artifact — `scope-plan.md` /
`investigation-brief.md` / `cross-area-brief.md` / `fadr-memo.md` — plus one of
14 area artifacts (e.g., `market-sizing.md`, `competitor-map.md`,
`risk-register.md`), all under [`../../templates/opportunity/`](../../templates/opportunity/).
Tracked work also emits `research-findings-ledger-<date>-<slug>.md` and
`research-workflow-state-<date>-<slug>.json`.

## Core principle

**Every research branch must end in a decision, not a note.** A branch that
produces "knowns + interesting reading" without naming the Facts, Assumptions,
Decisions, and Risks ([`core/fadr-framework.md`](./core/fadr-framework.md)) is
organized procrastination. This frame exists to enforce that gate.

## Activation nuance

If the opportunity statement is missing (`"research this"` with no `this`), ask
for the one-line opportunity statement before any routing. Fanning out without
scope produces 14 disconnected dumps — the named failure mode in the source.

## Workflow

1. **Pick intent.** Load [`intent-router.csv`](./intent-router.csv). Match the
   prompt to one of: `scope`, `investigate`, `synthesize`, `decide`. Ambiguous
   → ask once.
2. **Pick surface(s).** Load the intent's CSV from `intents/<intent>.csv`.
   Match the prompt to one or more surfaces, or `all` (scope / investigate
   only) for multi-surface fan-out — see
   [`subagent-dispatch.md`](./subagent-dispatch.md). Ambiguous → ask once with
   the CSV menu.
3. **Load grounded context.** Load only the files listed in the chosen CSV row:
   the surface playbook from `playbooks/<surface>.md` plus the `core_refs`
   listed. Do not load other playbooks. Skip this step when surface = `all` —
   each spawned surface agent loads only its own playbook in step 5.
4. **Identify the target persona** from [`core/personas.md`](./core/personas.md)
   (founder / operator / investor / skeptic). For `investigate`, default to all
   four lenses in parallel; for `scope` / `decide`, default to founder +
   skeptic; for `synthesize`, the synthesizer collapses lenses already produced.
5. **Spawn sub-agents in parallel (default for `investigate` and for `scope`
   with surface = `all`).** Per-surface fan-out: one sub-agent per CSV row, each
   loading only its own playbook + artifact template. Per-persona fan-out
   (single surface, `investigate`): one sub-agent per lens, all four reading the
   same playbook + artifact template but writing distinct perspectives. See
   [`subagent-dispatch.md`](./subagent-dispatch.md). Fall back to sequential
   lens-switching only if the host has no delegation primitive.
6. **Apply the playbook.** Use the heuristics in the loaded
   `playbooks/<surface>.md` tagged for the active intent. For `investigate`,
   fill the area artifact template with cited findings. For `scope`, produce a
   stage-aware shortlist of areas. For `synthesize`, consolidate area artifacts
   into the cross-area brief. For `decide`, fold each area's content into the
   F/A/D/R sections per [`core/fadr-framework.md`](./core/fadr-framework.md).
7. **Apply severity and confidence** from
   [`core/severity-rubric.md`](./core/severity-rubric.md) (0–4 for risks) and
   [`core/confidence-rubric.md`](./core/confidence-rubric.md) (H/M/L on every
   load-bearing claim). Auto-promote any **L** on a load-bearing claim to an
   assumption + test in the F/A/D/R fold.
8. **Emit output.** Scope → `../../templates/opportunity/scope-plan.md`.
   Investigate → `../../templates/opportunity/investigation-brief.md` plus the
   area's artifact under `../../templates/opportunity/artifacts/<area>.md`.
   Synthesize → `../../templates/opportunity/cross-area-brief.md`. Decide →
   `../../templates/opportunity/fadr-memo.md`.
9. **Create, resume, or close tracking state.** For investigate / synthesize /
   decide outputs with 5+ area artifacts, any severity 3–4 finding, or a
   save/track/closeout request, load
   [`trackable-findings.md`](./trackable-findings.md) and follow its ledger +
   workflow-state contract verbatim — including its stable `OR-<surface>-NNN`
   finding-ID namespace and its `docs/audits/` paths (with the
   `audit-artifacts/` fallback). Report both paths; keep roadmaps, issues, and
   non-tracking edits opt-in.

## Output requirements

Every output names the target persona, the playbook(s) applied, the
intent-specific load-bearing section (shortlist / artifact / cross-area brief /
F-A-D-R), the next falsifiable test (a one-week experiment that closes the
highest-leverage assumption — research without a next test is the named failure
mode), and the grounding sources from `skill.json.inspired_by`.

## Subagent dispatch

**Default for `investigate` and for `scope` with surface = `all`;** preferred
for `synthesize` (one sub-agent per area artifact being consolidated); optional
for `decide`; skip tiny deterministic queries. Spawn either per-surface fan-out
or per-persona fan-out (founder / operator / investor / skeptic) per
[`subagent-dispatch.md`](./subagent-dispatch.md).

## Reference map

- [`intent-router.csv`](./intent-router.csv) — level-1 router (intent).
- `intents/<intent>.csv` — level-2 router (surface) per intent.
- `playbooks/<surface>.md` — surface-specific playbooks (14 area + 2 intent-pseudo).
- [`subagent-dispatch.md`](./subagent-dispatch.md) — per-surface + per-persona dispatch.
- [`trackable-findings.md`](./trackable-findings.md) — ledger, workflow-state, closeout.
- [`starter-scenarios.csv`](./starter-scenarios.csv) — worked examples for bare invocation.
- `core/{severity,confidence}-rubric.md` — shared scales.
- [`core/fadr-framework.md`](./core/fadr-framework.md) — Facts / Assumptions / Decisions / Risks.
- [`core/personas.md`](./core/personas.md) — founder / operator / investor / skeptic.
- [`core/decision-gates.md`](./core/decision-gates.md) — go / no-go / pivot + kill criteria.
- [`core/modes.md`](./core/modes.md) — Guided Draft / Autopilot / Grill Me.
- `../../templates/opportunity/{scope-plan,investigation-brief,cross-area-brief,fadr-memo}.md` — intent outputs.
- `../../templates/opportunity/artifacts/*.md` — 14 area artifacts (one per surface).
