
# Maturity Rubric — Levels 4–5 (Extension)

This file extends `project-agentification/references/core/maturity-rubric.md`
(Levels 1–3) with the spec-architecture and sovereign-engineering levels
that only apply to repos with eval/measurement infrastructure.

Score each layer (legibility / action / control) independently 1–5;
overall maturity = min(layer scores). **Your weakest discipline is your
ceiling.** A perfect Legibility layer with no Control layer caps the
repo at Level 2.

## Levels

### Level 4 — Specification Architecture
- Specs precede code: PRDs, ADRs, runbooks live in `docs/specs/`, `docs/adr/`, `docs/runbooks/` and are first-class artifacts.
- Safety gates on agent pipelines: every prompt/tool/policy change triggers targeted evals.
- AI is a defined-responsibility colleague with explicit roles (PM, Dev, QA, SM) — either via BMAD-style personas or sub-agent design.
- Replayable execution: trajectories, event histories, structured logs joined to commits.
- **Signals:** PRs include self-verification evidence (logs, traces, eval scores) by default; spec drift triggers an automated audit.

### Level 5 — Sovereign Engineering
- Reusable plugin/skill catalog across teams; versioned, owned, reviewed.
- Cost tracking per agent session; model-routing policies (Haiku for exploration, Sonnet for daily, Opus for hard reasoning).
- Organisational governance: audit log for hook overrides, write-protection on AGENTS.md and skills with mandatory review.
- Provenance: SLSA-style attestations for release artifacts.
- **Signals:** agent throughput is bounded by review/governance throughput, not infrastructure; incidents have a disclosure path.

## Per-layer scoring

Same five levels apply within each layer. Layer score = **min across its
assessed sub-surfaces.** Overall maturity = min(legibility, action,
control). Levels 4–5 require harness-engineering infrastructure (specs,
evals, telemetry, governance); repos without that infrastructure cap at
Level 3.

## How to use during `assess`

1. Score Levels 1–3 against `project-agentification`'s rubric first.
2. If overall is already < 3, skip this file — fixing the lower-level
   gaps is the priority.
3. Otherwise, score the Level 4 / Level 5 signals using this file.

## Source

Engineering Agents — Harness Assessment framework. See
`skill.json:inspired_by["Engineering Agents — Harness Assessment"]`.
