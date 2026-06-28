# Reflection-log closeout report

**Scope:** <cluster / PR / diff / date range>
**Run date:** <YYYY-MM-DD>
**Evidence source:** <PR / diff / command output / audit result / manual review>

## Since-last-run scoreboard

```text
Since <YYYY-MM-DD> (<scope>):
  Closed since last run: <N>   (<entry slugs>)
  Regressions:           <N>   (<entry slugs>)
  Still open:            <N>
  New this run:          <N>
```

## Verification results

| Entry | Cluster | Claimed closure | Verification evidence | Result |
|---|---|---|---|---|
| `<YYYY-MM-DD-slug.md>` | RCF-CLUSTER-001 | <change> | <file:line, command, PR, review> | verified / still open |

## Entries to mark resolved

- `<YYYY-MM-DD-slug.md>` — resolved by <change + evidence>

## Entries left open

- `<YYYY-MM-DD-slug.md>` — <blocked / needs_evidence / failed verification>

## Follow-up work packages

| Package | Entries | Why still open | Next safe action |
|---|---|---|---|
| <name> | <slugs> | <reason> | <action> |

## Status-update checklist

- [ ] Every resolved entry has evidence, not just a merged issue or PR.
- [ ] Entry frontmatter `status:` changed only for verified entries.
- [ ] `## Closed by` names the PR/commit/diff and the verification summary.
- [ ] Any failed verification remains open with blocker notes.
