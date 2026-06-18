# Changelog

Notable changes to the informed-skills catalog. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); catalog maturity is
tracked by repository release tags (e.g. `0.0.1-alpha`), not per-skill status.

## [Unreleased]

### Changed
- **Renamed the agent-facing skills by use case** so each name states the job
  it does: `agent-experience` → `design-for-agent-users`, `agent-readiness` →
  `harden-repo-for-coding-agents`, and `agent-rules` → `rules-from-coding-agent-failures`
  (`agent-evals` unchanged). The old `--skill agent-experience`,
  `--skill agent-readiness`, and `--skill agent-rules` install commands no
  longer resolve — install the new names instead. Emitted audit-artifact
  filename prefixes moved with them (e.g.
  `agent-readiness-findings-ledger-*` → `harden-repo-for-coding-agents-findings-ledger-*`,
  `agent-rules-findings-ledger-*` → `rules-from-coding-agent-failures-findings-ledger-*`).
  Discipline concepts (`agent experience`/AX, the noun "agent-readiness")
  keep their names. Resolves the rename half of finding DX-MA-04. (See the
  rename notes on [ADR 0005–0008](./docs/adr/0006-discipline-front-doors-vs-one-engine-many-surfaces.md)
  and [`docs/runbooks/renaming-or-removing-a-skill.md`](./docs/runbooks/renaming-or-removing-a-skill.md).)
- **Split `review-heuristics` into 12 per-domain × per-function skills:**
  `dx-audit`/`dx-design`, `docs-audit`/`docs-design`,
  `perf-audit`/`perf-design`, `test-audit`/`test-design`, `ux-audit`,
  `ui-design`, and `architecture-audit`/`architecture-design`. An `-audit`
  skill audits/debugs an existing surface; a `-design` skill shapes a new one.
  (See [ADR 0008](./docs/adr/0008-reverse-review-consolidation-split-by-domain-and-function.md).)
- **Named the review half of each pair `-audit`** (not `-critique`), so the
  skill name carries its function in plain software vocabulary:
  `dx-audit`, `docs-audit`, `perf-audit`, `test-audit`, `ux-audit`,
  `architecture-audit`.
- **Grouped the agent-facing family under a shared `agent-` prefix:**
  `agent-experience` (umbrella — design/review software, docs, SDKs, repos so
  AI agents can consume them), `agent-readiness` (assess/harden/scaffold a
  repo's agent-readiness; was `project-agentification`), `agent-rules`
  (promote observed agent failures into rules/gates), and `agent-evals`
  (instrument an AI product's eval/optimization loops).
- CI `static-checks` now runs on a GitHub-hosted runner; the previous
  self-hosted runner had stopped reporting, leaving the required check dead.

### Removed
- The `review-heuristics` skill and its `--skill review-heuristics` install
  command. Install the per-domain skills instead — e.g.
  `npx skills add Thulr/informed-skills --skill dx-audit --skill dx-design`.

### Added
- `CHANGELOG.md` (this file) and `CONTRIBUTING.md`.

## [0.0.1-alpha]

- Initial published catalog of source-grounded Agent Skills.
