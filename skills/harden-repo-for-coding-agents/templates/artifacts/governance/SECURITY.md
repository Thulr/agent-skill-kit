<!-- TEMPLATE — SECURITY.md disclosure-path skeleton.

     Prescribed by governance scaffold. Required because:
     - Skill files, AGENTS.md, and hooks load into downstream agent
       sessions; treat them as production code (W5 attack surface).
     - GitHub Security Advisories is the standard private-disclosure
       channel; calling it out explicitly removes ambiguity for
       researchers and contributors.

     Be honest about enforcement state — do NOT claim branch protection
     is active if the GitHub rule has not yet been enabled (Copilot review
     of PR #5 caught this in our seed project). -->

# Security policy — <project-name>

## Reporting a vulnerability

Use **GitHub Security Advisories** to report a vulnerability privately:
<https://github.com/<owner>/<repo>/security/advisories/new>.

Do **not** open a public issue or PR for unpatched vulnerabilities.

We aim to acknowledge reports within <N> business days and to publish
fixes / advisories within <N> days for critical issues and <N> days for
lower-severity issues.

## In-scope

<!-- Tailor this list to your project. Defaults for an agent-surface repo: -->

- **Prompt injection** in skills, `AGENTS.md`, or any file an agent loads
  at session start.
- **Malicious skill PRs** — a contributor submits a skill that exfiltrates
  data, escalates privilege, or chains tool calls in unsafe ways.
- **Static-check bypass** — a path that lets a skill ship without passing
  the gates documented in `AGENTS.md`.
- **Supply-chain trust gaps** — unverified dependencies, missing
  attestations, ownership ambiguity.

## Out of scope

- Issues in dependencies you don't control. Report those upstream.
- Hypothetical risks without a demonstrated exploit path.

## What to include in a report

- A clear description of the vulnerability.
- A minimal reproduction (commands, files, expected vs actual behavior).
- The skill version (`skills/<name>/skill.json` `version` field, if present)
  and commit SHA you tested against.
- Suggested mitigation, if you have one.

## Defenses already in place

<!-- Be honest. List ONLY defenses that are actually wired today. Do NOT
     overstate. The Copilot review of our seed project flagged this exact
     pattern (asserting branch protection that wasn't yet enabled). -->

- <Defense 1, e.g., `.github/CODEOWNERS` requires review on agent-surface paths.>
- <Defense 2, e.g., per-skill static checks (`evals/run-static-checks.sh`)
  gate on SKILL.md structure, skill.json provenance, and source-author leakage.>
- <Defense 3, e.g., `.claude/hooks/<hook>.py` blocks destructive Bash actions
  at the harness layer; tested in CI.>
- Branch protection on `main` <"is being configured to require CI + at least
  one code-owner approval" — only state "is required" once the GitHub rule
  is enabled>. Until enabled, `CODEOWNERS` is documentation-only.
- Reflection-log workflow ([`docs/reflection-log/`](./docs/reflection-log/))
  captures and routes agent failures (one file per failure) so they become
  CI gates rather than recurring incidents.

## See also

- <pointers to relevant audit docs, threat models, or governance pages>.
