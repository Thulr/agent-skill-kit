# Reflection-log triage report

**Scope:** <repo / subsystem / date range>
**Log path:** `docs/reflection-log/`
**Run date:** <YYYY-MM-DD>

## Summary

- Entries read: <N>
- Open entries: <N>
- Resolved entries: <N>
- Clusters found: <N>
- Clusters ready for promotion (>=3 entries): <N>
- Open-loop warning: <yes/no — if yes, name what signal has not changed a future run yet>

## Since-last-run scoreboard

<!-- Include only when resuming from prior triage / workflow state. -->

```text
Since <YYYY-MM-DD> (<scope>):
  Closed since last run: <N>   (<ids-or-entry-slugs>)
  Regressions:           <N>   (<ids-or-entry-slugs>)
  Still open:            <N>
  New this run:          <N>
```

## Failure-mode clusters

### Cluster RCF-CLUSTER-001 — <short name>

**Pattern:** <one sentence: what keeps happening?>

**Entries:**
- `<YYYY-MM-DD-slug.md>` — <What to do differently line>
- `<YYYY-MM-DD-slug.md>` — <What to do differently line>

**Root cause:** <missing context / missing verification / unsafe action / skill failure / tool limitation / other>

**Closure surface:** <AGENTS.md rule | SKILL.md patch | playbook update | eval/trigger case | test fixture | hook | CI gate | docs/source fix | roadmap package | no-op/stale>

**Verification rule:** <specific command, audit check, browser/tool run, eval rerun, human review, or diff evidence>

**Promotion readiness:** <ready: >=3 entries | draft only: below W1 floor | blocked: needs evidence>

**Next safe action:** <triage only / ask user to choose / draft closure plan / implement autopilot>

## Closure queue

| Priority | Cluster | Entries | Closure surface | Verification | Status |
|---|---|---:|---|---|---|
| P0 | RCF-CLUSTER-001 | <N> | <surface> | <rule> | <discovered/planned/blocked> |

## Non-promoted entries

List entries that are singletons, stale, duplicates, or below the W1 floor. Do not delete them; they remain searchable signal for future triage.
