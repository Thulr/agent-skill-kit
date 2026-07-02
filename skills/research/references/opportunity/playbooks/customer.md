# Customer Playbook

## Scope

The pain, the job, the alternatives, the willingness to switch / pay.
Customer research succeeds when the job, the context, and the
alternative being fired are all named explicitly — and the evidence
is triangulated between stated preference (interviews, surveys) and
revealed preference (analytics, prior purchase, observed behavior).

- In: ICP definition, jobs-to-be-done, pain severity, current
  workarounds, decision criteria, willingness to pay, switching
  triggers, stated-vs-revealed evidence flagging.
- Out: market size (use `market.md`), competitive alternatives at the
  positioning level (`competitive.md`), buyer-vs-user split in B2B
  (`stakeholder.md`), channel discovery (`channel.md`).
- Intents this surface answers: scope, investigate, synthesize, decide.

## Grounding

- **Christensen / Hall / Dillon / Duncan — *Know Your Customers' Jobs
  to Be Done* (HBR 2016)** — users don't buy products, they hire
  them for a job. Name the job, the context, and what's being fired
  to make room.
- **Eric Ries — *The Lean Startup* (2011)** — build-measure-learn;
  validated learning beats vanity metrics; pivot is a forward
  decision, not an admission of defeat.
- **Teresa Torres — *Continuous Discovery Habits* (2021)** —
  research is a weekly habit, not a phase. Opportunity solution tree
  links opportunities to assumption tests.
- **Erika Hall — *Just Enough Research* (2nd ed. 2019)** — research
  is having the answers; right-sized research; the multiple-types
  taxonomy that protects you from doing only one kind.

## Good signals

- Every claim about user behavior is tagged stated / revealed and
  carries the count / source. "12 interviews" is different from
  "12 prior purchases."
- The job is named in the customer's vocabulary (verbatim quotes,
  domain terms from `domain.md`), not in product language.
- Current workaround is named explicitly. "Spreadsheets" and "email"
  count as workarounds and are usually the *real* competition (see
  `competitive.md`).
- Pain severity is anchored (frequency, monetary cost, emotional
  cost, opportunity cost). "Painful" without anchor is M-confidence
  at best.
- Willingness-to-pay test is observable: price-anchored interviews,
  smoke-test landing-page conversions, paid pilots — not "they said
  they'd pay."
- An explicit beachhead segment is named with the adjacency logic to
  the next segment.

## Common failures

- **Stated-only evidence treated as revealed.** "Most people said
  they'd switch" with no test of actual switching behavior is M at
  best; treating it as H drives the wrong product. Mitigation: tag
  every claim stated / revealed; auto-promote unanchored stated
  claims to Assumption + test.
- **Asking users what they want and shipping it.** Users describe
  the workaround, not the job. Mitigation: name the job, then the
  desired progress, then the obstacle — not the feature.
- **Persona without pain severity, workaround, or willingness to
  switch.** A persona that lists demographics + a one-line goal is a
  marketing artifact, not a research artifact.
- **Sampling on success.** Talking only to people who like the idea
  (founder's network, friendly users). Mitigation: deliberately
  sample non-users and former users.
- **JTBD as feature wrapper.** Restating the product's features as
  "jobs" without independently identifying the job from the customer
  side.
- **Single segment ICP without adjacency.** An ICP that doesn't
  explain who comes next leaves you with no growth path.

## Heuristics

- **(scope, investigate)** *Name the job, the context, and what's
  fired.* JTBD frame: "When [context], I want to [job], so I can
  [progress]. Today I [workaround]; I would fire it for [switch
  trigger]." Distinct from feature requests.
- **(investigate)** *Tag every behavior claim stated or revealed.*
  Stated-only → ceiling M, auto-promote to Assumption + test in
  F/A/D/R.
- **(investigate, decide)** *Anchor pain severity.* Frequency × cost
  (monetary / time / emotional / opportunity). "Annoying" doesn't
  drive switching; "expensive every Monday" does.
- **(investigate)** *Sample non-users and former users.* The most
  informative interviews are people who churned out, considered and
  rejected, or chose the workaround. Mitigates founder-network bias.
- **(scope, investigate)** *Name the beachhead with adjacency
  logic.* One segment by job + context, the reason it goes first,
  the segment that goes next, and how this one's adoption opens it.
- **(decide)** *Convert top assumptions into <1-week tests.* The
  highest-leverage Assumption becomes the next falsifiable
  experiment (paid pilot, landing-page smoke test, concierge
  service). Research without a next test is the failure mode.
- **(investigate, decide)** *Distinguish willingness to switch from
  willingness to pay.* They diverge. Switching is friction-bound;
  paying is value-bound. Name both.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is the job named in customer vocabulary, with context and fired alternative? | Feature dressed as JTBD | Re-interview; capture verbatim. |
| Is every behavioral claim tagged stated / revealed? | Silent treatment as revealed | Tag; auto-promote unanchored stated to Assumption + test. |
| Is pain severity anchored (frequency × cost)? | "Painful" with no anchor | Find frequency and cost from interviews / analytics; downgrade if you can't. |
| Are former users / rejecters / churned users in the sample? | Sampling on success | Re-sample explicitly across cohorts. |
| Is willingness to pay tested (paid pilot, smoke test, anchor), not just claimed? | Stated WTP only | Run a willingness-to-pay test before treating WTP claims as facts. |
| Is the beachhead named with adjacency? | Vague segment | Name segment + adjacency reason. |
| Is the next falsifiable assumption test named? | No next test | Name the top Assumption and its <1-week test. |

## Cross-references

- → `references/opportunity/playbooks/market.md` — for sizing the customer pain at the
  segment / market level.
- → `references/opportunity/playbooks/competitive.md` — for the workaround / do-nothing
  alternative as competition.
- → `references/opportunity/playbooks/stakeholder.md` — when user ≠ buyer
  (B2B / enterprise).
- → `references/opportunity/playbooks/channel.md` — for where these customers
  actually live and how to reach them.
- → `references/opportunity/core/confidence-rubric.md` — for the
  stated-vs-revealed evidence rules.
- → `references/opportunity/core/fadr-framework.md` — for the F/A/D/R fold at
  artifact end.
- → `templates/opportunity/artifacts/icp-and-jtbd.md` — the artifact this
  playbook produces under `investigate`.
