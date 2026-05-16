# Triage Runbook

**Test:** `path/to/test_file::test_name`
**Layer:** [unit | integration | e2e-ui | property-based | contract | snapshot | performance]
**Symptom:** [failing | flaky | slow]
**Persona:** on-call engineer

## Reproducer

[Exact steps or command to reproduce, including environment and seed if applicable]

## Hypotheses (ranked)

1. [Most likely cause; what playbook heuristic and failure mode point to it]
2. [Next most likely]
3. [Least likely but possible]

## Diagnostic steps

- [ ] [Step 1]
- [ ] [Step 2]

## Fix

**Failure mode:** [false-pass | brittleness | flakiness | gap | cost | confusion]
**Severity:** [0–4]
**Heuristic invoked:** [Named heuristic from layer playbook]

[Code or process change]

## Verification

[How we'll know the fix worked: test passes 100x in a row, runs in <X ms, etc.]

## Prevention

[What change to authoring guidance, lint rule, or playbook tag would have prevented this]
