# Agentification Assessment — `informed-skills`

**Date:** 2026-05-15
**Primary harness(es) detected:** none formally declared (repo is harness-agnostic by design; consumed by `claude-code` / `cursor` / `codex` via `npx skills add`)
**Sub-surfaces assessed:** all 10 (instruction-surface, specs, docs-index, skills, tools, sandbox, gates, telemetry, evals, governance)
**Lenses dispatched:** cold-context-agent / maintainer / adversarial / auditor (sequentially inside one sub-agent per sub-surface)

## Maturity scores

| Layer | Score (1–5) | Justification |
|---|---|---|
| Legibility | **1** | Limited by `instruction-surface` (no AGENTS.md/CLAUDE.md at all) and `docs-index` (no llms.txt, no repo map). `specs` is the bright spot at Level 2 (per-feature design specs exist) but the layer score is min(1,2,1). |
| Action | **1** | Limited by `tools` (zero MCP / typed function tools) and `sandbox` (no Dockerfile, devcontainer, or sandbox policy). `skills` scored Level 4 — the published skills are exemplary — but the layer minimum drags it down. |
| Control | **1** | Limited by `telemetry` (no reflection log, no run metadata, no traces) and `governance` (no CODEOWNERS, no branch protection, no SLSA, no SECURITY.md). `gates` and `evals` both at Level 2 — structure exists, enforcement does not. |

**Overall maturity ceiling: Level 1 — Ad hoc.** Three of the three layers tie at 1; the limiting sub-surfaces are `instruction-surface`, `docs-index`, `tools`, `sandbox`, `telemetry`, and `governance`. The repo's discipline ceiling is its **weakest** sub-surface, and there are six of them at Level 1.

The headline tension: the published **skills** are a Level 4 artifact sitting inside a Level 1 repo. The product is mature; the supply chain around it is not.

## Blocking gaps (severity 3–4)

| Sev | Layer | Sub-surface | Finding | Artifact pointer | Lens(es) |
|---|---|---|---|---|---|
| 4 | control | governance / gates | No CODEOWNERS, no required-reviewer rule, no visible branch protection — `skills/`, `.agents/`, `.github/` are PR-editable by anyone with push access, and the published skills load into downstream agent sessions via `npx skills add`. This is an active W5 supply-chain injection path. | `.github/` (no CODEOWNERS); merged PRs 1–4 were self-merged by `Thulr` | adversarial, auditor (raised by governance, gates, instruction-surface, sandbox) |
| 4 | control | gates | No PreToolUse/PostToolUse hooks anywhere — no `.claude/settings.json`, no `.git/hooks/*` beyond samples. Force-push to main, `rm -rf`, prod-DB writes are entirely unblocked at the harness layer. W3 "hard gates over soft prose" is taught in this repo's own playbooks but not applied to itself. | absent | adversarial, auditor |
| 3 | legibility | instruction-surface | No AGENTS.md or CLAUDE.md at repo root — every agent session starts cold; agent must rediscover `just check`, the `skills/` vs `.agents/skills/` split, and the `.experimental/` lane on every invocation. | absent | cold-context-agent, maintainer (raised by 4 of 10 sub-agents) |
| 3 | legibility | docs-index | No `llms.txt` / `llms-full.txt`; no repo map; no canonical `docs/adr/` or `docs/runbooks/` subdirectories. `docs/superpowers/` is invisible from the README layout table. | repo root | cold-context-agent, auditor |
| 3 | legibility | specs | No `constitution.md` and no `docs/adr/` series — non-obvious architectural decisions (the `.experimental/` bucket, `skill.json` provenance format, "skills are the product" framing) are undocumented hallucination bait. | absent | cold-context, maintainer |
| 3 | control | telemetry / instruction-surface | No reflection log (`docs/agent-failures.md`). Without one, the W1 floor of "≥3 observed failures" is unachievable — scaffolding AGENTS.md/skills cannot be evidence-driven because the evidence is never captured. This is the keystone gap: it blocks evidence-based hardening of every other layer. | absent | auditor, maintainer |
| 3 | control | evals | `trigger-evals.json` exists in 2 production skills with rich schemas (`should_trigger`, `expected_route`) but is never executed by any runner or CI step. Trigger accuracy is unmeasured; `expected_route` is dead schema. | `skills/{test,dx}-heuristics/evals/trigger-evals.json`; `.github/workflows/ci.yml` | auditor, maintainer |
| 3 | control | evals / skills | `.experimental/project-agentification/evals/run-static-checks.sh` is excluded from `just check` and CI — the Justfile glob `skills/*/evals/...` doesn't match dotfile dirs. The experimental lane silently bypasses the structural gates published skills must pass. | `Justfile`; `.github/workflows/ci.yml:20` | maintainer, cold-context |
| 3 | control | evals | Zero adversarial eval cases anywhere — no prompt-injection scenario, no conflicting-instruction case, no ambiguous-tool-output case, no long-context overflow case. All four playbook-H3 categories absent. | `skills/*/evals/` | adversarial |
| 3 | control | evals | `example-minimal` skill has no `evals/` directory. A new contributor templating from it ships skills with zero eval coverage and no CI static-check gate. | `skills/example-minimal/` | cold-context-agent |
| 3 | legibility | docs-index | No `SECURITY.md` / `ATTRIBUTION.md` with machine-readable license + reciprocity signal — autonomous ingestion agents redistributing skills downstream have no programmatic compliance check. | repo root | adversarial, auditor |
| 3 | control | governance | No SLSA / `actions/attest-build-provenance` step; published skill bundles ship with zero build provenance. | `.github/workflows/ci.yml` | auditor |
| 3 | control | governance / gates | No approval matrix — no documented action-type × risk-class mapping; agents have no documented ask-first tier for changes to skill files or hooks. | absent | auditor |
| 3 | control | telemetry / gates | No run metadata captured (model, prompt hash, tool-schema version, commit SHA); no append-only event history or `.traj`-style artifact. Regression attribution and incident reconstruction are impossible. | `.github/workflows/ci.yml` (no artifact upload) | auditor, cold-context |
| 3 | action | sandbox | No sandbox declaration anywhere. Skills consumed downstream run in whatever bare process sandbox the host harness provides; the CI runner (`ubuntu-latest`) has no egress allowlist. W10 active in the consumer environment. | repo root | adversarial, cold-context |

