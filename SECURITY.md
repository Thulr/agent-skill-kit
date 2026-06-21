# Security policy

`agent-skill-kit` publishes [Agent Skills](https://agentskills.io) that load into
downstream agent sessions (Claude Code, Cursor, Codex, Copilot, Windsurf, Aider).
A vulnerability in a published skill can affect every consumer; treat reports
accordingly.

## Reporting a vulnerability

**Do not open a public issue or PR for a security report.**

Use [GitHub Security Advisories](https://github.com/justinramos101/agent-skill-kit/security/advisories/new)
to file a private report. We will:

- Acknowledge receipt within **7 days**.
- Investigate and discuss remediation privately.
- Coordinate a public disclosure once a fix has shipped.
- Credit the reporter in the advisory and release notes (unless they prefer
  to remain anonymous).

If you cannot file via Security Advisories, email the repo owner via the
contact listed on their GitHub profile (`@justinramos101`). Include a working
proof-of-concept where possible.

## What counts as a security issue

In scope:

- **Prompt-injection vectors in published skills** — content in `skills/**/SKILL.md`
  or referenced files that could redirect an agent to exfiltrate data, take
  unauthorized actions, or persist instructions across sessions (W5).
- **Malicious-skill landings** — historical PRs or commits to `skills/`, `.agents/`,
  `.github/`, `Justfile`, or other agent-surface paths that look intentional
  (style, naming) but introduce a vector. Report even if already merged.
- **Secret-leak instructions** — skill content that instructs an agent to
  inspect, transmit, or log environment variables, credentials, or filesystem
  paths outside the workspace.
- **Static-check bypass** — gaps in `evals/run-static-checks.sh` or the CI
  workflow that let a malicious skill ship without review.
- **Supply-chain trust gaps** — issues with `skill.json` provenance, CODEOWNERS
  coverage, or branch-protection configuration that weaken the review gate.

Out of scope (open a normal issue instead):

- Bugs in skill *content* (heuristics that produce wrong recommendations).
- Documentation typos.
- Build / install issues unrelated to security.
- Vulnerabilities in upstream tools (`npx skills`, Claude Code, etc.) — report
  those to their respective maintainers.

## What to include in a report

- A minimal reproducer (file paths + the agent harness used).
- The expected vs observed agent behavior.
- The skill version (`skills/<name>/skill.json` `version` field, if present)
  and commit SHA you tested against.
- Suggested mitigation, if you have one.

## Defenses already in place

- `.github/CODEOWNERS` requires review on `skills/**`, `.agents/**`, `.github/**`,
  `Justfile`, `README.md`.
- Branch protection on `main` requires CI plus at least one code-owner approval;
  self-merges are blocked at the GitHub layer (verified on PR #5).
- Each skill ships static checks (`evals/run-static-checks.sh`) that gate on
  `SKILL.md` structure, `skill.json` provenance, and source-author leakage.
- `.claude/hooks/block-destructive-bash.py` blocks destructive Bash actions
  (force-push to main, `rm -rf` of protected dirs) at the harness layer.
- Reflection-log workflow ([`docs/reflection-log/`](./docs/reflection-log/))
  feeds AGENTS.md and skill rules from observed real failures.

If you find any of these defenses bypassable, please report under the policy above.
