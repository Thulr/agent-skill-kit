# dx-heuristics Findings Ledger — informed-skills pre-ship edge-pass

**Skill:** dx-heuristics
**Ledger file:** `docs/audits/dx-heuristics-findings-ledger-2026-06-02-preship-sweep.md`
**Source report:** `/dx-heuristics` edge-pass (surface: applicable subset of `all`), 2026-06-02 conversation
**Created:** 2026-06-02
**Last updated:** 2026-06-02
**Owner:** @Thulr (maintainer)

Intent: `edge-pass` · Mode: Autopilot · Lenses: first-time integrator, maintainer, adversarial debugger.
Skipped surfaces (no such surface in a skills catalog): credentials/auth, AI-SDK stochasticity, runtime logging-leak (secret hygiene covered via gitleaks).

## Status Summary

| Status | Count |
|---|---:|
| discovered | 13 |
| accepted | 0 |
| planned | 0 |
| in_progress | 0 |
| implemented | 0 |
| verified | 4 |
| closed | 0 |
| needs_evidence / blocked / deferred / wont_do / superseded | 0 |

Closed in this session (verified by probe + the now-enforced hook test suites): DX-AD-01, DX-AD-02, DX-AD-04, DX-AD-06.

## Findings

| Done | ID | Sev | Surface | Status | Finding | Evidence | Verification |
|---|---|---:|---|---|---|---|---|
| [x] | DX-AD-01 | 3 | destructive | verified | `find /etc -delete` and `find / -exec rm -rf {} +` bypassed the guard (deletes protected paths). **Fixed:** `check_find` + dispatch. | Probed: `check_command("find /etc -delete")` → ALLOW; `scripts/hooks/destructive_bash_policy.py:523` only special-cased `rm`/`git` | `check_command("find /etc -delete")` now blocks; fixture in all 3 hook test suites (`just check` green) |
| [x] | DX-AD-02 | 3 | destructive | verified | Wrapper bypasses: `nohup`/`timeout`/`flock`/`setsid`/`xargs rm -rf /etc` all ALLOWed; `nohup bash -c 'rm…'` too. **Fixed:** wrappers added + positional handling. | Probed ALLOW; `TRANSPARENT_WRAPPERS` omitted these | `check_command("timeout 5 rm -rf /etc")` now blocks; fixtures in all 3 suites |
| [ ] | DX-AD-05 | 3 | partial-setup | discovered | Hook is PreToolUse-only (Claude/Codex/Cursor); raw-terminal or non-hooked-harness `rm -rf` / force-push is unguarded, but AGENTS.md §Forbidden actions reads as blanket enforcement. | `AGENTS.md:208-251`; no caveat in CONTRIBUTING | `grep -i "only.*agent session\|not a git hook" AGENTS.md` matches |
| [ ] | DX-FI-01 | 3 | back-compat | discovered | Released tag `0.0.1-alpha` ships entirely different skill names (`clean-architecture`, `project-agentification`, `dx-heuristics`…) than README/`main` (`dx-critique`, `codebase-agent-readiness`…); README install `--skill` names don't resolve at the release. | `git ls-tree 0.0.1-alpha skills/` vs `ls skills/`; `README.md:84,92` | latest tag's `skills/` matches README skill names |
| [ ] | DX-FI-03 | 3 | fresh-machine | discovered | No prerequisites disclosed before `just check`: needs `just`, `python3`+PyYAML+jsonschema, Node/`npx`, `jq`; missing any → cryptic failure, no install hint (incl. how to install `just` itself). Merges AD-08, AD-09. | `CONTRIBUTING.md:28-35`; `scripts/list-installable-skills.sh` runs `npx` with no preflight | CONTRIBUTING lists prereqs + install hints before first `just check` |
| [ ] | DX-MA-03 | 3 | back-compat | discovered | The entire `_shared/` 190-symlink architecture depends on `npx skills` dereferencing symlinks at install; verified only against `skills@1.5.7` and no CI step exercises a real extracting install (only `add . --list`). | `scripts/list-installable-skills.sh:16`; spec `2026-05-16-…/spec.md` | CI does a real `npx skills add` into temp dir + asserts a shared file is regular-file content |
| [ ] | DX-AD-03 | 2 | destructive | discovered | `git -c remote.origin.push=+refs/heads/main push origin` bypasses the force-push guard (refspec via `-c` value). | Probed ALLOW; `check_git` reads `+refspec` from argv only | `check_command` blocks the `-c` config force-push form |
| [x] | DX-AD-04 | 2 | destructive | verified | Non-`rm` deleters `shred`/`truncate`/`unlink`/`rmdir` of protected paths ALLOWed (interpreter forms are residual-risk, out of scope). **Fixed:** `SIMPLE_DELETERS` + `check_simple_deleter`. | Probed ALLOW | `check_command("truncate -s 0 /etc/passwd")` now blocks; fixtures in all 3 suites |
| [x] | DX-AD-06 | 2 | env-skew | verified | CI omitted the `.cursor` destructive-hook test that `just check` runs. **Fixed:** added the `.cursor` line to the CI step. | `Justfile:11-13` vs `.github/workflows/ci.yml` | `grep cursor/hooks/test .github/workflows/ci.yml` now matches |
| [ ] | DX-AD-07 | 2 | partial-setup | discovered | YAML-frontmatter check `except ImportError: return` — silently skips on machines without PyYAML, the exact failure (bad `description:` → skill invisible to installer) it guards. | `scripts/check-release-contract.py:158-160` | missing-PyYAML run prints a visible warning, not a clean pass |
| [ ] | DX-FI-04 | 2 | fresh-machine | discovered | `just check` ends on the last sub-check's output with no overall "all passed" signal. | `Justfile` `check` recipe | `check` recipe prints a single success line at the end |
| [ ] | DX-FI-05 | 2 | consumer-install | discovered | Consumer running headline `npx skills add` gets an interactive picker the README never shows; install lanes read as 3 choices, not "you get `skills/`". | `README.md:13,119-139` | README shows picker output + states only `skills/` is published |
| [ ] | DX-FI-06 | 2 | partial-setup | discovered | `just install-hooks` runs `pre-commit run --all-files` (gitleaks fetch+scan) as part of install; offline/fetch failure leaves a half-configured state with pre-commit's error, not a repo message. | `scripts/install-hooks.sh:43-44` | offline `just install-hooks` exits 0 with a "scan skipped" warning |
| [ ] | DX-MA-01 | 2 | version-skew | discovered | All 18 installable `skill.json` carry hardcoded `"version":"0.1.0"`, matching neither the only tag (`0.0.1-alpha`) nor the stated "maturity = repo tag" model. | `jq .version skills/*/skill.json` → all `0.1.0` | versions trace to a release, or field is removed + documented |
| [ ] | DX-MA-02 | 2 | install-skew | discovered | Docs use bare `npx skills add` (floating-latest) while CI pins `skills@1.5.7`: published install runs an untested CLI version. | `README.md:10,77` vs `scripts/list-installable-skills.sh:7` (`1.5.7`) | README states a tested/min `skills` CLI version |
| [ ] | DX-MA-04 | 2 | back-compat | discovered | Renamed/removed skills (`agent-experience`→`design-for-agents`, `project-agentification`→`codebase-agent-readiness`, `review-heuristics` removed) silently break `--skill <oldname>` installs; no alias, deprecation window, or consumer compat policy. Merges MA-08. | `CHANGELOG.md:9-26`; no consumer compat section | README carries a renamed/removed `--skill` mapping + stability note |
| [ ] | DX-MA-05 | 2 | version-skew | discovered | `llms-full.txt` (machine-readable catalog index, a release artifact) still names removed `review-heuristics`. | `llms-full.txt:37` | `grep review-heuristics llms-full.txt` clean or clearly past-tense |
| [ ] | DX-AD-11 | 2 | error-recovery | discovered | Destructive-hook block messages offer no scoped false-positive override (unlike gitleaks `[[allowlists]]`); recovery is only "run it manually," which defeats the agent workflow. | `destructive_bash_policy.py:586-630` | block message / AGENTS.md documents a narrow override path |
| [ ] | DX-FI-07 | 1 | first-impressions | discovered | LICENSE copyright holder is `heuristic-skills contributors`, not `informed-skills`. | `LICENSE:3` | `grep -i copyright LICENSE` shows `informed-skills` |
| [ ] | DX-MA-07 | 1 | destructive | discovered | CODEOWNERS for the injection surface (`skills/`, `.agents/`, `.github/`) is single-owner `@Thulr` (placeholder); no second reviewer/escalation on a load-bearing review gate. | `.github/CODEOWNERS:18-30` | every protected path lists ≥2 owners/team |
| [ ] | DX-AD-10 | 1 | env-skew | discovered | No CI gate detects case-only filename collisions (macOS case-insensitive vs Linux CI); preventive — none exist today. | `git ls-files \| awk tolower \| uniq -d` clean | gate added; stays empty |
| [ ] | DX-MA-06 | 1 | install-skew | discovered | Working-tree `skills-lock.json` lists 36 stale/foreign skills + an absolute local path; correctly gitignored (not shipped), so cosmetic. | `.gitignore:8`; `skills-lock.json` | `git ls-files skills-lock.json` empty |
| [ ] | DX-FI-08 | 1 | env-skew | discovered | Contributor wrapper scripts assume GNU coreutils (`timeout`) absent on stock macOS. | observed on this machine | macOS contributor note added or GNU-only tools avoided |

