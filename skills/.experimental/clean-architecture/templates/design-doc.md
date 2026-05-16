# Architecture Design — <feature or system>

**Target persona:** <from references/core/personas.md>
**Surfaces in scope:** <list>
**Date:** <YYYY-MM-DD>

## Goal

<1–2 sentences. What is being built and why.>

## Acceptance criteria

<Observable, testable. Each criterion ties to one of the surfaces in
scope. Severity-tagged where relevant.>

- [ ] <criterion 1> — surface: <surface> — severity: <0–4 if blocker, omit if pure positive criterion>
- [ ] <criterion 2>
- [ ] ...

## Architecture sketch

<Brief description plus a layered, hexagonal, or onion diagram in text
form. Name each layer/ring/port and what lives in it.>

## Decisions

For each load-bearing decision, name the playbook heuristic that
underwrites it.

- **<Decision 1>:** <choice> — playbook heuristic: <playbook>#<n> (<intent>)
- ...

## Open questions

<Items where the three lenses disagreed, or where the design depends
on context the agent did not have.>

## Verification

<How to verify the design satisfies the acceptance criteria —
tests, dependency-graph check, peer review, prototype.>
