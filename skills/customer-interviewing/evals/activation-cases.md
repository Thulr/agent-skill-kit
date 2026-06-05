# customer-interviewing Activation Cases

Saved at `skills/customer-interviewing/evals/activation-cases.md`. Behavioral cases for
this single-layer skill (intents: `prep`, `critique-questions`, `conduct`, `synthesize`).

## Positive

The skill should activate and route correctly.

- "Here's my customer-interview question list — are these good questions?" → routes to
  `critique-questions`, loads `references/playbooks/critique-questions.md`.
- "Rewrite 'would you pay for this?' into something that gives real signal." → routes to
  `critique-questions`.
- "Help me plan discovery interviews for a churn problem — who do I talk to and how
  many?" → routes to `prep`, loads `references/playbooks/prep.md`, emits
  `templates/interview-plan.md`.
- "I want to set up continuous interviewing — a weekly cadence and a way to recruit." →
  routes to `prep`.
- "I freeze in interviews and end up pitching. How do I actually run the conversation?"
  → routes to `conduct`, loads `references/playbooks/conduct.md`.
- "I did six user interviews — now what? How do I make sense of them?" → routes to
  `synthesize`, loads `references/playbooks/synthesize.md`, emits
  `templates/interview-snapshot.md`.

## Negative

Near-miss prompts that share keywords but should route elsewhere. Each names the sibling.

- "Should we build this B2B SaaS idea? Validate the market and give me a go/no-go." → use `research` instead — desk/opportunity validation ending in a decision memo, not live interview craft.
- "Run a usability test on our checkout flow and find where users get stuck." → use `ux-audit` instead — evaluative testing of a built interface, not generative problem discovery.
- "Turn our research findings into a polished stakeholder memo." → use `writing-design` instead — authoring/structuring a narrative document, not synthesizing interviews into evidence.
- "Design an NPS survey to send to our whole user base." → use `research` instead (or a survey tool) — quantitative instrument design, not a one-to-one qualitative conversation.

## Boundary / edge

- "I'm about to talk to 5 users about why they churned — help me." → activates
  (generative discovery, likely `prep` or `conduct`); but if they actually want to
  evaluate a specific built flow, prefer `ux-audit`.
- "How should I interview internal stakeholders about requirements?" → activates only if
  treated as discovery-style conversation craft (`conduct` / `critique-questions`); flag
  that the respondent is an internal stakeholder, not a customer, so commitment signals
  read differently.

## Notes

- Cover the dominant phrasings users try, not just the wording in `description`.
- One negative per neighbor named in the intake brief: `research`, `ux-audit`,
  `writing-design`.
- Re-read after editing `trigger-evals.json` so the two artifacts agree.