## Decisions

- 2026-06-02 — Destructive-bypass cluster (DX-AD-01/02/03/04) is the top-priority group: per AGENTS.md §Forbidden actions, each confirmed bypass needs a `docs/reflection-log/` entry + a fixture in **both** `.claude` and `.codex` test files (and ideally `.cursor`) **before** the hook is patched.

## Blockers

- DX-AD-01, DX-AD-02 — confirmed destructive-guard bypasses with no other agent-session backstop for `rm`/`find`/protected-path deletion; border on severity 4 under the repo's own threat model.

## Closeout Notes

- 2026-06-02 — **DX-AD-01 / AD-02 / AD-04 / AD-06 closed.** `scripts/hooks/destructive_bash_policy.py` gained `check_find`, `check_simple_deleter`, a shared `_protected_path_reason`, the missing execution wrappers (`nohup`/`setsid`/`stdbuf`/`timeout`/`flock`/`watch`/`xargs`) with positional handling, and `check_segment` dispatch. 39 Round-5 fixtures added to all three hook test suites (`.claude`/`.codex`/`.cursor`, now 154 cases each); CI step extended to run the `.cursor` suite. Reflection-log entries: `docs/reflection-log/2026-06-02-hook-{find-delete-bypass,wrapper-bypasses,nonrm-deleters}.md`. `just check` green.
- **Still open: DX-AD-03** (`git -c remote.origin.push=+refs/heads/main push` force-push-to-main bypass) — a distinct config-injection mechanism, not part of this fix; needs `check_git` to inspect `-c remote.*.push` / `push.default` config values. Recommend a follow-up reflection-log entry + fixture + fix.
