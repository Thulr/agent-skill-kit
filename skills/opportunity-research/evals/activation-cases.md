# activation-cases.md — opportunity-research

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
- "audit the clean-architecture of our microservices boundaries" → use `clean-architecture` — that's code-architecture review, not opportunity-research.
- "review the developer experience of our public SDK — friction, errors, examples, docs" → use `dx-heuristics` — DX craft, not opportunity validation.
- "run a usability audit on our checkout funnel" → use `ux-accessibility-heuristics` — end-user UX, not opportunity-research.
- "set up a shared context file once so future reviews don't re-ask the same problem / audience / constraints questions" → use `validation-context` — it captures shared context; opportunity-research executes the actual research afterwards.
- "compare these three CRM vendors we shortlisted last week" → use `tradeoff-analysis` — that skill compares named options; opportunity-research is for the upstream "which research areas matter?" pass.
- "is this metric a good measure of activation, or can it be gamed?" → use `metric-sanity-check` — narrow metric critique; opportunity-research touches metrics inside artifacts but doesn't substitute for a metric audit.
- "review my survey questions for biased framing" → use `survey-question-review` — research-instrument audit, not opportunity-research.

## Edge

- "research this" (no object) → opportunity-research activates **only after** the user names the opportunity in one line. Fanning out 14 sub-agents without scope produces 14 disconnected dumps — the named failure mode in the source. Ask one blocker question first.
- "should we enter this market?" (no opportunity named) → activates only if the user names the opportunity / segment in the same prompt or in a one-question clarification. Otherwise route to `scope/all` for stage-aware shortlist after the clarification.
- "just give me the market size in dollars" → activates on `investigate/market` but emits a single artifact (`market-sizing.md`) and skips the F/A/D/R fold's full decision treatment unless the user opts in. The skill should not over-scope a narrow request into a 14-area fan-out.
