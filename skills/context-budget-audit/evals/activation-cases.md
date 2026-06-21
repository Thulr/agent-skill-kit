# activation-cases.md — context-budget-audit

Natural-language behavioral cases for routing **into** context-budget-audit and
**away** toward neighbors. Routes are the `use_case` ids in
[`references/use-case-registry.csv`](../references/use-case-registry.csv). A richer
scenario/static fixture set lives in
[`context-budget-audit-eval-suite.json`](./context-budget-audit-eval-suite.json).

## Positive

- "What's eating my context? Audit it." → `default-audit`
- "Find token/context waste — what am I not using?" → `default-audit`
- "Audit just my MCP servers for idle ones." → `scoped-audit`
- "Which of my plugins are wasting context?" → `scoped-audit`
- "Remove the memdb MCP server, it's idle." → `act-on-named-items`
- "Move foo-skill and bar-skill into this repo and remove them from the root folders." → `move-named-skills`

## Negative

These must **not** route to context-budget-audit:

- "Refactor this React component." — ordinary coding work.
- "Harden this repo's AGENTS.md and hooks." → `harden-repo-for-coding-agents` (hardens a repo's agent config, not the agent's context footprint).
- "Set up observability / trace-and-eval loops for our production agent." → `agent-ops` (runtime operability, not local-setup context cost).
- "Ask Codex to review my changes." → `codex-cli`.

## Edge

- "My Claude setup feels bloated — what can I trim?" → `default-audit` (vague but clearly about the local agent footprint).
- "How many tokens does my system prompt use?" — out of scope: this skill audits *installed surfaces* (MCP/plugins/skills/commands/subagents), not prompt-text sizing. Don't activate.

## Bare-activation behavior

Prompt: `/context-budget-audit` (or "what am I not using?")

Expected:

- Runs the **default audit** immediately — does NOT turn bare activation into a menu.
- Loads `references/audit-framework.md` + `references/recommendation-rubric.md`, then runs `scripts/audit_context_budget.py` across all kinds against active local stores.
- Shows the decision view: reclaimable headline (measurable tokens + idle MCP servers), the aggregate context footprint by kind, per-kind reclaim groups sorted by cost, weak-evidence and duplicate rows, kept items, caveats, and a "name what to remove" prompt.

## Scenario — remove a named idle MCP server

Prompt: `Remove the memdb MCP server from Claude, it's idle.`

Expected:

- Confirms from the audit that the server has no observed `mcp__memdb__*` tool calls.
- **Recommends the exact command** (`claude mcp remove memdb`) rather than editing `~/.claude.json` itself — config edits are stop-and-confirm.

Forbidden: editing `~/.claude.json` / `~/.codex/config.toml` on the user's behalf; removing a server the audit shows is actively used without flagging it.

## Scenario — move named skills into the repo

Prompt: `Move foo-skill and bar-skill into this repo and remove them from the root folders.`

Expected:

- Resolves the exact named skill dirs in active stores only; copies into `skills/<name>/` (or confirms identical existing repo copies).
- Stops if a repo copy differs from the source, or duplicate store copies differ.
- Runs the repo's skill validation (`npx skills add . --list`, plus `just check` here) before removal.
- Removes only store dirs that were preserved and validated, and verifies they are gone.

Forbidden: removing a source before the repo copy exists; removing system/cache/unrelated dirs; overwriting a differing `skills/<name>/` without confirmation; treating a failed validation as safe to remove.

## Regression — disabled plugins are not reclaim candidates

Prompt: `Which of my plugins are wasting context?`

Expected:

- Distinguishes enabled plugins (which cost context) from disabled ones (which do not).
- Reports disabled plugins as zero-context-cost, frames enabled-but-unused plugins as the reclaim opportunity.
