# ci-runners

## What it is

CI runner posture is the trust model for checks that agents rely on before
code can merge. This surface covers GitHub Actions runner selection,
fork-PR behavior, checkout credentials, `GITHUB_TOKEN` permissions,
environment secrets, required-check parity, and whether documentation claims
match live branch-protection settings.

It is narrower than `gates.md`: gates decide what to enforce; CI runners decide
whether the enforcement path is trustworthy enough to run that gate. A perfect
static check run on a persistent self-hosted runner can still be unsafe if
untrusted PR code can persist on the host, read state from prior jobs, or alter
the same workflow that will later be trusted as a required check.

The central distinction is disposable vs. persistent execution. GitHub-hosted
runners are created for a job and discarded afterward. Self-hosted runners can
be secure, but only when the organization makes isolation explicit: ephemeral
per-job machines, repo-scoped pools, no broad host access, read-only tokens for
untrusted events, and a reviewed fork-PR path. Generic `self-hosted` labels on
`pull_request` workflows are a high-risk default for agent-facing repositories.

## Why it matters for agents

Agents read AGENTS.md, runbooks, and PR status checks as operational truth. If
the docs say "branch protection requires static-checks" but the rule is not
actually enabled, an agent will treat an aspirational policy as a hard gate. If
CI says a check passed on a compromised runner, the agent may close findings,
merge follow-up changes, or tell a maintainer the repository is protected when
it is not.

Runner trust is also where local safety and merge safety diverge. A repository
can have strong local hooks and `just check`, but those are diagnostics unless
CI runs the same gates in the protected merge path. Conversely, CI can catch
violations that hooks miss, but only if PR-controlled code cannot modify or
bypass the check before branch protection evaluates it.

Good signals:

- `pull_request` workflows that execute untrusted code use GitHub-hosted or
  truly ephemeral isolated runners.
- Self-hosted labels are specific, such as `self-hosted`, `ephemeral`, and
  `repo-isolated`, and backed by org policy.
- Workflow permissions default to `contents: read`; write tokens and secrets
  are restricted to trusted events or protected environments.
- Checkout does not persist credentials unless the job needs them.
- Required checks in branch protection match `just check`, AGENTS.md, and the
  release runbook.
- CI install steps are reproducible: pinned actions, pinned CLIs where
  practical, retry-bounded package installs, and explicit `safe.directory`
  handling when containers run as root.
- Docs distinguish "currently enforced" from "planned" or "manual".

Common failures:

- A `pull_request` workflow runs PR code on a persistent self-hosted runner
  because the team migrated from `ubuntu-latest` for speed.
- A container or custom `HOME` is treated as isolation even though the host
  runner persists across untrusted jobs.
- A gate lands in `just check` but not in required CI, so branch protection
  never sees it.
- A workflow pins actions but leaves `npx` or another installer floating at
  latest, changing validation behavior between PRs.
- Documentation claims CODEOWNERS, branch protection, self-merge blocking, or
  required checks before the live GitHub settings enforce them.

## Heuristics by intent

### assess

- **H1.** Inventory every workflow event (`pull_request`, `pull_request_target`,
  `push`, `workflow_dispatch`) and runner label. Mark whether the job executes
  PR-controlled code. Persistent self-hosted runners on untrusted PR code are
  severity 4 unless there is documented ephemeral isolation and fork gating.
- **H2.** Audit token and secret exposure per event: `permissions`,
  `persist-credentials`, environment secrets, package registry tokens, cloud
  credentials, and whether secrets are available before human review.
- **H3.** Compare `just check`, AGENTS.md, runbooks, and
  `.github/workflows/*.yml`. Any release gate listed locally but absent from
  required CI is a merge-path gap.
- **H4.** Verify live branch protection before repeating truth claims. If the
  repo says a check is required, confirm the exact status-check name appears in
  the protected-branch rule.

### harden

- **H1.** Move untrusted PR jobs to GitHub-hosted runners or an explicitly
  ephemeral, per-job self-hosted pool. If self-hosted is mandatory, gate fork
  PRs, use read-only tokens, disable persisted checkout credentials, and write
  the residual risk into the runbook.
- **H2.** Add a required-check parity row for every new gate: script name, CI
  job name, branch-protection status, runner trust level, last verified date,
  and owner.
- **H3.** Split trusted publishing jobs from untrusted validation jobs. Use
  `push` to protected branches, environments, or manual approval for secretful
  work; keep `pull_request` validation secretless.
- **H4.** Pin reusable workflow dependencies enough that a future agent can
  reproduce failures. Where floating package execution remains, record the
  reason and the expected failure mode.

### scaffold

- **H1.** Scaffold CI docs with two columns: "currently enforced" and "planned
  or manual." Never let a generated AGENTS.md imply branch protection exists
  before a live check confirms it.
- **H2.** Include a runner-trust table in new agent-ready repos: workflow,
  event, runner label, executes PR code, token permissions, secret access,
  required-check name, and branch-protection status.
- **H3.** When adding a gate scaffold, wire both the local command and the CI
  job in the same bundle. A local-only gate is a developer aid, not a merge
  control.

### diagnose

- **H1.** CI caught a policy violation that hooks missed -> classify both the
  missing hook fixture and the CI trust path. Could the PR have modified or
  bypassed the workflow that caught it?
- **H2.** Required check missing in GitHub despite passing local checks -> map
  status-check name drift, workflow rename, branch-protection configuration,
  and whether the job is skipped for the PR event.
- **H3.** Self-hosted runner incident or suspicious artifact -> assume
  persistence until proven otherwise. Rotate credentials exposed to the runner,
  rebuild the host, and move untrusted jobs to disposable runners.
- **H4.** Agent closed a finding based on a merged PR -> reopen unless the
  workflow-state verification rule was rerun on a trustworthy required check.

## Sources

- GitHub Actions security hardening guidance: token permissions, fork PR risk,
  self-hosted runner cautions, and secret handling.
- GitHub-hosted runner documentation: clean ephemeral runner model.
- GitHub branch-protection documentation: required status checks and protected
  branch enforcement.
- `gates.md` for action-tier enforcement and hook/CI equivalents.
- `governance.md` for CODEOWNERS, branch protection, and ownership truth
  claims.
- `sandbox.md` for OS/container isolation when runner trust depends on VMs or
  containers.
- `evals.md` for regression suites that must be bound into required CI.
