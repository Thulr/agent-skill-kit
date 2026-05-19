---
date: 2026-05-19
harness: codex
sub-surface: skills
severity: 2
status: resolved
related:
  - 2026-05-19-clean-architecture-tracking-offer-instead-of-ledger.md
---
# Clean-architecture ledger creation lacked a concrete Markdown path

## What happened

Repeated clean-architecture audit runs did not reliably create a findings
ledger or persistent workflow state. One of three runs created a ledger, and
the ledger was not consistently saved as a Markdown file. The skill already
said threshold-triggered audits should "create" a ledger, but it did not
specify a filesystem path, a `.md` extension, a paired workflow-state JSON
file, or skill-prefixed filenames. That left agents free to inline a ledger in
the chat, offer to create one, skip workflow state, or skip the artifact.

## What to do differently

Audit skills that create tracking artifacts need a concrete artifact contract,
not just a template reference. Threshold-triggered ledgers should be written as
Markdown files under `docs/audits/`, paired workflow-state JSON should be saved
by default, and `audit-artifacts/` should be the fallback when the target is not
a repo or `docs/audits/` is not writable. Filenames should start with the skill
name, e.g.
`clean-architecture-findings-ledger-YYYY-MM-DD-scope.md` and
`clean-architecture-workflow-state-YYYY-MM-DD-scope.json`, so different audit
skills do not collide. Static checks should assert the default-save instruction,
the paired workflow-state artifact, and the filename convention.

## Closed by

Current patch. Clean-architecture now requires threshold-triggered audits to
write `docs/audits/clean-architecture-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
and
`docs/audits/clean-architecture-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
It falls back to matching `audit-artifacts/clean-architecture-...` paths when
the default directory is unavailable.
The shared trackable-findings workflow documents the skill-prefixed Markdown
ledger and workflow-state naming convention, and static checks cover the
saved-file contract.
