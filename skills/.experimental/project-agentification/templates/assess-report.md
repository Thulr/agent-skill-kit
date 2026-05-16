# Agentification Assessment — <repo-path>

**Date:** <YYYY-MM-DD>
**Primary harness(es) detected:** <claude-code | cursor | codex | copilot | windsurf | aider | none>
**Sub-surfaces assessed:** <list, or `all`>
**Lenses dispatched:** cold-context-agent / maintainer / adversarial / auditor

## Maturity scores

| Layer | Score (1–5) | Justification |
|---|---|---|
| Legibility | <N> | <one-line; cite weakest sub-surface> |
| Action | <N> | <one-line> |
| Control | <N> | <one-line> |

**Overall maturity ceiling:** <min(layer scores)> — limited by **<layer>** (weakest discipline is your ceiling).

## Blocking gaps (severity 3–4)

| Severity | Layer | Sub-surface | Finding | Artifact pointer | Lens(es) |
|---|---|---|---|---|---|
| <4> | <legibility|action|control> | <sub-surface> | <one-line description> | <file:line / hook name / MCP method> | <lens names> |
| ... | | | | | |

## Significant gaps (severity 2)

| Layer | Sub-surface | Finding | Artifact pointer |
|---|---|---|---|

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

## Verification

Re-run this audit after the next stage with these targeted checks:

- <how to prove the stage was completed; e.g., "AGENTS.md ≤ 200 lines AND hook gate for force-push to main exists in CI">
- <metric or signal to confirm the agent's behavior changed>

## Sources cited

(list of skill.json `inspired_by` entries that contributed to specific findings)
