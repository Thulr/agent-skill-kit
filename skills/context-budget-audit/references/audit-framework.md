# Audit Framework

## Why This Exists

Everything an agent loads at session start spends context budget before the user
types a word: MCP tool schemas, skill descriptions, slash-command and subagent
listings, and the components of every enabled plugin. The biggest single drain
is almost always MCP tool schemas — one chatty server can cost more than every
skill combined. This audit measures what is loaded, estimates the cost, and
checks recent history for whether each thing is actually used.

## Source Kinds

| Kind | What it is | Where it lives | Always-on cost |
| --- | --- | --- | --- |
| `mcp` | MCP servers (tool schemas injected per session) | `~/.claude.json` (`mcpServers`, per-project too), `~/.codex/config.toml` (`[mcp_servers.*]`) | Tool schemas — usually the largest item |
| `skill` | Agent skills | `~/.claude/skills`, `~/.agents/skills`, `~/.codex/skills`, `~/.pi/agent/skills`, `~/.pi/skills` | SKILL.md description |
| `command` | Slash commands | `~/.claude/commands/*.md`, `~/.codex/prompts/*.md` | Name + description |
| `subagent` | Custom subagents | `~/.claude/agents`, `~/.codex/agents` | Name + description |
| `plugin` | Plugins (bundle the above) | `~/.claude/plugins/installed_plugins.json`, enabled via `settings.json` `enabledPlugins` | Sum of enabled bundled components |

System skills (under `.system`) and plugin/marketplace caches are inventory-only:
protected from normal prune recommendations.

## Token Estimation

All token figures are deliberate estimates surfaced as estimates, never exact
telemetry.

- **Skill / command / subagent**: `ceil(chars / 4)` over the always-on text
  (the description, parsed from frontmatter including `>`/`|` block scalars).
- **Plugin (enabled)**: sum of its bundled skills'/commands'/agents' description
  estimates. A disabled plugin costs nothing and is reported as such.
- **MCP server**: `base + (observed distinct tools) × ~190 tokens`. This counts
  only tools that were actually invoked, so it is a **lower bound** — a server's
  full schema footprint includes tools never called. For an **idle** server (no
  tool calls observed) the cost cannot be measured from disk and is reported as
  unknown, with a prominent flag because idle servers are the highest-value
  things to verify and remove.

## Evidence Model

Default scan: newest evidence files first, last 90 days, bounded file count, and
per-file text bounded for regex (MCP tool-use detection streams every line so it
is never truncated). Display-only output.

**MCP usage (precise).** Strong evidence is a genuine tool-call invocation whose
name matches `mcp__<server>__<tool>`, pulled from `tool_use` blocks in
transcripts — not from tool *listings* in system reminders. Each observed tool
also informs the cost estimate. Usage is attributed to the server configured for
the agent that produced the transcript (`~/.claude` → Claude, `~/.codex` → Codex).

**Skill / command / subagent usage.**

- *Strong*: path references; activation verbs (`use/invoke/load/run … <name>`);
  `<name> skill`; `skill: "<name>"`; `/<name>` for commands; `subagent_type:
  "<name>"` / `<name> agent` for subagents.
- *Weak*: plain-name mentions, especially generic English words.

**Plugin usage.** Plain short-name mentions are weak evidence. A plugin's real
value shows through usage of its bundled components (audited under their own
kinds).

**Non-usage evidence** (never counted as use): a thing's own definition file,
install metadata, lock files, plugin catalogs, cache manifests, and this repo.

## Privacy Rules

- Never quote raw session text, prompts, tool payloads, auth files, tokens, or
  environment values.
- Display only paths, counts, timestamps, source-agent labels, estimates, and
  classification reasons.
- Skip files with sensitive names (`auth`, `.env`, `token`, `secret`,
  `credential`, `key`, `cookie`, …). If a useful source is skipped, count it as
  a partial scan.
- If older history is outside the window, call results "no recent evidence", not
  "never used".

## Duplicate Model

A skill name can appear in multiple active stores; name-level evidence cannot
prove which copy was loaded. Identical copies → keep one (prefer the repo copy)
and remove the rest by name; differing copies → preserve the richer/edited one
before pruning. The same MCP server name can be configured for both Claude and
Codex; these are distinct items and usage is attributed per agent.

## Conservative Defaults

- Never recommend deleting system or cache-managed items.
- Never edit `~/.claude.json`, `~/.codex/config.toml`, or `settings.json` — for
  MCP servers and plugins, recommend the exact command and let the user run it.
- Prefer `move-to-repo` for no-evidence custom skills not already in the repo.
- Prefer `reclaim-unused` for loaded-but-unused items; flag idle MCP servers
  with unknown-but-likely-large cost.
- Mark generic weak matches as `review-weak-evidence`, not used.

## Edge Signals

Escalate to human review when: the name is generic; an item has no evidence but
was installed/updated very recently; a skill has local edits not in the repo; a
source root was unreadable or a large share of evidence files was skipped.
