# Candidate Skill Plan: opportunity-research

Phase 3 artifact. Saved at
`.agents/state/candidate-plans/opportunity-research.md`.

## Back-links

- Intake brief: `.agents/state/intake-briefs/opportunity-research.md`
- Source dossier:
  `.agents/state/source-dossiers/opportunity-research-taxonomy.md`

## Source

- Title and creator: *Opportunity Research Taxonomy* (`convo.txt`,
  this repo) — user-curated, paraphrased; grounded in canonical
  business / product literature listed in the dossier.
- Why this source is being curated now (1 line): user requested the
  ultimate research skill with sub-agents, ≥18 templates, and nested
  routing — the convo's 14-area × 4-intent taxonomy maps cleanly onto
  a two-level routed skill and produces 14 real-world artifacts.

## Recommended Pack Decisions

- Pack tag(s) used: `discovery`, `validation`, `strategy`, `product`,
  `founder`, `research`. These describe capability domains, not the
  source; each would still make sense if `convo.txt` disappeared and
  each can accept future sources from books, talks, articles.
- New pack created? `discovery` and `validation` are conceptually
  established in business/product literature; `research` is a broad
  capability. None are source-named. No new pack created — all six
  are domain capability names.

## Draft Skill Candidates

```text
candidate:                  opportunity-research
pack:                       discovery, validation, strategy, product, founder, research
shape:                      two-level
depth:                      2
action:                     create
public_path:                skills/opportunity-research/
dossier_ref:                opportunity-research-taxonomy
audience_ref:               opportunity-research
shape_decision:
  rubric_evidence: |
    Depth-rubric Q1 (How many distinct invocations?): 4 intents × 14
    surfaces = 56 distinct invocation tuples → 9+ → two-level or deeper.
    Q2 (Orthogonal axes?): intent (what you're doing) × research-area
    (what you're researching) are independently meaningful — picking
    `investigate` vs `decide` changes which template loads regardless
    of area, and picking `customer` vs `legal` changes which playbook
    loads regardless of intent. 2 axes → two-level. Q3 (Content per
    leaf?): each (intent, area) leaf is 400–1500 words of playbook +
    template content → two-level. Q4 (Shared rubric?): severity (0–4),
    confidence (H/M/L), FADR framework, personas, decision-gates are
    all shared across leaves → single-layer or deeper. Q5 (SKILL.md
    word cap?): collapsing 14 playbooks into one SKILL.md would
    explode it well past 800 words → escalate to two-level.
  promotion_path: |
    Promote to depth 3 (intent × surface × persona) when persona-
    specific content per leaf grows past ~1500 words. Currently
    personas live in `core/personas.md` + `subagent-dispatch.md`
    (one shared file, ~600 words). If any single persona acquires
    enough lens-specific heuristics to need its own per-area routing,
    add `references/<intent>/<surface>.csv` routing by persona.
  axes: |
    Axis 1 = intent (scope | investigate | synthesize | decide).
    Axis 2 = surface / research-area (14: market, customer, competitive,
    domain, technical, data, operational, financial, legal, channel,
    gtm, stakeholder, risk, trend).
anti_pattern_check:
  - one_dim_collapsed:     no   # intent has 4 differentiated rows; each intent CSV has 14 differentiated surface rows.
  - registry_routes:       yes  # intent-router rows load different intent CSVs + different default templates; each intent CSV row loads a distinct (playbook + core-refs + artifact template) bundle.
  - cargo_culting:         no   # picked depth 2 because content demands it (see Q1–Q5 above), not because of prestige.
  - bloat_check:           yes  # SKILL.md target <600 words; each playbook target 400–1500 words; each artifact template target 200–600 words. All caps verified at scaffold time.
  - depth_orthogonality:   yes  # intent changes which template loads regardless of surface; surface changes which playbook loads regardless of intent.
playbook_outline:
  - market:
      heuristic_seeds:
        - "Size demand at three resolutions: TAM (the universe), SAM (who you can actually reach), SOM (year-1 realistic capture). Skip TAM-only sizing — it lies."
        - "A market can score big on size and still fail Porter's five forces. Run both."
      common_failure_seeds:
        - "Lumping market / customer / competitive / domain / technical into one 'market research' deliverable — the convo's #1 named failure mode."
        - "Confusing 'people exist' with 'market exists'."
  - customer:
      heuristic_seeds:
        - "Jobs-to-be-done framing: name the job, the context, and what is being fired."
        - "Triangulate stated (interviews) and revealed (analytics, prior behavior) preference; flag claims that have only one of the two."
      common_failure_seeds:
        - "Asking users what they want (stated) and shipping that — they often describe the workaround, not the job."
        - "Persona without pain severity, current workaround, or willingness to switch."
  - competitive:
      heuristic_seeds:
        - "Enumerate three competitor classes: direct (same job, same form), substitute (different form, same job), do-nothing (spreadsheet, email, manual)."
        - "Differentiation must be a tradeoff a competitor can't or won't copy — not a feature list."
      common_failure_seeds:
        - "Only mapping direct competitors — usually the real competition is the status quo."
        - "Positioning that describes the product, not the buyer's reference frame."
  - domain:
      heuristic_seeds:
        - "Capture the domain glossary first — outsiders consistently misuse insider terms in ways that telegraph naivety."
        - "Map who the actors are, what they each optimize for, and what unwritten rules they obey."
      common_failure_seeds:
        - "Treating domain as a one-time read; insider knowledge accretes over months and a 'glossary' written once stays naive."
        - "Skipping edge cases — domains live or die at the exceptions."
  - technical:
      heuristic_seeds:
        - "Decompose feasibility into architecture options, integration complexity, performance budget, security threat model, and maintainability — score each."
        - "Build-vs-buy is a decision per component, not per project; default-buy for commodity, default-build for the load-bearing differentiator."
      common_failure_seeds:
        - "Confusing 'we could build it' with 'we should build it'."
        - "Skipping the spike — a one-week prototype kills more bad bets than any architecture review."
  - data:
      heuristic_seeds:
        - "Inventory data by source / access / quality / coverage / freshness / labels / governance / instrumentation-gaps."
        - "Many 'AI ideas' are really data availability problems — confirm the data exists, you can access it, and it's the right shape before the AI work."
      common_failure_seeds:
        - "Assuming you have ground-truth labels when you have stale labels or no labels."
        - "Concentration on one data source — fragile if the source rate-limits, changes terms, or vanishes."
  - operational:
      heuristic_seeds:
        - "Walk the delivery flow end to end: who does what, where does it break, what does support look like at 10× volume."
        - "Identify the operational failure modes before launch; every shipped product has them, the question is whether they were predicted."
      common_failure_seeds:
        - "Confusing 'we could run it once' with 'we could run it 1000 times reliably'."
        - "Hidden labor — assuming staff or vendors fill gaps the product creates."
  - financial:
      heuristic_seeds:
        - "Unit economics: CAC + payback < 18 months, LTV/CAC > 3, gross margin matched to the business model (SaaS 70%+, transactional 30%+, marketplace take-rate logic)."
        - "Always emit best/base/worst-case — and name what would move you from base to worst."
      common_failure_seeds:
        - "Pricing chosen by feel; no comparable benchmark, no willingness-to-pay test."
        - "Cost models that omit support, sales, compliance, or migration."
  - legal:
      heuristic_seeds:
        - "Inventory: entity / contracts / IP / privacy / security compliance / industry rules / claims / employment / tax. Each row is a question to escalate, not advice."
        - "Privacy / compliance early is cheap; privacy / compliance late is existential — flag GDPR/CCPA/HIPAA/SOC-2 exposure up front."
      common_failure_seeds:
        - "Treating legal as a launch-blocker rather than a design constraint — it becomes a fire."
        - "Marketing claims that trigger regulator attention (health, finance, automated decisioning)."
  - channel:
      heuristic_seeds:
        - "Map channels by: cost per acquisition, friction, scalability, platform-dependence, fit-by-segment."
        - "Platform-dependent channels (App Store, search engines, social ads) carry concentration risk — model 50% rate hikes and 30-day deprecation."
      common_failure_seeds:
        - "A great product with no believable path to customers."
        - "Channel mix chosen by what's familiar, not by where the segment actually lives."
  - gtm:
      heuristic_seeds:
        - "Positioning answers: who is this for, what reference frame, what tradeoffs make those who fit love it. Dunford's frame."
        - "Beachhead first — pick one segment whose adoption proves the next segment is winnable."
      common_failure_seeds:
        - "Launching to 'everyone' — the message ends up resonating with no one."
        - "Confusing channel (where) with positioning (how you show up)."
  - stakeholder:
      heuristic_seeds:
        - "Name users vs buyers vs approvers vs blockers vs champions explicitly — in B2B they're often four different people."
        - "Procurement, security, legal, IT are blockers more often than budget — discover their requirements before the buyer says yes."
      common_failure_seeds:
        - "Optimizing for the user but ignoring the buyer (or vice versa) — 'yes' from one stalls in the other's queue."
        - "Champion without enough internal power to push past a blocker."
  - risk:
      heuristic_seeds:
        - "Categorize: assumption / market / execution / technical / operational / financial / legal / platform / fraud / reputation / concentration. Score severity × likelihood; name mitigations and kill criteria."
        - "Concentration on any one customer / channel / vendor / data source is its own risk class — model 30% loss."
      common_failure_seeds:
        - "Risk register that doesn't name kill criteria — just a worry list."
        - "Wishful mitigations ('we'll respond to the threat when it appears') that don't actually de-risk."
  - trend:
      heuristic_seeds:
        - "Separate signals (data) from narratives (stories about the data). Narratives are often 12+ months ahead of revenue."
        - "Name what would have to be true for this opportunity to be too early vs too late."
      common_failure_seeds:
        - "Confusing a popular narrative with an actual demand shift."
        - "Treating trend as scenery — every trend should produce a timing decision or a kill criterion."
registry_sketch:
  layers:
    - layer: intent-router
      rows:
        - row: scope
          loads: references/intents/scope.csv + templates/scope-plan.md
          notes: only intent that produces a research-plan (not investigation output); routes by stage/scope, not surface.
        - row: investigate
          loads: references/intents/investigate.csv + templates/investigation-brief.md
          notes: only intent that triggers sub-agent fan-out across surfaces.
        - row: synthesize
          loads: references/intents/synthesize.csv + templates/cross-area-brief.md
          notes: only intent that cross-cuts area artifacts into a single brief; expects 5+ prior area artifacts as input.
        - row: decide
          loads: references/intents/decide.csv + templates/fadr-memo.md
          notes: only intent that emits go/no-go + kill criteria; requires investigated or assumed F/A/D/R per area.
    - layer: intents/scope
      rows:
        - row: market
          loads: references/playbooks/market.md + references/core/decision-gates.md
          notes: distinct from competitive/customer — answers "is there opportunity" only.
        - row: customer
          loads: references/playbooks/customer.md + references/core/decision-gates.md
          notes: distinct from market — answers "is the pain real, observed, payable."
        - row: competitive
          loads: references/playbooks/competitive.md
          notes: distinct from market — answers "why us."
        - row: domain
          loads: references/playbooks/domain.md
          notes: distinct from technical — answers "do we understand the world we're entering."
        - row: technical
          loads: references/playbooks/technical.md
          notes: distinct from operational — answers "is it buildable."
        - row: data
          loads: references/playbooks/data.md + references/core/confidence-rubric.md
          notes: distinct from technical — answers "do we have the fuel."
        - row: operational
          loads: references/playbooks/operational.md
          notes: distinct from technical — answers "can we run it 1000 times reliably."
        - row: financial
          loads: references/playbooks/financial.md
          notes: distinct from market — answers "is it worth it (unit economics, not market size)."
        - row: legal
          loads: references/playbooks/legal.md + references/core/decision-gates.md
          notes: distinct — carries escalation marker; produces inventory, not advice.
        - row: channel
          loads: references/playbooks/channel.md
          notes: distinct from gtm — answers "where do they come from."
        - row: gtm
          loads: references/playbooks/gtm.md
          notes: distinct from channel — answers "how do we show up."
        - row: stakeholder
          loads: references/playbooks/stakeholder.md
          notes: B2B/enterprise-specific; collapses to "single buyer = single user" for consumer.
        - row: risk
          loads: references/playbooks/risk.md + references/core/severity-rubric.md
          notes: distinct — cross-cutting; risk surfaces ALSO show up in every other playbook's "Common failures."
        - row: trend
          loads: references/playbooks/trend.md
          notes: distinct from market — answers "is timing right" not "is opportunity there."
        - row: all
          loads: every surface row above (fan-out)
          notes: scope's `all` produces the recommended subset for the stage, not a literal "all 14 areas in scope."
    - layer: intents/investigate
      rows:
        - row: market   → references/playbooks/market.md   + templates/artifacts/market-sizing.md
        - row: customer → references/playbooks/customer.md + templates/artifacts/icp-and-jtbd.md
        - row: competitive → references/playbooks/competitive.md + templates/artifacts/competitor-map.md
        - row: domain   → references/playbooks/domain.md   + templates/artifacts/domain-glossary.md
        - row: technical → references/playbooks/technical.md + templates/artifacts/technical-feasibility.md
        - row: data     → references/playbooks/data.md     + templates/artifacts/data-inventory.md
        - row: operational → references/playbooks/operational.md + templates/artifacts/operating-model.md
        - row: financial → references/playbooks/financial.md + templates/artifacts/unit-economics.md
        - row: legal    → references/playbooks/legal.md    + templates/artifacts/legal-register.md
        - row: channel  → references/playbooks/channel.md  + templates/artifacts/channel-plan.md
        - row: gtm      → references/playbooks/gtm.md      + templates/artifacts/gtm-plan.md
        - row: stakeholder → references/playbooks/stakeholder.md + templates/artifacts/stakeholder-map.md
        - row: risk     → references/playbooks/risk.md     + templates/artifacts/risk-register.md
        - row: trend    → references/playbooks/trend.md    + templates/artifacts/trend-horizon.md
        - row: all      → fan-out one sub-agent per row above
      notes: "each row loads a distinct (playbook + artifact-template) pair — no two rows share both."
    - layer: intents/synthesize
      rows:
        - row: bundle   → references/playbooks/synthesis.md + every artifact under audit-artifacts/opportunity-research-*/
        - row: by-stage → references/playbooks/synthesis.md + references/core/decision-gates.md (filters by stage)
        - row: investor-brief → references/playbooks/synthesis.md + templates/cross-area-brief.md (investor-lens)
      notes: synthesize has only 3 sub-rows because it operates over already-produced artifacts; collapsed if fewer than 3 area artifacts exist.
    - layer: intents/decide
      rows:
        - row: go-no-go → references/playbooks/decide.md + references/core/decision-gates.md + templates/fadr-memo.md
        - row: kill-criteria → references/playbooks/decide.md + references/core/decision-gates.md
        - row: pivot   → references/playbooks/decide.md + references/core/decision-gates.md + templates/cross-area-brief.md
      notes: decide intent has 3 sub-rows; minimum-viable two-level still — the depth-rubric allows 3+ rows.
activation_case_seeds:
  positive:
    - prompt: "Help me research whether to build a B2B AI agent for legal-ops teams." -> route: (scope, all) — picks first-pass subset by stage.
    - prompt: "Size the market for prosumer audio plugins." -> route: (investigate, market)
    - prompt: "Who are our actual competitors if we launch a developer-focused log analytics tool?" -> route: (investigate, competitive)
    - prompt: "What's the customer pain we're actually solving for SMB accountants?" -> route: (investigate, customer)
    - prompt: "Is it feasible to build a CRM with offline-first sync?" -> route: (investigate, technical)
    - prompt: "Inventory the data we'd need to do per-customer churn prediction." -> route: (investigate, data)
    - prompt: "What does the operating model look like if we serve regulated healthcare?" -> route: (investigate, operational)
    - prompt: "Are the unit economics viable for a $20/mo prosumer subscription?" -> route: (investigate, financial)
    - prompt: "What legal questions should we escalate before storing EU citizen data?" -> route: (investigate, legal)
    - prompt: "Where do users for a Linux developer tool actually come from?" -> route: (investigate, channel)
    - prompt: "Position our offering against the do-nothing alternative." -> route: (investigate, gtm)
    - prompt: "Who needs to sign off on a $50k pilot in mid-market manufacturing?" -> route: (investigate, stakeholder)
    - prompt: "Build the risk register for our launch." -> route: (investigate, risk)
    - prompt: "Is now the right window for AI-native browsers?" -> route: (investigate, trend)
    - prompt: "Pull the area briefs together into one decision-ready opportunity brief." -> route: (synthesize, bundle)
    - prompt: "Convert the investigation into go / no-go with kill criteria." -> route: (decide, go-no-go)
  negative:
    - prompt: "Brainstorm new feature ideas." -> use sibling: morphological-analysis or scamper or novel-ideation because opportunity-research is for validating a *named* opportunity, not generating candidates.
    - prompt: "Red-team this pitch deck." -> use sibling: proposal-red-team because opportunity-research builds research substrate; red-team adversarially reviews a finished artifact.
    - prompt: "Stress-test our migration plan." -> use sibling: plan-red-team because opportunity-research does not review execution plans.
    - prompt: "Pre-mortem this launch." -> use sibling: premortem because the dedicated skill drills the specific work-backwards-from-failure interview.
    - prompt: "Critique this user-interview script." -> use sibling: interview-guide-critique because that skill audits research instruments; opportunity-research uses interview output, doesn't critique it.
    - prompt: "Review this persona doc for evidence gaps." -> use sibling: persona-critique.
    - prompt: "Audit the architecture of our microservices." -> use sibling: clean-architecture because that is code-architecture review, not opportunity research.
    - prompt: "Review the developer-experience of our SDK." -> use sibling: dx-heuristics.
    - prompt: "Run a usability audit on our checkout." -> use sibling: ux-accessibility-heuristics.
    - prompt: "Capture project context once so future reviews don't re-ask." -> use sibling: validation-context — it captures, opportunity-research executes.
    - prompt: "Compare these three vendors." -> use sibling: tradeoff-analysis — that skill compares named options; opportunity-research is for the upstream "which research areas matter?"
  edge:
    - prompt: "Should we enter this market?" -> activates only if the user names an opportunity / segment; otherwise ask one blocker question ("which opportunity?") before routing to (scope, all).
    - prompt: "Research this." (no object) -> activates only after a one-line clarification on what 'this' is; otherwise refuse to fan out — sub-agent fan-out without scope produces 14 disconnected dumps, the named failure mode.
    - prompt: "Just give me the market size." -> activates on (investigate, market) but emits a single artifact, not the full investigation brief — the skill should not over-scope a narrow request into a fan-out.
grounding_map:
  - source: "convo.txt — Opportunity Research Taxonomy"
    year: 2026
    playbooks: [market, customer, competitive, domain, technical, data, operational, financial, legal, channel, gtm, stakeholder, risk, trend, synthesis, decide]
    contribution: "The 14-area taxonomy, the four-layer FADR frame, the minimum-viable first-pass subset, and the 'organized procrastination' decision-gate test."
  - source: "Eric Ries, The Lean Startup"
    year: 2011
    playbooks: [customer, risk]
    contribution: "Build-Measure-Learn loop; validated learning; pivot vs persevere."
  - source: "Christensen, Hall, Dillon, Duncan — Know Your Customers' Jobs to Be Done (HBR)"
    year: 2016
    playbooks: [customer, competitive]
    contribution: "Jobs-to-be-done framing; competing-against-non-consumption."
  - source: "Michael Porter — The Five Competitive Forces (HBR)"
    year: 2008
    playbooks: [competitive, market]
    contribution: "Five-Forces frame: rivalry + buyer power + supplier power + substitutes + new-entrant threat."
  - source: "Geoffrey Moore — Crossing the Chasm"
    year: 2014
    playbooks: [market, gtm, customer]
    contribution: "Technology-adoption lifecycle; beachhead segment; chasm-jumping playbook."
  - source: "April Dunford — Obviously Awesome"
    year: 2019
    playbooks: [gtm, competitive]
    contribution: "Positioning as deliberate context-setting; the 'alternative' frame."
  - source: "Brian Balfour — Four Fits for $100M+ Growth"
    year: 2017
    playbooks: [channel, gtm, financial]
    contribution: "Four pairwise fits: product/market, product/channel, channel/model, model/market."
  - source: "David Skok — SaaS Metrics 2.0"
    year: 2013
    playbooks: [financial]
    contribution: "CAC, LTV, payback period, gross margin, magic number; canonical SaaS unit economics."
  - source: "Eric Evans — Domain-Driven Design"
    year: 2003
    playbooks: [domain]
    contribution: "Ubiquitous language; bounded contexts; cost of getting the domain model wrong."
  - source: "Nassim Taleb — Antifragile"
    year: 2012
    playbooks: [risk]
    contribution: "Fragile / robust / antifragile classification; concentration risk; convexity."
  - source: "Teresa Torres — Continuous Discovery Habits"
    year: 2021
    playbooks: [customer, scope-intent]
    contribution: "Opportunity solution tree; weekly customer touchpoints; assumption tests."
  - source: "Gary Klein — Performing a Project Premortem (HBR)"
    year: 2007
    playbooks: [risk]
    contribution: "Pre-mortem method (without duplicating the dedicated `premortem` skill)."
  - source: "Erika Hall — Just Enough Research (2nd ed.)"
    year: 2019
    playbooks: [scope-intent, customer, synthesize-intent]
    contribution: "Right-sized research; the multiple-types-of-research taxonomy."
  - source: "Peter Thiel — Zero to One"
    year: 2014
    playbooks: [competitive, market]
    contribution: "Last-mover advantage; secrets; the monopoly-vs-competition frame."
  - source: "Carlota Perez — Technological Revolutions and Financial Capital"
    year: 2002
    playbooks: [trend]
    contribution: "Installation vs deployment periods; long-wave timing."
  - source: "Daniele Procida — Diátaxis Documentation Framework"
    year: 2020
    playbooks: [scope-intent, synthesize-intent]
    contribution: "Four-quadrant separation (tutorial/how-to/reference/explanation) applied to research artifacts so the skill emits the right artifact kind."
  - source: "Andrew Chen, Geoff Lewis — growth-loops / platform-risk literature"
    year: 2018
    playbooks: [channel]
    contribution: "Platform-dependence risk as a first-class channel concern."
  - source: "Marc Andreessen — The Only Thing That Matters (Stanford EE204)"
    year: 2007
    playbooks: [market, customer]
    contribution: "Market quality dominates team and product; the product/market-fit threshold."
  - source: "Paul Graham — How to Get Startup Ideas / essays"
    year: 2012
    playbooks: [scope-intent]
    contribution: "Live-in-the-future; organic vs made-up ideas; founder-self-as-customer."
reason: |
  The convo's taxonomy is the most compact, decision-oriented research
  framework I can ground in canonical literature. Two-level routing
  with 14 area playbooks + 18 templates + sub-agent fan-out + FADR
  decision-gates is the simplest shape that meets the user's spec
  (sub-agents required, lots of templates, nested progressive
  disclosure). Without all three, the skill collapses back to
  "validation-context plus a checklist" — which already exists.
inspired_by: |
  convo-taxonomy, lean-startup-ries, jtbd-hbr-christensen, five-forces-porter,
  crossing-the-chasm-moore, obviously-awesome-dunford,
  four-fits-balfour, saas-metrics-skok, ddd-evans, antifragile-taleb,
  continuous-discovery-torres, premortem-klein, just-enough-research-hall,
  zero-to-one-thiel, perez-tech-revolutions, diataxis-procida,
  growth-loops-chen, only-thing-matters-andreessen, graham-essays.
```

