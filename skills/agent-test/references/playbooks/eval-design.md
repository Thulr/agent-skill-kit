# Eval Design Playbook

## Scope

Designing the eval suite itself for an AI product or for agent/skill activation — the
measurement instruments, not the loop that runs them. The work starts by naming *how*
the system fails before chasing any aggregate, then picking the smallest eval that gates
the change at hand and localizing each failure to a trajectory or trace rather than a
final pass/fail. This surface routes the deeper design problems — calibrating the judge,
grading the path, constructing held-out fixtures, evaluating activation — to its sibling
playbooks; here we set the failure-mode ontology, choose the staircase tier, and shape
the suite that the other surfaces fill in.

- **In:** the failure-mode ontology, the AI Optimization Staircase read as eval-design
  patterns (L1–L4 gates), trajectory/trace localization, choosing the smallest gating
  eval, the deterministic-check-vs-judge decision.
- **Out:** judge calibration and bias checks (see `judge-calibration`); run-level path
  grading (see `trajectory-tests`); held-out fixture construction and slice scoring
  (see `benchmark-design`); skill/agent activation evals (see `activation-evals`);
  operating the loop, drift watch, and rollout (see the `agent-ops` sibling SKILL).
- **Intents this surface answers:** do, review, design.

## Grounding

- You cannot improve a number you cannot decompose. Name the failure-mode ontology —
  loops, wrong-tool calls, lost hand-offs, hallucinated fields, format breaks — before
  optimizing any aggregate score, and confirm the evals localize each mode rather than
  reporting one pass/fail.
- Each staircase tier names a gate an eval must clear before a change persists: L1
  system-prompt/instruction changes gate on judge explanations + a held-out eval + a
  reviewed diff; L2 declarative signatures (parsers/classifiers/routers) gate on a
  schema metric + a train/test split; L3 sandbox/repair harnesses gate on isolation +
  tests + a repair loop; L4 system benchmarking gates on per-slice guardrail-vs-north-star
  scoring + a baseline + a rollback threshold.
- A deterministic check beats a judge whenever the property is checkable — schema
  validity, exact match, tool-arg shape, exit code. Reserve the judge for genuinely
  open-ended quality, and require it to emit explanations, not just a number.
- The smallest eval that gates the change is the right one. A one-line system-prompt
  edit does not need an L4 benchmark; a model swap cannot ship on a single judged case.

## Good signals

- A written failure-mode ontology exists before any aggregate is reported, and every
  mode maps to at least one eval that can attribute a failure to it.
- Each eval is tied to a staircase tier and clears that tier's gate — L1 changes carry
  judge explanations + a held-out check + a reviewed diff; L2 signatures carry a schema
  metric and a train/test split.
- Failures localize to a trajectory or trace span, so a red result names *where* and
  *which mode*, not merely *that* the run failed.
- The chosen eval is the smallest that gates the change at hand; nobody is building an
  L4 suite to land a prompt tweak, or shipping a model swap on one judged example.
- Deterministic checks cover every checkable property; the judge is scoped to the
  open-ended residue and emits an explanation with each verdict.
- The suite reports per-mode and per-slice results, never a lone aggregate pass-rate as
  the decision surface.
- A 0.95 per-step bar is recognized as compounding far below production across a
  multi-step run, so run-level evals exist alongside per-step ones (handed to
  `trajectory-tests`).
- Eval candidates are non-trivial — real prompt + completion + tool I/O — not skeleton
  metadata that tests nothing.

## Common failures

- **God Gate.** A single aggregate pass-rate stands in as the release gate, hiding which
  slice broke and conflating a guardrail regression (block ship) with a north-star dip
  (report only).
- **Trajectory Blindness.** Every span is graded in isolation and passes while the run
  fails — a loop, a wrong tool, a lost hand-off goes unmeasured because no path-level
  eval exists.
- Optimizing the metric instead of the behavior (Goodhart) — the score climbs while the
  product gets worse because the eval rewards a proxy.
- No failure-mode ontology: the team chases an aggregate they cannot decompose, so a
  regression is visible but not attributable.
