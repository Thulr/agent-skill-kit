# Cross-Area Brief — <opportunity-slug>

> Output of the `synthesize` intent. Consolidates area artifacts into
> a single decision-ready brief. **Preserves contradiction; does not
> average.**

## Opportunity statement

<one-line statement>

## Stage

<pre-idea | idea | validation | build | launch | scale>

## Lens

<one of: full (all areas) | stage-filtered | investor-brief>

## Areas synthesized

| # | Area | Artifact path | Confidence overall | Lead persona |
|---|---|---|---|---|
| 1 | <area> | <path> | <H/M/L> | <persona> |
| 2 | … |  |  |  |
| … |  |  |  |  |

Areas explicitly out of scope for this brief: <list with reasons>.

## Top-3 facts (cross-area)

The three highest-confidence + highest-impact facts across all areas.

- **F-1** (H, from <area>): <fact>. Implication: <what this changes>.
- **F-2** (H, from <area>): <fact>. Implication: <…>.
- **F-3** (M, from <area>): <fact>. Implication: <…>.

## Top-3 assumptions (ranked by leverage)

Highest-leverage assumptions — flipping any changes the call.

- **A-1** (leverage high, from <area>): <assumption>. Test: <falsifiable
  experiment, <1 week>. Owner: <name>. Deadline: <date>. Currently
  confidence <L/M/H>.
- **A-2** (leverage high, from <area>): <assumption>. Test: <…>. Owner:
  <…>. Deadline: <…>.
- **A-3** (leverage med, from <area>): <assumption>. Test: <…>. Owner:
  <…>. Deadline: <…>.

## Top-3 risks (severity × likelihood)

Cross-area risks ranked by severity (0–4) × likelihood (L/M/H).

- **R-1** (sev 4, lik <L/M/H>, category <…>, from <area>): <risk>.
  Mitigation: <…>. Owner: <…>. **Kill criterion candidate: yes/no.**
- **R-2** (sev 3, lik <L/M/H>, category <…>, from <area>): <risk>.
  Mitigation: <…>. Owner: <…>.
- **R-3** (sev <0–4>, lik <L/M/H>, category <…>, from <area>):
  <risk>. Mitigation: <…>. Owner: <…>.

## Cross-area contradictions (open questions)

Where two areas disagree. **Surfaced, not averaged.**

| # | Claim | Area A view | Area B view | What would resolve |
|---|---|---|---|---|
| 1 | <claim> | <view> | <view> | <test / evidence> |

## Cross-area coupling (severity upgrades)

Independent risks that compound when both fire.

| Risks coupled | Independent severities | Coupled severity | Reason |
|---|---|---|---|
| <R-x, R-y> | <2, 2> | <3 or 4> | <how they compound> |

## Recommended decision

<Go | Conditional-Go (with promoting tests) | No-Go | Pivot | Defer
(with named evidence-by-date)>

Reason: <one-paragraph summary linking the top-3 facts / assumptions /
risks to the recommendation>.

## Next falsifiable test (cross-area)

<one experiment that closes the highest-leverage assumption above —
typically the same as A-1, or a combined test covering A-1 + A-2.
Name success threshold, deadline, owner.>

## Inputs referenced

- `<path to area artifact>` — <area> investigation, <date>
- …

## Notes for the `decide` step

Hand off to `decide` intent (row `go-no-go` / `kill-criteria` /
`pivot`) with this brief as input. The F/A/D/R memo will inherit the
top-3 above and add formal kill criteria + review trigger.
