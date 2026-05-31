# Severity Rubric

Apply this 0–4 scale to every finding, risk, or anti-pattern.

| Rating | Label | Description | Priority |
| --- | --- | --- | --- |
| 0 | Not a problem | Preference or disagreement, not DX friction | Ignore |
| 1 | Cosmetic | Small polish issue, low task impact | Fix opportunistically |
| 2 | Minor | Causes delay, confusion, or avoidable lookup | Schedule fix |
| 3 | Major | Blocks common task completion or safe debugging | Fix soon |
| 4 | Critical | Prevents adoption, causes data loss, or leads to unsafe use | Fix immediately |

Rate severity by frequency, impact, persistence, and blast radius. Prefer
calibrating against concrete failure modes ("a first-time user cannot find
the smoke-test command") over abstract judgments ("documentation is bad").