## Reference Additions

None — this skill is self-contained at depth 2. No additions to
`skills/_shared/` or to existing public skills.

## Anti-pattern self-check (rubric walk)

- [x] No CSV layer at any depth has fewer than 3 differentiated rows
      (intent: 4 rows; intents/scope: 15 rows incl. `all`;
      intents/investigate: 15 rows incl. `all`; intents/synthesize:
      3 rows; intents/decide: 3 rows).
- [x] No routed candidate has a registry layer whose rows all load
      the same files (each row loads a distinct (playbook +
      artifact-template + core-refs) combination; the `all` rows
      explicitly fan out one sub-agent per surface row).
- [x] SKILL.md projected ≤600 words; each playbook target 400–1500
      words; each artifact template target 200–600 words.
- [x] For depth ≥2, every axis is independently meaningful.
      Confirmed: intent changes template regardless of surface;
      surface changes playbook regardless of intent.
- [x] Every `playbooks: []` in `grounding_map` is non-empty.
      Confirmed for all 19 grounding rows.
- [x] Every negative activation case names a specific sibling
      skill: `morphological-analysis`, `scamper`, `novel-ideation`,
      `proposal-red-team`, `plan-red-team`, `premortem`,
      `interview-guide-critique`, `persona-critique`,
      `clean-architecture`, `dx-heuristics`,
      `ux-accessibility-heuristics`, `validation-context`,
      `tradeoff-analysis`.
