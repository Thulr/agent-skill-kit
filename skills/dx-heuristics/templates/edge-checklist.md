<!-- Load-bearing section: Re-run trigger -->
# DX Edge-Case Pass: <surface(s)>

## Scope
- Surfaces covered: <list>
- Target developer: <persona from references/core/personas.md>
- Trigger: <pre-ship / migration / version bump / customer complaint>
- Playbook(s) applied: <list>

## Risk inventory

Grouped by category. Each risk block gets a severity (0-4 from severity-rubric.md) and a verification.

### Fresh-machine path

One block per risk. Repeat the shape for the categories below.

#### <Risk title, e.g. "Missing cache, no prior state">
- Severity:  <0-4>
- Status:    <ok / risk / blocker>
- Verify:    <command or check>

### Environment skew
- OS / shell / architecture / package manager / runtime version variance.

### Credentials and permissions
- Missing token, expired, insufficient scope, offline mode.

### Partial setup
- Service A running, service B not; codegen missing; fixtures stale.

### Version skew
- Docs / SDK / server / schema / examples / generated code drift.

### Destructive operations
- Data migration, irreversible side effect, secret in log.

### External dependencies
- Network flake, vendor outage, nondeterministic fixture.

### Backward compatibility
- Existing users; deprecated paths still working.

### Contributor path
- Local setup, tests, PR evidence, release notes.

## Blockers (severity 3-4)

- <Numbered list with fix + verification>

## Findings ledger

If this pass has 7+ risks, any severity 3–4 risk, or a save/track request,
create both tracking artifacts now: the Markdown ledger from
`templates/findings-ledger.md` at
`docs/audits/dx-heuristics-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
and the workflow state from `templates/workflow-state.json` at
`docs/audits/dx-heuristics-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`.
If the target is not a repo or `docs/audits/` is not writable, use matching
`audit-artifacts/dx-heuristics-...` paths. Report both paths; do not merely
offer tracking. Roadmaps and external issues require explicit confirmation.

## Risks accepted

- <Risk>: <why this is acceptable, who decided>

## Grounding sources applied

- <skill.json inspired_by entry> - <risk or check it informed>

## Re-run trigger

<When this pass should run again: release cadence / surface change /
dependency upgrade / customer signal.>
