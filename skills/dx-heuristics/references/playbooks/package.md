# Package Playbook

## Scope

How the project is distributed and consumed as a package: registry metadata
(npm, PyPI, crates, Maven, Homebrew), semver discipline, declared and peer
dependencies, install footprint, type definitions, source maps, lockfile and
provenance hygiene, and supply-chain surface. Distinct from `setup.md` (the
first-run experience after install) and `migration.md` (the upgrade path
between versions): this playbook covers the act of installing one version
cleanly. Routes to `setup.md` for first-run experience, `migration.md` for
upgrade paths, `readme.md` for registry-page metadata, and `auth.md` for
publish-credential hygiene.

## Grounding

- **Tom Preston-Werner — *Semantic Versioning 2.0.0* (semver.org)** — MAJOR.
  MINOR.PATCH with strict rules: breaking changes bump MAJOR, additions bump
  MINOR, fixes bump PATCH. The contract is what integrators rely on; quiet
  breaks in a MINOR or PATCH are an interface failure, not a labeling
  oversight.
- **Hyrum Wright — Hyrum's Law** — every observable behavior of a package,
  including transitive dependencies, lockfile shape, and install side
  effects, gets depended on by some integrator. Treat install behavior as a
  contract, not an implementation detail.
- **OpenSSF — Supply-chain Levels for Software Artifacts (SLSA) and npm /
  PyPI publishing guides** — provenance, signed releases, two-factor
  authentication on publish credentials, immutable version tags, and
  reproducible builds as baseline practice for any package that other people
  install.

## Good signals

- Versions follow semver and the MAJOR / MINOR / PATCH meaning is honored
  consistently across releases.
- Every release is tagged in git with the same version string the registry
  publishes; the tag and the package contents agree.
- Peer dependencies (or the language equivalent) are declared explicitly,
  with stated supported ranges, not silently bundled or assumed.
- Install footprint is measured in CI and gated against a documented
  ceiling; growth requires deliberate review.
- The package ships TypeScript declarations, Python type stubs, or
  equivalent type information without a separate install step.
- Source maps (or readable source) ship in the package so jump-to-definition
  resolves to something useful, not stripped output.
- The registry page metadata (`README`, `homepage`, `repository`, `license`,
  `keywords`) is filled in and matches the repo.
- Publish credentials require two-factor authentication; release provenance
  is signed where the registry supports it.
- Lockfile is committed for applications and not committed for libraries
  (or follows the language's convention); the choice is deliberate and
  documented.
- A documented uninstall removes everything the install added — binaries,
  config dirs, cached files.

## Common failures

- Breaking changes shipped in a MINOR or PATCH version; integrators bitten
  by silent semver violations stop trusting upgrade ranges.
- Git tag and registry version drift apart; users cannot trace a published
  version back to a specific commit.
- Peer dependencies are not declared; the package silently demands a
  specific framework version and fails at runtime with a confusing error.
- Install pulls in hundreds of megabytes of transitive dependencies with no
  ceiling, no review, and no awareness.
- TypeScript or type-stub support is shipped in a separate `@types/` package
  with its own version and lifecycle; user has to install two things and
  they drift.
- Source maps are stripped to save bytes; jump-to-definition lands on
  minified output and the integrator cannot read the source.
- The registry page shows "no description" or a generic placeholder because
  the publish step did not copy the README or fill in metadata.
- A maintainer's personal account is the sole publisher; if it is
  compromised or the maintainer leaves, the package cannot be updated.
- Lockfile is committed for a library, freezing transitive choices for every
  consumer; or no lockfile is committed for an application and "works on my
  machine" becomes the norm.
- The package is unpublished or yanked without a deprecation notice;
  consumers wake up to broken installs.

## Heuristics

- **Honest semver** *(audit, design)* — MAJOR / MINOR / PATCH match the
  actual contract change; integrators can safely use a caret or tilde range.
  Breaking changes never ship below a MAJOR bump.
- **Tag-registry parity** *(audit)* — every published version has a matching
  git tag and the tagged commit produces the package contents. Provenance is
  traceable from registry back to source.
- **Declared peer deps** *(design, audit)* — peer dependencies are listed
  with supported ranges, the install fails fast on mismatch, and the
  error names the expected range.
- **Install-size budget** *(audit, design)* — install footprint and bundle
  size are measured in CI; a documented ceiling exists and growth above the
  ceiling requires explicit approval.
- **Types in the box** *(design, audit)* — type definitions ship inside the
  primary package, not as a separate community-maintained package. One
  install gives the user types.
- **Readable jump-to-source** *(audit)* — published artifacts include source
  maps or readable source so IDE jump-to-definition lands somewhere the
  integrator can actually read.
- **Registry-page parity** *(audit)* — the registry page (npm, PyPI, crates)
  carries the README, license, homepage, and repository URL — what an
  evaluator sees on the registry matches what they see in the repo.
- **Two-factor publish** *(design, audit)* — publishing requires 2FA and
  release provenance is signed where the registry supports it; no single
  compromised credential can ship a malicious version.
- **Multi-publisher** *(audit)* — at least two maintainers can publish; a
  documented escalation path covers the case where the primary maintainer is
  unavailable.
- **Deliberate lockfile policy** *(audit)* — the lockfile choice (commit for
  apps, omit for libraries, or follow language convention) is deliberate and
  documented in `CONTRIBUTING.md`.
- **Deprecation over unpublish** *(design)* — replaced or abandoned packages
  carry a deprecation notice with a pointer to the successor; outright
  unpublish is reserved for security incidents and announced.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does versioning honor semver in practice? | Silent breaks erode trust | Audit recent releases; bump MAJOR when contract breaks |
| Do git tags and registry versions match? | Provenance gap | Add a release script that tags and publishes atomically |
| Are peer deps declared with ranges? | Runtime mismatch surprises | Move implicit framework deps to peer deps |
| Is install footprint measured in CI? | Bloat creeps in | Add a size check with a documented ceiling |
| Does the package ship types in the box? | Two-package drift | Bundle type definitions with the main package |
| Does the registry page show the README? | "No description" page | Fix the publish step to push README and metadata |
| Is publish protected by 2FA and provenance? | Single credential = full compromise | Enable 2FA; sign releases where supported |
| Is the lockfile policy documented? | Tribal knowledge or accidental drift | Document the choice in `CONTRIBUTING.md` |

## Cross-references

- → `setup.md` for the first-run experience after install.
- → `migration.md` for upgrade paths and deprecation lifecycle.
- → `readme.md` for the registry-page metadata that mirrors the README.
- → `auth.md` for publish-credential hygiene (2FA, rotation).
- → `ide.md` for type-definition and source-map consumption in editors.
