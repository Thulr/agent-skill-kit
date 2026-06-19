# dx-audit / dx-design — wiki-informed gap & removal audit (final)

> **Status of this document.** This is the corrected final report after an
> adversarial critique pass against `/Users/justin/Dev/ai-wiki` and all 20
> playbooks under `skills/_shared/dx/playbooks/`. Several draft items marked
> "Verified" were over-claimed: three cited public sources that turned out to
> be wiki-unshaped or unsupported, six items imported an agent/AI-native
> source as if it were generic human-DX, and several "net-new" gaps were
> already covered by existing heuristics. Those corrections are folded in
> below. **Every ADD is grounded in a public source; the private wiki is
> shaping input only and is never cited in any published skill**
> (source-of-truth-no-attribution rule).

## Summary

The private wiki extends the dx surfaces modestly. Because the wiki is
AI/agent-heavy, most of its volume routes to `design-for-agent-users`
(llms.txt, MCP, Agent-SDKs, agent-span telemetry, agent-PR triage,
agent-OAuth) rather than to dx. After stripping that agent framing — and,
critically, after **not** accepting "I can rephrase the heuristic without the
word 'agent'" as proof a gap is human-DX — roughly **16 net-new human-DX ADDs
survive** across ~13 surfaces, down from the draft's claimed ~25. The densest
real gains are in `package` (supply-chain install integrity), `api`/`sdk`
(spec-as-source-of-truth, contract testing, parse-don't-validate, resource
finalizers), `setup` (thin-slice adoptability, pinned installer, credential-
optional first verification), and `contributor` (issue-triage, API-change
gates). There are **no clean removals**, but the audit's original "nothing is
stale" claim was untested and is now flagged as a real inconsistency: dx
already ships agent-specific heuristics in `errors.md` and `telemetry.md`,
which sit in tension with the very routing rule this audit applies to new
ADDs. Net recommendation: **ship the clean ADDs, FIX the seven flagged items
before adding (verify source / fix routing / split the agent slice), CUT or
DOWNGRADE seven over-claimed items, and surface the pre-existing-agent-
heuristic inconsistency rather than declaring the playbooks clean.** Add no
new surface — the conservative bar is met.

### Headline counts

- **KEEP as-is (clean human-DX ADDs):** 16
- **FIX before adding** (source/routing/scope defect to resolve first): 7
- **CUT or DOWNGRADE** (already covered, or scope error): 7
- **Scope-routings to siblings** (deliberately NOT added to dx): ~12 themes
- **Removals:** 0 clean removals; **1 untested-removal inconsistency** flagged
- **New surfaces:** 0

### Highest-value findings

1. **`package` supply-chain install-integrity floor (Pi, wiki-confirmed)** —
   the cleanest, most generic ADD: exact pins, `save-exact`, lockfile-as-
   ground-truth, embedded `npm-shrinkwrap.json`, `--ignore-scripts` by
   default, scheduled `npm audit signatures`. Plain npm distribution,
   applicable to any human-maintained package. KEEP.
