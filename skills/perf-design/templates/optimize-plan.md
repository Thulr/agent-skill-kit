<!-- Load-bearing section: Sequenced steps -->
# Optimize: <known-slow surface / operation>

## Target
- Operation: <user-facing operation or service surface>
- Current state: <baseline measurements — p50, p99, throughput, saturation>
- Target state: <numeric target, measurement method named>
- Target persona: <persona from references/core/personas.md>
- Constraint: <deadline, blast radius, reversibility, dependency stability>
- Playbook(s) applied: <e.g., latency.md, resources.md>

## Profile (load-bearing)

<Required: profile under representative load before proposing any change. Attach or link the artifact. Note the load model used and whether it is open-loop or closed-loop. Note coordinated-omission status of the measurement.>

## Bottleneck

<Named resource or code path responsible for the largest share of the observed latency / throughput / saturation. Evidence: where in the profile.>

## Sequenced steps

Ordered, each with explicit before / after measurement. Smallest blast-radius first; only escalate if earlier steps do not move the metric.

### Step 1 — <change>
- Hypothesis:   <what this change is expected to move and by how much>
- Cost:         <small / med / large; reversibility>
- Before:       <measurement at baseline>
- After:        <measurement after change, same method>
- Outcome:      <kept / reverted / superseded>
- Side effects: <other metrics observed for regression>

### Step 2 — ...

## Verification

<How to prove the cumulative target was met — measurement method named, same boundary the user experiences. Include cold and warm conditions if relevant.>

## Regression guards

<What measurements continue running after the change so the gain does not silently regress. Add to dashboards, alerts, or CI benchmarks.>

## Grounding sources applied

- <skill.json inspired_by entry> - <step or measurement-method choice it informed>

## Findings ledger

If this optimization pass produced 7+ findings, any severity 3-4 finding, or a save / track request, create both tracking artifacts now: the Markdown ledger from `templates/findings-ledger.md` at `docs/audits/perf-design-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and the workflow state from `templates/workflow-state.json` at `docs/audits/perf-design-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`. Create the directory if needed. If the target is not a repo or `docs/audits/` is not writable, use matching `audit-artifacts/perf-design-...` paths. Populate and report both saved paths; do not merely offer or inline tracking. Roadmaps and external issues require explicit confirmation.

## Accepted trade-offs

- <Intentional compromises, e.g., reduced sampling vs diagnose-ability, hedged requests vs duplicate work>
