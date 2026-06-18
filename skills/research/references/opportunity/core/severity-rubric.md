# Severity rubric (0–4)

Used by `risk` playbook + the F/A/D/R fold + every artifact that lists
risks. Same 0–4 scale this repo uses elsewhere (the `<domain>-audit`
skills, `harden-repo-for-coding-agents`) so severities are comparable across skills.

| Score | Label | What it means here | Examples |
|---:|---|---|---|
| 0 | Note | Observation only; no action required. | "Market growth is steady, not accelerating." |
| 1 | Minor | Mild concern; flag but don't block. | "Channel CPA is 20% above our target — monitor." |
| 2 | Moderate | Worth fixing in the next planning cycle; do not ship without a mitigation noted. | "No defined SOC-2 timeline; enterprise pilot at risk." |
| 3 | Major | Blocks the next stage gate. Must have a named mitigation and an owner before proceeding. | "Single-vendor data dependency with no alternate source." |
| 4 | Critical / Kill-trigger | If unmitigated, this is sufficient on its own to kill the opportunity. Must be either resolved or named in the kill criteria. | "Regulatory ruling that makes the core mechanic illegal." |

## How to assign

1. **Pick severity first.** What's the consequence if this is true and
   we don't act? Score the consequence, not the likelihood.
2. **Then estimate likelihood** separately (Low / Med / High). The
   risk register multiplies severity × likelihood for ordering, but
   severity alone gates whether the risk needs explicit kill criteria.
3. **Anything scored 4 becomes a kill criterion** by default. The
   `decide` intent and `core/decision-gates.md` enforce this.
4. **Anything scored 3 needs a named owner + mitigation** before the
   artifact is considered complete.

## Common mis-scoring

- **Likelihood masquerading as severity.** "It's unlikely" doesn't
  reduce severity; it reduces likelihood. Keep the two separate.
- **Severity inflation in red-team mode.** Not everything is a 4. If
  every finding is a 4, you've lost calibration — most findings are
  1–2.
- **Severity deflation in build mode.** Founders systematically
  under-score severity on their own opportunity. Use the `skeptic`
  persona lens to recalibrate.
