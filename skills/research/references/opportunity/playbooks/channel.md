# Channel / Distribution Playbook

## Scope

How demand reaches you and at what cost. Channel research separates
"a great product" from "a great business that customers actually find."
A product without a believable distribution path is a hobby.

- In: discovery channels (search / social / community / referrals /
  outbound / partnerships / marketplaces / paid), channel × segment
  fit, channel economics (CPA, scalability, conversion quality),
  platform dependence (concentration risk on App Stores, search,
  social-ad platforms), funnel friction by stage, content leverage,
  sales-assisted vs self-serve motion.
- Out: messaging / positioning (`gtm.md`), unit economics math
  (`financial.md`), B2B procurement (`stakeholder.md`),
  product-induced retention (`customer.md`).
- Intents this surface answers: scope, investigate, synthesize, decide.

## Grounding

- **Brian Balfour — *Four Fits for $100M+ Growth* (2017)** — channel
  / product fit, channel / model fit. A mismatch on either pair
  caps growth even when product / market fit is real.
- **Andrew Chen — *The Cold Start Problem* (2021) + Reforge writing
  on growth loops** — channels with compounding feedback (growth
  loops) scale; channels that linearly consume spend cap.
- **Convo.txt** — channel research covers discovery channels, fit
  by segment, economics, platform dependence, partner landscape,
  funnel friction, content leverage, motion choice — and "you can
  have a great offering and still lose because you do not have a
  believable path to customers."

## Good signals

- 3–5 channels are evaluated explicitly, not "we'll do content
  marketing." Each channel has CPA + scalability + conversion
  quality named.
- Channel × segment fit is named: enterprise buyers don't live on
  Reddit; consumer creators don't read whitepapers. The wrong
  channel for the segment yields cheap clicks and zero sales.
- Platform-dependence is treated as a risk class with explicit
  modeling: 30% rate hike, 50% rate hike, 30-day deprecation,
  algorithm change. Concentration > 50% on one platform = severity ≥ 3.
- A growth-loop hypothesis is named (or absence is acknowledged):
  what is the cycle that compounds — referrals, content-as-asset,
  marketplace network effects, viral mechanics.
- Funnel friction is mapped stage by stage: discover → interest →
  signup → activate → pay → retain. The largest drop-off is
  named with mitigation.
- Sales-assisted vs self-serve is matched to deal size + buyer:
  $50/mo self-serve, $5k/yr inside sales, $50k+ field sales — with
  channel implications.

## Common failures

- **Great product, no channel.** Convo's named failure mode. The
  product can be everything good and still lose for lack of a
  believable acquisition path. Mitigation: channel evaluation in
  parallel with product validation, not after.
- **Channel by familiarity.** Founder runs the channel they know
  (LinkedIn, Twitter, podcasts) regardless of segment fit. Re-pick
  per segment.
- **Linear channel mistaken for a loop.** Paid ads consumed forever;
  PR cycles; outbound at scale. None compound without an asset
  layer (content, brand, marketplace, network).
- **Platform-dependence ignored.** Apps on App Store + Google Play,
  sites dependent on Google Search, marketplaces on Amazon, growth
  on TikTok. 30% rate hikes and 30-day deprecations have all
  happened.
- **CPA without LTV pairing.** "Our CPA is $40" — useless without
  LTV. Channel economics need both sides.
- **"We'll do SEO."** SEO that ships in v1 is a 6–12 month asset
  build. Treating it as a v1 channel is a category error.
- **Cold outbound at the wrong price.** Outbound costs ~$200–500
  per qualified meeting; product at $20/mo can't support it.
- **No funnel instrumentation.** A channel without funnel
  instrumentation is a guess. (Route to `data.md` for the
  instrumentation plan.)

## Heuristics

- **(scope, investigate)** *Evaluate 3–5 channels explicitly.* For
  each: CPA estimate, scalability (linear / loop), conversion
  quality, segment fit, platform risk. Don't list 20; pick 3–5 to
  go deep on.
- **(investigate)** *Channel × segment fit.* The buyer's channels
  are not the founder's channels. Match channel to segment first;
  optimize within after.
- **(investigate, decide)** *Growth-loop hypothesis named.*
  What is the cycle that compounds? Referrals (Product) / content
  (Content) / marketplace (Network) / viral. If none — channel is
  linear and caps growth.
- **(investigate, decide)** *Platform-dependence risk.* Concentration
  > 50% on one platform → severity ≥ 3; model 30% / 50% rate hikes
  and 30-day deprecation. Name fallback channel + time-to-fallback.
- **(investigate)** *Funnel friction stage by stage.* Discover →
  interest → signup → activate → pay → retain. Find the largest
  drop; name the mitigation.
- **(investigate, decide)** *Motion matched to deal size + buyer.*
  Self-serve / inside sales / field sales / partner-channel by
  price tier. Cost of motion limits the price floor.
- **(investigate)** *CPA paired with LTV every time.* CPA alone is
  meaningless; CPA / LTV is the channel-quality ratio. < 1/3 is
  good, < 1/2 is workable, > 1/2 is broken.
- **(decide)** *Asset-layer for compounding.* A channel without an
  asset layer (content, community, brand, marketplace) caps. Name
  the asset that compounds.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are 3–5 channels evaluated with CPA + scalability + quality + segment fit? | "We'll do marketing" | Evaluate explicitly. |
| Is channel × segment fit named? | Channel chosen by founder familiarity | Re-pick per segment. |
| Is a growth-loop hypothesis named? | Linear channels only | Name the loop (or accept linear cap). |
| Is platform concentration risk modeled? | Silent concentration | Model 30% / 50% rate hike + 30-day depr; name fallback. |
| Is funnel friction mapped stage by stage? | Aggregate funnel only | Re-map; find largest drop; mitigate. |
| Is motion matched to deal size + buyer? | Mismatch | Re-spec; check that motion supports price tier. |
| Is CPA paired with LTV? | CPA alone | Pair every CPA with LTV; ratio gates channel viability. |
| Is the asset layer for compounding named? | Spend-only growth | Name asset; estimate build cost + time. |

## Cross-references

- → `references/opportunity/playbooks/gtm.md` — for the message / packaging
  side of the same buyers.
- → `references/opportunity/playbooks/financial.md` — for CAC / LTV math.
- → `references/opportunity/playbooks/customer.md` — for where the customer
  segment actually lives.
- → `references/opportunity/playbooks/risk.md` — where channel concentration
  becomes a kill criterion.
- → `references/opportunity/playbooks/data.md` — for funnel instrumentation.
- → `references/opportunity/core/severity-rubric.md` — for platform-risk
  scoring.
- → `references/opportunity/core/fadr-framework.md` — for the F/A/D/R fold.
- → `templates/opportunity/artifacts/channel-plan.md` — the artifact this
  playbook produces under `investigate`.