## Significant gaps (severity 2)

| Layer | Sub-surface | Finding | Artifact pointer |
|---|---|---|---|
| action | skills | `trigger-evals.json` schema diverges between skills (`dx-heuristics` flat list with `should_trigger`; `test-heuristics` nested `{skill, queries[]}` with `should_activate` + `expected_route`). No cross-skill lint enforces parity. | `skills/{dx,test}-heuristics/evals/trigger-evals.json` |
| action | skills | No CONTRIBUTING guide encodes the quality bar (provenance minimums, eval structure, "3 observed failures before scaffold"). README §Authoring is 4 sentences pointing at `npx skills init`. | `README.md:99–113` |
| legibility | specs | No `docs/runbooks/` — operational procedures (publishing a skill, CI failure recovery) reinvented per session. | absent |
| legibility | specs | Design specs have `status:` field but no formal lifecycle; spec↔implementation drift has no detection mechanism. | `docs/superpowers/specs/*` |
| legibility | instruction-surface | Skill SKILL.md files act as de facto instruction surface but only load on trigger match; agents invoked for non-skill tasks have no repo-level orientation to fall back on. | `skills/*/SKILL.md` |
| control | gates | CI gates only check skill-structure invariants — no CI gate mirrors any harness-layer constraint, so a future PreToolUse hook would have no CI redundancy. | `.github/workflows/ci.yml:14–27` |
| control | evals | Behavioral cases in `activation-cases.md` are "manual review by design" — no grader, no run history, no pass/fail log. Routing regressions undetectable between manual audits. | `skills/dx-heuristics/evals/activation-cases.md:22–29` |
| control | evals | No eval-case provenance tag (`source: real-failure | synthesized`). Likely all synthesized — the W1 distribution-tail failure mode. | all `trigger-evals.json`, `activation-cases.md` |
| control | governance | No model routing policy, no cost tracking — agents default to most-capable model with no feedback signal. | absent |
| action | sandbox | CI uses floating `ubuntu-latest` tag, not pinned digest or container image. Eval reproducibility drifts silently. | `.github/workflows/ci.yml:9` |
| control | telemetry | CI doesn't upload eval/test artifacts — pass/fail history evaporates with log retention. | `.github/workflows/ci.yml:9–28` |

## Minor friction (severity 1)

- `maintainers` field in all `skill.json` files is the opaque string `"justin"` — not resolvable by external contributors or automated CODEOWNERS lookup.
- `THIRD_PARTY.md` exists as a 427-byte placeholder, not a machine-parseable schema.
- `example-minimal` appears in install menus with a "never use" description — mildly confusing, recoverable.
- `docs/superpowers/{plans,specs}/` uses a non-canonical path; agents following the standard `docs/specs/` + `docs/adr/` convention won't find it.
- No `.devcontainer/` — contributor environments diverge from CI silently.
- No redaction policy for future telemetry (currently moot, will be live the moment anything is captured).

## Cosmetic (severity 0)

- Skill descriptions use "Use when…" / "Trigger for…" rather than the "Make sure to use this skill whenever…" pushy ending recommended in the skills playbook. Both forms are trigger-word-rich; low risk.

## Conflicts and open questions

