# ADR 0004: Shared Skill Schemas Are Canonical and Migrated Together

**Status:** Accepted (2026-05-16)

## Context

This repo has multiple skills with similarly named files that are intended to be
machine-validated and eventually machine-executed (e.g. `evals/trigger-evals.json`).

A concrete failure mode observed here: different skills evolved incompatible JSON
shapes under the same filename, which prevented writing a shared validator/runner
and caused “dead schema” (files that exist but are not trusted).

## Decision

When a file is described as "canonical" across skills, that schema is a contract:

- The canonical shapes live in [`schemas/`](../../schemas/) as JSON Schema files
  ([`skill.schema.json`](../../schemas/skill.schema.json) and
  [`trigger-evals.schema.json`](../../schemas/trigger-evals.schema.json)).
- Every skill's `evals/run-static-checks.sh` validates against the schemas via
  [`scripts/validate-against-schema.py`](../../scripts/validate-against-schema.py).
  Inline shape validators inside `run-static-checks.sh` are not allowed
  (re-introducing them recreates the drift this ADR exists to prevent).
- Per-skill assertions that vary by skill (e.g. `name == <skill-dir>`) stay in
  each skill's `run-static-checks.sh`.
- Any schema change edits the schema file (one place) and migrates every skill's
  affected data file in the same PR (no staged migrations).

## Consequences

- Schema changes are usually one edit to a single file under `schemas/`.
- Validation and future runners become practical (one contract, one implementation).
- Adds a `python3-jsonschema` dependency (apt-installed in CI, pip-installed locally).
- Avoids long-lived drift that forces human memory to substitute for tooling.

## History

- **2026-05-16:** Original decision (this ADR, PR #7). Schemas live under
  `schemas/` and are validated via `scripts/validate-against-schema.py`. Triggered
  by Copilot review of PR #7 catching duplicated maintainer-handle validators
  across four `run-static-checks.sh` files — the second occurrence of cross-skill
  validator drift after the `trigger-evals.json` `version` field gap in PR #5.