- [x] Every playbook in `playbook_outline` has ≥2 heuristic seeds
      and ≥1 common-failure seed (14/14 confirmed above).

All boxes checked.

## Review Handoff (Phase 5 complete)

- **Draft paths:** `skills/opportunity-research/` — 53 files total
  - `SKILL.md` (998 words, under 1200-word cap)
  - `skill.json` (21 `inspired_by` sources with `playbooks[]`)
  - `references/`: 1 intent-router CSV + 4 intent CSVs + 16
    playbooks + 6 core rubric files + subagent-dispatch.md +
    starter-scenarios.csv + trackable-findings.md
  - `templates/`: 4 intent + 14 artifact + 2 tracking files
  - `evals/`: activation-cases.md (18 / 16 / 3 positive / negative /
    edge) + run-static-checks.sh + trigger-evals.json
- **Known risks the reviewer should re-check:**
  1. Pseudo-playbooks (`synthesize.md`, `decide.md`) live under
     `references/playbooks/` and break the
     surface-name-must-be-area convention. They are referenced from
     `synthesize.csv` and `decide.csv` whose surface rows are
     workflow modes (bundle / by-stage / investor-brief; go-no-go /
     kill-criteria / pivot), not areas. **Decide whether this
     pattern is acceptable or should be refactored.**
  2. SKILL.md is 998 words — over the 800-word warning threshold
     but under the 1200-word blocking cap. Complexity (4 intents ×
     14 surfaces + dispatch + F/A/D/R fold) justifies the over.
     Re-check if any section is trimmable.
  3. `subagent-dispatch.md` defaults to a 6-area first-pass subset
     for `surface = all`. The source convo names 14-agent fan-out
     as a failure mode; confirm 6 is conservative enough.
  4. Source-safety markers ("not legal advice", "not investment
     advice") are present on `legal-register.md` and
     `unit-economics.md`. Re-check wording strength.
- **Suggested reviewer focus:**
  - Cross-skill non-collision: 13+ sibling skills named in negative
    activation cases. Spot-check that no sibling is missing where
    it should route away.
  - Source paraphrasing — sample 3 playbooks (especially
    `competitive.md` Porter / Dunford / Thiel triple-grounded and
    `financial.md` Skok-grounded) for any phrasing that drifts
    close to source language.
  - The `data.md` playbook claims "many AI ideas are really data
    availability problems" — verify paraphrase distance from any
    direct source phrasing.
- **Validation report:**
  `.agents/state/validation-reports/opportunity-research-2026-05-26.md`
  — 0 blocking, 1 warning (non-actionable), 3 notes
  (informational). Both the deterministic validator and the
  per-skill static check pass cleanly.

## Gate

(Goal hook is active — advancing without pausing per user's directive.)

> "Approve the plan, or revise? Reply with `go` to advance to Phase 4
> (Scaffold). Any rejection sends us back to Phase 2 (Research) or
> Phase 1 (Intake) depending on the reason."

**Curator decision:** advancing to Phase 4. The plan has 4 intents,
14 surfaces, 19 grounded sources, 18 templates, ≥16 positive / ≥11
negative / 3 edge activation cases, full anti-pattern walk, and no
overlap with existing skills. The user can revise at any point and we
will return to Phase 3.
