---
name: agent-test
description: "Use for AGENT TEST — designing the measurement an AI agent or skill is judged by. DO — write evals, judges, trajectory tests, benchmarks, activation evals. REVIEW — audit eval suite trustworthiness. DESIGN — shape failure-mode-first eval suites. Triggers: 'design our agent evals', 'is our LLM judge trustworthy', 'are trajectory tests real'"
license: MIT
---

# Agent Test

Designing the measurement an **AI agent or skill is judged by** — evals, LLM-as-judges,
trajectory tests, held-out benchmarks, and activation evals. The agent-actor analog of human
test design. Provenance lives in `skill.json`; this file is runtime routing only.

**Produces:** a `change-plan.md` (DO), an `audit-report.md` plus a findings-ledger +
workflow-state when tracked (REVIEW), or a `design-doc.md` / `refactor-runbook.md` /
`explanation.md` (DESIGN).

## Boundaries

Do NOT use to operate or watch the loop these evals feed (use agent-ops), design the SDK/tool surface (use agent-dx), write agent-native docs (use agent-docs), or scaffold repo CI gates (use harden-repo-for-coding-agents), or to operate the eval/optimization loop, autonomy, and reliability (use agent-ops).

## Core principle

**A trusted-but-wrong instrument is worse than none — name the failure mode before the
aggregate, and calibrate the judge before it gates.** You cannot improve a number you cannot
decompose. agent-test *designs* the measurement; `agent-ops` *operates* it (runs the loop,
watches drift). Prefer a deterministic check to a judge whenever the property is checkable.

## Activation

- **Bare invocation** (`"use agent-test"`, `"start"`): show a compact menu: mode choice (guided / autopilot / grill me?) and numbered intents from the router. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with intent and surface inferable: skip to step 3.
- **Ambiguous invocation**: ask one — e.g., *"Are you writing an eval, calibrating a judge, building trajectory tests, or designing benchmarks?"* or *"Is this a new eval suite or an audit of existing tests?"*

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`; match to `do`, `review`, or `design`.
   Ambiguous → ask once.
2. **Pick surface.** Load `references/intents/<intent>.csv`; match one or more of `eval-design`,
   `judge-calibration`, `trajectory-tests`, `benchmark-design`, `activation-evals` — or `all`
   for a REVIEW fan-out. Ambiguous → ask once with the menu.
3. **Load grounded context.** Load only the chosen row's `playbook` plus its `core_refs`. Do not
   load other playbooks (the `review`/`all` row carries none — each surface agent loads its own).
4. **Identify the target persona** from `references/core/personas.md`.
5. **Then calibrate to project scale** (REVIEW / DESIGN) per `references/calibration.md`: below
   Load-bearing, narrow scope, collapse same-mechanism gaps into one systemic finding, and split
   **Now** vs **Later (as it grows)**. The tier feeds emission, never severity.
6. **Dispatch lenses in parallel** (REVIEW default when permitted): one surface per agent for
   `all`; otherwise the three lenses below. Sequential fallback if no delegation primitive.
7. **Apply the playbook.** Use the heuristics tagged for the intent. For REVIEW, score each
   surface 0–10 (`references/core/score-rubric.md`); synthesize lens findings, preserving
   disagreements as open questions. Apply severity and stable `AGENT-TEST-<surface>-NNN` IDs
   (`references/core/severity-rubric.md`): `AGENT-TEST-EVAL`, `AGENT-TEST-JUDGE`,
   `AGENT-TEST-TRAJ`, `AGENT-TEST-BENCH`, `AGENT-TEST-ACT`.
8. **Emit.** DO → `templates/change-plan.md`. REVIEW → `templates/audit-report.md`. DESIGN →
   `templates/design-doc.md` (shape), `templates/refactor-runbook.md` (sequence a hardening), or
   `templates/explanation.md` (explain a principle).
9. **Create, resume, or close tracking state** (REVIEW). For an audit with 7+ findings, any
   severity 3–4, or a save/track/closeout request, load `references/trackable-findings.md`. If
   the request names an existing ledger, workflow-state, PR, or `AGENT-TEST-*` ID, read
   saved state first; update statuses only after each verification rule passes. Otherwise write
   the ledger at `docs/audits/agent-test-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and
   workflow state at `docs/audits/agent-test-workflow-state-<YYYY-MM-DD>-<scope-slug>.json` (fall
   back to `audit-artifacts/agent-test-...` if `docs/audits/` is unwritable). Report both paths;
   keep roadmaps, issues, and non-tracking edits opt-in.

> **Wrong direction?** If the user says this isn't what they meant, go back to Understand (step 1) — do not patch in the wrong direction. Restate the corrected understanding and re-plan.

## Modes

Guided Draft (default), Autopilot, Grill Me — see `references/modes.md`. Offer at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the intent, surface(s), persona, playbook(s) applied, and grounding sources
from `skill.json`; REVIEW adds severity + verification per finding and the project tier. **Name
the coverage you are deliberately NOT adding (YAGNI), not only what you are.**

## Subagent dispatch

Default for REVIEW when delegation is permitted; skip tiny work. Spawn three lenses in parallel
— **decomposition-and-coverage** (failure-mode ontology, localized evals, tier fit),
**judge-and-trust** (judge calibration, bias checks, explanations, held-out disjointness), and
**trajectory-and-gaming** (path grading, march-of-nines, per-slice vs god-gate, metric-gaming,
activation false/missed) — per `references/subagent-dispatch.md`, then synthesize, ordering by
severity.

## Reference map

- `references/intent-router.csv` + `references/intents/<intent>.csv` — the two routing layers.
- `references/playbooks/<surface>.md` — the five measurement surfaces.
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/core/{severity-rubric,score-rubric,personas,glossary}.md` — scales, audience, terms.
- `references/{calibration,trackable-findings,modes}.md` — shared (symlinks).
- `templates/*.md` — change-plan, audit-report, design-doc, refactor-runbook, explanation.
- `evals/`, `skill.json` — gates and provenance.
