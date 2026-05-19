---
date: 2026-05-19
harness: codex
sub-surface: skills
severity: 2
status: resolved
related: []
---
# Clean-architecture audit offered tracking choices instead of creating a ledger

## What happened

A full clean-architecture audit crossed both tracking triggers: 7+ findings and
severity 3 findings. The runtime response ended with:

> This audit has 7+ findings and Severity 3 items, so it qualifies for a findings ledger, roadmap slice, or grouped GitHub issues. I did not create anything external.

That preserved the external-issue safety boundary, but it failed the intended
default. At that point the audit should create a findings ledger, not merely
offer ledger / roadmap / issue choices. The installed skill had tracking
templates, but its `SKILL.md`, `trackable-findings.md`, and audit templates
still described an offer-first workflow. The repo source was worse: tracking
artifacts were absent, so static checks could not catch the drift.

## What to do differently

Separate internal tracking artifacts from external side effects. A threshold
trigger (7+ findings or any severity 3-4 finding) should create the findings
ledger by default. Roadmaps, workflow state, and GitHub issues remain opt-in,
and external issues still require confirmation. Static checks should require
the tracking reference, ledger template, and audit-template language that says
"create the ledger" and "do not merely offer tracking choices."

## Closed by

Current patch. Added trackable-findings and tracking templates to the source
package, changed clean-architecture runtime instructions and audit templates
from "tracking offer" to "create findings ledger," updated activation cases
and trigger evals, and added static gates for ledger-by-default behavior.
