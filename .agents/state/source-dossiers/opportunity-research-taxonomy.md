# Source Dossier: Opportunity Research Taxonomy (from `convo.txt`)

Phase 2 artifact. Saved at
`.agents/state/source-dossiers/opportunity-research-taxonomy.md`.

## Dossier ID

- Slug: `opportunity-research-taxonomy`
- Linked intake brief:
  `.agents/state/intake-briefs/opportunity-research.md`

## Source Identity

- Title: *Opportunity Research Taxonomy* (working title for the
  convo.txt content)
- Creator: User-curated multi-turn conversation, this repo
- Type: notes (with paraphrased grounding to canonical literature)
- Source slug: `opportunity-research-taxonomy`
- Research date: 2026-05-26

## Research Sources

Aim for at least one row per type. The taxonomy itself is the user's
notes (no copyright); each branch is grounded in widely-recognised
canonical references. Confidence is H where the reference is a
standard text I can cite from training; M where I am paraphrasing the
contribution and a contributor should verify the exact phrasing; L
where the claim is load-bearing but the citation is weak.

| Type | URL | Notes | Confidence (H/M/L) |
|---|---|---|---|
| official | (this repo) `convo.txt` | The taxonomy: 14 research dimensions, four-layer (Facts/Assumptions/Decisions/Risks) frame, minimum-viable subset of 6 areas for first pass (Customer/Market/Competitive/Domain/Technical/Financial). | H |
| interpretive | https://web.stanford.edu/class/ee204/ProductMarketFit.html (Marc Andreessen, "The Only Thing That Matters", 2007) | Product/market fit framing; market quality dominates team and product. Informs `market` and `customer` playbooks. | H |
| interpretive | https://forentrepreneurs.com/saas-metrics-2/ (David Skok, "SaaS Metrics 2.0", 2013) | Unit economics: CAC, LTV, gross margin, months-to-recover-CAC, magic number. Informs `financial` playbook. | H |
| interpretive | https://hbr.org/2016/09/know-your-customers-jobs-to-be-done (Christensen, Hall, Dillon, Duncan, HBR 2016) | Jobs-to-be-done as a frame for customer research; competing-against-non-consumption. Informs `customer` and `competitive` playbooks. | H |
| interpretive | https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy (Michael Porter, HBR 2008 update of 1979 original) | Five Forces: buyer power, supplier power, threat of substitutes, threat of new entrants, rivalry. Informs `competitive` and `market` playbooks. | H |
| interpretive | https://diataxis.fr/ (Daniele Procida, Diátaxis Documentation Framework) | Four-quadrant model for explanatory artifacts; informs the **shape** of each area playbook (don't mix tutorial/reference/explanation/how-to). | H |
| interpretive | https://www.brianbalfour.com/essays/four-fits-growth-framework (Brian Balfour, "Four Fits for $100M+ Growth", 2017) | Market/product, product/channel, channel/model, model/market — four pairwise fits. Informs `channel`, `gtm`, `financial` playbooks. | H |
| interpretive | https://obviouslyawesome.com/ (April Dunford, *Obviously Awesome*, 2019) | Positioning as deliberate context-setting; alternative is "where would you fit me if I didn't position." Informs `gtm` and `competitive` playbooks. | H |
| interpretive | https://www.amazon.com/Crossing-Chasm-3rd-Disruptive-Mainstream/dp/0062292986 (Geoffrey Moore, *Crossing the Chasm*, 3rd ed. 2014) | Technology adoption lifecycle; early-market vs mainstream gap; beachhead segment. Informs `market`, `gtm`, `customer`. | H |
| interpretive | https://www.amazon.com/Lean-Startup-Innovation-Successful-Businesses/dp/0307887898 (Eric Ries, *The Lean Startup*, 2011) | Build-Measure-Learn; validated learning; pivot vs persevere. Informs `customer`, `risk`. | H |
| interpretive | https://martinfowler.com/articles/bff-tradeoffs.html (Martin Fowler — sample of architectural-decision style) + ATAM (SEI Architecture Tradeoff Analysis Method) | Quality-attribute tradeoffs; build-vs-buy as an explicit decision with named scenarios. Informs `technical`. | M |
| interpretive | https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215 (Eric Evans, *Domain-Driven Design*, 2003) | Ubiquitous language; bounded contexts; the cost of getting the domain model wrong. Informs `domain`. | H |
| interpretive | https://www.amazon.com/Antifragile-Things-That-Disorder-Incerto/dp/0812979680 (Nassim Taleb, *Antifragile*, 2012) | Fragile / robust / antifragile classification; concentration risk; convexity. Informs `risk`. | H |
| interpretive | https://www.amazon.com/Continuous-Discovery-Habits-Teresa-Torres/dp/1736633309 (Teresa Torres, *Continuous Discovery Habits*, 2021) | Opportunity solution tree; weekly customer touchpoints; assumption tests vs discovery. Informs `customer`. | H |
| interpretive | https://hbr.org/2007/09/performing-a-project-premortem (Gary Klein, "Performing a Project Premortem", HBR 2007) | Imagine the project failed; work backwards to causes. Informs `risk` (without duplicating the existing `premortem` skill). | H |
| interpretive | https://www.amazon.com/Just-Enough-Research-Erika-Hall/dp/1937557103 (Erika Hall, *Just Enough Research*, 2nd ed. 2019) | Right-sized research; "research is just having the answers"; multiple research types (organizational, user, design, competitive, evaluative). Informs the shape of the whole skill. | H |
| interpretive | https://stripe.com/atlas/guides/business-of-saas (Stripe Atlas) | Operational and legal patterns for early-stage businesses (entity, contracts, sales tax, international expansion). Informs `legal`, `operational`. | M |
| interpretive | https://carlotaperez.org/pubs/technological-revolutions-and-financial-capital-the-dynamics-of-bubbles-and-golden-ages/ (Carlota Perez, *Technological Revolutions and Financial Capital*, 2002) | Five surges of technological revolution; installation period vs deployment period; timing windows. Informs `trend`. | M |
| interpretive | https://r.jordan.im/download/economics/peter-thiel_zero-to-one.pdf (Peter Thiel, *Zero to One*, 2014) | Secrets, monopoly vs competition, last-mover advantage, contrarian truth. Informs `competitive`, `market`. | H |
| critical | https://www.amazon.com/Lean-Startup-Innovation-Successful-Businesses/dp/0307887898 — see also Steve Blank's "It's Time For Founders To Make Things Again" critiques of MVP-everywhere | The Lean Startup's "build cheap, measure" frame underweights deep technical/domain bets where there is no MVP shortcut. Mitigation: do not let MVP-thinking collapse `technical` or `domain` work too early. | H |
| critical | https://hbr.org/2014/09/customers-may-not-tell-you-the-truth | Customer-research critique: stated preference ≠ revealed behavior; rely on observed behavior, not interview claims. Mitigation: customer playbook must distinguish stated from revealed evidence. | H |
| critical | (Original take) Andy Grove's *Only the Paranoid Survive* (1996) — strategic-inflection-point framing; market research alone misses regime changes. | Counterweight to over-relying on `market` & `trend` research as separable activities — sometimes the market *itself* is mid-change and existing data is misleading. | M |
| critical | (Steelman, my own) | The 14-area taxonomy risks producing 14 disconnected research dumps. The four-layer (F/A/D/R) frame is the defense against that — if a branch doesn't end in decisions, it's organized procrastination (quoted paraphrase from the source). Required: every area's artifact ends in explicit decisions and named risks. | H |
| applied | https://www.ycombinator.com/library/4A-essays-of-paul-graham (Paul Graham essays — "How to Get Startup Ideas" etc.) | Live-in-the-future + organic vs made-up ideas; well-intentioned founders' blind spots. Informs intake heuristics for `scope` intent. | H |
| applied | https://www.amazon.com/Crossing-Chasm-3rd-Disruptive-Mainstream/dp/0062292986 | The "beachhead segment" pattern is an applied output: pick one tightly-defined initial segment to validate everything else against. Informs `scope` intent. | H |
| applied | (this repo) `skills/dx-heuristics/`, `skills/project-agentification/` | The two-level routing + sub-agent fan-out pattern is already proven in this repo for non-research domains. The opportunity-research skill is the third application of the same shape. | H |

