# activation-cases.md — design-for-agent-users

The umbrella agent experience (AX) discipline. It owns the AX review heuristics
(agent-readable docs, AI/Agent SDK design, repo agent-readiness, human-vs-agent
audience conflicts) and routes to `harden-repo-for-coding-agents` (harden),
`rules-from-coding-agent-failures` (promote), and `agent-evals` (instrument) for the
doing.

## Positive

- "Review our llms.txt and AGENTS.md so coding agents can navigate the repo." → `ax-docs`
- "Is our documentation retrieval-friendly for RAG and agents?" → `ax-docs`
- "Design the streaming, tool-use, and agent-loop API for our new LLM SDK." → `ai-sdk`
- "Is this AGENTS.md agent-ready and do our harness mirrors stay in sync?" → `repo-readiness`
- "Resolve the human-vs-agent doc conflict where tooltip-only guidance is invisible to agents." → `audience-conflicts`
- "Scaffold AGENTS.md, hooks, and a sandbox to harden this repo for Claude Code." → hand off to `harden-repo-for-coding-agents` (`harden-repo`)
- "Promote our recurring agent failures into rules." → hand off to `rules-from-coding-agent-failures` (`promote-rules`)
- "Audit our AI feature's feedback loops and set up evals." → hand off to `agent-evals` (`instrument-loops`)

## Negative

- "Refactor this React component." (code change, no agent-experience surface)
- "Run a usability audit on our checkout flow." (end-user UX → `ux-audit`)
- "Review the p99 latency of our payments service." (systems perf → `perf-audit`)

## Edge

- "Make our REST API reference clearer for human developers." → human DX docs;
  use `dx-audit` / `docs-audit` (or their `-design` siblings), not AX.
  Only routes here when the reader is an agent.
- "Should our product expose an MCP server, and how do we document it for
  agents?" → `repo-readiness` (review); the actual MCP scaffolding is a hand-off
  to `harden-repo-for-coding-agents`.
- "Harden the repo for coding agents." → ambiguous between AX (the umbrella) and
  `harden-repo-for-coding-agents` (the arm). AX names the arm and hands off; a direct
  `harden-repo-for-coding-agents` invocation is equally valid.
