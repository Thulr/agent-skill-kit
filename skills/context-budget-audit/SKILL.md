---
name: context-budget-audit
description: "Audit and prune per-session context waste — MCP servers, plugins, skills, subagents. Triggers: 'what's eating my context', 'trim my agent setup'. Do NOT use to harden a repo's agent config (use harden-repo-for-coding-agents) or for runtime trace/eval observability (use agent-ops)."
license: MIT
---

# Context Budget Audit

## Overview

Audit everything that consumes per-session context across local agent setups,
estimate what each costs, scan recent local history for usage evidence, and show
a prune decision view sorted by reclaimable context. Then act on the user's named
removal list.

Context sources audited (`kinds`): `mcp` (MCP servers), `skill`, `command`
(slash commands), `subagent`, `plugin`.

## Boundaries

Do NOT use to harden a repo's agent config, hooks, or gates (use
harden-repo-for-coding-agents), or for runtime agent observability and
trace/eval loops (use agent-ops) — this skill measures and prunes what loads
into your agent's per-session context.

The normal loop:

1. Run the audit.
2. The user names items to remove, disable, or move into this repo.
3. Act per kind (see Act On Named Items), validating before any deletion.

## Activation

- **Bare invocation** (`"use context-budget-audit"`, `"start"`, `"what am I not
  using?"`): run the default audit immediately — it is read-only; do not turn
  bare activation into a menu. No writes.
- **Ambiguous invocation**: ask one — e.g., *"Are you auditing MCP servers,
  plugins, skills, or all sources?"* or *"Is this a full context audit or a
  narrower 'find unused skills and move keepers into this repo' pass?"*
- **Concrete invocation**: run the default audit.

## Operating Contract

- Default scope: active local stores under `~/.claude`, `~/.codex`, `~/.agents`,
  and `~/.pi` for the five kinds above.
- Use `scripts/audit_context_budget.py` for the audit. Do not hand-roll the
  inventory or evidence scan unless the script is blocked.
- The script is read-only. It never deletes, disables, or edits a config file —
  it only reports and recommends. All removal is the agent's job under the gates
  below, only after the user names targets.
- Do not write Markdown or JSON artifacts by default. Display the decision view
  directly unless the user asks to save output.
- Treat all counts as evidence matches, not exact invocations, and all token
  figures as estimates, not exact context measurements.
- MCP usage is detected from genuine tool-call invocations (`mcp__<server>__*`)
  in transcripts, not from tool listings. An MCP server with no observed tool
  calls is **idle**: its full cost cannot be measured from disk, but idle MCP
  servers are usually the single largest reclaimable context item — surface them
  first.
- "No evidence" means no evidence in the bounded scan window, not proof of
  lifetime non-use.
- Keep raw transcript, prompt, and credential contents out of reports. Display
  only paths, counts, timestamps, estimates, and classification reasons.
- A user message naming items to "remove", "disable", "delete", "move into the
  repo", or "preserve here" is explicit authorization for those named items only.

## Workflow

### 1. Audit

Load `references/audit-framework.md` and `references/recommendation-rubric.md`,
then run:

```bash
python3 scripts/audit_context_budget.py --repo-root <repo-root> --no-write
```

Use the current repository as `<repo-root>` when it has a `skills/` directory;
otherwise use the user's named repository. A full run scans recent transcripts
and typically takes 30–60s.

Scope flags (only add when the user asks, or to go faster):

- `--only mcp` or `--kinds mcp,skill` to restrict to specific source kinds.
- `--evidence-days 0` for an all-history scan; lower the number for a faster
  recent-only pass.
- `--max-evidence-files N` to bound the scan.
- `--json`, `--json-output PATH`, `--markdown-output PATH` for saved/automated
  output.

Show the decision view as-is: the reclaimable headline (measurable tokens plus
idle MCP servers); the **context footprint** (total always-on tokens across ALL
items by kind, plus the heaviest items); per-kind reclaim groups sorted by cost;
weak-evidence rows; duplicate skills; kept items; the no-cost/managed summary;
caveats; and the "name what to remove" prompt.

The footprint matters as much as the reclaim list: "skill descriptions
compressed to save space" warnings are driven by **aggregate** load (count ×
description length), not by individual non-use. When the footprint for a kind is
large, the levers are (a) reduce how many items load — uninstall niche ones or
scope installs per-agent instead of fanning out to all agents — and (b) shorten
the heaviest descriptions. Check for cross-store duplicates first, but do not
assume duplication is the cause; a large set of distinct items is common.

