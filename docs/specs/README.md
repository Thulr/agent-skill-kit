# Specs

Specs are the handoff artifact for non-trivial work in this repository (new
skills, cross-skill schema changes, new gates/hooks, distribution changes).

Guidance:

- Prefer vertical slices (a change that is usable end-to-end) over horizontal
  phases (e.g. “write all schemas first”).
- Write only from real requirements / observed failures (no boilerplate specs).
- If a spec implies a durable repo-level decision, also add an ADR under
  `docs/adr/`.

Suggested per-change layout (one folder per significant change):

`docs/specs/YYYY-MM-DD-<short-slug>/`
- `spec.md` — problem, constraints, approach, acceptance criteria
- `plan.md` — ordered execution plan
- `tasks.md` — checkbox list; keep tasks outcome-shaped

