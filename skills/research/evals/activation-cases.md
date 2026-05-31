# Activation cases — research

The `research` skill routes by decision-frame: **report** (open-ended topic
research, no decision) and **opportunity** (validate a named opportunity toward an
F/A/D/R go/no-go). Cases below are grouped by frame; they were merged from the
former `topic-research` and `opportunity-research` skills when the two consolidated
(see docs/specs/2026-05-28-catalog-consolidation/).

---

## Report frame (formerly topic-research)


Natural-language activation and behavioral cases for the
topic-research skill. Each case names the expected behavior (route
selected, output produced, or refusal to activate).

## Positive cases

These should activate topic-research and route to the named depth.

- **"Research the current state of developer documentation for AI APIs."**
  → `survey`. Topic is concrete, scope is moderate. Default depth.
- **"Give me a primer on differential privacy."**
  → `brief`. "Primer" signals orientation, ~1-page output.
- **"Do a thorough literature review on retrieval-augmented generation."**
  → `deep-dive`. "Thorough" + "literature review" signals exhaustive mode.
- **"Tell me what's known about server-driven UI patterns."**
  → `survey`. Open-ended request for structured knowledge.
- **"Summarize the literature on prompt injection defenses."**
  → `survey`. "Summarize the literature" = scoping/survey shape.
- **"What's the state of the art in formal verification of smart contracts?"**
  → `survey` or `deep-dive` depending on user signal on depth.
- **"I want to learn about CAP theorem trade-offs."**
  → `brief`. "Learn about" with a focused concept = primer.
- **"Get me up to speed on multi-tenant database isolation strategies."**
  → `survey`. "Up to speed" = mid-depth orientation.

## Negative cases

These should NOT activate topic-research; they belong to other skills.

- **"Validate whether building a docs-as-code SaaS is a good opportunity."**
  → `opportunity-research`. Named opportunity to validate (go/no-go), not a topic to learn about.
- **"Review this design doc for weaknesses."**
  → `spec-red-team` or `proposal-red-team`. Critique of existing artifact.
- **"Compare Postgres and MySQL for our workload."**
  → `tradeoff-analysis`. Fixed options to compare, not open research.
- **"Brainstorm names for our new SDK."**
  → `bmad-brainstorming` or `novel-ideation`. Ideation, not research.
- **"Fix the failing test in user_test.py."**
  → No skill — this is a coding task.
- **"Audit our API docs for DX problems."**
  → `dx-critique`. Review of existing artifact, not topic research.
- **"What should we ship next quarter?"**
  → Strategy/prioritization, not topic research. Probably `nominal-group-technique` or a roadmap skill.
- **"Critique my user research interview guide."**
  → `interview-guide-critique`. Critique of existing instrument.

## Edge cases

Cases that look like topic-research but require careful handling.

- **"Research AI."** — Activates, but the topic is too broad. The skill
  must ask one blocker question to narrow scope before searching.
  Without narrowing, the report produces a 20-page survey of nothing.
- **"Research how OAuth 2.0 works."** — Activates as `brief`. Even
  though it sounds like a question, the user wants a primer-shaped
  output. Don't treat it as a one-line factual answer.
- **"What does the research say about X — is it worth investing in?"** —
  Mixed signal: "what does the research say" sounds like topic-research,
  but "is it worth investing in" is a decision frame. Ask one
  disambiguating question: do they want the research report (this
  skill) or the validation memo (opportunity-research)?
- **"Read these three papers and tell me what they say."** — Borderline.
  If the user provides specific sources, the search-strategy step is
  short-circuited. Can still produce a report-shaped output, but
  treat as `brief` and surface that the search was user-provided.
- **"Do research on documentation for developer experience."** — Activates
  as `survey`. This is the canonical example for which topic-research
  exists: catch-all "research X for me" without a decision frame.
- **"Research and decide whether we should adopt Bun."** — Hybrid. The
  research part fits topic-research; the decision part does not.
  Surface the split: offer topic-research for the evidence base,
  then point at tradeoff-analysis or opportunity-research for the
  decision.

## Output requirements (behavioral)

Every report produced by topic-research must include:

- A one-sentence research question with explicit in-scope / out-of-scope.
- The depth mode applied.
- The search strategy (source types, terms, exclusions).
- Confidence (H/M/L) on every load-bearing claim.
- A citation at the point of every load-bearing claim.
- Explicit limitations section naming what was not covered.
- A "what would change this report" pointer to evidence that would
  meaningfully revise the conclusions.

A report missing any of these is not topic-research output.

---

## Opportunity frame (formerly opportunity-research)


Activation cases for the `opportunity-research` skill. The validator
counts bullets under `## positive`, `## negative`, and `## edge` /
`## boundary` headers and verifies each negative names a sibling
skill it disambiguates from.

## Positive

