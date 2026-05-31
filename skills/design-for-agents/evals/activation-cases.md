# activation-cases.md — design-for-agents

The umbrella agent experience (AX) discipline. It owns the AX review heuristics
(agent-readable docs, AI/Agent SDK design, repo agent-readiness, human-vs-agent
audience conflicts) and routes to `codebase-agent-readiness` (harden),
`evidence-driven-agent-rules` (promote), and `eval-flywheel` (instrument) for the
doing.

## Positive

- "Review our llms.txt and AGENTS.md so coding agents can navigate the repo." → `ax-docs`
- "Is our documentation retrieval-friendly for RAG and agents?" → `ax-docs`
- "Design the streaming, tool-use, and agent-loop API for our new LLM SDK." → `ai-sdk`
- "Is this AGENTS.md agent-ready and do our harness mirrors stay in sync?" → `repo-readiness`
- "Resolve the human-vs-agent doc conflict where tooltip-only guidance is invisible to agents." → `audience-conflicts`
- "Scaffold AGENTS.md, hooks, and a sandbox to harden this repo for Claude Code." → hand off to `codebase-agent-readiness` (`harden-repo`)
- "Promote our recurring agent failures into rules." → hand off to `evidence-driven-agent-rules` (`promote-rules`)
- "Audit our AI feature's feedback loops and set up evals." → hand off to `eval-flywheel` (`instrument-loops`)

## Negative

- "Refactor this React component." (code change, no design-for-agents surface)
- "Run a usability audit on our checkout flow." (end-user UX → `ux-critique`)
- "Review the p99 latency of our payments service." (systems perf → `perf-critique`)

## Edge

- "Make our REST API reference clearer for human developers." → human DX docs;
  use `dx-critique` / `docs-critique` (or their `-design` siblings), not AX.
  Only routes here when the reader is an agent.
- "Should our product expose an MCP server, and how do we document it for
  agents?" → `repo-readiness` (review); the actual MCP scaffolding is a hand-off
  to `codebase-agent-readiness`.
- "Harden the repo for coding agents." → ambiguous between AX (the umbrella) and
  `codebase-agent-readiness` (the arm). AX names the arm and hands off; a direct
  `codebase-agent-readiness` invocation is equally valid.
