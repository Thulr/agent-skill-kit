# Judge Calibration Playbook

## Scope

Designing an LLM-as-judge you can trust to gate a change. A judge that scores
free-form outputs is only as good as its calibration against ground truth: until
it has been measured against a human-labeled set — precision, recall, and the
position/length/self-preference bias checks — it is an opinion machine, not a
measurement instrument. This surface designs the judge prompt, its rubric, the
calibration protocol, and the recalibration trigger; it decides when a
deterministic check should replace the judge entirely. It does not run the judge
on production traffic or watch its scores drift over time — that hand-off is
`agent-ops`: we design the judge and certify it; agent-ops runs it and watches
for drift.

- **In:** judge-prompt and rubric design, calibration against a human-labeled
  set, precision/recall scoring, position/length/self-preference bias probes,
  failure-explanation requirements, deterministic-check substitution,
  recalibration triggers on prompt/model change.
- **Out:** operating the judge in production and watching score drift
  (`agent-ops`); the trajectory grading the judge feeds (`trajectory-tests`);
  release/model-swap gating (`benchmark-design`); the eval suite the judge scores
  within (`eval-design`); activation grading (`activation-evals`).
- **Intents this surface answers:** do, review, design.

## Grounding

- A judge is trustworthy only once measured against a human-labeled set: report
  precision and recall against those labels, and run the position, length, and
  self-preference bias probes. An uncalibrated judge silently certifies
  regressions — the Vague Judge anti-pattern — because nobody knows its error
  rate.
- A judge must emit a failure *explanation*, not just a score. A bare number
  cannot be audited, cannot localize the failure mode, and cannot be argued with
  when it disagrees with a human label.
- A deterministic check beats a judge whenever the property is checkable. JSON
  validity, schema conformance, regex/string match, numeric tolerance, and
  exact-set membership are checks, not judgment calls — spend the judge budget on
  the genuinely subjective slice.
- Recalibrate when the judge prompt or the judge model changes. Calibration is a
  property of (prompt × model × rubric), not a permanent certificate; a model
  swap or a prompt edit invalidates the prior precision/recall numbers.
- Known judge biases are public and measurable: position bias (favoring the first
  or last option in a pairwise prompt), length/verbosity bias (favoring longer
  answers), and self-preference (favoring outputs from the same model family).

## Good signals

- The judge has a precision and recall number against a held-out human-labeled
  set, and those numbers are recorded next to the gate the judge feeds.
- The judge emits a structured failure explanation (which criterion failed, on
  what span) alongside every score, so a disagreement can be inspected.
- Position bias is controlled: pairwise prompts randomize or swap order and
  confirm the verdict is stable under the swap.
- Length and self-preference bias have been probed — length-matched pairs and
  cross-model pairs — and the residual bias is quantified, not assumed absent.
- Checkable properties are graded deterministically; the judge is reserved for
  the subjective residual, and the split is explicit in the rubric.
- The rubric defines each label operationally (anchored examples per score), so
  two humans — and the judge — converge on the same label.
- A recalibration trigger is wired: any change to the judge prompt or model
  forces a re-run of the human-labeled calibration before the judge gates again.

## Common failures

- **Vague Judge.** A judge ships without ever being measured against human
  labels; it silently certifies regressions because its precision/recall is
  unknown and its rubric is "rate quality 1-10" with no anchors.
- **Score without explanation.** The judge returns a bare number; failures can't
  be localized to a criterion or span, and human-judge disagreements can't be
  adjudicated.
- **Judge for a checkable property.** A judge grades JSON validity, schema
  conformance, or exact-match — wasting tokens and adding noise where a
  deterministic check is exact and free.
- **Stale calibration.** The judge prompt or model changed but the old
  precision/recall numbers are still quoted; the certificate no longer describes
  the instrument in use.
- **Position bias ignored.** A pairwise judge always reads option A first; it
  systematically favors A (or B) and the win-rate is an artifact of ordering, not
  quality.
