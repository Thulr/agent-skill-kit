# Architecture

Durable reference for **how the catalog is organized and where things live** —
the "what" in the [`docs/` Diátaxis map](../README.md). For path-level detail see
`AGENTS.md` §Layout and the repo `README.md` §Layout; this doc is the conceptual
map those tables don't give you.

## Skill taxonomy

Published skills fall into three shapes:

- **Per-domain audit/design pairs** — a `<domain>-audit` skill audits/debugs
  an existing surface (lenses → severity-scored findings + optional ledger); a
  `<domain>-design` skill shapes a new one (good-shaped pattern → design doc).
  Domains: `docs`, `dx`, `perf`, `test`, `writing`. A domain's pair shares
  its playbooks/lenses/rubrics from `skills/_shared/<domain>/` (one source, two
  skills). See [ADR 0008](../adr/0008-reverse-review-consolidation-split-by-domain-and-function.md).
- **Single-function skills** — `ux-audit` (audit only) and `ui-design`
  (build/polish only) are domains that only do one side; `minimal-modular-code`
  is a single skill spanning review and design for code minimality and
  parallel-readiness (it replaced the former `architecture` pair — see
  [ADR 0009](../adr/0009-replace-architecture-pair-with-minimal-modular-code.md)).
- **Agent-mirror family** — agent-facing work organized by *actor* (an agent is an
  actor, not a peer audience): `agent-dx` / `agent-docs` / `agent-ux` / `agent-ops` /
  `agent-test`, with `agent-ops` the front-door routing to the standalone arms
  `harden-repo-for-coding-agents` and `rules-from-coding-agent-failures`
  (see [ADR 0011](../adr/0011-actor-axis-agent-mirror-family.md));
  `research` is one skill routed by decision-frame (`report` | `opportunity`).

`ux`/`dx`/agent-experience are **audience-differentiated peers** of one parent
discipline, not nested ([ADR 0007](../adr/0007-experience-disciplines-are-audience-peers.md)).

## Install lanes

Three lanes; every path-based gate must cover all three (AGENTS.md Rule 1):

- `skills/<name>/` — published, installable skills (the product).
- `skills/.experimental/<name>/` — reserved lane, kept empty for now.
- `.agents/skills/<name>/` — repo-local authoring/review skills
  (`skill-curator`, `skill-reviewer`), mirrored to
  `.claude/skills/` for Claude Code.

`skills/_shared/` holds cross-skill primitives — catalog-wide singletons
(`lenses.md`, `modes.md`, `empirical-warnings.md`, `trackable-findings.md`,
templates) plus per-domain subtrees (`_shared/<domain>/`). Consumers symlink
them; `npx skills` dereferences at install, so installed skills are
self-contained. Enforced by `scripts/check-shared-content.sh`.

## Validation model

`just check` (and the `static-checks` CI job) run, across all three lanes:
install discovery, the release-contract + JSON-schema checks, instruction-surface
and shared-content symlink checks, routing-CSV well-formedness, the doc-link
check, the destructive-bash hook tests, and every skill's
`evals/run-static-checks.sh`. CI runs on a GitHub-hosted runner.

## Where each kind of knowledge lives

| Need | Location |
|---|---|
| Why a non-obvious decision was made | [`docs/adr/`](../adr/) |
| How to perform a maintainer procedure | [`docs/runbooks/`](../runbooks/) |
| Intent/constraints for a significant change | [`docs/specs/`](../specs/) |
| Observed agent failures (evidence for rules) | [`docs/reflection-log/`](../reflection-log/) |
| Curated index for AI agents | `llms.txt` / `llms-full.txt` (repo root) |
| Hand-curated agent instructions | `AGENTS.md` (repo root) |
| Notable changes / renames / removals | [`CHANGELOG.md`](../../CHANGELOG.md) |
