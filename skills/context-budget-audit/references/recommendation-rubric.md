# Recommendation Rubric

## Action Taxonomy

| Action | Meaning | Typical next step |
| --- | --- | --- |
| `keep-active` | Strong usage evidence in recent history. | Keep it loaded. |
| `consolidate-duplicates` | Used skill appears in multiple active stores. | Pick a canonical store, compare contents, remove redundant copies. |
| `review-weak-evidence` | Only weak or generic-name evidence. | Inspect the row before removing. |
| `reclaim-unused` | Loaded into context but no usage evidence in the window. | Remove/disable to reclaim context (per-kind guidance below). |
| `disabled-no-cost` | Plugin installed but not enabled. | Leave it; it costs no session context. Uninstall only to free disk. |
| `keep-managed-system` | System/built-in item. | Do not prune manually. |
| `ignore-managed-cache` | Plugin/marketplace/temporary cache copy. | Ignore for normal pruning; clean only via the owning tool. |

## Scoring Heuristics (in order)

1. **Management boundary** — system and cache items are protected.
2. **Loaded vs not** — a disabled plugin has no context cost; it is never a
   reclaim candidate (only a disk-cleanup one).
3. **Evidence strength** — strong beats weak; weak beats none only when the name
   is not generic.
4. **Duplication** — duplicate active skill stores need consolidation review even
   when the name is used.
5. **Cost** — within `reclaim-unused`, sort by estimated context cost; treat idle
   MCP servers as highest-value despite unknown cost.
6. **Recency** — recent install/update reduces prune confidence but is not usage.

## Per-Kind Removal Guidance

The audit script never edits anything. Removal is gated and kind-specific.

- **Skill** — copy-validate-remove: preserve into `skills/<name>/` if wanted,
  run the repo's skill validation (`npx skills add . --list`, plus `just check`
  or `./scripts/validate-skills.sh` if the repo ships one), then remove the
  validated store copy. Never remove a store copy without a validated repo copy.
- **Slash command / subagent** — single `.md` file: show the path, confirm it is
  the named item, delete only that file.
- **MCP server** — config edit, so **recommend the command, do not run it**:
  - Claude: `claude mcp remove <name>` (add `-s user` / `-s project` as needed).
  - Codex: remove the `[mcp_servers.<name>]` block from `~/.codex/config.toml`.
- **Plugin** — prefer disabling: set it to `false` in `enabledPlugins` (or use
  the `/plugin` UI). Uninstall removes it from `installed_plugins.json`. Do not
  hand-delete cache directories. Recommend, do not run.

## Reclaim Lens

Recommend removing a loaded item when both are true:

- It has no strong usage evidence in recent local traces, and
- Removing it is low-regret (reinstallable, in the repo, idle, or redundant).

For idle MCP servers, recommend verifying first (the user may have set one up
recently or use it rarely) — but call out that an unused MCP server is typically
the largest single context win available.

## Prune Safety Gates

Before any deletion or config change:

- The target list is explicit and resolved to exact locations.
- The current audit is recent enough for the user's risk tolerance.
- Any keep-worthy skill has been copied into the repo or intentionally dropped.
- Duplicate skill copies were content-compared.
- The action does not target system, cache, auth, or unrelated paths.
- Config-backed removals (MCP, plugins) are handed to the user as commands, not
  executed by the agent.

## Decision Display Quality Bar

A good display includes: inventory counts by kind; a reclaimable headline that
separates measurable tokens from idle MCP servers; a **context footprint** of
total always-on tokens by kind across all items plus the heaviest items (the
aggregate that drives "descriptions compressed" warnings, independent of
non-use); per-kind reclaim groups
sorted by cost; last-used date and evidence counts for rows with evidence;
duplicate groups; a no-cost/managed summary; caveats that token figures are
estimates and counts are evidence matches; and no raw session or credential
content. Machine-readable JSON only when the user asks for automation or saved
output.
