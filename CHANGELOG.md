# Changelog

Notable changes to the informed-skills catalog. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); catalog maturity is
tracked by repository release tags (e.g. `0.0.1-alpha`), not per-skill status.

## [Unreleased]

### Changed
- **Split `review-heuristics` into 12 per-domain × per-function skills:**
  `dx-critique`/`dx-design`, `docs-critique`/`docs-design`,
  `perf-critique`/`perf-design`, `test-critique`/`test-design`, `ux-critique`,
  `ui-design`, and `architecture-critique`/`architecture-design`. A `-critique`
  skill audits/debugs an existing surface; a `-design` skill shapes a new one.
  (See [ADR 0008](./docs/adr/0008-reverse-review-consolidation-split-by-domain-and-function.md).)
- **Renamed `agent-experience` → `design-for-agents`** (design/review software,
  docs, SDKs, and repos so AI agents can consume them).
- **Renamed `project-agentification` → `codebase-agent-readiness`** (assess,
  harden, scaffold a repo's agent-readiness).
- CI `static-checks` now runs on a GitHub-hosted runner; the previous
  self-hosted runner had stopped reporting, leaving the required check dead.

### Removed
- The `review-heuristics` skill and its `--skill review-heuristics` install
  command. Install the per-domain skills instead — e.g.
  `npx skills add Thulr/informed-skills --skill dx-critique --skill dx-design`.

### Added
- `CHANGELOG.md` (this file) and `CONTRIBUTING.md`.

## [0.0.1-alpha]

- Initial published catalog of source-grounded Agent Skills.
