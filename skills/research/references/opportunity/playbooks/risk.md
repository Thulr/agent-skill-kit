# Risk Playbook

## Scope

What could kill the bet. Risk research is cross-cutting — every other
playbook surfaces risks, and `risk.md` is where they're catalogued,
scored, and converted into mitigations + kill criteria. The playbook
produces a structured register, not a worry list.

- In: risk categorization (assumption / market / execution /
  technical / operational / financial / legal / platform / fraud /
  reputation / concentration); severity × likelihood scoring; named
  mitigations; named owners; kill criteria; pre-mortem-style
  failure backcasting.
- Out: full premortem interview (`premortem` skill); plan
  stress-testing (`plan-red-team`); proposal red-team
  (`proposal-red-team`); per-area deep dives (the surface playbooks).
- Intents this surface answers: scope, investigate, synthesize, decide.

## Grounding

- **Nassim Taleb — *Antifragile* (2012)** — fragile / robust /
  antifragile; concentration risk; convexity (asymmetric payoffs);
  the false security of probabilistic-only risk management.
- **Gary Klein — *Performing a Project Premortem* (HBR 2007)** —
  imagine the bet failed in 18 months; work backwards to causes.
  Used here as a heuristic within `risk`; the dedicated `premortem`
  skill runs the full interview.
- **Daniel Kahneman — *Thinking, Fast and Slow* (2011)** — base
  rates, planning fallacy, inside vs outside view. Forces external
  reference points when teams over-trust their own forecasts.
- **Convo.txt** — risk research covers 11+ categories and produces
  "a prioritized risk register, severity and likelihood, mitigations,
  kill criteria or guardrails."

## Good signals

- Risks are categorized by source (assumption / market / execution
  / technical / operational / financial / legal / platform / fraud
  / reputation / concentration), not just "risks."
- Each risk has severity (0–4 per `core/severity-rubric.md`),
  likelihood (Low / Med / High), confidence in the assessment,
  named mitigation, named owner, and a status.
- Severity-4 risks become kill criteria or have explicit
  mitigations with success thresholds.
- Concentration risk is treated as a first-class category — one
  customer / channel / vendor / data source / regulatory regime
  contributing > 30% gets surfaced even if other indicators are
  green.
- Pre-mortem narrative is present: "Imagine the bet failed in 18
  months. Working backwards, what happened?" Each plausible failure
  trail maps to a category above.
- Outside-view base rates are referenced (X% of marketplaces in
  category Y reach scale within Z years).
- "Watch and see" is not on the mitigation menu. Either we test
  the risk, mitigate the structure, or accept it explicitly.

## Common failures

- **Risk register as worry list.** A list with no severity, no
  owner, no mitigation, no kill criteria is a wall not a tool.
- **Severity inflation under skeptic lens / deflation under founder
  lens.** Calibration drifts by lens. Mitigation: use both lenses
  (per `core/personas.md`) and reconcile.
- **Concentration ignored.** "We have one big customer, but they
  love us." Concentration is independent of relationship quality;
  > 30% on any axis is severity ≥ 3.
- **Inside-view-only forecasting.** Forecasting from project
  details without reference to base rates of similar projects.
  Use outside view.
- **Mitigations without success thresholds.** "We'll improve
  retention" is not a mitigation; "retention to X% by month 6 or
  we kill" is.
- **Severity-4 risks unresolved AND not in kill criteria.** The
  worst failure mode — a known-fatal risk hangs around uncalled.
- **Risk register written once and not maintained.** Risks evolve;
  the register should be updated at every milestone. Stale registers
  drift to fiction.

## Heuristics

- **(scope, investigate)** *Categorize by 11 sources.* Assumption,
  market, execution, technical, operational, financial, legal,
  platform / vendor, fraud / abuse, reputation, concentration. Each
  surface playbook surfaces risks; `risk.md` is where they collect.
- **(investigate)** *Score severity (0–4) + likelihood (L/M/H) +
  confidence.* Three dimensions. Severity is the consequence;
  likelihood is the probability; confidence is how much we trust
  the assessment.
- **(investigate, decide)** *Concentration is first-class.* One
  customer / channel / vendor / data source / regulatory regime
  > 30% = severity ≥ 3. Independent of relationship quality.
- **(investigate)** *Pre-mortem narrative.* "It's 18 months from
  now. The bet failed. Working backwards — what happened?" Each
  plausible trail maps to a risk row.
- **(investigate)** *Outside-view base rates.* What % of comparable
  bets reached scale? What was the median time? Use outside view
  to recalibrate inside-view forecasts.
- **(investigate, decide)** *Mitigations with success thresholds.*
  "Get to X by Y or we kill" — not "improve."
- **(investigate, decide)** *Kill criteria from severity-4.* Every
  severity-4 risk is either resolved, mitigated to threshold, or
  named as kill criterion. None can hang unresolved.
- **(decide)** *Antifragile structuring.* Beyond mitigating each
  risk, can the structure be changed so the same external event
  *helps* rather than hurts? Optionality, diversification,
  reversibility.

## Quick diagnostic

| Question | If no | Action |
| --- | --- | --- |
| Are risks categorized by source (11 categories)? | "Risks" lumped | Categorize. |
| Does each risk have severity × likelihood × confidence + owner + mitigation? | Partial | Complete the row. |
| Are concentration risks (>30%) surfaced as severity ≥ 3? | Silent | Surface; score. |
| Is a pre-mortem narrative present? | Forward-only forecasting | Run the backwards narrative. |
| Are outside-view base rates referenced? | Inside-view-only | Find base rates from comparable bets. |
| Do mitigations have success thresholds? | "Improve" / "monitor" | Re-spec with thresholds + deadlines. |
| Are all severity-4 risks resolved or in kill criteria? | Hanging severity-4 | Resolve or name as kill criterion. |
| Are there antifragile structural changes (not just mitigations)? | Mitigation-only | Look for optionality + diversification + reversibility. |

## Cross-references

- → All other playbooks — each surfaces risks; `risk.md` collects.
- → `references/playbooks/financial.md` — for the cash / runway
  risk class.
- → `references/playbooks/channel.md` — for platform concentration.
- → `references/playbooks/legal.md` — for regulatory exposure.
- → `references/core/severity-rubric.md` — the canonical 0–4 scale.
- → `references/core/decision-gates.md` — where severity-4 risks
  feed kill criteria.
- → `references/core/fadr-framework.md` — for the F/A/D/R fold.
- → `templates/artifacts/risk-register.md` — the artifact this
  playbook produces under `investigate`.
- → Sibling skill `premortem` — for the full backwards-from-failure
  interview, when the user wants that depth specifically.
