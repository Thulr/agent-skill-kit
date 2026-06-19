# Agent Docs — HARDEN — <name>

**Target persona:** <from references/core/personas.md> (often Persona D)
**Surfaces in scope:** <list>
**Linked findings:** <AGENT-DOC-... IDs, if this came from a REVIEW ledger>
**Starting state:** <one line>
**Target state:** <one line>
**Date:** <YYYY-MM-DD>

## Why this hardening

<2–4 sentences: the gaps driving it (cite the audit report if one exists) and the constraint set
(agents keep reading the docs, no big-bang, every step reversible).>

## Step sequence

Each step is reversible: the docs stay usable at the end of every step. Effort is
S (≤ 1 day) / M (≤ 1 week) / L (≤ 1 month).

### Step 1 — <name>

- **Effort:** <S/M/L>
- **What changes:** <one sentence>
- **Safety net:** <symlink a mirror before deleting the fork, move an invariant to a gate before
  trimming prose, keep the old anchor as a redirect, measure before removing always-loaded content>
- **Done when:** <observable predicate — a retrieval test, a parity check, not a config flag>
- **Closes findings:** <AGENT-DOC-... IDs, or `none`>
- **If we stop here:** <what state we are left in — must be usable, no safety invariant left only in prose>
- **Playbook heuristic:** <playbook>#<heuristic> (<intent>)

### Step 2 — ...

(repeat per step)

## Open questions

<Where the safety net is uncertain, or where sequencing is contested (e.g. moving an invariant to
a gate that does not exist yet — hand the gate to harden-repo-for-coding-agents first).>

## Verification

<How to verify each step landed safely — a retrieval test, a mirror-parity check, a
chunk-survivability spot-check, a trigger eval. When linked findings exist, run a verification
closeout pass and update the ledger / workflow state only for IDs whose checks pass.>

## Grounding sources applied

- <skill.json inspired_by entry> — <hardening-sequence choice it informed>
