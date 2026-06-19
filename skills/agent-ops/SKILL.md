---
name: agent-ops
description: Use for AGENT OPS — operating a running AI agent system, and the front-door for the agent skill family. DO — wire observability, a trace-and-eval loop, an autonomy controller, a budget, or a release gate for a running agent. REVIEW — audit an agent system's observability, optimization loop, autonomy controls, reliability/cost, or maturity, then score it. DESIGN — shape an operating loop, gate autonomy, decompose a release gate, assess maturity and route the work to the right sibling, or explain a principle. Triggers on 'set up a trace-and-eval loop', 'is our agent autonomy safe to enable', 'where are we on the agent maturity ladder', 'make our agent system production-ready'. Do NOT use to design the SDK/tool surface an agent consumes (use agent-dx), design evals/judges/benchmarks (use agent-test), write agent-native docs (use agent-docs), scaffold repo gates/hooks (use harden-repo-for-coding-agents), or promote failures into rules (use rules-from-coding-agent-failures).
license: MIT
---

# Agent Ops

Operating a running AI agent system — observing it, closing its improvement loop, governing its
autonomy, keeping it reliable and bounded in cost — and the **front-door** for the agent skill
family. Provenance lives in `skill.json`; this file is runtime routing only.

**Produces:** a `change-plan.md` (DO), an `audit-report.md` plus a findings-ledger +
workflow-state when tracked (REVIEW), or a `design-doc.md` / `refactor-runbook.md` /
`explanation.md` (DESIGN).

## Core principle

**Score on observed emission, not field presence; let autonomy run only behind a gate and a
circuit-breaker.** A system you cannot reconstruct from its traces, whose loop never closes, or
that self-improves ungated fails at machine speed. agent-ops *operates*; it hands building off
to the siblings below.

## Activation

- **Bare invocation** (`"use agent-ops"`, `"make our agent production-ready"`, `"start"`): load
  `references/intent-router.csv`, show the intent menu, offer the mode. Wait. No file
  inspection, network calls, or writes.
- **Concrete invocation** with intent and surface inferable: skip to step 3.
- **Ambiguous scope**: ask one blocker question naming the candidate intent or surface, or
  whether the work should route to a sibling (see Front-door). Do not inspect private systems first.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`; match to `do`, `review`, or `design`.
   Ambiguous → ask once.
2. **Pick surface.** Load `references/intents/<intent>.csv`; match one or more of
   `observability`, `optimization-loop`, `autonomous-controller`, `cost-and-reliability`,
   `maturity-and-governance` — or `all` for a REVIEW fan-out. Ambiguous → ask once with the menu.
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
   disagreements as open questions. Apply severity and stable `AGENT-OPS-<surface>-NNN` IDs
   (`references/core/severity-rubric.md`): `AGENT-OPS-OBS`, `AGENT-OPS-LOOP`, `AGENT-OPS-CTL`,
   `AGENT-OPS-REL`, `AGENT-OPS-GOV`.
8. **Emit.** DO → `templates/change-plan.md`. REVIEW → `templates/audit-report.md`. DESIGN →
   `templates/design-doc.md` (shape), `templates/refactor-runbook.md` (sequence a rollout), or
   `templates/explanation.md` (explain a principle).
9. **Create, resume, or close tracking state** (REVIEW). For an audit with 7+ findings, any
   severity 3–4, or a save/track/closeout request, load `references/trackable-findings.md`. If
   the request names an existing ledger, workflow-state, PR, or `AGENT-OPS-*` ID, read
   saved state first; update statuses only after each verification rule passes. Otherwise write
   the ledger at `docs/audits/agent-ops-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and
   workflow state at `docs/audits/agent-ops-workflow-state-<YYYY-MM-DD>-<scope-slug>.json` (fall
   back to `audit-artifacts/agent-ops-...` if `docs/audits/` is unwritable). Report both paths;
   keep roadmaps, issues, and non-tracking edits opt-in.

## Front-door — routing out

agent-ops operates; it does not build. Hand off when the work is building: **`agent-dx`**
(SDK/tool/error/telemetry surface), **`agent-docs`** (AGENTS.md, llms.txt, MCP discovery),
**`agent-test`** (evals/judges/benchmarks), **`harden-repo-for-coding-agents`** (repo
gates/hooks), **`rules-from-coding-agent-failures`** (promote failures). A generic "make this
agent-friendly" lands here; route it onward.

## Modes

Guided Draft (default), Autopilot, Grill Me — see `references/modes.md`. Offer at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the intent, surface(s), persona, playbook(s) applied, and grounding sources
from `skill.json`; REVIEW adds severity + verification per finding and the project tier. **Name
the operating machinery you are deliberately NOT adding (YAGNI), not only what you are.**

## Subagent dispatch

Default for REVIEW when delegation is permitted; skip tiny work. Spawn three lenses in parallel
— **signal-and-trace** (substantive spans, graded trajectory, no dashboard/telemetry theater),
**loop-and-control** (observed-emission readiness, gated autonomy, circuit-breakers), and
**reliability-and-governance** (march-of-nines, decomposed release gates, budgets, maturity,
provenance) — per `references/subagent-dispatch.md`, then synthesize, ordering by severity.

## Reference map

- `references/intent-router.csv` + `references/intents/<intent>.csv` — the two routing layers.
- `references/playbooks/<surface>.md` — the five operator surfaces.
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/core/{severity-rubric,score-rubric,personas,glossary}.md` — scales, audience, terms.
- `references/{calibration,trackable-findings,modes}.md` — shared (symlinks).
- `templates/*.md` — change-plan, audit-report, design-doc, refactor-runbook, explanation.
- `evals/`, `skill.json` — gates and provenance.