2. **`package` release-age cooldown — the one correct de-slanting in the
   audit.** The wiki grounds this in the "14-Day Package Rule," which is
   explicitly about protecting *autonomous coding agents*. The draft correctly
   re-anchored on npm/pnpm primary docs and dropped the agent framing — **this
   is the model to follow.** BUT the specific version numbers ("npm
   `min-release-age` ≥11.10.0; pnpm default 1440 min in v11") are **not** in
   the wiki (the wiki only grounds Pi's `min-release-age=2` and nanoclaw's
   `minimumReleaseAge: 4320`). FIX: re-fetch npm/pnpm docs to confirm the
   version floors/defaults, or strike the numbers and keep the mechanism.
3. **Three source defects masquerading as "Verified."** vLLM
   "accepted-but-ignored fields / escape hatch" does not appear in the wiki
   (only "compatibility boundary" does); `graphql/dataloader` has **no** wiki
   entity at all (every wiki "dataloader" hit is PyTorch ML); these were
   tagged "Verified" without grounding. Both are downgraded to
   needs-verification with the public source actually checked before adding.
4. **Six agent-native imports rephrased into human-DX.** `errors`
   success-shaped-failure (WorkOS generated-SQL), `logging` default-terse
   (Lopopolo agent-harness), `auth` RFC 8693 (OAuth-for-AI-agents),
   `perf` TTFT (LLM streaming inference), `ide` tree-sitter (RAG-chunking /
   ContextBench) all have an agent-native **source, failure mode, and
   designed surface**. Rephrasing into human-DX language produces exactly the
   W1-style plausible boilerplate the repo's promotion floor warns against.
   Apply the audit's own decision rule — "decide by surface being designed,
   not by 'a human calls it'" — to these, not just the easy cases.
5. **The "no removals" claim is untested against dx's own embedded agent
   heuristics.** `errors.md` ships four agent-specific heuristics
   (agent-readable envelope, tool-error-shaped-for-retry, replay-ready
   capture); `telemetry.md` ships AI/agent-SDK heuristics. Under the routing
   rule this audit enforces on new ADDs ("agent-as-consumer →
   design-for-agent-users"), those are removal/relocation candidates — or the
   rule is being applied inconsistently. The honest finding names the tension;
   it does not declare the playbooks clean.

---

## Add (clean — well-grounded human-DX)

Grouped by surface. Every item is tied to a public source (never the wiki).

### api (`skills/_shared/dx/playbooks/api.md`)
- **Spec-as-source-of-truth — one machine-readable API definition derives
  server + OpenAPI docs + typed client.** Source: Effect-TS `@effect/platform`
  HttpApi (`https://github.com/Effect-TS/effect/blob/main/packages/platform/README.md`).
  Severity 3. Consolidates the spec-first and multi-transport-bindings themes.
- **Consumer-driven contract testing + `can-i-deploy` deployment-safety
  gate.** Source: Pact / PactFlow (`https://docs.pact.io/`). Severity 3.
  Wiki-confirmed (`entities/pact.md`, `entities/pactflow.md`,
  `sources/pact-smartbear-contract-testing-docs.md`); the MCP/TEA slice is the
  agent part, correctly omitted. Operationalizes the Hyrum's-Law citation
  api.md already carries.

### sdk
- **Parse, don't validate — the decoded type IS the usable value (string →
  `URL` instance), not a boolean validity check.** Sources: Alexis King,
  "Parse, Don't Validate"
  (`https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/`);
  concrete instance Effect-TS schema docs. Severity 3. Wiki-corroborated.
- **Resource-safety contract — client lifecycle finalizers run on success,
  failure, AND cancellation/interrupt.** Source: Effect-TS Resource Management
  (`https://effect.website/docs/resource-management/introduction/`); broader
  lineage bracket / try-with-resources / RAII. Severity 2. Stronger than the
  existing cancel-only heuristic. Note: existence well-corroborated; URL form
  matches the docs-site pattern but was not adversarially fetched.
- **Adoption friction as an explicit design axis — minimize assumptions the
  library forces on the consumer's stack.** Sources: Effect-TS
  `effect-vs-neverthrow` and `schema-vs-zod` comparison docs. Severity 2.
  Caveat: these are Effect's own one-sided comparison pages — cite the
  reusable adoption-cost *principle*, not the head-to-head verdict.

### cli
- **Stream separation — primary/parseable output on stdout; errors, progress,
  prompts, and logs on stderr** (verify with `tool … | jq` returning clean
  data). Source: clig.dev (`https://clig.dev/`, "Output" section) — already an
  inspired_by source, no new citation needed. Severity 3. Genuinely net-new:
  cli.md has pipe-safe `--json` and TTY detection but no explicit
  stdout-data / stderr-everything-else separation.
- **Strict, documented parser contract — unknown flags and excess positionals
  fail with a clear validation error, not a silent no-op; ordering constraints
  stated in `--help`.** Source: `@effect/cli` README
  (`https://github.com/Effect-TS/effect/blob/main/packages/cli/README.md`).
  Severity 3. Caveat (carried from draft): the README confirms the parser
  model, but the exact options-before-positionals ordering sentence did not
  surface verbatim — cite clig.dev's predictability stance for the ordering
  claim if the README does not state it explicitly.
- **Interactive wizard/prompt mode for missing required input — offer a guided
  `--wizard` that builds the command and echoes the scriptable equivalent.**
  Source: `@effect/cli` README. Severity 2. Aligns with the repo's own CLI
  prompt-library DX bar.

### errors
- **Mark retryable vs non-retryable explicitly in the error contract** (a
  `retryable` discriminator on the typed error / code catalog). Source: Om
  Bharatiya, `ai-system-design-guide` reliability-patterns
  (`https://github.com/ombharatiya/ai-system-design-guide`). Severity 2.
  Refinement to the existing error-envelope heuristic; retry mechanics already
  in sdk.md. (The companion "success-shaped-failure" item is CUT — see below.)

### setup (`skills/_shared/dx/playbooks/setup.md`)
- **Adoptable in a thin slice — a broad SDK/framework documents a minimal
  first-use needing only a fraction of the surface.** Source: Effect-TS
  Getting Started / Why Effect?
  (`https://effect.website/docs/getting-started/introduction/`). Severity 3.
- **Pinned installer in the quickstart — the bootstrap command pins or names
  the version so the documented first-run is reproducible** (distinct from the
  existing project-runtime pin). Source: `github/spec-kit` README
  (`https://github.com/github/spec-kit/blob/main/README.md`). Severity 3.
  **Accuracy fix:** spec-kit installs via **`uv tool install specify-cli
  --from git+https://github.com/github/spec-kit.git@<tag>`**, not `npx`; the
  README stresses using the latest release tag. Phrase the example around the
  `uv`+tag form; do not imply an `npx` bootstrap.
- **Credential-optional first verification — the smoke test/default test
  command passes on a fresh clone with zero secrets, skipping (not failing)
  checks needing optional paid credentials and naming what was skipped.**
  Source: `earendil-works/pi` README, Development Commands
  (`https://github.com/earendil-works/pi`). Severity 3.

### inner-loop (`skills/_shared/dx/playbooks/inner-loop.md`)
- **Per-PR preview/ephemeral environment — make the change runnable/observable
  per-PR before merge to compress the feedback round-trip.** Source: Mehedi
  Hassan (Granola), "Feedback Loops Are All You Need"
  (`https://www.youtube.com/watch?v=ON5LIT0M4do`); the broader
  ephemeral-preview-per-PR practice is well-documented publicly if a non-AI
  canonical citation is preferred. Severity 2. Placement nuance: straddles
  inner-loop and contributor.md; route to contributor.md if a strict
  local/outer split is preferred. Cite only the general DX practice, not the
  AI-specific parts of the talk.

### contributor
- **Issue triage contract — route "how do I" to Q&A, reserve the tracker for
  repo work, run triage → confirm → owner lifecycle.** Source: MLflow
  `ISSUE_POLICY.md`
  (`https://github.com/mlflow/mlflow/blob/master/ISSUE_POLICY.md`).
  Severity 3.
- **User-facing API changes gate on docs + examples + backward-compatibility
  review.** Sources: Hugging Face "Contribute to PEFT"
  (`https://huggingface.co/docs/peft/developer_guides/contributing`); MLflow
  CONTRIBUTING. Severity 3. PR-time enforcement counterpart to the catalog's
  existing Hyrum's-Law/SemVer grounding.
- **Open a proposal issue before non-trivial work — align scope with
  maintainers before code.** Sources: PEFT contributing guide; MLflow
  ISSUE_POLICY. Severity 2. Doubly grounded.

### migration
- **Usage-gated removal — emit a metric/log on every deprecated-path call and
  gate removal on observed traffic falling to near-zero, not on a calendar
  window alone.** Source: Om Bharatiya, `ai-system-design-guide`
  (`https://github.com/ombharatiya/ai-system-design-guide`); Stripe applies
  the same to dated API versions. Severity 3. Subsumes the
  additive-params/new-names candidates (already covered by expand-contract).
- **Migration risk is a judgment call, not a CI result — high-risk migrations
  (data backfills, lock-taking DDL, dependency additions) carry an explicit
  risk note (lock behavior, backfill size, rollback path, blast radius)
  reviewed separately from the test result.** Source: Ronacher & Poncela
  Cubeiro (Earendil), "The Friction is Your Judgment"
  (`https://youtu.be/_Zcw_sVF6hU`). Severity 3. **Scope note:** the source
  frames this around *AI-coding-agent* PR review ("agents optimize for
  progress," route mechanical violations back via lint, wake a human for
  judgment-bearing changes). The migration-risk-note reframing is the **most
  defensible** of the agent-sourced items — migration risk review is a general
  human-DX concern that long predates agents — but it earns its place on the
  general principle, not the agent framing. Complements "Tested upgrade path"
  and "Reversible schema changes."

### package (`skills/_shared/dx/playbooks/package.md`)
- **Right-sized distributable — offer a smaller subset / granular entry points
  / verified tree-shakeability so size-constrained consumers aren't forced to
  take the whole library.** Source: Effect-TS Micro module + v4 docs
  (`https://effect.website/docs/micro/`). Severity 3. Distinct from the
  measure-and-gate "Install-size budget" heuristic.
- **Manifest-doc agreement — documented version floors, engine ranges, and
  prerequisite counts must match the authoritative manifest
  (pyproject/package.json/Cargo.toml); mismatches are a DX defect class.**
  Source: `swe-bench/SWE-bench` (README "Python 3.8+" vs pyproject `>=3.10`,
  `https://github.com/swe-bench/SWE-bench`). Severity 3. Wiki-confirmed;
  cleanest item in the audit.
- **Operational install-integrity floor — exact pins + save-exact +
  min-release-age + lockfile-as-ground-truth gate + embedded
  `npm-shrinkwrap.json` for end-users + `--ignore-scripts` by default +
  scheduled `npm audit` / `npm audit signatures --omit=dev`.** Source:
  `earendil-works/pi` supply-chain hardening section
  (`https://github.com/earendil-works/pi`). Severity 3. Wiki-confirmed; every
  control is plain npm distribution applicable to any human-maintained
  package.
- **Monorepo package segmentation by responsibility layer — shape
  published-artifact boundaries so consumers depend only on the layer they
  need (Pi: CLI / core / ai / tui under one namespace).** Source:
  `earendil-works/pi` README. Severity 2. Scope strictly to the
  registry-publish granularity decision, not internal module design (which
  overlaps minimal-modular-code).

### examples
- **Example-as-fixture — at least one canonical example is reused as a
  validation fixture (request-schema assertion, contract/smoke test against a
  live or recorded call), so divergence between the documented example and
  real behavior fails the build.** Source: MLflow "Model Signatures and Input
  Examples" (`https://mlflow.org/docs/latest/ml/model/signatures/`).
  Severity 2. Extends Snippet-source parity and CI-tested; do NOT import
  MLflow-specific signature-inference/UI mechanics.

### logging (`skills/_shared/dx/playbooks/logging.md`)
- **Startup banner emits load-bearing config/capacity facts, and docs point at
  those exact lines** (derived limits: worker/pool/cache sizes, bound ports,
  effective config loaded, detected CPU/GPU). Source: vLLM serving/optimization
  docs (`https://docs.vllm.ai/en/stable/configuration/optimization/`).
  Severity 2. Distinct from on-demand doctor/status — this is the unprompted
  boot-time banner.

### config (`skills/_shared/dx/playbooks/config.md`)
- **Config interpolation/shell expansion is a load-time code-execution
  surface — if your config format supports `$VAR`/`$(cmd)`, document it as code
  execution, treat untrusted/checked-in config as untrusted code, and warn
  before evaluating config from an unreviewed directory.** Source:
  `charmbracelet/crush` README
  (`https://github.com/charmbracelet/crush/blob/main/README.md` — "crush.json
  is trusted code"). Severity 3. Distinct from "No secrets in committed files"
  (static leakage, not execution). **This is the human-DX half only** — the
  trusted-broker/sandbox half is split off (see FIX list). Pair with
  errors.md/auth.md secret-hygiene cross-references.

---

## Fix before adding

Resolve the defect, then add (or drop). Each was tagged "Verified" or "needs
verification" in the draft but does not yet hold up.

- **api — vLLM "drop-in/compatible-API contract review" (SOURCE DEFECT).**
  The specific heuristic ("enumerate accepted-but-ignored fields; route
  vendor-only params through an explicit escape hatch") does **not** appear in
  the wiki's vLLM pages — the wiki supports only "segment users by
  compatibility boundary" (`concepts/agent-experience.md`). Marked "Verified"
  without grounding; this is plausible-but-unsourced synthesis. **Downgrade to
  needs-verification and fetch
  `https://docs.vllm.ai/en/stable/serving/openai_compatible_server/` to confirm
  the accepted-but-ignored-fields language before adding.**
- **sdk — `graphql/dataloader` batching (SOURCE DEFECT).** The wiki has **no**
  `graphql/dataloader` entity; every wiki "dataloader" hit is PyTorch ML. The
  citation is a real public repo, so it is not fabricated, but it is **not
  wiki-informed.** Drop the "secondary Effect batching guide" hand-wave; fetch
  `https://github.com/graphql/dataloader` and confirm it actually frames
  coalescing as a caller-transparent deep-module affordance. The heuristic is
  legitimate (aligns with sdk.md's Ousterhout grounding) — just label it
  not-wiki-shaped and verify the citation is apt. Severity 2.
- **package — `min-release-age` version/default numbers (SOURCE DEFECT).** The
  wiki grounds only Pi `min-release-age=2` (2 days) and nanoclaw
  `minimumReleaseAge: 4320` (3 days). The draft's "npm `min-release-age`
  ≥11.10.0; pnpm `minimumReleaseAge`, default 1440 min in v11" are **not** in
  the wiki and the "Verified (adversarially)" tag cannot be taken on faith.
  Re-fetch npm (`https://docs.npmjs.com/cli/v11/using-npm/config`) and pnpm
  (`https://pnpm.io/settings`) primary docs to confirm the version floors and
  the 1440-min default, or strike the specific numbers and keep the mechanism.
  The reframing away from the wiki's "14-Day Package Rule" podcast source is
  correct and is the model de-slanting.
- **auth — RFC 8693 delegated upstream access (ROUTING CONTRADICTION).** The
  draft routes "agent-facing auth (MCP-OAuth / Token Vault / CIBA)" to
  `design-for-agent-users` in §Scope, then keeps **RFC 8693 token-exchange
  vaulting** as a dx-auth ADD. But in the wiki,
  vault-refresh-token-and-mint-short-lived-scoped-tokens **is** the
  OAuth-for-AI-agents mechanism — `concepts/oauth-for-ai-agents.md` literally
  reads `Token Vault | Store upstream refresh tokens; RFC 8693 token
  exchange`, and `concepts/cross-app-access.md` describes the same exchange
  flow. You cannot route the parent pattern to the sibling and keep its core
  mechanism in dx. **Either (a) keep only the narrow already-portable crumbs
  auth.md lacks, or (b) move the RFC 8693 ADD to `design-for-agent-users` to
  match your own routing.** The Auth0 "Identity for AI Agents" worked-example
  URL (`https://youtu.be/VSdV-AdSlis`) is an agent source regardless. The
  draft's other auth items (hashed key storage, server-side scope enforcement,
  both grounded in OWASP ASVS — already a dx-auth grounding source) are fine
  human-DX and survive; do NOT cite the candidate's unresolvable "AI System
  Design Guide" URL for either.
- **ide — tree-sitter vs LSP (SOURCE/SCOPE DEFECT).** The wiki's tree-sitter
  usage is entirely **RAG document-chunking** and **ContextBench
  agent-retrieval** — there is no human editor-integration "layer-choice"
  heuristic anywhere in the wiki. Once you "drop the ContextBench/agent-pipeline
  framing," nothing wiki-shaped remains; it becomes a free-standing claim cited
  to tree-sitter's own docs, and ide.md is already LSP-grounded. **Either
  confirm it stands on tree-sitter's public docs alone (and label it
  not-wiki-informed) or cut.** Do not present it as a wiki-surfaced gap.
  Severity 2.
- **config — trusted-broker / don't-pass-secrets-into-sandbox half (SPLIT +
  NEEDS VERIFICATION).** The config-as-code-execution kernel (above) is
  genuinely human-DX and KEEPS. But the "use an opaque handle + trusted
  broker/egress proxy that injects auth past the boundary" half is the same
  **agent-sandbox** material the draft routes to `design-for-agent-users`
  elsewhere — the Harshil Agrawal "Why sandbox AI-generated code" talk is
  agent-native, and its public canonical URL was **not** independently
  confirmed. **Split the agent slice off; do not ship it as one ADD with the
  config-as-code-execution kernel.** If the broker half is wanted, route it to
  `design-for-agent-users` and confirm/replace the talk URL first.
- **setup — spec-kit `npx` → `uv` (ACCURACY).** Already folded into the clean
  ADD above; flagged here for tally completeness. The pinned-installer ADD is
  well-grounded and KEEPS; correct any `npx`-implying phrasing to the
  `uv tool install … @<tag>` form the wiki and README actually show.

---

## Cut or downgrade

Already covered by an existing heuristic, or an agent/AI-native import.

- **CUT — errors "success-shaped-failure check."** In the wiki this is
  overwhelmingly an **AI/agent** concept: the WorkOS/Galow source is about
  **LLM-generated SQL** ("generated SQL as a deploy artifact… runs and must
  return rows"); the "valid syntax, zero rows" failure lives in
  `concepts/tool-use.md` and `concepts/agent-experience.md` ("a valid-looking
  query returns zero rows because the agent used the wrong wildcard"; "Validator
  and retry loop"). The generic "pair a query op with an independent output
  checker" reframing is a stretch, and errors.md already covers
  swallowed-exception / phantom-success. **Route generated-query validation to
  `design-for-agent-users`, or cut; do not add to dx errors.**
- **CUT or DEMOTE — logging "default terse."** Sourced to Lopopolo "Extreme
  Harness Engineering," which is explicitly an **agent-harness** talk ("humans
  do not write the product code"; "agent-friendly architecture can look
  overbuilt for humans"). logging.md already has **"Single verbosity dial."**
  The draft's "strip the agent-harness slant" instruction does all the work for
  an import whose entire source context is agent-harness. **Cut, or demote to a
  one-line reinforcement of the existing dial — not a severity-3 ADD.**
- **DEMOTE — telemetry "cardinality as the governing axis."** telemetry.md
  **already** carries the low-vs-high-cardinality split as the survive-redaction
  and content-capture-toggle heuristics ("token counts, latencies, finish
  reasons… stay observable even when content capture is disabled"; "structural
  attributes flow even when content capture is off"). The draft itself says it
  only "sharpens" the existing split. **Demote from an ADD to a one-line edit
  to the existing heuristic** (add the cardinality-blowup failure mode to the
  framing).
- **CUT or FOLD — telemetry "telemetry-out-of-the-box" (Vercel AI SDK single
  flag).** Overlaps logging.md's existing **"Conventions over invention"**
  ("Libraries that emit traces depend on the observability API, not a specific
  SDK") and telemetry.md's SDK-layer toggle. "One enable flag → standard
  `gen_ai.*` spans" is the same idea from the producer's side.
  Borderline-redundant; **if kept, fold into the existing convention heuristic
  rather than a standalone ADD.**
- **DOWNGRADE — api/sdk Convex idempotency + two-phase quota.** api.md already
  has **"Idempotency by default"**; sdk.md already honors **Retry-After** with
  full-jitter budget. The genuinely net-new slivers are (a) *persist the request
  as a durable row before the side-effecting call* and (b) *producer-side 429
  carrying concrete wait time*. **Collapse the two Convex ADDs into a single
  refinement note** on the existing idempotency / Retry-After heuristics, not
  two severity-2 ADDs.
- **DOWNGRADE — perf "benchmark-harness hygiene."** perf.md already has
  **"Profiling docs"** + **"Perf CI gates."** Warm-up / isolation /
  timestamped-artifacts is a real missing repeatability layer (wiki-confirmed
  via the DGX Spark on-device source: "three warm-up runs, timestamped output
  directories"), but it is an **addendum to an existing heuristic, not a
  standalone gap.**
- **DE-LLM or ROUTE — perf "TTFT/TTFC streaming-latency metric."** perf.md's
  scope is install/build/CLI/IDE/doc-site latency. TTFT is an
  **inference/AI-product streaming** metric (DGX Spark = "running LLMs
  locally"; the wiki: "Time to first token is the UX metric"). It is not
  human-DX-of-a-dev-tool in the perf.md sense. **Keep the generic method
  (decompose a latency budget across pipeline stages; track first-response
  separately from end-to-end) and drop the LLM-token framing, or route TTFT
  proper to the AI-product perf surface.**

---

## Remove / route

No clean removals from existing playbooks. The within-dx re-homings the draft
identified stand:

- **errors → telemetry + sdk:** Silent provider degradation ("200 while
  quality falls"; provider-switching as the only knob) is a legitimate dx gap
  but not an errors-surface concept — a degraded-but-200 response produces no
  error to shape. Route detection to telemetry.md, and per-call cost bound +
  fallback/provider-switch contract to sdk.md. Sources confirmed (Granola
  "Feedback Loops Are All You Need"; `ai-system-design-guide`). Severity 2.
- **api → sdk:** Long-running-operation durable-execution vocabulary
  (compensation finalizers, at-most-once vs retried activities,
  payload-by-reference, durable clocks) should strengthen sdk.md's existing
  WAITER/poller heuristic, not be raised on the api surface. Severity 0
  (reinforcement, not a gap).

**Untested-removal inconsistency (NEW finding — the draft's "no removals"
claim was not tested).** dx already ships agent-specific heuristics inside its
human-DX playbooks: `errors.md` carries four (Agent-readable error envelope,
Tool-error feedback shaped for retry, Replay-ready error capture, plus the
WorkOS practitioner grounding bullet); `telemetry.md` carries AI/agent-SDK
heuristics (SDK-layer content-capture toggle, pluggable redactor,
inline-vs-reference content discipline, gen-ai span fields). **Under the very
routing rule this audit enforces on new ADDs — "agent-as-consumer →
`design-for-agent-users`" — these are removal/relocation candidates, OR the
rule is being applied inconsistently (strict for new material, lax for what is
already shipped).** This is not a recommendation to rip them out unprompted; it
is a flag that the audit cannot honestly declare "nothing out-of-scope in any
current playbook" while it routes new agent material away. Resolve the policy
once: either dx playbooks may carry a bounded agent-as-consumer appendix (in
which case several CUT items above could instead be such appendices), or they
may not (in which case the existing four errors heuristics and the
telemetry AI block are relocation candidates). Name the decision; do not leave
the rule contradicting the shipped content.

---

## Scope clarifications (deliberately NOT added to dx)

These wiki themes look dx-adjacent but correctly belong to a sibling:

- **AI/Agent-SDK design → `design-for-agent-users`.** Provider-agnostic
  `LanguageModel` service with per-vendor adapters; auto-retry on
  schema-validation failure for structured LLM outputs. The generalizable seams
  (pluggable backend, validate-then-bounded-retry) already exist in sdk.md.
- **Multi-transport bindings + A2A → spec-first add / `design-for-agent-users`.**
  REST/gRPC/JSON-RPC over one op set is subsumed by the Effect HttpApi
  spec-first ADD; the A2A portion is sibling protocol territory.
- **Docs for agents → `design-for-agent-users` / docs.** llms.txt,
  agent-readable docs, RAG chunking, Markdown doc endpoints, ADR-as-docs-system.
  Confirmed correct: dx `docs.md` is purely developer docs (Diátaxis,
  quickstart, reference); the agent-readable surface belongs to the sibling.
- **CLI-gateways-for-AI ("prefill-not-execute", LLM-as-stateless-UNIX-utility,
  agent swarms, `MYCLI_LLM_OFF`) → `design-for-agent-users`.** The one
  dx-worthy kernel (stream separation) was extracted as a standalone cli ADD;
  the env-flag-to-disable kernel is already covered by cli.md "Env-var forms of
  flags."
- **Agent-facing auth → `design-for-agent-users`.** MCP-OAuth / Token Vault /
  CIBA / Cross-App-Access / ID-JAG, machine-readable `auth.md` registration
  discovery, credential-broker/proxy-injection for sandboxed agent code. **Per
  the FIX above, the RFC 8693 vault-and-mint mechanism belongs here too**, to
  match this routing. The portable human-DX crumbs (revocation UX, token
  scoping, OAuth-on-localhost failure) are already in dx auth.
- **Plugin/extension agent surfaces → `design-for-agent-users`.** Pi-extensions
  primitives, Crush manifest model-vs-user invocation flags, Crush
  hooks-before-permission-checks protocol. Generic discovery/isolation already
  covered by plugin.md.
- **AI/agent observability → `agent-evals` / `design-for-agent-users`.**
  Trace-linked evals, MELT, agent-span taxonomy, OpenInference span kinds, MCP
  W3C traceparent propagation. Answers "is the agent doing a good job?", not "is
  my library's telemetry well-designed?" The portable
  cardinality/token-precision/content-capture crumbs are already in dx
  telemetry (see the inconsistency flag above).
- **IDE-as-agent-customization-modal → `design-for-agent-users`.** Editor modal
  surfacing skills/instructions/hooks/MCP for an agent to consume; dx `ide` = an
  SDK a human consumes via autocomplete/diagnostics. (The tree-sitter item is
  separately a source defect — see FIX.)
- **Maintainer triage of agent-generated PRs → `design-for-agent-users`.**
  Driver is AI-agent-generated PR volume; the human-OSS-maintainer version
  already lives in dx contributor.
- **Release-gates as agent pass/block checkpoints → `agent-readiness`.**
  Critic/LLM-as-judge gates, trace-evidence handoff. The human release-
  discipline slice already lives in package.md.
- **Config semantic-vs-syntactic tool-arg validation + repair-retry →
  `design-for-agent-users`.** Agent-loop tool-call argument validation, not
  runtime config validation; config.md already has schema-validated config +
  fail-at-load.
- **`minimal-modular-code` overlap:** monorepo package segmentation is held to
  the registry-publish-granularity slice only; internal module-boundary design
  stays with minimal-modular-code.
- **test surface:** PEFT's "regression test that fails before, passes after" is
  a test-design concern, not contributor-flow; route to the test skills if
  added at all.

---

## New surface?

**No.** No flagged theme justifies a 21st dx surface. The two near-misses both
resolve to existing surfaces: IDE-as-agent-customization-modal is
agent-as-consumer (`design-for-agent-users`), and maintainer-flow-under-agent-PR-volume
is the agent-driven variant of the existing dx `contributor` surface. The
conservative bar is met.

---

## Limitations

- **Source defects gate three items.** vLLM compat-contract and
  `graphql/dataloader` batching are now needs-verification (public source not
  shaped by / not present in the wiki); the package min-release-age **numbers**
  need a primary-doc re-fetch before they can ship.
- **Routing contradiction gates one item.** The auth RFC 8693 ADD must either
  shrink to the portable crumbs or move to `design-for-agent-users` to match
  the audit's own §Scope routing.
- **The de-slanting test is necessary but not sufficient.** "Cite the principle,
  strip the agent words" is the right move when only the *framing* is
  agent-flavored (the package release-age cooldown is the model). It is **not**
  sufficient when the source, the failure mode, AND the designed surface are all
  agent-native (Lopopolo agent-harness, WorkOS generated-SQL, OAuth-for-agents,
  DGX inference). Rephrasing those into human-DX language produces the W1-style
  plausible boilerplate the repo's promotion floor warns against. Apply the
  audit's own rule — "decide by surface being designed, not by 'a human calls
  it'" — to all six, not just the easy cases.
- **Numbers to gate, methods to keep.** Bhargava's per-stage latency budgets are
  Together-specific (the source flags this); the mycli "200–500ms" cold-start
  figure is the wiki's synthesis, not the primary source; DGX TTFT numbers are
  point measurements. Add the method, gate the numbers.
- **One-sided vendor sources.** The sdk "adoption friction" ADD rests on
  Effect's own comparison pages — cite the reusable adoption-cost principle, not
  the head-to-head verdict. Several Effect-anchored adds share a single-vendor
  grounding bias; a second independent public instance would strengthen them but
  is not blocking.
- **Talk sources are qualitative.** Granola, Lopopolo, DGX Spark, Ronacher, and
  the observability-panel talks are vendor/product narratives with no quantified
  deltas — fine for qualitative DX heuristics, not for numeric gates.
- **Wiki is shaping input only.** Every ADD above is grounded in a public
  source; the wiki is never cited in any published skill, per the
  source-of-truth-no-attribution rule.

---

## Net keep / fix / cut tally

- **KEEP as-is (16):** api spec-as-source-of-truth; api consumer-driven contract
  testing (Pact, wiki-confirmed); sdk parse-don't-validate; sdk resource-safety
  finalizers; sdk adoption-friction (principle only); cli stream-separation; cli
  strict-parser (with the clig.dev ordering caveat); cli wizard/prompt mode;
  setup thin-slice adoptability; setup pinned-installer (`uv`+tag); setup
  credential-optional first verification; inner-loop per-PR preview; contributor
  issue-triage; contributor API-changes-gate-on-docs; contributor
  proposal-issue-before-work; migration usage-gated removal; migration
  risk-is-a-judgment-call (general principle); package right-sized distributable;
  package manifest-doc agreement (cleanest item); package operational
  install-integrity floor; package monorepo segmentation; examples
  example-as-fixture; errors retryable-discriminator; logging vLLM
  startup-banner; config interpolation-as-code-execution (human-DX half).
  *(Several of the migration/auth/contributor entries carry the
  cite-the-principle caveat noted inline; the count groups closely-related Pi
  package controls as one floor.)*
- **FIX before adding (7):** vLLM compat-contract (source); dataloader batching
  (source label); package min-release-age numbers (source); auth RFC 8693
  (routing); ide tree-sitter (source/scope); config trusted-broker half (split
  off the agent slice); spec-kit `npx`→`uv` (accuracy, folded into the ADD).
- **CUT or DOWNGRADE (7):** errors success-shaped-failure (cut/route); logging
  default-terse (cut/demote); telemetry cardinality-axis (demote to
  existing-heuristic edit); telemetry out-of-the-box (fold into logging
  "conventions over invention"); api/sdk Convex pair (collapse to one
  refinement); perf benchmark-hygiene (demote to addendum); perf TTFT
  (de-LLM or route).
- **MISSED in the draft (1):** the "no removals" claim is untested against dx's
  own pre-existing agent heuristics (errors.md / telemetry.md) given the routing
  rule the draft enforces on new ADDs — surface the inconsistency rather than
  declaring the playbooks clean.

**Files examined:** all 20 playbooks under
`/Users/justin/Dev/informed-skills/skills/_shared/dx/playbooks/`; wiki sources
under `/Users/justin/Dev/ai-wiki/wiki/{entities,concepts,sources}/` — notably
`concepts/14-day-package-rule.md`, `concepts/tool-use.md`,
`concepts/agent-experience.md`, `concepts/oauth-for-ai-agents.md`,
`concepts/cross-app-access.md`,
`sources/extreme-harness-engineering-ryan-lopopolo-openai.md`,
`sources/the-friction-is-your-judgment-armin-ronacher-cristina-poncela-cubeiro-earendil.md`,
`sources/earendil-works-pi-github.md`, `sources/nanoclaw-repo-docs.md`,
`sources/github-spec-kit-readme.md`, `entities/github-spec-kit.md`,
`sources/running-llms-locally-practical-llm-performance-on-dgx-spark-mozhgan-kabiri-chimeh-nvidia.md`,
`sources/swe-bench-repo-docs.md`, `entities/pact.md`, `entities/pactflow.md`,
`sources/pact-smartbear-contract-testing-docs.md`, `entities/effect-ts.md`,
`entities/mlflow.md`.