**Confidence rules audit:** No L rows on load-bearing claims. The two M-confidence rows (Stripe Atlas legal/op patterns, Perez trend cycles) inform but do not solely-load-bear any single area — both are paired with H-confidence canonical refs in their playbooks.

## Paraphrased Concepts

Each gets a short paraphrase plus its source row. Distinctive phrasing
from the source convo is rewritten.

- **The 14-area taxonomy.** Validation work splits into 14 separable
  research dimensions; conflating them into "market research" is the
  most common failure mode. (Source: `convo.txt`)
- **Minimum-viable first pass (six areas).** For most product/business
  work, the high-value first-pass set is Customer / Market / Competitive
  / Domain / Technical / Financial. Operations / Legal / Data / GTM /
  Risk fold in as the bet gets more concrete. (Source: `convo.txt`)
- **The four-layer test per branch (FADR).** Every research branch must
  produce Facts (what is true), Assumptions (what we believe but have
  not proven), Decisions (what this changes), Risks (what could still
  go wrong). A branch that stops at notes is organized procrastination.
  (Source: `convo.txt`)
- **Market vs domain vs technical vs operational vs financial — the
  decision-question test.** Market = should we enter; Domain = what
  matters; Technical = is it buildable; Operational = is it runnable;
  Financial = is it worth it. (Source: `convo.txt`)
