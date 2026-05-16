# Snapshot / Approval Test Playbook

## Scope

Tests that compare current output against an approved reference (snapshot, golden file, approval). Widely used for rendered components, generated code, serialized output, and complex data structures. Routes to `unit.md` when a focused assertion would be clearer. Routes to `contract.md` when the output is a wire format and the consumer is a different service.

## Grounding

- **Llewellyn Falco — Approval Testing** — the approval-testing pattern as a discipline: generate output, diff against approved, human reviews every change. The reviewer-discipline framing is load-bearing.
- **Kent Beck — *Test-Driven Development By Example*** — characterization tests (a sibling concept): pin behavior when you don't know what it should be, so you can change it safely.
- **Jest / Vitest / Insta snapshot documentation** — the practical state-of-the-art: inline vs file snapshots, serializers, custom matchers, the `--update` workflow.

## Good signals

- Each snapshot has a clear name and scope. The diff on failure is small and reviewable.
- Snapshots are reviewed in PRs alongside the code change — never "update all and ship."
- Unstable elements (timestamps, IDs, random hashes, ordering) are stripped or stabilized before snapshotting.
- The right things are snapshotted: output shape, generated code, rendered DOM — not arbitrary internal state.
- Snapshot files live alongside their tests, are checked into version control, and are part of code review.
- One assertion per snapshot file (or one logical chunk), not one mega-snapshot per page.

## Common failures

- `--update` run on every PR without diff inspection — every snapshot becomes a rubber-stamp. False-pass at scale.
- One giant snapshot per page covers 50 components; a single change produces an unreviewable diff and gets rubber-stamped.
- Snapshots include timestamps, IDs, or generated hashes that change every run — flake city.
- Internal state snapshotted (private fields, implementation details) — brittle to legitimate refactors.
- Snapshots are checked in but never reviewed — the snapshot is treated as the spec, but no human read it.
- Snapshots stored separately from tests (in a `__snapshots__` directory mid-merge-conflict) and ignored in PRs.

## Heuristics

- **Snapshots reviewed, not rubber-stamped** *(review, author)* *(false-pass)* — every diff inspected before approval. `--update-all` without review is the worst anti-pattern in this layer; it converts every snapshot into a tautology.
- **One assertion per snapshot file** *(review, author)* *(confusion)* — small, focused snapshots beat one mega-snapshot. A snapshot whose diff spans 500 lines is unreviewable; reviewers default to "looks fine, ship."
- **Snapshot represents intent, not just output** *(review)* *(confusion)* — name + scope reveal what's being approved. "renders user card with name and avatar" beats "snapshot 4." A snapshot whose intent isn't clear becomes a maintenance burden.
- **Stable across irrelevant axes** *(review)* *(flakiness)* — strip dates, IDs, ordering, hashes, locale-dependent formatting, line endings before snapshotting. Use serializers that normalize the variation away.
- **Right things snapshotted** *(review, strategize)* *(gap, brittleness)* — output shape, generated code, rendered DOM, public API response — not arbitrary internals. Snapshots of internals are brittleness machines; snapshots of nothing (where a focused assertion would be clearer) are confusion machines.
- **Updates require diff review in PR** *(review)* *(false-pass)* — process gate: snapshot diffs appear in the PR; the reviewer is expected to read them. CI can fail when snapshots change without a corresponding PR description note.
- **Snapshot churn budgeted** *(review, prune)* *(cost)* — snapshots that change every PR are signaling something (over-broad scope, unstable inputs); they should be redesigned or deleted, not maintained.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are snapshot diffs reviewed in PR? | False-pass at scale | Require PR notes for snapshot updates; train reviewers |
| Is each snapshot focused and small? | Unreviewable diffs | Split mega-snapshots into focused per-component snapshots |
| Are unstable elements stripped? | Flakiness | Add serializers/normalizers for dates, IDs, ordering |
| Are the right things snapshotted? | Brittleness or confusion | Move internal-state snapshots to focused assertions |
| Are snapshots versioned with the test? | Drift between code and approved output | Move snapshots adjacent to tests; include in PR |
| Is churn budgeted? | Snapshots change every PR; no signal | Redesign over-broad snapshots or delete |

## Cross-references

- → `unit.md` when a focused assertion would be clearer than a snapshot
- → `contract.md` when the output is a wire format consumed by a different service
- → `core/failure-modes.md` — false-pass (rubber-stamping) is the headline mode; brittleness is a close second
- → `core/personas.md` — persona 4 (test skeptic) is the natural reviewer; persona 1 (test author) keeps the snapshots focused
