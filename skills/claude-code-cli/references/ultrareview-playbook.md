# Ultrareview Playbook

Claude Code includes a hosted multi-agent review command:

```bash
claude ultrareview [target]
```

Use this only when the user asks for a deeper branch or PR review, or when a
local `claude -p` review is not enough for the risk level.

## When to Use

- branch-level review before opening or merging a PR
- high-risk refactors touching several subsystems
- security-sensitive changes where independent reviewers are useful
- PR review where the target can be a PR number, PR URL, or base branch

## Stop Conditions

Ultrareview is user-initiated — do not auto-run. Stop before running
ultrareview if:

- the current branch or target is unclear
- the repository contains sensitive changes the user has not approved sending
- auth, network, or cost constraints are unknown
- the user only asked for a quick local review

## Presentation

Treat ultrareview output like external review feedback. Summarize the actionable
findings, verify claims before editing, and report any findings that need user
judgment.
