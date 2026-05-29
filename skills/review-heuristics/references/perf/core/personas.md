# Target Personas

Every finding, design, diagnosis, or strategy must name the target persona.
Pick one or more from this set.

- **On-call engineer** — wakes at 3am; has only the dashboards, alerts,
  runbooks, logs, and traces. Cares about diagnose-ability, recovery
  path, and noise discipline. Suffers first when a surface is opaque.
- **SRE / reliability engineer** — owns SLO program, error-budget
  policy, alerting, and post-incident review. Cares about SLI selection,
  alert calibration, and whether reliability work has a budget.
- **Performance engineer** — owns profiling, benchmark suites, and
  optimization work. Cares about profile fidelity, before / after
  measurement, coordinated omission, and whether the slow-path is
  characterized.
- **Capacity planner** — owns the scalability curve and headroom. Cares
  about the bottleneck resource, load model, and projection to 10× /
  100× load.
- **Platform / observability engineer** — owns the instrumentation
  stack (collectors, agents, pipelines, backends). Cares about cost,
  cardinality, retention, propagation discipline, and pipeline failure
  modes.
- **Application owner** — owns a specific service or surface. Cares
  about local SLOs, dashboards that match team mental model, and
  on-call burden for their service.
- **End user (browser / network tier only)** — perceives latency, error
  rate, and responsiveness from the client side. Cares about perceived
  performance, including spinner discipline and progress feedback.

If a finding affects multiple personas, name them all and rank by
severity impact per persona — a critical issue for on-call may be
cosmetic for the capacity planner, and vice versa.
