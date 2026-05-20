# ci-runners

## Scope

This playbook covers CI runner trust and enforcement posture for agent-facing
repositories: GitHub Actions runner selection, fork-PR behavior, checkout
credentials, `GITHUB_TOKEN` permissions, environment secrets, required-check
parity, branch-protection truth claims, and whether local gates actually run in
the merge path. It is narrower than the `gates` playbook: `gates` decides what
to enforce; this playbook decides whether the CI surface is trustworthy enough
to enforce it.

## Grounding

Recent PR review exposed a P1 failure class: moving required checks from
GitHub-hosted runners to persistent self-hosted runners can execute
PR-controlled code on infrastructure that is not disposable. GitHub's Actions
security guidance says GitHub-hosted runners are ephemeral clean machines, but
self-hosted runners have no such guarantee and can be persistently compromised
by untrusted workflow code. The same risk appears on private/internal repos
where any reader can fork and open a PR, especially when `GITHUB_TOKEN` or
environment secrets are available.

The posture claim matters as much as the YAML. If AGENTS.md, SECURITY.md, or a
runbook says branch protection requires a check, the auditor must confirm the
rule is actually enabled. "Will be configured" and "is required" produce very
different agent behavior.

## Good signals

- `pull_request` workflows that execute untrusted code use GitHub-hosted or
  truly ephemeral isolated runners, not long-lived shared hosts.
- Self-hosted labels are specific (`self-hosted`, `ephemeral`, `repo-isolated`)
  and backed by an org policy; generic `self-hosted` is treated as high risk.
- Workflow permissions default to `contents: read`; write tokens and secrets
  are limited to trusted events or protected environments.
- Required checks in branch protection match the scripts listed in `just check`
  and AGENTS.md; no local-only release gate is treated as merge protection.
- CI installs are reproducible: pinned actions, pinned CLIs, retry-bounded apt
  setup, `safe.directory` handling when containers run as root.
- Docs state current enforcement honestly: planned protections are labeled
  planned until a live rule verifies them.

## Common failures

- `pull_request` runs PR code on a persistent self-hosted runner because the
  workflow migrated from `ubuntu-latest` for speed or local tool availability.
- A container or custom `HOME` is mistaken for isolation even though the host
  runner can remain compromised.
- A gate is added to `just check` but not to the required CI workflow, so
  branch protection never sees it.
- A workflow uses pinned actions but leaves `npx` or another installer floating
  at latest, changing validation behavior between PRs.
- Documentation claims branch protection, CODEOWNERS, or self-merge blocking
  before GitHub actually enforces it.

## Heuristics

- **H1** *(assess, auditor).* For every workflow triggered by `pull_request`,
  identify whether the job runs untrusted PR code and what runner label it uses.
  Persistent self-hosted runners on untrusted PRs are severity 4 unless a
  documented ephemeral isolation mechanism and fork-PR gate exist.
- **H2** *(assess, adversarial).* Audit token and secret exposure per event:
  `permissions`, persisted checkout credentials, environment secrets, and
  whether secrets are available before a human-reviewed protection rule passes.
  Treat "containerized" as insufficient if the host persists.
- **H3** *(assess, maintainer).* Compare `just check`, AGENTS.md required
  commands, repo scripts, and `.github/workflows/*.yml`. Any release gate that
  exists locally but not in required CI is a merge-path gap.
- **H4** *(harden, auditor).* Move untrusted PR jobs to GitHub-hosted runners
  or to an explicitly ephemeral, per-job self-hosted pool. If the org must use
  self-hosted runners, gate fork PRs, use read-only tokens, disable persisted
  checkout credentials, and label the residual risk.
- **H5** *(harden, maintainer).* Add a required-check parity row whenever a
  new gate lands: script name, CI job name, branch-protection status, runner
  trust level, and last verified date.
- **H6** *(scaffold, cold-agent).* When scaffolding CI docs, write enforcement
  posture in two columns: "currently enforced" and "planned / manual." Never
  let a future agent infer protection from aspirational text.
- **H7** *(diagnose, adversarial).* If CI caught a policy violation that a hook
  missed, classify it as both a hook fixture gap and a runner/trust question:
  could the same PR have modified or bypassed the CI job that caught it?

## Quick diagnostic

Run this pass before recommending CI as an enforcement layer:

1. List each workflow event (`pull_request`, `push`, `workflow_dispatch`) and
   runner label.
2. Mark whether the workflow executes PR-controlled code.
3. Record token permissions, checkout credential persistence, and secret
   access.
4. Compare required branch checks against `just check` and AGENTS.md.
5. Reword any doc that says "requires" when the live setting is only planned.

## Cross-references

- `gates.md` decides action tiers and hook/CI equivalents.
- `governance.md` owns CODEOWNERS, branch protection, SLSA, and ownership.
- `sandbox.md` covers OS/container isolation; use it when runner isolation
  depends on containers, VMs, or network egress controls.
- `evals.md` covers regression suites that should be bound into CI.
