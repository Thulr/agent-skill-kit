# activation-cases.md — topic-research

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
  → `dx-heuristics`. Review of existing artifact, not topic research.
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
