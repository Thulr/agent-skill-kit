# Tasks: Add `artifact-host-integration`

- [x] Confirm `design-host-integration/` is the source; classify as
      `heuristics`/`singleton` (gate-driven).
- [x] `SKILL.md` (router + modes + workflow, <900 words, fenced vs `ui-design`/`dx-design`).
- [x] `skill.json` (`status: published`, `@Thulr`, `inspired_by` = host pack,
      `metadata.{family,function,catalog_summary,source_paths}`).
- [x] Seven reference playbooks distilled from the pack (architecture +
      tweak-panel, fixed-canvas, speaker-notes, mentioned-elements, direct-edit,
      bundling-export); `references/modes.md` relative symlink to `_shared/`.
- [x] Templates: `integration-checklist.md`, `handoff-readiness.md`.
- [x] `evals/`: `run-static-checks.sh` (own copy), `trigger-evals.json`
      (positives per route + `ui-design`/`dx-design`/`ux-audit` negatives + edge),
      `activation-cases.md`.
- [x] Catalog surface: `catalog/catalog.json` Pick-a-skill row; `build-catalog.py
      --write`; `llms-full.txt` heuristics bullet.
- [x] Boundary: cross-link from `ui-design/references/prototypes-and-host.md`.
- [x] `just check` green across all three lanes.
- [ ] Open PR from a feature branch (not yet — awaiting maintainer go-ahead).
