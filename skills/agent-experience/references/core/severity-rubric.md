# Severity Rubric

Use this for AX audit findings, debug hypotheses, design risks, and measurement gaps.

| Severity | Name | Meaning | Default action |
|---|---|---|---|
| 0 | Note | Polish, preference, or optional improvement with no clear task impact. | Mention only if useful; do not block. |
| 1 | Low | Minor friction or inconsistency; agents/humans can recover without external help. | Batch with adjacent cleanup. |
| 2 | Medium | Noticeable friction causing retries, wrong retrieval, context switching, or stale-context risk for a common path. | Fix in planned work; verify with one concrete scenario. |
| 3 | High | A primary audience (agent or human) fails a core task, misuses an API/tool, cannot recover from error, or receives version-stale guidance. | Prioritize before launch or next release; add regression coverage. |
| 4 | Critical | The surface actively enables unsafe/destructive action, irreversible harm, credential leakage, duplicate side effects, or systematic agent misexecution. | Stop the release or disable the path until fixed and verified. |

## Escalators

Raise severity one level when any applies:

- The affected surface or error is on the first-success path.
- The failure is silent: agents or humans cannot tell the surface is wrong.
- The problem affects more than one audience.
- The docs/schema say one thing while the product/API does another.
- The issue creates duplicate charges, irreversible destructive work, or unsafe retries.
- The only recovery path is to contact support or inspect source code.

## De-escalators

Lower severity one level only when evidence shows:

- The path is rare and clearly marked advanced.
- A nearby alternative surfaces the same task correctly.
- Telemetry or eval data shows minimal real-world exposure.
- The issue is cosmetic and does not change action, recovery, or retrieval.
