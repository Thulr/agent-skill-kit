<!-- Load-bearing section: Root cause -->
# Diagnose: <reported symptom>

## Reported symptom
- What was observed: <p99 spike, throughput cliff, error-budget burn, cardinality blowup, etc.>
- Where: <service / surface / region / customer cohort>
- When: <window of occurrence; ongoing / resolved>
- Severity: <user impact and blast radius>
- Target persona: <persona from references/core/personas.md>
- Playbook(s) applied: <e.g., latency.md, resources.md>

## Hypotheses (ranked)

One block per hypothesis, highest likelihood first. Hypothesize before measuring; rank by signal, not by what is convenient to check.

### Hypothesis 1 — likelihood: <high / med / low>
- Cause:             <cause>
- Evidence for:      <signal — trace, metric, log, recent change>
- Evidence against:  <counter-signal>
- Disconfirmation:   <the cheapest measurement that would refute this>

## Diagnostic steps

Ordered, narrowest-first. Each step should disconfirm at least one hypothesis. Name the measurement (profile, histogram, trace query, log query) explicitly.

1. <Measurement> -> <expected observation if hypothesis N holds>
2. ...

## Root cause

<The cause established by the measurements above. Cite the playbook heuristic violated. State what evidence is now considered conclusive vs suggestive.>

## Immediate mitigation

<The action that stops user impact now, with risk and reversibility called out.>

## Verified fix

<The change that addresses the root cause, not just the symptom. Name the verification measurement.>

## Verification

<How to prove the fix worked — measurement method named (e.g., "p99 at the gateway boundary returns to <baseline>; verified by <dashboard / SLO burn rate>"). Include cold and warm conditions if relevant.>

## Prevention

<What would make this *class* of symptom impossible or detectable earlier — added SLI, alert, runbook step, capacity guardrail, retry safeguard. Cite the playbook anti-pattern.>

## Grounding sources applied

- <skill.json inspired_by entry> - <hypothesis, measurement, or prevention choice it informed>
