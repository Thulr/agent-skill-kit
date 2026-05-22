# Perf and Observability Score Rubric

Rate the current posture 0–10 for the target persona and surface. Target
is always 10/10.

- **10:** Latency and throughput budgets are measured at the tail (p95,
  p99, max) with no coordinated-omission risk; saturation, traces, logs,
  and metrics together answer "why is this slow right now" without
  tribal knowledge; SLOs reflect user experience and error-budget policy
  is enforced; capacity headroom is projected forward.
- **8–9:** Strong posture with minor gaps — one or two surfaces are
  thin, but the on-call rotation can recover in expected time.
- **6–7:** Usable posture; diagnosis depends on prior context or
  spelunking. Tail percentiles exist but are not the primary metric;
  some surfaces lack ownership.
- **4–5:** On-call can succeed only with help; SLOs are aspirational
  rather than enforced; cardinality or volume is uncontrolled.
- **1–3:** User-impacting symptoms are routinely opaque; the dashboard
  does not answer the diagnostic question; capacity is unknown.
- **0:** The system cannot be operated against a reliability target.

Always state the current score, the target score (10), and the minimum
changes needed to reach 10/10.
