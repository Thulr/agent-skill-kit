# Target Developer Personas

Every DX finding, design, debug, or edge-pass must name the target developer.
Pick one or more from this set.

- **Evaluator** — has not committed to using this surface yet; reads only the
  README, registry page, and the first example to decide whether to adopt.
  Bounces fast on missing install command, broken first example, or
  abandoned-looking maintenance signals. Distinct from the first-time user:
  the evaluator may never become one.
- **First-time user** — has decided to try this surface and is in the first
  hour of use; reads only public docs/examples; has no tribal knowledge or
  maintainer access.
- **Integrator** — building on top of this surface in their own product; cares
  about contracts, examples, and version stability.
- **Contributor** — submitting code/docs back to this project; needs local
  setup, tests, PR loop, and review expectations.
- **Maintainer** — owns this surface long-term; cares about compatibility,
  migration cost, deprecation, and support burden.
- **Operator** — runs this in production; cares about config, observability,
  failure modes, and incident response.
- **Migration user** — moving from a previous version, deprecated path, or
  competing tool; needs explicit upgrade guidance and compatibility windows.

If a finding affects multiple personas, name them all and rank by severity
impact per persona — a critical issue for first-time users may be cosmetic for
maintainers.
