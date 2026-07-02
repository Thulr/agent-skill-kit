# Go-To-Market Playbook

## Scope

How you position, message, package, and launch. Channel research asks
*where* you go; GTM research asks *how you show up* — what category,
what reference frame, what tradeoffs, what proof. Per Dunford, the
default is whatever the buyer happens to compare you against; the
deliberate version is the position you choose to fight for.

- In: target segment sequencing, positioning (category + reference
  frame + tradeoff), messaging by segment / persona, packaging and
  pricing presentation, sales motion (PLG / founder-led / outbound /
  partnership), onboarding, activation, proof (case studies,
  testimonials, benchmarks), launch plan.
- Out: where the customer is (`channel.md`), unit economics
  (`financial.md`), pure positioning critique against an existing
  pitch (`proposal-red-team`), competitor analysis without
  positioning (`competitive.md`).
- Intents this surface answers: scope, investigate, synthesize, decide.

## Grounding

- **April Dunford — *Obviously Awesome* (2019)** — positioning as
  deliberate context-setting: who is this for, what reference frame,
  what tradeoffs make those who fit love it. Defaults are someone
  else's positioning.
- **Geoffrey Moore — *Crossing the Chasm* (2014)** — beachhead and
  bowling-alley sequencing; the early-market vs mainstream gap;
  pragmatist segments need peer-references not innovator hype.
- **April Dunford's "obvious-to-target, weird-to-everyone-else"
  test** — positioning that's deliberately narrow is more durable
  than positioning that's broadly inoffensive.
- **Convo.txt** — GTM covers positioning, messaging, packaging,
  pricing presentation, sales motion, onboarding, activation, proof,
  launch plan — and "channel research asks where you go; GTM
  research asks how you show up."

## Good signals

- Target segment is sequenced — beachhead, then adjacent, with
  adjacency logic. "Everyone" is not a target.
- Positioning has three components: who it's for (segment),
  reference frame (the category / alternative the buyer compares
  against), tradeoff (what we're worse at to be better at the
  thing that matters).
- Messaging is segment-specific. The same product positioned
  differently for different segments is fine; the same message
  for every segment is suspect.
- Packaging includes 1–3 tiers max, with named "best for" criteria
  per tier — not 7 tiers and a custom column.
- Sales motion matches deal size + buyer (per `channel.md`). The
  motion implies the touchpoint cost; touchpoint cost implies the
  price floor.
- Onboarding routes the user to the first activation event quickly.
  Time-to-activation is the early-retention proxy.
- Proof artifacts are credible to the target segment: enterprise
  needs enterprise references, dev tools need GitHub stars + dev
  testimonials, prosumer needs reviews + creator endorsements.
- Launch plan names the first 30 days: who, what, when, how
  measured.

## Common failures

- **Launching to everyone.** Message resonates with no one. The
  beachhead pattern exists for this reason.
- **Position that describes the product, not the reference frame
  the buyer should hold.** "AI-native X" without context. The
  Dunford failure mode.
- **Confusing channel with positioning.** "We'll do podcasts" is
  channel. "We're the trustworthy alternative to X for Y" is
  positioning. Channels deliver positioning; without positioning,
  the channel just delivers noise.
- **Packaging by feature, not by buyer.** Tiers organized around
  internal feature toggles instead of buyer-jobs. The buyer can't
  tell which tier to pick.
- **Pricing without anchor.** A price chosen by feel; presented
  without the value anchor ("saves 5 hours/week at $40/hr =
  $800/mo of value, priced at $99"). The anchor closes the gap
  between perception and willingness.
- **Sales motion mismatch.** Self-serve product needs sales handoff
  to close a $50k enterprise deal; field-sales product can't
  support a $10/mo prosumer plan. Match motion to deal size.
- **Onboarding longer than time-to-value.** Users churn before
  they see the first useful moment. Time-to-activation is the
  metric.
- **Proof at the wrong level.** Three reference quotes from peers
  the buyer doesn't respect = no proof. Match proof to segment
  expectations.
- **Launch as an event, not a sequence.** One-day launch with no
  60-day follow-up — the cohort acquired on launch day churns
  through Q1.

## Heuristics

- **(scope, investigate)** *Beachhead sequencing.* Pick one
  segment as the beachhead with adjacency logic to the next 1–2
  segments. Sequence the messaging accordingly.
- **(investigate)** *Position with three components.* Who it's for
  (segment), reference frame (the category / alternative they
  compare against), tradeoff (what we're worse at to be better at
  what matters most). Per Dunford.
- **(investigate)** *Segment-specific messaging.* Same product;
  different message per segment. If the message is the same for
  all segments, segmentation is decorative.
- **(investigate, decide)** *Packaging at 1–3 tiers max.* "Best
  for" criteria per tier in plain language. No "Enterprise: call
  us" without a referenceable price band.
- **(investigate)** *Pricing with value anchor.* Price next to
  value computed ("saves $800/mo, priced $99"). Anchor closes
  perception gap.
- **(investigate, decide)** *Motion ↔ deal size + buyer.*
  Self-serve ($/seat or $/use < $200/mo), inside sales
  ($200–5000/mo), field sales (>$5000/mo). Mismatch caps growth.
- **(investigate)** *Time-to-activation as metric.* Onboarding's
  job is to reach activation fast; activation predicts retention.
- **(investigate, decide)** *Proof at segment level.* Enterprise
  needs enterprise references; dev tools need dev social proof;
  prosumer needs creator endorsement. Match proof to segment.
- **(decide)** *Launch as 60-day sequence.* Day 0 / day 30 / day
  60 named: who is told, what proof exists, what the activation
  metric must be for next-segment expansion to start.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is the beachhead sequenced with adjacency logic? | "Everyone" target | Pick beachhead; name adjacency. |
| Does positioning name segment + reference frame + tradeoff? | Product-described positioning | Re-position per Dunford's three components. |
| Is messaging segment-specific? | Same message all segments | Per-segment; check resonance. |
| Is packaging at 1–3 tiers with named "best-for"? | Feature-based tiers | Re-package by buyer-job. |
| Is pricing presented with value anchor? | No anchor | Anchor on customer value. |
| Is motion matched to deal size + buyer? | Mismatch | Re-spec motion. |
| Is time-to-activation defined? | Open-ended onboarding | Define activation event + target time. |
| Is proof matched to segment expectations? | Generic testimonials | Match per segment. |
| Is launch a 30 / 60 day sequence with named metrics? | Launch as event | Re-spec as sequence. |

## Cross-references

- → `references/opportunity/playbooks/channel.md` — for where the messaging is
  delivered.
- → `references/opportunity/playbooks/customer.md` — for the JTBD that
  positioning targets.
- → `references/opportunity/playbooks/competitive.md` — for the reference frame
  positioning fights for.
- → `references/opportunity/playbooks/financial.md` — for pricing's value
  anchor.
- → `references/opportunity/playbooks/stakeholder.md` — for B2B buyer vs user
  in messaging.
- → `references/opportunity/core/fadr-framework.md` — for the F/A/D/R fold.
- → `templates/opportunity/artifacts/gtm-plan.md` — the artifact this playbook
  produces under `investigate`.