- "we're considering building an AI-powered scheduling assistant for in-home healthcare visits — can you help me figure out which research areas actually matter before we commit?" → route: `scope/all` — first-pass stage-aware shortlist.
- "size the market for an AI coding assistant aimed at solo founders shipping side projects" → route: `investigate/market`
- "I want to understand who the actual customer is for a tool that helps lawyers draft initial pleadings — JTBD + pain severity, not feature requests" → route: `investigate/customer`
- "map the competitive landscape for our developer-focused log analytics product, including the do-nothing alternative" → route: `investigate/competitive`
- "build a domain glossary and workflow map for B2B payments reconciliation — I want to know what outsiders consistently get wrong" → route: `investigate/domain`
- "is it technically feasible to build a CRM with offline-first sync that can handle 100k contacts per device? give me 3 architecture options" → route: `investigate/technical`
- "do we have the data we'd need to train per-customer churn prediction, or is this an AI idea that's actually a data problem?" → route: `investigate/data`
- "what does the operating model look like if we serve regulated healthcare — staffing, support tiers, runbooks, vendor SLAs?" → route: `investigate/operational`
- "do the unit economics support a $19/mo prosumer subscription — base, best, and worst case with named drivers?" → route: `investigate/financial`
- "what legal questions should we escalate to counsel before storing EU citizen data in our analytics product?" → route: `investigate/legal`
- "where do users for a developer-focused open-source CLI actually come from — and what's the channel concentration risk if we overinvest in HN?" → route: `investigate/channel`
- "position our product against the do-nothing alternative for SMB accountants — what category, what reference frame, what tradeoff?" → route: `investigate/gtm`
- "for a $50k enterprise pilot in mid-market manufacturing, who needs to sign off — users, buyers, approvers, blockers, champion?" → route: `investigate/stakeholder`
- "build the risk register for our SaaS launch — 11 categories, severity x likelihood, severity-4 → kill criteria" → route: `investigate/risk`
- "is now the right window for AI-native browsers, or are we too early — separate signals from narratives, name what would resolve the timing call" → route: `investigate/trend`
- "we have 6 area briefs already, pull them into one decision-ready opportunity brief for the board" → route: `synthesize/bundle`
- "convert the investigation into a go / no-go decision with named kill criteria and review trigger" → route: `decide/go-no-go`
- "given the investigation, what kill criteria should we forward-commit to so we don't re-litigate later?" → route: `decide/kill-criteria`

## Negative

- "brainstorm 20 new feature ideas for our existing product" → use `morphological-analysis` or `scamper` or `novel-ideation` — opportunity-research is for validating a *named* opportunity, not generating candidates.
- "red-team this pitch deck — what objections will leadership raise?" → use `proposal-red-team` — opportunity-research produces the underlying substrate; red-team adversarially reviews the finished artifact.
- "stress-test our migration plan to mid-market — what could go wrong with the sequencing?" → use `plan-red-team` — opportunity-research does not review execution plans.
- "do a premortem on this launch — assume it failed in 18 months and work backwards" → use `premortem` — risk playbook here borrows the heuristic, but the dedicated skill runs the full backwards-from-failure interview.
- "critique this user-interview script — too leading, missing critical-incident probes?" → use `interview-guide-critique` — that skill audits research instruments; opportunity-research consumes interview output, doesn't critique it.
- "review my user-persona docs for evidence gaps and stereotype risk" → use `persona-critique` — opportunity-research builds new ICPs from the customer playbook; doesn't audit existing persona docs.
- "audit the clean-architecture of our microservices boundaries" → use `architecture-critique` — that's code-architecture review, not opportunity-research.
- "review the developer experience of our public SDK — friction, errors, examples, docs" → use `dx-critique` — DX craft, not opportunity validation.
- "run a usability audit on our checkout funnel" → use `ux-critique` — end-user UX, not opportunity-research.
- "set up a shared context file once so future reviews don't re-ask the same problem / audience / constraints questions" → use `validation-context` — it captures shared context; opportunity-research executes the actual research afterwards.
- "compare these three CRM vendors we shortlisted last week" → use `tradeoff-analysis` — that skill compares named options; opportunity-research is for the upstream "which research areas matter?" pass.
- "is this metric a good measure of activation, or can it be gamed?" → use `metric-sanity-check` — narrow metric critique; opportunity-research touches metrics inside artifacts but doesn't substitute for a metric audit.
- "review my survey questions for biased framing" → use `survey-question-review` — research-instrument audit, not opportunity-research.

## Edge

- "research this" (no object) → opportunity-research activates **only after** the user names the opportunity in one line. Fanning out 14 sub-agents without scope produces 14 disconnected dumps — the named failure mode in the source. Ask one blocker question first.
- "should we enter this market?" (no opportunity named) → activates only if the user names the opportunity / segment in the same prompt or in a one-question clarification. Otherwise route to `scope/all` for stage-aware shortlist after the clarification.
- "just give me the market size in dollars" → activates on `investigate/market` but emits a single artifact (`market-sizing.md`) and skips the F/A/D/R fold's full decision treatment unless the user opts in. The skill should not over-scope a narrow request into a 14-area fan-out.
