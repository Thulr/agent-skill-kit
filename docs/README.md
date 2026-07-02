# Docs

This directory holds durable, repo-level documentation that agents and humans can
discover reliably. Keep `AGENTS.md` short and point here for depth.

Diataxis mapping (roughly):

- `docs/specs/` — explanation of intent/constraints for significant work
- `docs/adr/` — explanation of non-obvious architectural decisions (the “why”)
- `docs/runbooks/` — how-to procedures for maintainers (the “how”)
- `docs/architecture/` — reference docs / repo maps (the “what”)

Other docs in this repo:

- `docs/reflection-log/` — per-failure entries; the evidence base that governs new rules/gates (see its `README.md` for the recording-bar vs. promotion-bar distinction)

**Dated docs** (reflection-log entries, older `docs/specs/`) use
the skill names current at their date; see [`CHANGELOG.md`](../CHANGELOG.md) for
renames and removals. They are point-in-time records and are not rewritten.

