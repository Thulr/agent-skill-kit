# specs

## What it is

The specs surface covers every natural-language artifact that precedes and governs implementation:
Spec Kit's `constitution.md → spec.md → plan.md → tasks.md` chain, BMAD-METHOD's 4-phase loop
(Analysis → Planning → Solutioning → Implementation) with its six default v6 role agents
(Analyst, Technical Writer, PM, UX, Architect, Developer — QA, code review, and sprint planning
fold into the Developer agent's workflows), PRDs, ADRs (`docs/adr/NNNN-decision-name.md`),
and runbooks (`docs/runbooks/`). The governing principle is Spec Kit's inversion: *"Specifications do not serve code — code serves
specifications."* When spec and code disagree, the spec wins. In harnesses that support skills
mode (`--integration-options="--skills"`), Spec Kit installs as skills rather than raw markdown,
enabling progressive disclosure of each phase.

## Why it matters for agents

- **Specs are the handoff artifact that makes multi-agent work.** Cognition's two principles
  (share full context; actions carry implicit decisions) require that agent boundaries re-create
  shared context — PRD, plan, tasks files do exactly that (W4).
- **Agents default to horizontal phasing; specs must force vertical slices.** Left unguided, an
  agent builds DB → API → UI, delaying end-to-end feedback. Vertical-slice (tracer-bullet) tasks
  in the PRD override this default and expose integration failures early.
- **ADRs prevent hallucinated rationale.** The most common gap in agent reasoning is "why is the
  code this way?" — a `docs/adr/` series converts that tribal knowledge into a discoverable,
  durable, first-class artifact.
- **Runbooks close the operational loop.** Without `docs/runbooks/`, agents generating on-call or
  deployment instructions invent procedures that match their training data, not your infrastructure.

## Heuristics by intent

### assess

- **H1.** Verify a `constitution.md` or equivalent project charter exists at the repo root or
  in `docs/specs/` — its absence means every Spec Kit phase starts without the invariants that
  prevent feature-level drift. (severity cap: 3; lens: cold-agent)
- **H2.** Check that PRDs specify vertical-slice tasks (cross-layer slices ending in working
  software) rather than horizontal phases — agents given horizontal phase specs will ship DB
  migrations before any UI proves the model is correct. (severity cap: 3; lens: maintainer)
- **H3.** Confirm `docs/adr/` contains at least one ADR per non-obvious architectural constraint
  visible in the codebase — every undocumented constraint is hallucination bait for the next
  agent session. (severity cap: 2; lens: cold-agent)
- **H4.** Audit runbooks in `docs/runbooks/` for infrastructure-specific commands (cluster names,
  secret paths, region endpoints) — a runbook with generic placeholders will be executed literally
  by an agent, usually at 2 AM during an incident. (severity cap: 4; lens: adversarial)
- **H5.** Check whether the spec surface is installed as skills or slash commands (Spec Kit
  `--integration-options="--skills"`) rather than raw markdown files — raw files are always-loaded
  token cost; skills-mode phases load only on trigger. (severity cap: 2; lens: auditor)
- **H6.** Verify BMAD personas each produce a structured handoff artifact consumed by the next
  persona — absent briefs between PM, Architect, and Developer phases violate Cognition Principle 1.
  (severity cap: 3; lens: maintainer)

### harden

- **H1.** Agent invents architectural rationale not present in the codebase → add
  `docs/adr/NNNN-decision-name.md` for each constraint; reference the ADR series in `AGENTS.md`
  so agents know to consult it before proposing structural changes.
- **H2.** Spec and code diverge after implementation → establish a CI gate (e.g.,
  `speckit.analyze` or a custom script) that diffs `tasks.md` completion markers against open
  PRs; fail the build when implementation ships without closing a tasks-file item.
- **H3.** Agent phases work horizontally despite spec → replace horizontal phases with
  vertical-slice task blocks in `docs/specs/<feature>/tasks.md`; use the format
  `- [ ] <slice-name>: <user-visible outcome> (touches: <layer1>, <layer2>)`.
- **H4.** Multi-agent handoffs lose context → require each BMAD persona to produce a structured
  brief before the next starts (PM → `brief.md`, Architect → `arch.md`) stored in
  `docs/specs/<feature>/`.
- **H5.** Runbook executed literally with wrong infrastructure values → replace inline values in
  `docs/runbooks/<name>.md` with `${VAR_NAME}` references; add a preamble requiring the agent to
  resolve all variables before executing any command.
- **H6.** Spec Kit installed as raw markdown (always-loaded) → migrate to skills mode via
  `--integration-options="--skills"` to install each phase as a `.claude/skills/<phase>/SKILL.md`;
  only the ~100-token metadata loads at startup, full instructions load on trigger.

### scaffold

- **Do not autogenerate specs, ADRs, or runbooks from templates without project context (W9).**
  LLM-generated context files drop task success ~3% and inflate cost >20% (Mündler et al.,
  arXiv:2602.11988). Every spec artifact must reference at least one stated requirement,
  named threat, or architectural decision — no placeholder copy, no "TBD" sections shipped
  to production.
- **H1.** Initialize Spec Kit with `constitution.md` first — define project purpose, non-goals,
  and invariants that no phase may violate; this file is the highest-precedence constraint in the
  entire spec chain.
- **H2.** Structure each PRD section as: Problem → Constraints → Vertical Slices → Acceptance
  Criteria; the Vertical Slices section must list at least one slice that spans UI + API +
  persistence in a single deployable unit.
- **H3.** Scaffold ADRs with the standard four-section format: Context, Decision, Consequences,
  Status; number sequentially (`NNNN`); link from `AGENTS.md` with the summary line so agents
  can find the relevant ADR without reading all of them.
- **H4.** Scaffold runbooks with a mandatory preamble: prerequisites, environment variables
  required, expected duration, rollback procedure; agents execute the first command they encounter
  — the preamble must not be skippable.

### diagnose

- **H1.** Agent ignores the spec and implements from intuition → rank hypotheses: (1) spec not
  referenced in `AGENTS.md`, never discovered cold-start; (2) raw markdown is too long, triggering
  "lost in the middle" decay — migrate to skills mode (W6); (3) spec contradicts existing code and
  agent defaults to code as more concrete.
- **H2.** Spec and code drifted after a sprint → rank hypotheses: (1) `tasks.md` never updated
  as items completed — check commit history; (2) harness update silently dropped spec from
  auto-injected context; (3) BMAD handoff brief absent — Dev persona re-derived constraints and
  diverged from Architect's intent.
- **H3.** Agent builds horizontal layers despite vertical-slice tasks → hypotheses: (1) task
  entries name layers not outcomes (`Create DB schema` vs `User can log in`); (2) an AGENTS.md
  rule overrides spec with "complete infrastructure before UI"; (3) reorder `tasks.md` so each
  slice's steps are contiguous.
- **H4.** Runbook execution fails mid-procedure → hypotheses: (1) `${VAR_NAME}` placeholders not
  resolved before execution; (2) runbook targets stale infrastructure — check ADR history for
  changes after the runbook date; (3) runbook assumes idempotency the underlying API doesn't
  guarantee — add state-check steps before destructive commands.

## Empirical warnings

- **W9** — Autogenerated specs/ADRs produce surface-plausible scaffolds with low fitness;
  hand-author from stated requirements or named threats only. (Underlying measurement from
  Mündler et al.: autogenerated context drops task success ~3%, inflates cost >20%.)
- **W4** — BMAD/CrewAI multi-agent topologies survive only when PRD/plan/tasks re-create shared
  context across boundaries; absent briefs cause conflicting implicit decisions (Cognition P2).
- **W6** — Token budget is dominant; install spec phases as skills (on-trigger), not raw markdown
  (always-loaded); prefer on-demand → on-trigger → always-loaded.

## Canonical examples

- **github/spec-kit** — reference implementation of `constitution.md → spec.md → plan.md →
  tasks.md`; 29+ harness integrations; skills-mode install for Claude Code and Codex.
- **BMAD-METHOD** — multi-agent orchestration with explicit handoff briefs across its six default
  v6 agents (Analyst, Tech Writer, PM, UX, Architect, Developer); Party Mode for parallel agent
  sessions in one harness.
- **joelparkerhenderson/architecture-decision-record** — battle-tested ADR templates; use as
  the reference format for `docs/adr/NNNN-decision-name.md`.
- **EPAM case study** — spec-driven flow "especially well-fit for greenfield, legacy
  modernization, and brownfield" once agents are treated as spec-consumers, not code-search engines.

## Sources

- "GitHub Spec Kit" — `constitution.md → specify → plan → tasks → implement` flow;
  spec-as-source-of-truth inversion; skills-mode install (`--integration-options="--skills"`).
- "BMAD-METHOD" — 4-phase loop with six default v6 role agents; explicit handoff artifact pattern;
  quality gates between phases; multi-agent Party Mode.
- "Don't Build Multi-Agents" — Cognition Principle 1 (share full context) and Principle 2
  (conflicting decisions from conflicting actions); PRD/plan/tasks as the handoff artifacts that
  make multi-agent safe.
- "AGENTS.md" — `docs/adr/` and `docs/specs/` as first-class subdirectory layout; AGENTS.md as
  table of contents into the spec tree, not a duplicate of it.
