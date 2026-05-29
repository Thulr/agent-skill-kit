<!-- Load-bearing section: Prevention -->
# DX Debug: <reported friction>

## Reported friction
- What the user tried: <action>
- What they saw: <output, error, silence>
- What they expected: <intended outcome>
- Target developer: <persona from references/dx/core/personas.md>
- Playbook(s) applied: <e.g., errors.md, cli.md>

## Hypotheses (ranked)

One block per hypothesis, highest likelihood first.

### Hypothesis 1 — likelihood: <high / med / low>
- Cause:             <cause>
- Evidence for:      <signal>
- Evidence against:  <counter-signal>

## Diagnostic steps

Ordered, narrowest-first. Each step should disconfirm at least one hypothesis.

1. <Command or check> → <expected output if hypothesis N holds>
2. ...

## Fix candidates

One block per candidate.

### Fix candidate 1
- Change:        <the specific change>
- Addresses:     hypothesis <#>
- Cost:          <small / med / large>
- Blast radius:  <local / surface / system>

## Recommended action

<The fix to ship now, and why. Cite the playbook heuristic violated.>

## Verification

<How to prove the fix worked, and how to prove the friction is gone for the
target developer — not just the original reporter.>

## Prevention

<What would make this *class* of friction impossible — typed contract,
validation, error message change, doc update, test, lint rule. Cite the
playbook anti-pattern.>

## Grounding sources applied

- <skill.json inspired_by entry> - <hypothesis, fix, or prevention choice it informed>
