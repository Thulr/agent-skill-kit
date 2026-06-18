---
name: design-for-agent-users
description: Use to DESIGN or REVIEW software, docs, SDKs, and repos so AI agents can consume them as a first-class audience — agent experience (AX), the agent-facing analog of UX and DX. Covers agent-readable docs (llms.txt, AGENTS.md, MCP and tool descriptions, RAG-friendly structure), AI and Agent SDK design (streaming, tools, structured output, agent loops, tracing), repo agent-readiness review, and human-versus-agent audience conflicts. The umbrella AX discipline — it routes to harden-repo-for-coding-agents to HARDEN a repo, rules-from-coding-agent-failures to PROMOTE observed failures into rules, and agent-evals to INSTRUMENT an AI product's eval loops. Triggers on 'make our app agent-friendly', 'review our llms.txt for agents', 'design an Agent SDK', 'is this AGENTS.md agent-ready', 'AX review'. Do NOT use for human developer experience (use dx-audit or dx-design), end-user UX (use ux-audit), or to actually scaffold a repo's gates and hooks (use harden-repo-for-coding-agents).
license: MIT
---

# Agent Experience

Designing software, repos, docs, SDKs, and feedback loops for **AI agents as a
first-class consumer audience** — the agent-facing analog of UX and DX.
Grounding lives in `skill.json`; this file is runtime routing only.

**Produces:** an AX review/design/debug report for the chosen surface; or, when
the job is to *build / harden / measure*, a hand-off to the right implementation
arm.

## Core principle

Treat the agent as an audience with its own ergonomics: **machine readability,
context budget (W6), deterministic action, stable contracts, recoverable errors,
explicit authority/trust boundaries, and evidence-driven scaffolding** (never
`/init`; W9). Two AX-specific inversions of UX: keep deliberate **judgment
friction** where the agent crosses a real authority or trust boundary (auth
scope, money movement, irreversible side effect) instead of smoothing it away,
and treat a run as a **durable session**, not a stateless request. The
good-shaped path is one a context-window-bound agent can **ground** itself in
(reconstruct the job, workflow, and success criteria), then find, parse, act on,
and recover from.

## Two things this skill does

1. **Reviews the AX surfaces it owns** — agent-readable docs, AI/Agent SDK
   design, repo agent-readiness, and human-vs-agent audience conflicts (the
   playbooks under `references/playbooks/`).
2. **Routes to the implementation arms** when the user wants to *do*, not review:
   - → `harden-repo-for-coding-agents` — harden a repo (AGENTS.md, hooks, gates,
     sandbox, MCP, specs): the repo-hardening arm.
   - → `rules-from-coding-agent-failures` — promote observed agent failures into
     rules/gates: the evidence/feedback arm (needs a feedback signal).
   - → `agent-evals` — audit an AI integration and build eval/optimization
     loops: the instrument-the-loop arm.

## Activation

- **Bare invocation** (`"agent experience"`, `"AX review"`): load
  [`references/ax-router.csv`](./references/ax-router.csv), show the route menu,
  wait. No file inspection, no writes.
- **Concrete review/design/debug of an AX surface:** pick the route, go to step 2.
- **Concrete build/harden/measure intent:** name the arm skill and hand off; do
  not duplicate its workflow.

## Workflow

1. **Pick route.** Load [`references/ax-router.csv`](./references/ax-router.csv).
   Match the prompt to a playbook route (`ax-docs`, `ai-sdk`, `repo-readiness`,
   `audience-conflicts`) or a hand-off route (`harden-repo`, `promote-rules`,
   `instrument-loops`).
2. **Playbook route:** load the named playbook + `references/core/severity-rubric.md`,
   dispatch the four lenses from [`references/lenses.md`](./references/lenses.md),
   rate each finding by severity, and emit `templates/ax-review-report.md`. Track
   findings per [`references/trackable-findings.md`](./references/trackable-findings.md)
   when over threshold.
3. **Hand-off route:** state which arm skill and why, then stop.

## Modes

Guided Draft (default), Autopilot, Grill Me — see
[`references/modes.md`](./references/modes.md). Offer the mode at bare invocation;
default to Guided Draft otherwise.

## Empirical warnings

W2–W10 in [`references/empirical-warnings.md`](./references/empirical-warnings.md).
The W1 ≥3-evidence floor lives in `rules-from-coding-agent-failures` (see
`references/empirical-warnings-w1.md`).

## Reference map

- `references/ax-router.csv` — route → playbook / arm-skill router.
- `references/playbooks/` — `ax-docs`, `ai-sdk`, `agent` (repo-readiness),
  `audience-conflicts`.
- `references/core/` — `severity-rubric.md`, `audience-matrix.md` (AX excerpt;
  full four-audience matrix lives in the `docs-audit` skill).
- `references/{lenses,modes,empirical-warnings,agent-friendly-architecture,trackable-findings}.md`
  — shared, symlinked from `skills/_shared/`.
- `skill.json` — provenance; `evals/` — gates.
