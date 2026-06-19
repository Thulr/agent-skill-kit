# Change Plan — <what agent-ops change you are making>

**Target persona:** <from references/core/personas.md> (usually Persona A)
**Surfaces in scope:** <observability | optimization-loop | autonomous-controller | cost-and-reliability | maturity-and-governance>
**Date:** <YYYY-MM-DD>

A pre-flight plan for an in-progress operations change to a running agent system. Fill it
before wiring much; it is a thinking tool, not a deliverable to track.

## What already exists

<What you observed before changing — the existing traces, loop, gate, or budget you will build
on. Confirm spans carry real content (prompt + completion + tool I/O) before relying on them.
If a signal is missing, say so and how you checked.>

## The minimal change

- **Reuse:** <existing signal/loop/gate this builds on>
- **Add:** <the smallest new operating machinery the present need forces>
- **Remove:** <dashboards/alerts/loops this lets you retire — answer even if "nothing">

## Operations check

- **Observable:** <do spans carry prompt+completion+tool I/O; is the trajectory graded?>
- **Loop closes:** <does the signal become an eval/fix/rollback rule, on observed emission?>
- **Autonomy gated:** <if a controller runs — held-out eval, circuit-breaker, one-diff-per-cycle, revert?>

## Seams I am deliberately NOT adding

<The dashboards, tiers, or autonomy you considered and are leaving out because no present need
forces them (YAGNI). Naming them documents the restraint.>

## Blast radius

<Which runs, budgets, and downstream consumers this touches. If it changes an autonomous loop
or a release gate, note it is a coordinate-or-stage change, not a free one.>

## Routing

- **Mechanical** (alert wiring, span attributes, budget config): handled by <gate / locally>.
- **Judgment call to flag to a human:** <enabling autonomy, a rollback-threshold change, a new
  cost ceiling — or "none">.

## Grounding sources applied

- <skill.json inspired_by entry> — <how it shaped this plan>
