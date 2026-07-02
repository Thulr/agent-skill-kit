# Synthesize Playbook

## Scope

The cross-area consolidation pass. After area artifacts are produced,
`synthesize` rolls them into one decision-ready brief. The point is
not summarization — it's **integration**: surfacing the contradictions
between areas, the coupling between risks, the assumptions one area
treats as fact that another flags as risky.

- In: cross-area consolidation, contradiction surfacing, coupling
  analysis (how one area's findings change another's), top-3
  facts / assumptions / risks across areas, named decisions and
  remaining open questions, falsifiable next test.
- Out: per-area deep dive (route to `investigate` + the area
  playbook); final go/no-go (`decide` playbook); execution plan
  stress-test (`plan-red-team`).
- Intents this surface answers: synthesize (primary), scope and
  decide (secondary, for cross-cutting checks).

## Grounding

- **Erika Hall — *Just Enough Research* (2019)** — research has to
  be assembled, not just gathered; synthesis is the load-bearing
  step the field calls "having the answers."
- **Daniele Procida — Diátaxis** — synthesis output is
  explanation + reference, not tutorial. Don't write the brief as
  a how-to.
- **Convo.txt** — implicit synthesis throughout, especially the
  test that "a research branch that ends in notes but not decisions
  is just organized procrastination."

## Good signals

- Synthesis preserves contradiction. Where two areas disagree
  (founder lens vs skeptic lens; market signals vs financial model;
  customer interviews vs revealed analytics), the disagreement is
  surfaced as an open question, not averaged away.
- Coupling is surfaced. "Concentration risk on channel X" is one
  risk in `channel.md`; if the same channel also drives 60% of
  acquisition in the financial model, the coupling makes it
  severity-4.
- Top-3 facts (highest-confidence, highest-impact) are named across
  areas — not "every fact from every area."
- Top-3 assumptions (highest-leverage, ranked by what flips
  downstream) are named with the falsifiable test that closes each.
- Top-3 risks (highest severity × likelihood) are named with named
  mitigations and owners.
- The next falsifiable test is named — a <1-week experiment that
  closes the highest-leverage assumption.
- Confidence is preserved through synthesis: L claims in an area
  artifact stay L in the brief, even if cited next to H claims.

## Common failures

- **Synthesis as concatenation.** Copy-paste the 14 area artifacts
  into one document = no synthesis, just length. Mitigation:
  consolidation rules below.
- **Averaging away disagreement.** Founder lens scored a risk 1;
  skeptic scored it 4; brief lists it as 2. The delta was the
  signal, now hidden.
- **L claims promoted by proximity to H claims.** A bullet next
  to a strongly-sourced fact reads as well-sourced. Re-tag every
  bullet in the synthesis with its original confidence.
- **Missing the coupling.** Two areas independently show severity-2
  risks; together they're severity-4. The synthesizer's job is to
  catch coupling.
- **No top-3 prioritization.** "Here are 40 facts" — the
  prioritization is exactly what synthesis is for.
- **Synthesis without a next test.** Pure descriptive output is
  organized procrastination, the named failure mode. Synthesis
  emits a next falsifiable test.

## Heuristics

- **(synthesize)** *Preserve contradiction.* Two areas disagree?
  Surface as open question with both sides cited. The synthesizer
  does not vote.
- **(synthesize)** *Look for coupling.* For each top risk, scan
  other areas for compounding factors. Severity-2 + severity-2
  on coupled factors = severity-3 or -4 in the brief.
- **(synthesize)** *Top-3 facts.* Highest-confidence, highest-impact
  across areas. Cite the area artifact for each.
- **(synthesize)** *Top-3 assumptions ranked by leverage.* What
  flips downstream if this is false? Include the test.
- **(synthesize)** *Top-3 risks ranked by severity × likelihood.*
  Include named mitigation + owner + kill-criterion implication.
- **(synthesize)** *Preserve confidence.* L stays L; M stays M;
  H stays H. No upgrade by proximity.
- **(synthesize)** *Name the next test.* One falsifiable
  experiment, ideally <1 week, that closes the top assumption.
  Synthesis without a next test is description, not decision-support.
- **(scope, decide)** *Use stage to filter.* For investor-brief
  synthesis, lead with market / financial / competitive / risk.
  For pre-launch synthesis, lead with operational / legal / channel
  / gtm.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are area-vs-area contradictions surfaced as open questions? | Averaged away | Re-do; preserve. |
| Is coupling between risks captured (severity upgrade where coupled)? | Independent risks only | Scan; upgrade coupled. |
| Are top-3 facts / assumptions / risks identified with citations? | Long list | Prioritize. |
| Are confidence tags preserved (no proximity upgrade)? | Mixed | Re-tag every claim. |
| Is the next falsifiable test named? | Pure description | Add the test. |
| Is the synthesis stage-filtered (investor vs pre-launch lens)? | One-size brief | Filter per the intent's CSV row. |

## Cross-references

- → All area playbooks — the synthesis inputs.
- → `references/opportunity/playbooks/decide.md` — the next intent after
  synthesis.
- → `references/opportunity/core/fadr-framework.md` — synthesis output ends
  in the F/A/D/R fold.
- → `references/opportunity/core/personas.md` — synthesis preserves lens
  disagreements rather than collapsing them.
- → `references/opportunity/intents/synthesize.csv` row `bundle` / `by-stage`
  / `investor-brief` — the entry point.
- → `templates/opportunity/cross-area-brief.md` — the artifact this playbook
  produces.
