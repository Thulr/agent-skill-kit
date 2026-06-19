# Agent Ops — ROLLOUT — <name>

**Target persona:** <from references/core/personas.md> (often Persona D)
**Surfaces in scope:** <list>
**Linked findings:** <AGENT-OPS-... IDs, if this came from a REVIEW ledger>
**Starting state:** <one line>
**Target state:** <one line>
**Date:** <YYYY-MM-DD>

## Why this rollout

<2–4 sentences: the findings driving it (cite the audit report if one exists) and the
constraint set (the production loop keeps running, no big-bang, every step reversible, only
green changes staged).>

## Step sequence

Each step is reversible: the system is operable at the end of every step. Effort is
S (≤ 1 day) / M (≤ 1 week) / L (≤ 1 month).

### Step 1 — <name>

- **Effort:** <S/M/L>
- **What changes:** <one sentence>
- **Safety net:** <held-out eval before enabling, circuit-breaker, shadow/canary, dual-run,
  rollback threshold>
- **Done when:** <observable predicate — a real span/run/metric, not a config flag>
- **Closes findings:** <AGENT-OPS-... IDs, or `none`>
- **If we stop here:** <what state we are left in — must be operable, autonomy still gated>
- **Playbook heuristic:** <playbook>#<heuristic> (<intent>)

### Step 2 — ...

(repeat per step)

## Open questions

<Where the safety net is uncertain, or where sequencing is contested (e.g. enabling autonomy
before the held-out margin is proven).>

## Verification

<How to verify each step landed safely — a real captured trajectory, a held-out eval pass, a
forced-rollback drill, a budget-breach test. When linked findings exist, run a verification
closeout pass and update the ledger / workflow state only for IDs whose checks pass.>

## Grounding sources applied

- <skill.json inspired_by entry> — <rollout-sequence choice it informed>
