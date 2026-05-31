# Confidence rubric (H / M / L)

Every load-bearing claim in an area artifact gets one of three
confidence levels. The rubric exists because *unmarked* confidence is
the dominant failure mode: a founder reads cited data with the same
weight as a vibe, and unanchored vibes drive decisions.

## The scale

| Level | What it requires | Examples |
|---|---|---|
| **H (High)** | Multi-source corroborated + named primary source + revealed (not stated) evidence where applicable. Reproducible by a colleague reading the same sources. | Public 10-K filing of three comparable companies; a peer-reviewed published number; observed analytics from prior product runs. |
| **M (Medium)** | Single credible source, or stated-preference data (interviews / surveys), or expert estimate from a domain insider. Reproducible argument, not reproducible number. | An analyst report from a known firm; 12 user interviews with consistent themes; a benchmark from a respected practitioner blog. |
| **L (Low)** | Inference from indirect evidence, single anecdote, or founder intuition. Plausible but not testable from the cited sources alone. | "Most of my friends would buy this"; one customer said yes in a hallway; "Hacker News thinks AI is hot." |

## Auto-promotion rule

**Any L on a load-bearing claim is auto-promoted to an Assumption + a
named test in the F/A/D/R fold.** The opportunity does not advance to
`decide` until either the test runs or the dependency on the L claim
is removed. This is the load-bearing rule — it's what stops Ls from
being silently treated as Hs once they're written down.

## Stated vs revealed evidence (customer / market)

When the evidence concerns user behavior, mark it explicitly:

- **Stated preference** (interviews, surveys, "would you buy this") →
  default ceiling is M, even with many data points. Stated preference
  systematically diverges from revealed preference.
- **Revealed preference** (analytics, prior purchase, observed
  behavior) → can reach H given source quality.

A bet that depends on stated preference without revealed corroboration
is an L on the revealed-evidence axis even if the interview count is
high.

## Common failure modes

- **Confidence inflation late in the deck.** Source list at the top is
  H; conclusions on the last slide get treated as H even though they
  rest on M / L assumptions. Tag conclusions, not just sources.
- **Unmarked confidence.** No tag = silent H. Always tag.
- **L treated as M by repetition.** A claim cited three times in
  three artifacts is still L if all three trace back to the same
  founder intuition.
- **Anchoring on the highest-confidence claim.** A single H next to
  five Ls reads as "well-grounded" — it isn't.
