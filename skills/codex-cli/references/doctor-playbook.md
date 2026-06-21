# Doctor Playbook

Use this when Codex CLI invocation fails or setup is uncertain.

## Command

```bash
codex doctor --summary --ascii
```

Use `--json` when another script needs a machine-readable report. Redacted
doctor output is acceptable to summarize, but do not store credentials or raw
environment dumps in workflow state.

## Common Blockers

- Codex is not installed or not on `PATH`.
- Authentication is missing or expired.
- Config contains unsupported fields for the installed Codex version.
- Sandbox or approval policy blocks the requested operation.
- The repository is not a git repo for review commands.

## Response Pattern

Report:

1. the exact command run
2. whether Codex CLI is available
3. whether auth/config/runtime checks passed
4. the next concrete fix or setup step

Do not run login/logout automatically unless the user explicitly asks.
