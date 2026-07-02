# Market Playbook

## Scope

Whether and how big the opportunity is at the level of demand,
segments, growth, structure, and timing. Routes to `customer.md` for
the pain-and-willingness-to-pay axis; to `competitive.md` for
positioning and substitutes; to `trend.md` for timing-window
analysis. Answers Andreessen's "the only thing that matters" — is
there a real market that pulls a product into fit.

- In: TAM / SAM / SOM sizing, segment shape, growth, demand signals,
  market structure (fragmented vs winner-take-most), Porter's Five
  Forces at market level, beachhead-segment identification.
- Out: pain severity (use `customer.md`), competitive moats
  (`competitive.md`), unit economics (`financial.md`), regulatory
  exposure (`legal.md`).
- Intents this surface answers: scope, investigate, synthesize, decide.

## Grounding

- **Marc Andreessen — *The Only Thing That Matters* (2007)** — market
  quality dominates team and product; the market 'pulls' a
  fit-finding product into shape. The market is a quality, not just a
  size.
- **Michael Porter — *Five Competitive Forces* (1979 / 2008 HBR)** —
  market attractiveness is structural: rivalry, buyer power, supplier
  power, substitutes, new-entrant threat. A big market can be
  unattractive.
- **Geoffrey Moore — *Crossing the Chasm* (2014)** — the technology
  adoption lifecycle and the chasm between early-market enthusiasts
  and mainstream pragmatists. Mainstream pragmatists need a beachhead.
- **Peter Thiel — *Zero to One* (2014)** — sub-segment monopoly beats
  fractional share of a giant market; small + dominated > large +
  contested.

## Good signals

- Sizing is given at three resolutions: TAM (universe), SAM (you
  could reach), SOM (year-1 realistic capture). All three have
  explicit assumptions named.
- Segments are defined by job, behavior, or context — not just by
  industry / company size / demographic. The segment can be
  *reached* via a named channel.
- Five Forces analysis is present and produces an explicit
  attractiveness call (not a generic "fragmented industry" label).
- A beachhead segment is named with the reason it goes first — and
  why the segment adjacent to it is reachable from this start.
- Demand signals (search trends, hiring postings, existing spend on
  workarounds, related-product growth) are cited, not asserted.
- Growth direction is named (accelerating / steady / decelerating),
  not just "growing."

## Common failures

- **Lumping market / customer / competitive / domain into "market
  research".** The convo's #1 named failure mode — produces a slide
  with no decisions. Mitigation: route each branch to its own
  playbook.
- **TAM-only sizing.** "It's a $50B market" tells you nothing about
  whether you can reach any of it. SAM and SOM are load-bearing.
- **Confusing 'people exist' with 'market exists'.** A population is
  not a market; a market requires demand, willingness to pay, and a
  reachable channel.
- **No Five-Forces call.** A big market dominated by an
  irreplaceable supplier, infinite substitutes, or zero switching
  costs is not attractive at any size.
- **Beachhead chosen by what's familiar.** The beachhead should be
  the segment whose pain is most acute *and* whose adoption forms a
  reference point for adjacent segments — not the segment the
  founder happens to know.
- **"Growing market" without rate or driver.** Growth without a
  named cause can reverse silently.

## Heuristics

- **(scope, investigate)** *Size at three resolutions.* TAM / SAM /
  SOM with explicit assumptions for each. Skip TAM-only.
- **(investigate, decide)** *Run Five Forces explicitly.* Score each
  of rivalry, buyer power, supplier power, substitutes, new-entrant
  threat as Low / Med / High. Produce an explicit attractiveness
  call.
- **(scope, investigate)** *Name the beachhead.* One segment, named
  by job + context, with the reason for adjacency. Vague "SMB" /
  "developers" / "knowledge workers" labels are placeholders, not
  segments.
- **(investigate)** *Cite three demand signals.* Search trends,
  hiring postings, existing spend on workarounds, related-product
  growth, competitor funding rounds. Three independent signals beats
  one assertion.
- **(investigate, decide)** *Name market structure.* Fragmented
  (many small players), oligopoly (few large), winner-take-most
  (network effects), or commodity (price-only competition). Each has
  a different defensible strategy.
- **(decide)** *Distinguish 'now' from 'maybe later'.* If the market
  is real but the timing window isn't open, route to `trend.md` for
  the timing call before committing.
- **(investigate)** *Find adjacent monopoly.* Per Thiel — is there a
  sub-segment we could dominate before scaling outward? Adjacent
  monopolies are more defensible than fractional share of a giant
  market.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are TAM / SAM / SOM all sized with named assumptions? | TAM-only sizing | Size SAM and SOM; cite the assumptions. |
| Is the beachhead segment named with adjacency logic? | Vague segment | Name the segment by job + context + adjacency reason. |
| Is the Five-Forces call explicit? | No structural call | Score five forces; emit attractiveness call. |
| Are three independent demand signals cited? | Asserted, not cited | Find three signals; if you can't, downgrade confidence to L. |
| Is the growth rate and driver named? | "Growing" with no rate | Find the rate; if you can't, downgrade to L. |
| Is timing addressed? | Silent on timing | Route to `trend.md` for the timing analysis. |

## Cross-references

- → `references/opportunity/playbooks/customer.md` — for pain severity and
  willingness to pay (the demand-quality axis).
- → `references/opportunity/playbooks/competitive.md` — for substitutes,
  do-nothing, and moats (the structural-defensibility axis).
- → `references/opportunity/playbooks/trend.md` — for timing-window analysis.
- → `references/opportunity/core/decision-gates.md` — for the market-quality
  threshold the `go` outcome requires.
- → `references/opportunity/intents/investigate.csv` row `market` — the entry
  point for this playbook.
- → `templates/opportunity/artifacts/market-sizing.md` — the artifact this
  playbook produces under `investigate`.