- **The W1 chicken-and-egg.** Multiple sub-agents recommended adding AGENTS.md / CLAUDE.md (instruction-surface, sandbox, governance), but W1 forbids scaffolding from less than 3 observed failures — and `telemetry` confirms no reflection log exists to capture those failures. **Resolution path:** start `docs/agent-failures.md` first, accrue ≥3 entries from real sessions, *then* hand-curate AGENTS.md. Do not run `/init`.
- **Skills as Level 4 island.** The published skills are mature, but the repo around them is Level 1. Open question for the maintainer: is the agentification target *this repo as a development environment* (focus on hardening governance/gates/telemetry) or *this repo as a skills distributor* (focus on supply-chain trust — CODEOWNERS, SLSA, write-protected skill files)? Both are valid; the recommended actions differ.
- **`.experimental` lane bypasses gates.** Two sub-agents independently flagged the Justfile glob silently excluding `.experimental/project-agentification`. Is this intentional (experiments are exempt) or a bug? If intentional, document it; if a bug, fix the glob.

## Recommended stage

Three layers at Level 1 → **Stage 0 (Triage) first, then Stage 1 (Habitat)**.

- [x] **Stage 0 — Triage (1–2 days).** Close the supply-chain bleed and unblock evidence-driven authoring.
- [ ] Stage 1 — Habitat (1–2 weeks). Add hooks + CI enforcement + first AGENTS.md (only after Stage 0 reflection log has ≥3 entries).
- [ ] Stage 2 — Specs (1 month). `constitution.md`, `docs/adr/`, `docs/runbooks/`.
- [ ] Stage 3 — MCP and observability. Only relevant if a skill-execution MCP is contemplated.
- [ ] Stage 4 — Governance. SLSA attestations, model routing, cost tracking.

**Top three actions for Stage 0:**

1. **Add `CODEOWNERS` + enable branch protection** requiring CI pass + at least one reviewer on `skills/**`, `.agents/**`, `.github/**`, `Justfile`, `README.md`. — closes the Sev-4 W5 supply-chain path (governance / gates / instruction-surface / sandbox findings).
2. **Create `docs/agent-failures.md` with a template** (one row per: date, harness, what the agent did, what went wrong, what rule would have prevented it). Backfill 1–2 known recent failures if any exist. — unblocks the W1 floor for every future AGENTS.md / skill scaffold (keystone telemetry/instruction-surface gap).
3. **Fix the `.experimental` glob in `Justfile` and `.github/workflows/ci.yml`** so `skills/.experimental/*/evals/run-static-checks.sh` actually runs in CI. Either expand to dotdirs or move out of `.experimental/`. — closes the Sev-3 silent-bypass gap raised by both `evals` and `skills` sub-agents.

## Verification

Re-run this audit after Stage 0 with these targeted checks:

- `CODEOWNERS` exists, lists owners for `skills/**`, `.agents/**`, `.github/**`. Branch-protection rule on `main` requires the CI status check + ≥1 review. Verify by attempting a self-merged PR — it should be blocked.
- `docs/agent-failures.md` exists, has ≥1 dated entry, and is linked from README. A green light to start Stage 1's AGENTS.md is: this file has ≥3 entries.
- `just check` output includes `Running .../project-agentification/evals/run-static-checks.sh`. CI workflow log shows the same step executed.
- Re-run the assess on `control` layer only — expect governance to move from Level 1 to Level 2 (still no SLSA / model routing / approval matrix, but supply-chain bleed closed).

The agent-behavior signal to track: after AGENTS.md lands in Stage 1, do PRs need fewer "where do I put this" / "what's the right command" round-trips? If yes, the instruction surface is doing work.

## Sources cited

- ETH Zürich / LogicStar.ai (Mündler et al., arXiv:2602.11988) — W1 autogeneration penalty; applied to chicken-and-egg conflict.
- HumanLayer + Augment Code 2500-repo study — W2 ≤200-line ceiling; applied to "do not run /init" recommendation.
- DEV community write-up on Copilot agent mode — W3 hard gates vs prose; applied to gates layer Level 1→2 ceiling.
- Walden Yan (Cognition), *Don't Build Multi-Agents* — W4 shared-context principle; applied to specs handoff finding.
- Prompt Security AGENTS.md exfiltration writeup — W5 attack surface; applied to Sev-4 CODEOWNERS finding.
- Anthropic, *Effective Context Engineering for AI Agents* — W6 token budget; applied to docs-index missing-llms.txt finding.
- Vercel internal Next.js benchmark — W7 skills-vs-AGENTS.md separation; applied to Stage 0 sequencing.
- Software Mansion agentic engineering guide — W9 auto-init lies; applied to "don't run /init" caveat.
- OpenHands / OWASP — W10 process-sandbox risk; applied to sandbox layer findings.

---

**Empirical warnings invoked across this audit:** W1, W2, W3, W4, W5, W6, W7, W8, W9, W10 (all ten).
