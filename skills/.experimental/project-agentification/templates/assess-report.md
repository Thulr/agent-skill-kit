# Agentification Assessment — <repo-path>

**Date:** <YYYY-MM-DD>
**Primary harness(es) detected:** <claude-code | cursor | codex | copilot | windsurf | aider | none>
**Sub-surfaces assessed:** <list, or `all`>
**Lenses dispatched:** cold-context-agent / maintainer / adversarial / auditor

## Maturity scores

| Layer | Score (1–5) | Justification |
|---|---|---|
| Legibility | <N> | <single line; cite weakest sub-surface; no `|`> |
| Action | <N> | <single line; no `|`> |
| Control | <N> | <single line; no `|`> |

**Overall maturity ceiling:** <min(layer scores)> — limited by **<layer>** (weakest discipline is your ceiling).

## Parallel agent partitioning (optional; if multi-agent work is desired)

Use this checklist to assess whether multiple agents can work in parallel without stepping on each other:

- [ ] **Design rules identified:** a short list of stable contracts (public interfaces/APIs, schemas, shared types, dependency rule).
- [ ] **Design rules protected:** CODEOWNERS / required reviewers + CI-required checks for changes to those contracts.
- [ ] **Boundaries enforced:** forbidden imports / dependency direction / cycle detection (don’t rely on agent reasoning).
- [ ] **Partition strategy explicit:** agents assigned to independent modules “under” the design rules; avoid concurrent edits to the same contract artifacts.
- [ ] **Integration signal exists:** contract/integration tests fail fast when module boundaries or interfaces drift.

## Blocking gaps (severity 3–4)

| ID | Severity | Layer | Sub-surface | Status | Finding | Artifact pointer | Verification | Lens(es) |
|---|---:|---|---|---|---|---|---|---|
| <AG-GATES-001> | <4> | <legibility|action|control> | <sub-surface> | discovered | <one-line description> | <file:line / hook name / MCP method> | <narrow check that proves the gap is fixed> | <lens names> |
| ... | | | | | | | | |

## Significant gaps (severity 2)

| ID | Layer | Sub-surface | Status | Finding | Artifact pointer | Verification |
|---|---|---|---|---|---|---|

## Minor friction (severity 1)

(table — same shape)

## Cosmetic (severity 0)

(brief bulleted list; optional)

## Conflicts and open questions

- <Lens A said X, lens B said don't-X. Recommend deciding before scaffold/harden.>

## Recommended stage

Based on the weakest layer, the next stage to target is:

- [ ] Stage 0 — Triage (1–2 days). <when to pick>
- [ ] Stage 1 — Habitat (1–2 weeks). <when to pick>
- [ ] Stage 2 — Specs (1 month). <when to pick>
- [ ] Stage 3 — MCP and observability. <when to pick>
- [ ] Stage 4 — Governance. <when to pick>

**Top three actions for the next stage:**

1. <action> — closes <gap-id>
2. <action> — closes <gap-id>
3. <action> — closes <gap-id>

## Tracking offer

If this report has 7+ findings, any severity 3–4 finding, or the user asks
for follow-through, offer to create:

- `templates/findings-ledger.md` — source of truth for finding statuses.
- `templates/roadmap.md` — staged work packages that close finding IDs.
- `templates/github-issue.md` — issue-shaped work packages, only with confirmation.
- `templates/workflow-state.json` — machine-readable continuation state.

Checking off a finding requires a verification closeout pass; `implemented`
or closed GitHub issue is not enough.

## Verification

Re-run this audit after the next stage with these targeted checks:

- <how to prove the stage was completed; e.g., "AGENTS.md ≤ 200 lines AND hook gate for force-push to main exists in CI">
- <metric or signal to confirm the agent's behavior changed>

## Sources cited

(list of skill.json `inspired_by` entries that contributed to specific findings)
