# Harden Recommendation — <failure-mode-name>

**Date:** <YYYY-MM-DD>
**Layer / surface:** <e.g., control / gates>
**Severity if unaddressed:** <0–4>
**Linked findings:** <AG-... IDs, if this recommendation came from an assessment ledger>

## Failure mode

<One paragraph: what the agent did wrong / what the threat actor could do. Concrete — name the file, the command, the input shape.>

## Root cause

<Which layer and surface. Cite the playbook heuristic that this violates (e.g., "gates playbook H3: no PreToolUse hook for destructive bash").>

## Recommendation

**Add / edit:** <exact artifact — file path, hook name, MCP method, approval tier>

<Concrete instructions; if it's a hook, paste the hook definition; if it's an MCP method, paste the schema.>

## Token-cost note

- [ ] Always-loaded (e.g., AGENTS.md line) — costs N tokens per session.
- [ ] On-trigger (skill activated by description match) — costs N tokens only when triggered.
- [ ] On-demand (MCP method called by agent) — costs ~0 tokens until invoked.

## Verification

<Green-M&M-style test the agent must pass after the change. Example: "Submit a PR that includes a force-push to main; confirm the hook rejects it with exit code 2.">

If linked findings exist, run a verification closeout pass and update the
ledger/workflow state only for IDs whose checks pass.

## Empirical warnings invoked

<list of W-IDs from references/empirical-warnings.md that justify this recommendation>

## Sources cited

(list of skill.json `inspired_by` entries)
