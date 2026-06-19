# Package Playbook

## Scope

How the project is distributed and consumed as a package: registry metadata
(npm, PyPI, crates, Maven, Homebrew), semver discipline, declared and peer
dependencies, install footprint, type definitions, source maps, lockfile and
provenance hygiene, and supply-chain surface. This playbook covers installing
one version cleanly; it routes to `setup.md` for the first-run experience,
`migration.md` for upgrade paths, `readme.md` for registry-page metadata, and
`auth.md` for publish-credential hygiene.

## Grounding

- **Tom Preston-Werner — *Semantic Versioning 2.0.0* (semver.org)** — MAJOR.
  MINOR.PATCH with strict rules: breaking changes bump MAJOR, additions MINOR,
  fixes PATCH. The contract is what integrators rely on; quiet breaks in a
  MINOR or PATCH are an interface failure, not a labeling oversight.
- **Hyrum Wright — Hyrum's Law** — every observable behavior of a package
  (transitive dependencies, lockfile shape, install side effects) gets
  depended on by some integrator. Treat install behavior as a contract, not an
  implementation detail.
- **OpenSSF — Supply-chain Levels for Software Artifacts (SLSA) and npm /
  PyPI publishing guides** — provenance, signed releases, 2FA on publish
  credentials, immutable version tags, and reproducible builds as baseline
  practice for any package others install.

## Good signals

- Versions follow semver and MAJOR / MINOR / PATCH meaning is honored
  consistently across releases.
- Every release is git-tagged with the version string the registry publishes;
  tag and package contents agree.
- Peer dependencies (or the language equivalent) are declared explicitly with
  stated ranges, not silently bundled or assumed.
- Install footprint is measured in CI and gated against a documented ceiling.
- Consumers can import a subset via granular entry points; tree-shakeability
  is verified, not assumed.
- Documented version floors and prerequisites match the manifest, checked in
  CI rather than by hand.
- The package ships TypeScript declarations, Python type stubs, or equivalent
  type information without a separate install step.
- Source maps (or readable source) ship so jump-to-definition resolves to
  something useful, not stripped output.
- Registry-page metadata (`README`, `homepage`, `repository`, `license`,
  `keywords`) is filled in and matches the repo.
- Publish credentials require 2FA; release provenance is signed where the
  registry supports it.
- The lockfile choice (commit for apps, omit for libraries, or language
  convention) is deliberate and documented.
- A documented uninstall removes everything the install added — binaries,
  config dirs, caches.

## Common failures

- Breaking changes shipped in a MINOR or PATCH; integrators bitten by silent
  semver violations stop trusting upgrade ranges.
- Git tag and registry version drift apart; users cannot trace a published
  version back to a specific commit.
- Peer dependencies are undeclared; the package silently demands a specific
  framework version and fails at runtime with a confusing error.
- Install pulls in hundreds of megabytes of transitive dependencies with no
  ceiling or review.
- The README's stated minimum version contradicts the manifest, so installs
  pass discovery then fail late on an unsupported runtime.
- Floating ranges and an ungated lockfile let a freshly published (possibly
  compromised) transitive release land in a clean install, with no age floor
  and `postinstall` scripts running unchecked.
- Type support ships in a separate `@types/` package with its own version
  and lifecycle; the user installs two things and they drift.
- Source maps are stripped to save bytes; jump-to-definition lands on
  minified output the integrator cannot read.
- The registry page shows "no description" because the publish step did not
  copy the README or fill in metadata.
- A maintainer's personal account is the sole publisher; if compromised or the
  maintainer leaves, the package cannot ship updates.
- The lockfile is committed for a library, freezing transitive choices for
  every consumer; or omitted for an application, so "works on my machine"
  becomes the norm.
- The package is unpublished or yanked without a deprecation notice; consumers
  wake to broken installs.

## Heuristics

- **Honest semver** *(audit, design)* — MAJOR / MINOR / PATCH match the actual
  contract change; integrators can safely use a caret or tilde range. Breaking
  changes never ship below a MAJOR bump.
- **Install-size budget** *(audit, design)* — install footprint and bundle
  size are measured in CI against a documented ceiling; growth above it
  requires explicit approval.
- **Tag-registry parity** *(audit)* — every published version has a matching
  git tag whose commit produces the package contents; provenance is traceable
  from registry back to source.
- **Declared peer deps** *(design, audit)* — peer dependencies are listed with
  supported ranges; the install fails fast on mismatch and the error names the
  expected range.