- **Length/self-preference bias unprobed.** The judge rewards verbosity or its own
  model family, and the eval rewards the wrong behavior — a quiet Goodhart toward
  longer or same-family outputs.
- **Calibration set leakage.** The human-labeled calibration set overlaps with the
  examples the prompt/rubric was tuned on, so reported precision/recall is
  optimistic and the gate is softer than it reads.

## Heuristics

- **(do, review, design) Calibrate before the judge gates anything.** Build a
  human-labeled set, score the judge's precision and recall against it, and record
  those numbers next to the gate. An uncalibrated judge is a Vague Judge — treat
  its verdicts as unmeasured until the labels exist.
- **(do, design) Require a failure explanation, not just a score.** Make the judge
  emit which criterion failed and on what span. A bare number can't be audited or
  localized; the explanation is what makes a disagreement actionable.
- **(review, design) Prefer a deterministic check whenever the property is
  checkable.** Route JSON validity, schema, regex, numeric tolerance, and set
  membership to code; reserve the judge for the subjective residual and state the
  split in the rubric.
- **(do, review) Probe position bias.** Randomize or swap option order in pairwise
  prompts and confirm the verdict holds under the swap; an order-dependent verdict
  is an artifact, not a measurement.
- **(do, review) Probe length and self-preference bias.** Score length-matched and
  cross-model pairs; quantify the residual bias rather than assuming the judge is
  neutral on verbosity or its own family.
- **(do, design) Anchor every rubric label with examples.** Give each score a
  concrete positive and negative exemplar so humans and the judge converge; "rate
  1-10" without anchors is the seed of an uncalibrated judge.
- **(review, design) Recalibrate on any prompt or model change.** Treat the
  precision/recall numbers as a property of (prompt × model × rubric); invalidate
  and re-run calibration whenever any of the three changes.
- **(review) Keep the calibration set disjoint from tuning data.** Hold the labeled
  set out of whatever the prompt and rubric were iterated on, or the reported
  precision/recall is optimistic and the gate is softer than it reads.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Does the judge have precision/recall against a human-labeled set? | Vague Judge — error rate unknown, regressions certified silently | Build a labeled set; score and record precision/recall before gating |
| Does every verdict carry a failure explanation? | Scores can't be localized or adjudicated | Require which-criterion / which-span output alongside the score |
| Are checkable properties handled deterministically? | Judge wastes budget and adds noise on exact properties | Route JSON/schema/regex/numeric/set checks to code |
| Is position bias controlled in pairwise prompts? | Win-rate is an ordering artifact | Swap/randomize order; confirm the verdict is stable |
| Are length and self-preference bias probed? | Eval quietly rewards verbosity or same-family outputs | Score length-matched and cross-model pairs; quantify residual bias |
| Was the judge recalibrated after the last prompt/model change? | Stale certificate describes a different instrument | Re-run calibration against the labeled set on every prompt/model change |

## Cross-references

- `eval-design` — the judge scores within the eval suite this designs; the
  failure-mode ontology there defines the criteria the judge explains against.
- `trajectory-tests` — a judge grades per-span content, but a run can fail with
  every span passing; trajectory tests grade the path the judge cannot see.
- `benchmark-design` — a calibrated judge with known precision/recall is a
  prerequisite for using it in a release or model-swap gate with a baseline and
  rollback threshold.
- `activation-evals` — when activation is graded by a judge rather than a
  deterministic route check, the same calibration and bias-probe discipline
  applies.
- → `agent-ops` for operating the calibrated judge: running it on production
  traffic and watching its scores drift — we design and certify the judge here,
  agent-ops runs it.
- `references/core/severity-rubric.md`, `references/core/score-rubric.md` — REVIEW
  scales; finding IDs `AGENT-TEST-JUDGE-NNN`.
- `references/intents/{do,review,design}.csv` row `judge-calibration` — the entry
  points.