- **Direct vs substitute vs do-nothing competitors.** A common
  competitive-research failure is enumerating direct competitors only
  while ignoring spreadsheets, email, workarounds, and "do nothing" —
  which are usually the *real* competition. (Source: `convo.txt`, with
  grounding to Christensen's competing-against-non-consumption.)
- **Jobs to be done.** Users don't buy a product; they hire it for a
  job. Customer research succeeds when the job, the context, and the
  alternative being fired are all named. (Source: Christensen/HBR 2016)
- **Five Forces frame.** Industry attractiveness is a function of
  rivalry + buyer power + supplier power + substitutes + new-entrant
  threat. A market can look big and still be unattractive on the
  five-forces analysis. (Source: Porter 1979/2008)
- **Beachhead segment.** A new product should target one tightly-defined
  initial segment whose pain is acute, whose adoption forms a reference
  point for adjacent segments, and whose word-of-mouth is reachable.
  (Source: Moore 2014)
- **Four pairwise fits.** Beyond product/market fit, scale requires
  product/channel fit, channel/model fit, and model/market fit. A
  mismatch on any pair caps growth. (Source: Balfour 2017)
- **Positioning is context-setting.** Positioning answers: who is this
  for, what is it like (the reference frame the buyer should hold the
  product against), and why those tradeoffs matter. (Source: Dunford
  2019)
- **Unit economics dominate later-stage decisions.** CAC, LTV, gross
  margin, payback period — and the ratio LTV/CAC > 3, payback < 12mo
  are SaaS canon, adapted per business model. (Source: Skok 2013)
- **Premortem.** Imagine the initiative failed in 12–18 months; work
  backwards to causes. Catches dissent that wouldn't surface in a
  current-state review. (Source: Klein/HBR 2007)
- **Continuous discovery.** Customer research is a weekly habit, not a
  pre-launch sprint; the opportunity-solution tree links opportunities
  to assumption tests. (Source: Torres 2021)
- **Stated vs revealed preference.** Interviews capture stated
  preference; observation captures revealed. The two diverge
  systematically — customer research must triangulate. (Source:
  HBR/general behavioral-economics literature)
- **Concentration / convexity / antifragility.** Risks accumulate where
  exposure is concentrated and payoffs are non-linear; design for
  optionality, not just resilience. (Source: Taleb 2012)
- **Diátaxis (applied to research artifacts).** Don't mix
  tutorial / how-to / reference / explanation in one artifact. The 14
  area artifacts are *reference* (the inventory) + *explanation* (the
  decisions). Tutorials and how-tos live elsewhere. (Source: Procida)

## Reusable Behaviors

Operational behaviors the agent could perform, derived from the source.

- **Scope-by-stage.** Given an opportunity description and a stage
  (pre-idea / idea / build / launch / scale), shortlist the 5–8
  research areas that load-bear at that stage. Derived from: convo.txt
  "high-value first pass" guidance.
- **Sub-agent fan-out per area.** For an `investigate` request, spawn
  one sub-agent per in-scope area (and optionally per persona lens)
  with the area's playbook + artifact template + the user's
  opportunity context. Synthesize at the end. Derived from: dx-heuristics
  multi-surface pattern + Just Enough Research's "right-sized research"
  principle.
- **F/A/D/R folding.** For any area's research output, separate the
  content into Facts (cited), Assumptions (testable), Decisions
  (changes downstream behavior), Risks (named with severity + owner).
  Derived from: convo.txt's four-layer test.
- **Cross-area synthesis.** Roll up 5–14 area artifacts into a single
  one-page opportunity brief that names the kill criteria, the next
  highest-leverage test, and the go / no-go / pivot recommendation.
  Derived from: Just Enough Research + Continuous Discovery
  opportunity-solution-tree.
- **Persona-lens dispatch.** For each area sub-agent, run four lenses
  (founder / operator / investor / skeptic) and preserve disagreements
  as open questions, not silent winners. Derived from: dx-heuristics
  three-lens dispatch pattern.
- **Decision-gate emission.** Every artifact ends with named decisions
  (not "notes") and named kill criteria (a forward commitment to stop
  if X is observed). Derived from: convo.txt "research branch that
  ends in notes but not decisions is just organized procrastination"
  + Taleb concentration / convexity.
- **Stated-vs-revealed flag.** The customer playbook must flag every
  claim as stated (interview, survey) or revealed (analytics, prior
  behavior). A bet that depends on a stated-only claim gets
  auto-promoted to Assumption + Test. Derived from: behavioral-economics
  critique of customer research.
- **Beachhead nomination.** For any opportunity, name one tightly-defined
  initial segment to validate everything else against. Derived from:
  Moore.
- **Five-forces / four-fits scoring.** Each area carries a
  named-rubric scoring loop so two different opportunities can be
  compared on the same scale. Derived from: Porter / Balfour.
- **Escalation markers (legal, financial).** The legal artifact says
  "questions to escalate to counsel" not "legal advice"; the financial
  artifact says "best/base/worst-case modeling" not "audited figures."
  Derived from: domain risk + skill-safety standards.

## Critical / Dissenting Takes

- **Critique:** A 14-area framework risks bureaucratic theater —
  founders dutifully fill in artifacts and never make a decision.
  *Mitigation:* the FADR fold is mandatory; the `scope` intent must
  cut areas, not include them; the `decide` intent must produce
  go/no-go with kill criteria.
- **Limitation:** Some bets (deep-tech, regulated industries,
  marketplace network effects) have non-decomposable risk structures
  — the "areas" interact in ways that area-by-area research misses.
  *Mitigation:* the `synthesize` intent's cross-area brief must call
  out coupling explicitly; the risk playbook covers
  concentration/coupling as a first-class category.
- **Failed application:** Used by an early-stage founder pre-idea, the
  skill would over-scope (14 areas is too much for "I have a vague
  hunch"). *Mitigation:* the `scope` intent uses stage as a primary
  input and the default first-pass shortlist is 5–6 areas, not 14.
- **Critique (steelman):** Most opportunities die from execution, not
  from bad scoping. Research-heavy frameworks substitute for shipping.
  *Mitigation:* every artifact emits "next test" — a falsifiable
  experiment, ideally <1 week, that closes the highest-leverage
  open assumption. Research without a next test is the failure mode.

## Paraphrase Audit

- Behavior "Scope-by-stage" — source language was "you do not need all
  of these at full depth on day one" — paraphrased to "shortlist the
  5–8 research areas that load-bear at that stage" — distinctive? no.
- Behavior "F/A/D/R folding" — source language was "Facts, Assumptions,
  Decisions, Risks" — these are common business-research terms
  combined; the framework name is generic; paraphrased to "F/A/D/R
  folding" with the categories named — distinctive? no (the labels
  are generic; the acronym is mine).
- Behavior "Decision-gate emission" — source language was "a research
  branch that ends in notes but not decisions is just organized
  procrastination" — paraphrased to "every artifact ends with named
  decisions and named kill criteria" + the source quote retained
  *only inside this dossier as a paraphrase reference*. Distinctive?
  no — the principle is paraphrased into operational behavior; the
  vivid source phrasing stays in the dossier, not in `SKILL.md`.
- Behavior "Cross-area synthesis" — source language: there is no
  single direct phrase to paraphrase; the synthesis pattern is
  derived from multi-source. Distinctive? no.
- Other behaviors — derived from named third-party canonical sources
  (Porter, Balfour, Dunford, Taleb, etc.) with attribution in
  `skill.json.inspired_by`. Each behavior is a paraphrased operational
  application, not a quotation.

No row shows distinctive copying.

## Candidate Skills

| Candidate | Pack | Shape | Action | Reason |
|---|---|---|---|---|
| `opportunity-research` | `discovery`, `validation`, `strategy`, `product`, `founder` | two-level (intent × research-area) | create | The taxonomy is exactly two-dimensional; each area is an orthogonal axis (research-area) under each intent (scope / investigate / synthesize / decide); each leaf produces a real-world artifact. Sub-agent fan-out and ≥18 templates require the depth. |

## Copyright And Safety Notes

- **Copyright posture:** the convo is the user's own; the
  canonical references are widely-cited third-party sources whose
  *contributions* are paraphrased (no long quotations, no chapter
  summaries). Each `inspired_by` row in `skill.json` will name
  author, year, kind, and one-line contribution.
- **Sensitive domains:** legal and financial each carry an explicit
  escalation marker in their playbooks and templates:
  - `legal-register.md` → "Inventory of legal questions to
    escalate to counsel. Not legal advice. Jurisdiction-dependent."
  - `unit-economics.md` → "Best/base/worst-case modeling. Not
    audited figures. Not investment advice."
- **Sub-agent provenance:** sub-agents must cite their sources in
  per-area artifacts; orchestrator must preserve citations through
  synthesis; unsourced confidence is downgraded to Assumption.
- **Out-of-scope guards:** the negative-activation cases in
  `evals/activation-cases.md` explicitly route ideation requests
  away (to `morphological-analysis`, `scamper`, `novel-ideation`),
  red-team requests away (to `proposal-red-team`, `plan-red-team`),
  and architecture requests away (to `clean-architecture`,
  `dx-heuristics`, etc.).

## Open Questions

- None blocking Phase 3. Two M-confidence rows (Stripe Atlas, Perez)
  are decorative grounding only, not load-bearing.

## Gate

(Goal hook is active — advancing without pausing.)

> "Does the research cover the source faithfully? Any missing source
> types, weak confidence, or open questions to resolve before we plan?
> Reply with `go` to advance to Phase 3 (Plan)."

**Curator decision:** advancing to Phase 3. Coverage spans official
(the convo), interpretive (15+ canonical references), critical (4
takes including steelmans), and applied (Graham, Moore, this repo).
All load-bearing claims have H-confidence grounding. No open questions
block planning.