### 2. Act On Named Items

Resolve each named item to a kind and exact location from the audit, then:

**Skill — move into repo and/or remove installed copy** (the preserved
copy-validate-remove flow):

1. For each named skill, look only in active stores: `~/.claude/skills/<name>`,
   `~/.agents/skills/<name>`, `~/.codex/skills/<name>` (excluding `.system`),
   `~/.pi/agent/skills/<name>`, `~/.pi/skills/<name>`. Require `SKILL.md`.
2. If `skills/<name>/` does not exist, copy one source directory there.
   If it exists and is identical, treat it as already preserved. If it differs,
   stop and show the differing paths.
3. If the same skill exists in multiple stores: identical copies → keep one repo
   copy and remove the named identical store copies; differing copies → stop and
   ask which is canonical.
4. Run the repo's skill validation: `npx skills add . --list` (universal), plus
   the repo's own gate if it has one (`just check` here, or
   `./scripts/validate-skills.sh` in repos that ship it).
5. Remove only the store directories that were successfully preserved and
   validated. Verify each path is gone.

**Slash command / subagent — delete the file**: these are single `.md` files.
Show the exact path, confirm it is the named item, then delete only that file.

**MCP server — recommend the removal command (config edit = stop-and-confirm)**:
do not edit `~/.claude.json`, `~/.codex/config.toml`, or settings yourself.
Surface the precise action and let the user run it:

- Claude global/project: `claude mcp remove <name>` (or `claude mcp remove -s user <name>`); if unsure the syntax is current, check `claude mcp remove --help` first.
- Codex: remove the `[mcp_servers.<name>]` block from `~/.codex/config.toml`.

**Plugin — recommend disable/uninstall (config edit = stop-and-confirm)**:
prefer disabling over deleting cache. Surface the action: disable via the
`/plugin` UI or by setting the plugin to `false` in `enabledPlugins`; uninstall
removes it from `installed_plugins.json`. Do not hand-delete plugin cache dirs.

Report acted, already-done, recommended-to-user, skipped, and blocked items.

> **Wrong direction?** If the user says this isn't what they meant, go back to
> the Audit (step 1) — do not patch in the wrong direction. Restate the
> corrected understanding and re-plan.

## Stop Conditions

Stop and ask before acting when:

- A named item cannot be found in active stores/config.
- The target is a system skill, plugin/marketplace cache, or unrelated directory.
- `skills/<name>/` exists but differs from the store source, or duplicate store
  copies differ.
- Repository validation fails after copying a skill.
- The action would edit `~/.claude.json`, `~/.codex/config.toml`, or
  `settings.json` — recommend the command and let the user run it instead.
- The action would inspect credentials, raw transcripts, or auth files.

## Edge-Case Pass

Before final output, check:

- Absent sources are reported as absent, not treated as empty evidence.
- Idle MCP servers are surfaced as high-value/unknown-cost, never as "~0 tokens".
- System and cache items are excluded from normal prune actions.
- Disabled plugins are reported as zero-context-cost, not as reclaim candidates.
- Token figures and usage counts are labeled estimates/evidence, not exact.
- Generic names (`review`, `research`, `run`, `verify`, `tdd`, …) are discounted.
- No raw prompt, credential, token, or transcript content appears in output.
- Every removed skill store path has a validated `skills/<name>/` copy; every
  config edit was handed to the user, not performed by the agent.

## Output Contract

For audits, return: scope and kinds scanned; reclaimable headline; the context
footprint (total always-on tokens by kind across all items, plus heaviest
items); per-kind reclaim groups; weak-evidence and duplicate groups; kept items;
no-cost/managed summary; caveats; and a prompt asking which items to remove.

For act workflows, return: items acted on (skills copied/removed, command/agent
files deleted); commands recommended to the user for config-backed items;
already-done, skipped, and blocked items with reasons; validation results.

## Reference Map

- `references/audit-framework.md`: source-kind model, evidence model, token
  estimation, scanning scope, and privacy rules.
- `references/recommendation-rubric.md`: action taxonomy and per-kind removal
  guidance.
- `references/use-case-registry.csv`: compact router for audit, act, scoped, and
  eval tasks.
- `scripts/audit_context_budget.py`: deterministic local audit engine.
- `evals/context-budget-audit-eval-suite.json`: static and scenario fixtures.