- **Right-sized distributable** *(design, audit)* — size-constrained consumers
  can take a subset, not the whole library: granular entry points (subpath
  exports / submodules) and verified tree-shakeability (`sideEffects` correct,
  ESM, a bundle check proving dead code drops). This is the *shape* lever;
  install-size budget is the *measure-and-gate* lever.
- **Manifest-doc agreement** *(audit)* — documented version floors, engine
  ranges, and prerequisite counts match the authoritative manifest
  (`pyproject.toml` / `package.json` / `Cargo.toml`) exactly. A README saying
  "Python 3.8+" over a manifest pinned `>=3.10` is a DX defect class — it sends
  consumers down installs that fail late. Assert the match in CI, or generate
  the doc claim from the manifest.
- **Install-integrity floor** *(design, audit)* — operational supply-chain
  baseline: exact pins (`save-exact`, no floating ranges); the lockfile is
  ground truth, gated in CI on drift; an embedded `npm-shrinkwrap.json` freezes
  the tree end-users resolve; `--ignore-scripts` by default so a transitive
  `postinstall` cannot run on install; and scheduled `npm audit` / `npm audit
  signatures`. Adapt tool names per ecosystem; the controls are general.
- **Release-age cooldown** *(design, audit)* — installs prefer versions public
  for a minimum age, filtering out a compromised just-published release before
  it reaches builds. npm's `min-release-age` is in **days** (default `null` /
  off; from npm 11.10.0); pnpm's `minimumReleaseAge` is in **minutes** (default
  `1440` ≈ 1 day since pnpm v11). Mind the unit difference — set the floor per
  tool.
- **Publish-granularity segmentation** *(design, audit)* — in a monorepo,
  shape *published-artifact* boundaries by responsibility layer (e.g. core /
  CLI / framework-integration under one namespace) so a consumer depends only
  on the layer it needs. This is about what ships as separate packages;
  internal module design stays out of scope.
- **Types in the box** *(design, audit)* — type definitions ship inside the
  primary package, not as a separate community-maintained one. One install
  gives the user types.
- **Readable jump-to-source** *(audit)* — published artifacts include source
  maps or readable source so IDE jump-to-definition lands where the integrator
  can read.
- **Registry-page parity** *(audit)* — the registry page (npm, PyPI, crates)
  carries the README, license, homepage, and repository URL; what an evaluator
  sees there matches the repo.
- **Two-factor publish** *(design, audit)* — publishing requires 2FA and
  provenance is signed where supported; no single compromised credential can
  ship a malicious version.
- **Multi-publisher** *(audit)* — at least two maintainers can publish, with a
  documented path when the primary is unavailable.
- **Deliberate lockfile policy** *(audit)* — the lockfile choice (commit for
  apps, omit for libraries, or follow language convention) is documented in
  `CONTRIBUTING.md`.
- **Deprecation over unpublish** *(design)* — replaced or abandoned packages
  carry a deprecation notice pointing to the successor; outright unpublish is
  reserved for security incidents and announced.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does versioning honor semver in practice? | Silent breaks erode trust | Audit recent releases; bump MAJOR when the contract breaks |
| Do git tags and registry versions match? | Provenance gap | Tag and publish atomically in a release script |
| Are peer deps declared with ranges? | Runtime mismatch surprises | Move implicit framework deps to peer deps |
| Is install footprint measured in CI? | Bloat creeps in | Add a size check with a documented ceiling |
| Can consumers take a subset / is tree-shaking verified? | Whole library forced on everyone | Add subpath exports; verify dead-code drop |
| Do README version floors match the manifest? | Late install failures | Assert the match in CI or generate it from the manifest |
| Pins exact, lockfile gated, scripts off, audits scheduled? | Supply-chain exposure on install | save-exact, gate the lockfile, default --ignore-scripts, schedule audit signatures |
| Does the package ship types in the box? | Two-package drift | Bundle type definitions with the main package |
| Does the registry page show the README? | "No description" page | Fix the publish step to push README and metadata |
| Is publish protected by 2FA and provenance? | Single credential = full compromise | Enable 2FA; sign releases where supported |
| Is the lockfile policy documented? | Tribal knowledge or drift | Document the choice in `CONTRIBUTING.md` |

## Cross-references

- → `setup.md` for the first-run experience after install.
- → `migration.md` for upgrade paths and deprecation lifecycle.
- → `readme.md` for the registry-page metadata that mirrors the README.
- → `auth.md` for publish-credential hygiene (2FA, rotation).
- → `ide.md` for type-definition and source-map consumption in editors.
