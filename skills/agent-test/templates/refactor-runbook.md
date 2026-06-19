# Agent Test — HARDEN — <name>

**Target persona:** <from references/core/personas.md> (often Persona D)
**Surfaces in scope:** <list>
**Linked findings:** <AGENT-TEST-... IDs, if this came from a REVIEW ledger>
**Starting state:** <one line>
**Target state:** <one line>
**Date:** <YYYY-MM-DD>

## Why this hardening

<2–4 sentences: the trust gaps driving it (cite the audit report if one exists) and the
constraint set (the release pipeline keeps running, no big-bang, every step reversible).>

## Step sequence

Each step is reversible: the suite is usable at the end of every step. Effort is
S (≤ 1 day) / M (≤ 1 week) / L (≤ 1 month).

### Step 1 — <name>

- **Effort:** <S/M/L>
- **What changes:** <one sentence>
- **Safety net:** <calibrate before trusting, keep the old gate alongside the new one, disjoin
  the held-out set before re-baselining, shadow the new judge>
- **Done when:** <observable predicate — a calibration report, a held-out pass, not a config flag>
- **Closes findings:** <AGENT-TEST-... IDs, or `none`>
- **If we stop here:** <what state we are left in — must be usable, no instrument trusted before calibrated>
- **Playbook heuristic:** <playbook>#<heuristic> (<intent>)

### Step 2 — ...

(repeat per step)

## Open questions

<Where the safety net is uncertain, or where sequencing is contested (e.g. swapping a god-gate
for per-slice scoring without losing comparable history).>

## Verification

<How to verify each step landed safely — a judge-calibration report, a held-out run, an
activation positive/negative/edge pass. When linked findings exist, run a verification closeout
pass and update the ledger / workflow state only for IDs whose checks pass.>

## Grounding sources applied

- <skill.json inspired_by entry> — <hardening-sequence choice it informed>
