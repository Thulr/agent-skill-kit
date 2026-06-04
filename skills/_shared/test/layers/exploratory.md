# Exploratory Testing Playbook

## Scope

Time-boxed, charter-driven sessions where a tester investigates the system to discover information about its quality. Distinct from "ad-hoc clicking around" — exploratory testing is structured. Routes to `unit.md` or `integration.md` when a finding becomes a regression test. Always references `core/oracles.md` (SFDIPOT and FEW HICCUPPS).

## Grounding

- **Elisabeth Hendrickson — *Explore It! Reduce Risk and Increase Confidence with Exploratory Testing*** — the charter format, session-based test management, and the practical bridge from exploration to automated regression tests.
- **James Bach & Michael Bolton — Rapid Software Testing methodology** — the SFDIPOT and FEW HICCUPPS oracles distilled in `core/oracles.md`, and the discipline of stating *what you're looking for* before you start.
- **Cem Kaner — *Testing Computer Software*** — exploratory testing as a complement to (not a replacement for) automation; the role of the tester as an investigator.

## Good signals

- Every session has a written charter: "explore [target] with [tools/resources] to discover [information about quality]."
- Sessions are time-boxed (30–90 minutes), not open-ended.
- Notes are kept during the session — observations linked to oracles, not just bug counts.
- A debrief happens after every session: what was found, what wasn't covered, what the next charter should be.
- Bugs found here become regression-purpose automated tests; the session feeds the suite, doesn't replace it.
- Variation is deliberate — the session covers different SFDIPOT axes than the last one (Data this time, Time next time).
- The tester is named, the charter is dated, the report is durable.

## Common failures

- "Exploratory testing" used as a label for unstructured clicking-around with no charter.
- Sessions that run for hours with no time-box — reviewer fatigue, diminishing returns.
- Notes that record bug counts but not what was *not* covered — gives no signal on the gap.
- Findings die in a notebook; never become regression tests; the same bug ships again three months later.
- Every session covers the same SFDIPOT axes (usually Function and Data) — the rest of the system is uninvestigated.
- No oracle attached to observations: "this seems weird" is not actionable; "this violates *History* — version 2.3 returned X here" is.

## Heuristics

- **Has a charter** *(author)* *(gap)* — explicit "explore [target] with [resources] to discover [information]" framing. Without a charter, the session has no oracle and no end condition.
- **Time-boxed session** *(author, strategize)* *(cost)* — 30–90 minutes, then debrief. Open-ended sessions decay into rabbit holes; the time-box forces focus and produces clean checkpoints.
- **Note-taking with oracle attached** *(audit, author)* *(gap)* — every observation is linked to an oracle from `core/oracles.md` (e.g., "violates *Standards* — not WCAG-compliant," or "violates *Image* — error message uses competitor's terminology"). "Looks weird" is not a finding.
- **Reproducer captured before triage** *(audit, triage)* *(confusion, gap)* — record the steps to reproduce *before* reasoning about cause. The steps are durable; the theory of cause may be wrong.
- **Findings convert to automated tests** *(audit, prune)* *(cost)* — bugs found in exploration become regression-purpose unit or integration tests; sessions feed the automated suite, they don't replace it. A bug found twice is a process failure.
- **Variant exploration tracked** *(audit)* *(gap)* — sessions deliberately vary along an SFDIPOT axis the previous session didn't. Tracking which axes have been covered in the last N sessions surfaces the systematic gap.
- **Brittleness check** *(audit)* *(brittleness)* — exploratory sessions often surface UI fragility (selectors that aren't semantic, copy that's hardcoded, layouts that break at unusual widths) — treat these as findings against the e2e/UI layer's brittleness mode, not just as "small things."
- **Session is reviewable** *(audit)* *(confusion, flakiness)* — the charter, notes, and reproducer steps are written down; another tester (or the same one in three months) can resume the line of investigation. A session whose value died with the tester wasn't really a session.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Is there a written charter? | Session has no end condition | Write one before starting |
| Was it time-boxed? | Diminishing returns; tester fatigue | Set 60 minutes; stop at the bell |
| Are observations linked to oracles? | Findings aren't actionable | Tag each observation with an oracle from `core/oracles.md` |
| Are reproducers captured? | Findings can't be triaged later | Record steps before reasoning about cause |
| Did findings become regression tests? | Same bug ships again | Convert each confirmed bug into an automated test |
| Are SFDIPOT axes tracked across sessions? | Same axes repeated; rest uninvestigated | Pick a different axis next charter |

## Cross-references

- → `core/oracles.md` — SFDIPOT and FEW HICCUPPS, the load-bearing reference for this layer
- → `unit.md` and `integration.md` — where exploratory findings become permanent regression tests
- → `e2e-ui.md` — the layer where exploratory sessions most often surface findings
- → `core/failure-modes.md` — gap is the dominant mode addressed by exploration
- → `core/personas.md` — persona 4 (test skeptic) is the natural exploratory-tester archetype
