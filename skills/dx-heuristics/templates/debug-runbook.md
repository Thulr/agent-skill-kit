<!-- Load-bearing section: Prevention -->
# DX Debug: <reported friction>

## Reported friction
- What the user tried: <action>
- What they saw: <output, error, silence>
- What they expected: <intended outcome>
- Target developer: <persona from references/core/personas.md>
- Playbook(s) applied: <e.g., errors.md, cli.md>

## Hypotheses (ranked)

| # | Hypothesis | Evidence for | Evidence against | Likelihood |
| - | --- | --- | --- | --- |
| 1 | <cause> | <signal> | <counter-signal> | high/med/low |

## Diagnostic steps

Ordered, narrowest-first. Each step should disconfirm at least one hypothesis.

1. <Command or check> → <expected output if hypothesis N holds>
2. ...

## Fix candidates

| Fix | Hypothesis addressed | Cost | Blast radius |
| --- | --- | --- | --- |
| <change> | <#> | <small/med/large> | <local/surface/system> |

## Recommended action

<The fix to ship now, and why. Cite the playbook heuristic violated.>

## Verification

<How to prove the fix worked, and how to prove the friction is gone for the
target developer — not just the original reporter.>

## Prevention

<What would make this *class* of friction impossible — typed contract,
validation, error message change, doc update, test, lint rule. Cite the
playbook anti-pattern.>
