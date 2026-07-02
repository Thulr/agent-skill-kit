# Changelog Playbook

## Scope

The release-notes surface: `CHANGELOG.md`, GitHub release pages, registry
release notes, and the per-version "what changed" content developers consult
before upgrading. Distinct from `migration.md` (the procedural upgrade guide
between specific versions) and `package.md` (the act of installing a single
version): this playbook covers the *human-readable record of change* that
makes versions reviewable and decisions traceable. Routes to `migration.md`
for in-depth upgrade procedures, `package.md` for version-number discipline,
and `docs.md` for changelog placement in the doc IA.

## Grounding

- **Olivier Lacan — Keep a Changelog (keepachangelog.com)** — a chronological
  changelog with stable categories (Added / Changed / Deprecated / Removed /
  Fixed / Security), an Unreleased section at the top, and a version-and-date
  heading for each release. The format is conventional precisely so it is
  scannable by humans and parseable by tools.
- **Tom Preston-Werner — Semantic Versioning 2.0.0 (semver.org)** — version
  numbers carry contract meaning: MAJOR breaks, MINOR adds, PATCH fixes. The
  changelog entry for a release must explain the version number; an
  unsubstantiated MAJOR or a hidden break in a MINOR makes versioning a lie.
- **Hyrum Wright — Hyrum's Law** — integrators depend on every observable
  behavior, including things the changelog did not call out. Calling out
  what changed — even minor-looking behavioral shifts — narrows the
  surprise surface.

## Good signals

- A `CHANGELOG.md` exists at the repo root and the latest release is at the
  top.
- Each release has a version number, a release date, and entries grouped
  into stable categories (Added, Changed, Deprecated, Removed, Fixed,
  Security or the equivalent project convention).
- An "Unreleased" section sits at the top, accumulating entries between
  releases; users always have a preview of what's coming.
- Breaking changes are labeled explicitly and link to the migration guide
  for that change.
- Every entry has a one-line summary scannable in three seconds, with a
  link to a PR, issue, or commit for depth.
- Entries are written from the integrator's perspective ("renamed
  `client.list()` to `client.list_paged()`") rather than the contributor's
  ("refactor list traversal").
- The `CHANGELOG.md` is linked from the README, the docs site, and the
  registry page.
- Release tags, registry release notes, and `CHANGELOG.md` content agree
  on what shipped in that version.
- For security fixes, the entry names the CVE or advisory if one exists
  and the affected version range.

## Common failures

- No changelog at all; users read git history or release commits and infer
  what changed.
- Auto-generated commit-log dump labeled "changelog"; users get
  `chore(deps): bump foo from 1.0.0 to 1.0.1` with no integrator context.
- Breaking changes buried in the "Changed" section with no warning; users
  upgrade and find out at runtime.
- Changelog entries are written from the contributor's perspective and
  require knowing the internal module layout to interpret.
- No "Unreleased" section; users cannot see what is queued for the next
  release without trawling merged PRs.
- The git tag, registry release notes, and `CHANGELOG.md` disagree on what
  shipped — version 1.4.2 in the registry includes changes the changelog
  attributes to 1.4.3.
- Security fixes are silently rolled into a normal release with no callout,
  leaving users with no signal to prioritize the upgrade.
- Entries link to internal trackers (private Jira IDs, internal commits)
  that the public reader cannot open.
- The most recent release is six months old and the README claims active
  development; mismatch signals neglect.
- "Various improvements and bug fixes" as the only entry; the user learns
  nothing.

## Heuristics

- **Keep-a-Changelog structure** *(design, audit)* — each release has a
  version, date, and entries grouped under the stable categories. Entries
  read top-to-bottom newest-first.
- **Unreleased-at-top** *(design, audit)* — an "Unreleased" section
  accumulates entries between releases; merging a change adds an entry
  there as a matter of process.
- **Explicit breaking-change callouts** *(design, audit)* — breaking
  changes are labeled prominently (e.g., `**BREAKING:**`) and link to the
  migration guide for that change. A breaking change hidden in `Changed`
  is a contract failure.
- **Integrator-perspective entries** *(audit, design)* — entries describe
  what the user sees ("renamed `foo()` to `bar()`") rather than what the
  contributor did ("refactored foo module"). The reader is an integrator,
  not a teammate.
- **One-line scannable summary** *(design)* — every entry has a one-line
  summary readable in three seconds; depth lives in linked PRs or issues,
  not in paragraphs.
- **Three-surface parity** *(audit)* — git tags, registry release notes,
  and `CHANGELOG.md` agree on what shipped in each version; a single
  release script keeps them in sync.
- **Security callouts** *(design, audit)* — security fixes have their own
  category or label, name the CVE or advisory if one exists, and state the
  affected version range. Silent security fixes leave users exposed longer.
- **Discoverable changelog** *(audit)* — the changelog is linked from the
  README, the docs site, and the registry page. Hiding it behind navigation
  is the same as not having one for most users.
- **No internal-tracker links** *(audit)* — links resolve for the public
  reader; private Jira IDs and internal commit URLs are out-of-policy.
- **Honored version meaning** *(audit, design)* — the changelog substantiates
  the version number: a MAJOR has explicit breaking entries, a MINOR has
  Added entries, a PATCH has only Fixed entries (or matches the project's
  documented variant).

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is there a `CHANGELOG.md` at the repo root? | Users read git history | Adopt Keep a Changelog; backfill recent releases |
| Are entries grouped under stable categories? | Mixed messages, hard to scan | Adopt Added/Changed/Deprecated/Removed/Fixed/Security |
| Is there an Unreleased section at the top? | Queue invisible to users | Add an Unreleased section to the merge workflow |
| Are breaking changes labeled explicitly? | Upgrade surprises | Add `**BREAKING:**` prefix and migration link |
| Are entries written for integrators? | Internal-jargon entries | Rewrite from the user's perspective |
| Do tags, registry notes, and changelog agree? | Three-surface drift | Single release script syncs all three |
| Are security fixes called out? | Users miss critical upgrades | Add a Security category with CVE or advisory link |
| Is the changelog linked from README and docs? | Discovery failure | Add prominent links from both surfaces |

## Cross-references

- → `dev-docs.md` for where the changelog lives in the doc-site IA.
- → `readme.md` for the link that surfaces the changelog to evaluators.
- → the `dx-audit` / `dx-design` skills for the in-depth upgrade procedure
  linked from breaking-change entries (`migration`) and the semver
  discipline the changelog substantiates (`package`).
