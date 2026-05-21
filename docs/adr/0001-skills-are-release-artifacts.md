# ADR 0001: Skills Are Release Artifacts

**Status:** Accepted (2026-05-16)

## Context

This repository's product is the content under `skills/`. The
`skills/.experimental/` lane is reserved and intentionally empty for the
current release model; prerelease maturity is communicated by repository tags
such as `0.0.1-alpha`, not by shipping draft/experimental skill directories.
Downstream consumers install skills with
`npx skills add Thulr/informed-skills`, and the resulting instructions load into
agent sessions with broad permissions.

That makes changes to skill content (and the distribution surfaces around it)
meaningfully closer to “shipping production code” than “editing docs”.

## Decision

Treat any PR that changes:

- `skills/**`
- `skills/.experimental/**` if a future release explicitly reopens that lane
- `.agents/skills/**`
- `.github/**`

as a release artifact that requires production-grade review and gates.

Concrete requirements:

- `just check` must pass.
- Required reviewers are enforced via `.github/CODEOWNERS` and branch protection.

## Consequences

- Increased review overhead for skill changes.
- Lower supply-chain / prompt-injection risk (fewer unaudited edits to artifacts
  that will be executed or trusted by downstream agents).
- “Documentation” changes in these paths should be written like code: explicit,
  testable where possible, and kept consistent across skills.
