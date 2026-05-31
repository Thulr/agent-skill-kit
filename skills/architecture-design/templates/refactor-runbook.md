# Architecture Refactor — <name>

**Target persona:** <from references/core/personas.md>
**Surfaces in scope:** <list>
**Linked findings:** <CA-... IDs, if this refactor came from an audit ledger>
**Starting state:** <one line>
**Target state:** <one line>
**Date:** <YYYY-MM-DD>

## Why this refactor

<2–4 sentences. The findings driving the refactor (cite the audit
report if one exists) and the constraint set (feature work continues,
big-bang forbidden, etc).>

## Step sequence

Each step is reversible: the system is shippable at the end of every
step. Effort is S (≤ 1 day) / M (≤ 1 week) / L (≤ 1 month).

### Step 1 — <name>

- **Effort:** <S/M/L>
- **What changes:** <one sentence>
- **Safety net:** <characterization tests, dual-write, etc.>
- **Done when:** <observable predicate>
- **Closes findings:** <CA-... IDs, or `none`>
- **If we stop here:** <what state we are in>
- **Playbook heuristic:** <playbook>#<n> (<intent>)

### Step 2 — ...

(repeat per step)

## Open questions

<Items where lenses disagreed about sequencing, or where the safety
net is uncertain.>

## Verification

<How to verify each step landed safely — tests, dependency-graph
delta, characterization-test pass rate. When linked findings exist, run a
verification closeout pass and update the ledger/workflow state only for IDs
whose checks pass.>

## Grounding sources applied

- <skill.json inspired_by entry> - <refactor sequence choice it informed>
