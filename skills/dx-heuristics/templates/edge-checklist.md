<!-- Load-bearing section: Re-run trigger -->
# DX Edge-Case Pass: <surface(s)>

## Scope
- Surfaces covered: <list>
- Target developer: <persona from references/core/personas.md>
- Trigger: <pre-ship / migration / version bump / customer complaint>
- Playbook(s) applied: <list>

## Risk inventory

Grouped by category. Each row gets a severity (0-4 from severity-rubric.md) and a verification.

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

## Risks accepted

- <Risk>: <why this is acceptable, who decided>

## Re-run trigger

<When this pass should run again: release cadence / surface change /
dependency upgrade / customer signal.>
