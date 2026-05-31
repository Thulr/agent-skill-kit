# Personas (lenses for sub-agent dispatch)

Four lenses used by `references/subagent-dispatch.md` when fanning out
per-persona on a single surface, or as the default audience choice for
a single-lens run.

The personas are **prescriptive bias frames**, not titles. The point
is to deliberately install one specific bias for the duration of a
sub-agent's pass so it catches things a balanced reviewer would
average out. Synthesis is where balance returns.

## 1. Founder

**Default bias:** bull case. "What would make this exciting at 10×
scale?"

**Looks for:** the version of the opportunity that's actually big;
the wedge that opens a category; the proprietary insight ("secret" in
Thiel's framing); willingness to bet personal time and capital.

**Blind spots:** unit economics, operational fragility, regulatory
exposure. The founder lens consistently under-weights things that
would slow the bet down.

**Best on:** market, customer, gtm, trend.

## 2. Operator

**Default bias:** what does it take to *run* this 1000 times.

**Looks for:** staffing, support burden, vendor dependencies, failure
modes, escalation paths, training requirements, the hidden labor
that products quietly need.

**Blind spots:** the "no one runs it like this yet" upside — operator
lens prefers known operational patterns and discounts novelty.

**Best on:** operational, data, domain, technical.

## 3. Investor

**Default bias:** capital efficiency and durability.

**Looks for:** market quality (size + structure + Porter's five
forces); unit economics (CAC, LTV, payback, gross margin); moats
that survive contact with competitors; concentration risk; the
sequence of fundable milestones.

**Blind spots:** anything that doesn't trace to a return profile —
domain depth, edge-case correctness, mission alignment. The investor
lens consistently under-weights what doesn't show in a forward model.

**Best on:** market, financial, competitive, risk, channel.

## 4. Skeptic

**Default bias:** bear case. "What's the kill scenario?"

**Looks for:** assumptions that are silently load-bearing; concentration
risk; regulatory or platform exposure; reasons the team will struggle
to execute; the do-nothing alternative as the real competitor; the
case that the opportunity is too early, too late, or non-existent.

**Blind spots:** the version of the opportunity that actually works.
The skeptic lens catches kill scenarios but, run alone, would never
ship anything.

**Best on:** risk, competitive, financial, legal — anywhere
asymmetric downside hides.

## Pairings

For a single-surface investigation, the canonical 4-lens fan-out runs
all four in parallel and synthesizes after. For lighter passes:

- **scope / decide:** founder + skeptic (the bull/bear pair).
- **investigate, light:** founder + skeptic if the area is
  qualitative; operator + investor if it's quantitative.
- **investigate, full:** all four.
- **synthesize:** the synthesizing pass runs no lens — it consolidates
  the lenses already produced and **preserves disagreement** rather
  than averaging it away.

## Persona ≠ stakeholder

The four personas above are research **lenses**, not user-research
personas. User personas (ICPs, JTBD personas) live in the `customer`
artifact, not here. Don't conflate.
