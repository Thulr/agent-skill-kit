---
date: 2026-06-03
harness: claude-code
sub-surface: skills
severity: 2
status: open
related: ["2026-06-03-skilljson-skillmd-description-divergence"]
---
# Audit-family intent-router IDs and CSV schema diverge across six skills

## What happened

A cross-skill consistency audit (this session, reading every
`references/intent-router.csv`) found the six audit skills do not share an intent
vocabulary or, in one case, a CSV schema. No agent tripped in production — this was
surfaced by audit, not by a failure; behavior within each skill is correct. The gap
is in the shared *contract* a router, eval harness, or template-copying contributor
would reasonably assume.

- **Broad-scan intent named inconsistently.** `architecture-audit`, `docs-audit`,
  `dx-audit`, `perf-audit` name it `audit`; `test-audit/references/intent-router.csv:2`
  names it `review` while its own gloss reads "Audit existing tests…" — the ID and
  the gloss word are swapped relative to the four siblings.
- **Single-item intent named three ways for one shape.** "investigate one
  failing/slow/broken item" is `debug` (`docs-audit`, `dx-audit`), `diagnose`
  (`perf-audit`, `writing-audit`), and `triage` (`test-audit`).
- **CSV schema mismatch.** Five skills use columns
  `intent,name,when_to_use,registry_file,default_template`; `ux-audit`'s
  `references/intent-router.csv` uses `intent,trigger_examples,detail_files,templates,notes`.
  A script that parses these routers uniformly breaks on ux-audit.

## What to do differently

The smallest fix is a per-skill standardization (rename `test-audit`'s `review`
intent → `audit`; pick one name per shape for `debug`/`diagnose`/`triage`; converge
ux-audit's CSV onto the 5-column schema). Each cascades into
`references/intents/<intent>.csv`, the default template, `run-static-checks.sh`
(which asserts the exact intent set per skill), and `activation-cases.md` — so it is
a real multi-file change per skill, not a one-liner. `triage` (tests) and `diagnose`
(perf) are defensible domain idiom; the genuinely un-reconciled bits are the
`audit`↔`review` swap and the `debug`↔`diagnose` split for one shape.

This is **one** observation — below the W1 ≥3 promotion floor (record, don't
scaffold). Promote (a CI gate asserting a shared intent-router column schema + an
allowed-intent vocabulary) only if ≥2 more intent-router inconsistencies surface.
Found alongside the sibling metadata-uniformity gap in
`2026-06-03-skilljson-skillmd-description-divergence`.

## Closed by

Not yet closed.
