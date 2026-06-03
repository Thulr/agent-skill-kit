# Observability Notes

The assistant backend sends full traces to Braintrust and LangSmith. Product
also stores thumbs-down feedback rows, support escalations, sampled production
transcripts, cost, and latency.

Missing pieces:

- No trace replay set.
- No eval labels or deterministic pass/fail checks.
- No LLM judge critique schema.
- No mapping from failure class to prompt, rule, tool schema, or harness change.
- No nightly or release cadence.
- No rollback threshold or owner.
