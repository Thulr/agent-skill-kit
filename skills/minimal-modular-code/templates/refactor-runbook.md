# Minimal Modular Code — REFACTOR — <name>

**Target persona:** <from references/core/personas.md> (often Persona D)
**Surfaces in scope:** <list>
**Linked findings:** <MM-... IDs, if this came from a REVIEW ledger>
**Starting state:** <one line>
**Target state:** <one line>
**Date:** <YYYY-MM-DD>

## Why this refactor

<2–4 sentences: the findings driving it (cite the audit report if one exists) and the
constraint set (feature work continues, big-bang forbidden, every step reversible).>

## Step sequence

Each step is reversible: the system is shippable at the end of every step. Effort is
S (≤ 1 day) / M (≤ 1 week) / L (≤ 1 month).

### Step 1 — <name>

- **Effort:** <S/M/L>
- **What changes:** <one sentence>
- **Safety net:** <characterization tests, parallel-change/dual-write, branch-by-abstraction>
- **Done when:** <observable predicate>
- **Closes findings:** <MM-... IDs, or `none`>
- **If we stop here:** <what state we are left in — must be shippable>
- **Playbook heuristic:** <playbook>#<n> (<intent>)

### Step 2 — ...

(repeat per step)

## Open questions

<Where the safety net is uncertain, or where sequencing is contested.>

## Verification

<How to verify each step landed safely — tests, a dependency-graph delta,
characterization-test pass rate. When linked findings exist, run a verification closeout pass
and update the ledger / workflow state only for IDs whose checks pass.>

## Grounding sources applied

- <skill.json inspired_by entry> — <refactor-sequence choice it informed>
