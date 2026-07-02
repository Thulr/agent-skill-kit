# Domain Playbook

## Scope

The world the opportunity enters — workflows, vocabulary, actors,
incentives, unwritten rules, edge cases. Domain research is what
keeps a technically sound product from failing in a market it doesn't
understand. The cost of getting the domain model wrong is high and
silent; the cost of getting it right is one carefully maintained
glossary plus a stakeholder map.

- In: ubiquitous-language glossary, actor map, workflow map, success
  metrics by stakeholder, unwritten rules, edge cases, things
  outsiders consistently misunderstand.
- Out: B2B power dynamics (`stakeholder.md`), competitor analysis
  (`competitive.md`), technical feasibility (`technical.md`), legal
  / regulatory rules that are formal (`legal.md`).
- Intents this surface answers: scope, investigate, synthesize, decide.

## Grounding

- **Eric Evans — *Domain-Driven Design* (2003)** — ubiquitous
  language across team + domain experts; bounded contexts; the cost
  of an unshared domain model.
- **Christian Madsbjerg — *Sensemaking* (2017)** — thick description
  vs thin data; domain understanding from immersion, not just
  surveys.
- **Geoffrey Moore — *Crossing the Chasm* (2014)** — mainstream
  pragmatists buy from peers they trust in their domain; the
  beachhead is partly a domain-knowledge proof.
- **Convo.txt** — the operational frame: actors, workflows,
  vocabulary, rules and constraints, edge cases, incentives, success
  metrics, institutional knowledge.

## Good signals

- Glossary is maintained in the domain's vocabulary (using terms
  insiders use, including the ones that look the same as common
  English words but mean something specific — "claim," "policy,"
  "case," "ticket").
- Actors are named with their incentive and success metric: the
  underwriter optimizes for combined ratio, the broker for
  commission, the claimant for time-to-payout.
- Workflows are traced end-to-end with handoffs, queue depths, and
  typical delays. Each handoff is a place edge cases live.
- Unwritten rules are surfaced explicitly ("nobody approves a claim
  on Friday afternoon," "renewals always slip 30 days past the
  formal deadline").
- Edge cases are documented with their frequency. "Rare but
  expensive" is the case where products die.
- A short list of things outsiders consistently misunderstand is
  maintained — usually 5–15 items.

## Common failures

- **Domain as a one-time read.** Domain knowledge accretes; a
  glossary written once stays naive. Mitigation: re-visit after
  every 5–10 interviews / customer conversations.
- **Skipping edge cases.** Domains live or die at exceptions:
  "everyone files claims" hides the 3% of policies that don't allow
  claims at all and break your workflow. Mitigation: explicit
  edge-case section, not just happy-path.
- **Treating jargon as decoration.** Insider terms encode
  constraints. "An ARR-paying customer" is different from "a
  paying customer." Get the terms right; products dressed in
  insider language are more credible.
- **Workflow that's the official one, not the actual one.** Every
  domain has a published process and a real one. Research is for
  the real one; the gap between them is the opportunity surface.
- **Single-source domain knowledge.** One insider on the team is
  fragile; if they leave, the domain model goes with them.
  Mitigation: at least one insider + one outsider doing the
  glossary review.
- **Confusing domain with market.** Market = is there demand; domain
  = what matters in how the work gets done. Both matter and they're
  different.

## Heuristics

- **(scope, investigate)** *Build the glossary first.* Domain terms,
  acronyms, lookalike words (terms that mean something specific
  inside the domain and something different outside). Distinguish
  terms from concepts.
- **(investigate)** *Actor map with incentive + success metric.*
  Each actor: role, what they optimize for, how their success is
  measured, what they care about preserving, what makes them say
  yes / no.
- **(investigate)** *Trace workflows end-to-end with handoffs.*
  Where work passes between actors, what queues form, what typical
  delays are. Handoffs are edge-case habitat.
- **(investigate)** *Unwritten rules section, explicit.* "Nobody
  does X on Fridays," "everyone routes around system Y," etc. These
  rules break feature ideas that look obvious from outside.
- **(investigate, decide)** *Edge-case inventory by frequency.* List
  the unusual cases the domain handles regularly, even if 1–5%. Rare
  + expensive is the case products die at.
- **(investigate)** *Outsider-misunderstanding list.* What do
  outsiders consistently get wrong? This list doubles as the
  positioning differentiator and the new-hire onboarding doc.
- **(decide)** *Validate with insider + outsider review.* Insider
  catches naivety; outsider catches captured-thinking. Both, not
  one.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is the glossary written in the domain's vocabulary, including lookalike terms? | Outsider-language glossary | Re-interview insiders; capture verbatim. |
| Does each actor have incentive + success metric? | Role-only map | Add incentives + success metrics per actor. |
| Are workflows traced end-to-end with handoffs? | Official process only | Re-trace with insider for actual handoffs and queue depths. |
| Are unwritten rules surfaced explicitly? | Implicit | Ask insiders directly for the rules that aren't written down. |
| Is the edge-case inventory present with frequencies? | Happy-path only | Add edge cases ≥1% frequency + their consequences. |
| Are there ≥5 outsider-misunderstanding items? | Empty | Ask insiders what outsiders consistently get wrong. |
| Is the glossary reviewed by both insider + outsider? | Single perspective | Add the other; revise. |

## Cross-references

- → `references/opportunity/playbooks/stakeholder.md` — for B2B power dynamics
  built on top of the actor map.
- → `references/opportunity/playbooks/technical.md` — for translating workflow +
  edge cases into architectural constraints.
- → `references/opportunity/playbooks/legal.md` — when formal regulations
  formalize domain constraints.
- → `references/opportunity/playbooks/customer.md` — for the user-pain side of
  the domain workflow.
- → `references/opportunity/core/fadr-framework.md` — the F/A/D/R fold.
- → `templates/opportunity/artifacts/domain-glossary.md` — the artifact this
  playbook produces under `investigate`.
