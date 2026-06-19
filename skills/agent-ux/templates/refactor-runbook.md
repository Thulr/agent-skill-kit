# Agent UX — HARDEN — <name>

**Target persona:** <from references/core/personas.md> (often Persona D)
**Surfaces in scope:** <list>
**Linked findings:** <AGENT-UX-... IDs, if this came from a REVIEW ledger>
**Starting state:** <one line>
**Target state:** <one line>
**Date:** <YYYY-MM-DD>

## Why this hardening

<2–4 sentences: the gaps driving it (cite the audit report if one exists) and the constraint set
(the human UI keeps working, no big-bang, every step reversible).>

## Step sequence

Each step is reversible: the surface stays usable at the end of every step. Effort is
S (≤ 1 day) / M (≤ 1 week) / L (≤ 1 month).

### Step 1 — <name>

- **Effort:** <S/M/L>
- **What changes:** <one sentence>
- **Safety net:** <add the machine-readable path beside the human one, gate a destructive action
  before enabling an agent on it, stabilize a handle before retargeting, ship consent visibility first>
- **Done when:** <observable predicate — a tree read, a selector-stability test, not a config flag>
- **Closes findings:** <AGENT-UX-... IDs, or `none`>
- **If we stop here:** <what state we are left in — must be usable, no irreversible action left unguarded>
- **Playbook heuristic:** <playbook>#<heuristic> (<intent>)

### Step 2 — ...

(repeat per step)

## Open questions

<Where the safety net is uncertain, or where sequencing is contested (e.g. enabling an agent on a
payment flow before idempotency is proven).>

## Verification

<How to verify each step landed safely — an accessibility-tree read, a selector-stability test, an
idempotency/retry test, a destructive-action gate drill. When linked findings exist, run a
verification closeout pass and update the ledger / workflow state only for IDs whose checks pass.>

## Grounding sources applied

- <skill.json inspired_by entry> — <hardening-sequence choice it informed>
