# ADR 0004: Shared Skill Schemas Are Canonical and Migrated Together

**Status:** Accepted (2026-05-16)

## Context

This repo has multiple skills with similarly named files that are intended to be
machine-validated and eventually machine-executed (e.g. `evals/trigger-evals.json`).

A concrete failure mode observed here: different skills evolved incompatible JSON
shapes under the same filename, which prevented writing a shared validator/runner
and caused “dead schema” (files that exist but are not trusted).

## Decision

When a file is described as “canonical” across skills (e.g. the `trigger-evals.json`
schema in `AGENTS.md`), that schema is a contract:

- Every skill uses the same shape.
- Every skill's `evals/run-static-checks.sh` enforces the documented contract.
- Any schema change migrates every skill in the same PR (no staged migrations).

## Consequences

- Schema changes are more work up front (migrate everything immediately).
- Validation and future runners become practical (one contract, one implementation).
- Avoids long-lived drift that forces human memory to substitute for tooling.

