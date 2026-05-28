# Intake Brief: opportunity-research

Phase 1 artifact. Saved at `.agents/state/intake-briefs/opportunity-research.md`.

## Source seed

- Title / creator / URL: `convo.txt` (this repo). A multi-turn conversation
  enumerating the 14 dimensions of research that go into validating a
  product or business opportunity (market, customer, competitive, domain,
  technical, data, operational, financial, legal, channel, GTM,
  stakeholder, risk, trend) and collapsing each branch into the
  four-layer **Facts / Assumptions / Decisions / Risks** frame.
- One-line of what the source is about: A practical, opinionated taxonomy
  for "what kinds of research a CEO/CTO/PM/agent must do before betting
  on an opportunity" — including the test that *a research branch which
  ends in notes but not decisions is just organized procrastination*.
- Why this source, now: The user asked for the **ultimate research skill**
  — sub-agent-driven, template-heavy, with nested progressive disclosure.
  The convo is a self-contained, decision-oriented taxonomy that maps
  cleanly onto a two-level routed skill (intent × research-area) and
  produces 14 real-world artifacts.

## Audience

- Who invokes the skill: founders, product managers, technical leads,
  investors doing diligence, agents scoping a feature/product/business
  bet. Mid-to-senior — they know what an ICP is; they want a forcing
  function across blind spots, not a primer.
- When in their workflow they reach for it: at the front of any new
  initiative (idea, feature, product, business unit), or when an
  initiative *should* have been validated but a step was skipped.
  Also at re-evaluation points (post-launch failure analysis,
  pivot calls, M&A diligence).
- What they already know: standard product/strategy vocabulary
  (segment, ICP, JTBD, unit economics, GTM, CAC/LTV). The skill should
  not re-teach Lean Startup or Porter — it should orchestrate research
  across them.

## Success criteria

- First-fire outcome: the user names an opportunity (one sentence). The
  skill scopes the 5–8 areas that actually matter for their stage,
  spawns sub-agents to fill each area's artifact template with the
  user's specific context plus web-grounded evidence, then synthesizes a
  one-page **opportunity brief** with explicit Facts / Assumptions /
  Decisions / Risks per area.
- Later-signal of value: the user comes back for re-runs (post-launch
  re-investigation, pivot diagnosis, follow-on funding diligence) and
  re-uses the saved area-artifacts as living documents.
- Tells of missing/wrong: the skill produces a research dump without
  decisions; the artifacts read like book chapters rather than
  decision-ready briefs; the skill substitutes for `proposal-red-team`
  or `validation-context` rather than feeding them; sub-agents
  duplicate work instead of fanning out across orthogonal areas.

## Scope boundaries

- **In scope (what this skill must handle):**
  - Scoping: pick & sequence which of the 14 areas matter for the
    user's stage/opportunity.
  - Investigating: spawn sub-agents (one per in-scope area, optionally
    crossed with persona lenses) to fill each area's artifact template.
  - Synthesizing: roll up area findings into one decision-ready brief.
  - Deciding: convert findings into Facts / Assumptions / Decisions /
    Risks per area + a go / no-go / pivot recommendation with kill
    criteria.
  - Producing **14 distinct deliverable artifacts** (market sizing,
    ICP+JTBD, competitor map, domain glossary, technical feasibility,
    data inventory, operating model, unit economics, legal register,
    channel plan, GTM plan, stakeholder map, risk register, trend
    horizon) — these are real-world artifacts a founder/PM hands to a
    board, investor, or team.
- **Out of scope (deliberately left to other skills / the user):**
  - Adversarial review of an already-drafted proposal → `proposal-red-team`.
  - Stress-testing an execution plan → `plan-red-team`.
  - Working backward from assumed failure → `premortem`.
  - Ideating *what* to build → `morphological-analysis`, `scamper`,
    `novel-ideation`, `tree-of-thoughts-deep-dive`.
  - Critiquing user-research instruments → `interview-guide-critique`,
    `survey-question-review`, `persona-critique`.
  - Setting up one-time shared context for repeated reviews →
    `validation-context`.
  - Picking between named candidate approaches → `tradeoff-analysis`.
  - Architecture review of an already-built system → `clean-architecture`.
  - DX/UX/test/perf craft reviews → `dx-heuristics`,
    `ux-accessibility-heuristics`, `test-heuristics`,
    `perf-observability-heuristics`.
  - User-facing UI craft → `ui-design-craft`.
