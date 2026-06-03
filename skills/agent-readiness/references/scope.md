# Scope

For any repo that wants coding agents (Claude Code, Cursor, Codex, Copilot, Aider, Windsurf, AGENTS.md-compatible harnesses) to work well in it. This skill makes no assumptions about eval infrastructure, benchmarks, telemetry, or run-level measurement — it works from project knowledge (stack, layout, monorepo scope, build/test commands, top-level invariants).

If you also have a feedback signal — eval suites, run-level telemetry, A/B baselines, or a skill catalog under test — pair this skill with `agent-rules`, which layers a reflection-log workflow on top (capture observed agent failures, promote recurring patterns into AGENTS.md rules via the W1 ≥3-entries floor). This skill does not require it; most repos won't.
