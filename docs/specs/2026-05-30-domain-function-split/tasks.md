# Tasks: domain × function split

Tracks the execution of [`spec.md`](./spec.md). See ADR 0008.

- [x] **T0** — ADR 0008; supersede ADR 0005 (in part); reconcile 0006/0007; index.
- [x] **T1** — Write this spec + tasks.
- [ ] **T2** — `_shared/dx/`: move `playbooks/`, `core/personas.md`,
  `subagent-dispatch.md`, `first-impressions-checklist.md` (git mv); rewrite
  `references/dx/` → `references/` paths inside the moved files.
- [ ] **T3** — Build `dx-critique` (audit/debug/edge-pass): SKILL.md, skill.json
  (critique-scoped provenance), evals (recover + specialize), local rubrics +
  templates, symlinks into `_shared/dx/`.
- [ ] **T4** — Build `dx-design` (design): SKILL.md, skill.json (design-scoped),
  lean evals, design-doc template, symlinks into `_shared/dx/`.
- [ ] **T5** — `just check` green on the dx pair + `_shared/dx/`. Freeze the
  recipe.
- [ ] **T6** — Fan out: `docs`, `perf`, `test`, `architecture` critique+design
  pairs (parallel subagents following T2–T5).
- [ ] **T7** — `ux` → `ux-critique` rename (pure critique).
- [ ] **T8** — `ui-craft` → `ui-design` rename (pure produce; keep quality-review
  as self-polish).
- [ ] **T9** — Delete `skills/review-heuristics/`.
- [ ] **T10** — Catalog surface: README, llms.txt, CODEOWNERS, install commands,
  AGENTS.md path repoints.
- [ ] **T11** — `just check` green across all three lanes; `npx skills add . --list`
  shows the 12 (example-minimal still hidden).

## Open engineering calls (made in spec; flag if reversing)

- Shared substrate via `_shared/<D>/` symlinks, **not** literal duplication
  (better than the "two copies" downside; no drift).
- `-design` skills get **lean** evals (no severity/score/tracking gates).
- Finding-ID namespace owned by `-critique` skill of each domain.