- **Neighboring skill not to replicate:** `validation-context` (which
  *captures* problem/audience/constraints once) — opportunity-research
  *does the research itself*, then can hand off context for later
  reviews. The skills compose; they don't overlap.

## Comparable existing skills

Grepped `skills/*/SKILL.md` and the global skills surface. Three closest:

- `skills/dx-heuristics/` — two-level (intent × surface) with sub-agent
  dispatch by lens. Same shape, completely different domain
  (developer-experience craft vs. opportunity validation). I will copy
  the structural pattern from here.
- `skills/project-agentification/` — multi-mode workflow with playbooks
  and templates for repo-level agent-readiness assessment. Different
  domain; the workflow-state + tracked-findings pattern transfers.
- Global `validation-context` skill — sets up a one-time context file
  so future reviews don't re-ask the same questions. Distinct from
  `opportunity-research`: that captures context once; we *execute the
  research* and produce artifacts. Recommend pairing — capture context
  once with `validation-context`, then iterate research with
  `opportunity-research`.

## Safety, copyright, sensitive-domain notes

- `convo.txt` is the user's own conversation; no third-party copyright
  attaches to the *taxonomy itself*. Canonical references that will
  ground specific areas (Christensen, Porter, Skok, Ries, Hall, Dunford,
  Moore, Taleb, Diátaxis, etc.) get cited in `skill.json.inspired_by`
  with paraphrased contributions — never long quotations.
- **Sensitive-domain handling:** the legal/compliance playbook will
  carry an explicit escalation marker ("this skill produces an
  inventory of legal questions to escalate — it does NOT give legal
  advice"). Financial unit-economics templates will not claim to
  produce audited figures. Both flags are non-optional.
- **Sub-agent provenance:** sub-agents must cite their sources in their
  per-area artifact; the orchestrator must preserve those citations
  through synthesis. Unsourced confidence is downgraded to Assumption.

## Working hypothesis

> _Hypothesis:_ **Pack tag:** `opportunity-research`, `discovery`,
> `validation`, `strategy`, `product`, `founder`. **Shape:**
> two-level routing — Axis 1 (intent) is `scope | investigate |
> synthesize | decide`; Axis 2 (surface) is the 14 research areas. Each
> intent owns its own template (4 intent templates) and each surface
> owns its own artifact template (14 artifact templates) for a total of
> 18 templates. Sub-agent dispatch fans out one agent per in-scope
> surface for `investigate`, optionally crossed with four persona
> lenses (founder / operator / investor / skeptic). Shared core
> rubrics: severity (0–4), confidence (H/M/L), FADR framework, persona
> taxonomy, decision-gates / kill-criteria. Progressive disclosure: the
> SKILL.md loads only `intent-router.csv` at activation; each intent
> CSV loads only one playbook + the named core refs; sub-agents load
> only their lens + their area playbook. **No file outside the
> committed leaf is read.** Depth could promote to 3 (intent × surface
> × persona) if persona-specific content grows past ~1500 words per
> leaf, but two-level is the right starting point — the persona axis
> is currently small enough to live inside `core/personas.md` +
> `subagent-dispatch.md`.

## Gate

(Goal hook is active — advancing without pausing per the user's
explicit directive to "treat the condition itself as your directive
and do not pause to ask the user what to do.")

> "Anything missing or wrong before we research? Reply with `go` to
> advance to Phase 2 (Research), or describe what to revise."

**Curator decision:** advancing to Phase 2 under the goal-hook
override. The intake brief is recorded for auditability; the user can
intervene at any point and we will revise.
