# Severity Rubric

Apply this 0–4 scale to every finding, risk, or anti-pattern.

| Rating | Label | Description | Priority |
| --- | --- | --- | --- |
| 0 | Not a problem | Preference or disagreement, not a perf / observability concern | Ignore |
| 1 | Cosmetic | Minor polish; dashboard label, metric naming, log field nit | Fix opportunistically |
| 2 | Minor | Causes wasted time during diagnosis; gap is reachable via tribal knowledge | Schedule fix |
| 3 | Major | A class of user-impacting symptoms cannot be diagnosed cleanly; on-call escalation is frequent; tail percentiles are unmeasured; SLO alerts fire on noise | Fix soon |
| 4 | Critical | User-impacting outage or regression cannot be diagnosed from current instrumentation; coordinated omission renders latency measurements meaningless; SLO program does not reflect user experience; capacity ceiling is unknown and load is climbing | Fix immediately |

Rate severity by frequency, blast radius, recovery time, and whether the
problem is recoverable from current instrumentation. Calibrate against
concrete failure modes ("on-call cannot answer why p99 doubled from the
existing dashboards") rather than abstract judgments ("observability is
weak").
