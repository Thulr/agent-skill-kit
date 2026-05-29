# Tasks — catalog consolidation

Outcome-shaped checklist. `just check` must pass at each phase boundary.

## Phase ① — shared engine + routing-CSV contract
- [ ] Add `skills/_shared/routing-contract.md` (canonical CSV routing-layer contract).
- [ ] Add `scripts/check-routing-csv.sh` enforcing a known header per routing CSV; wire into `Justfile` `check` across all three lanes (Rule 1).
- [ ] `just check` green.

## Phase ② — merge research (2 → 1)
- [ ] Scaffold `skills/research/` with `references/report/` (topic-research) + `references/decide/` (opportunity-research) via `git mv`.
- [ ] Write `frame-router.csv`, merged `SKILL.md`, merged `skill.json`, merged `evals/*`, one `run-static-checks.sh`.
- [ ] Relative-symlink shared files into `_shared`.
- [ ] Delete `skills/topic-research/`, `skills/opportunity-research/`.
- [ ] `just check` green.

## Phase ② — merge review (7 → 1)
- [ ] Scaffold `skills/review-heuristics/references/<domain>/` for dx, docs, perf, test, ux, ui-craft, architecture via `git mv`.
- [ ] Move per-domain `templates/` under `templates/<domain>/`.
- [ ] Write `domain-router.csv`, merged `SKILL.md`, merged `skill.json` (union inspired_by), merged `trigger-evals.json` (domain-prefixed routes), merged `activation-cases.md`, one `run-static-checks.sh`.
- [ ] Relative-symlink shared files into `_shared`; normalize the 2 forked CSV headers onto the contract.
- [ ] Delete the 7 review skill dirs.
- [ ] `just check` green.

## Phase ③ — catalog surface
- [ ] README: rewrite "Which skill should I use?", per-skill sections, install commands.
- [ ] AGENTS.md: update §Layout references and any neighbor language.
- [ ] `llms.txt` / `llms-full.txt`: regenerate/update entries.
- [ ] `skills-lock.json`: refresh (non-gating; regenerate via `skills` CLI if available).
- [ ] CODEOWNERS: confirm path globs still cover (no per-skill entries → no change expected).
- [ ] Reflection-log entry for the falsified-cap finding.
- [ ] ADR if a durable decision warrants one (merge policy).
- [ ] Final `just check` green; commit per phase on `looper`.
