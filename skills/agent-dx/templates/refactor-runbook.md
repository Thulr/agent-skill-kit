# Agent DX — HARDEN — <name>

**Target persona:** <from references/core/personas.md> (often Persona D)
**Surfaces in scope:** <list>
**Linked findings:** <AGENT-DX-... IDs, if this came from a REVIEW ledger>
**Starting state:** <one line>
**Target state:** <one line>
**Date:** <YYYY-MM-DD>

## Why this hardening

<2–4 sentences: the findings driving it (cite the audit report if one exists) and the
constraint set (callers keep working, the public contract is not frozen for the duration,
every step reversible).>

## Step sequence

Each step is reversible: the surface is shippable at the end of every step. Effort is
S (≤ 1 day) / M (≤ 1 week) / L (≤ 1 month).

### Step 1 — <name>

- **Effort:** <S/M/L>
- **What changes:** <one sentence>
- **Safety net:** <contract/version compatibility, schema round-trip tests, additive hooks
  before enforcing, dual-emit telemetry before switching>
- **Done when:** <observable predicate>
- **Closes findings:** <AGENT-DX-... IDs, or `none`>
- **If we stop here:** <what state we are left in — must be shippable, contract intact>
- **Playbook heuristic:** <playbook>#<heuristic> (<intent>)

### Step 2 — ...

(repeat per step)

## Open questions

<Where the safety net is uncertain, or where sequencing is contested (e.g. a breaking error
`code` change that needs a deprecation window).>

## Verification

<How to verify each step landed safely — schema round-trip, an injection test, a redaction
test, a loop-bound test. When linked findings exist, run a verification closeout pass and
update the ledger / workflow state only for IDs whose checks pass.>

## Grounding sources applied

- <skill.json inspired_by entry> — <hardening-sequence choice it informed>