- A judge is used where a deterministic check would settle the property, adding noise and
  cost to something that was exactly checkable.
- The eval is mis-sized for the change — an L4 benchmark blocks a one-line edit, or a
  model swap ships behind a single judged case with no baseline or rollback.
- The **march of nines** is ignored: a per-step bar that looks high compounds to a
  run-level pass-rate far below what production needs.
- Eval candidates are skeleton metadata, so the suite is green against fixtures that
  never reflected a real session.

## Heuristics

- **(review, design) Name the failure-mode ontology before any aggregate.** List the
  concrete ways the system fails and confirm the suite can attribute a red result to a
  named mode. If it cannot decompose, it cannot improve.
- **(design) Pick the staircase tier, then design to its gate.** L1 → judge
  explanations + held-out eval + reviewed diff; L2 → schema metric + train/test split;
  L3 → isolation + tests + repair loop; L4 → per-slice guardrail-vs-north-star + baseline
  + rollback. The tier sets the contract.
- **(do, design) Choose the smallest eval that gates the change at hand.** Match eval
  weight to change risk — a prompt tweak gets an L1 gate, a model swap gets an L4 suite.
  Over-building delays the change; under-building ships it blind.
- **(review, design) Localize every failure to a trajectory or trace.** Design the eval
  so a red result names the span and mode, not just the verdict. Reassemble spans into
  the ordered path before grading; hand the path-grading mechanics to `trajectory-tests`.
- **(do, review) Prefer a deterministic check to a judge whenever the property is
  checkable.** Schema, exact match, tool-arg shape, exit code — assert them directly.
  Scope the judge to the open-ended residue and require explanations from it.
- **(review, design) Never let one aggregate pass-rate be the gate.** Split guardrails
  (block ship) from north-star/capability metrics (report only) and report per-slice.
  Send slice and baseline construction to `benchmark-design`.
- **(design) Budget for the march of nines.** A 0.95 per-step bar compounds well below
  production over a multi-step run; design run-level evals, not only per-step ones.
- **(do) Demand non-trivial eval candidates.** Every fixture must carry a real prompt +
  completion + tool I/O. Reject skeleton metadata before it seeds the suite.
- **(review) Watch for Goodhart.** Confirm the eval rewards the behavior, not a proxy a
  change could game without improving the product.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is there a written failure-mode ontology before the aggregate? | The number can't be decomposed | Name the failure modes; map each to an attributing eval |
| Is each eval tied to a staircase tier and its gate? | The change can persist ungated | Assign the tier; design to L1/L2/L3/L4's gate |
| Does a red result localize to a trajectory/trace span? | Trajectory Blindness | Add run-level path grading (see `trajectory-tests`) |
| Is this the smallest eval that gates the change? | Over- or under-built gate | Re-size the eval to the change's risk |
| Is a judge used where a deterministic check would do? | Needless noise and cost | Replace with an exact/schema/exit-code assertion |
| Is the gate a single aggregate pass-rate? | God Gate hides the broken slice | Split guardrail vs north-star; report per-slice |

## Cross-references

- `judge-calibration` — calibrating the judge this suite relies on against a
  human-labeled set, with precision/recall and position/length/self-preference bias
  checks, once a property isn't deterministically checkable.
- `trajectory-tests` — reassembling spans into the ordered path and grading run-level
  behavior (loops, wrong tool, lost hand-off) that per-span grading misses.
- `benchmark-design` — constructing disjoint held-out fixtures above the count floor and
  the per-slice guardrail-vs-north-star scoring an L4 gate needs.
- `activation-evals` — designing the evals that test whether a skill or agent activates
  on the right prompts and stays silent on the wrong ones.
- → `agent-ops` (sibling SKILL) — operating the loop these instruments feed: running the
  suite, watching drift, staging and rolling back. The hand-off is "we design the eval;
  `agent-ops` runs it and watches drift."
- finding IDs `AGENT-TEST-EVAL-NNN`.
- `references/intents/{do,review,design}.csv` row `eval-design` — the entry points.