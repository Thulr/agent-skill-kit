# Research Report — Effective Documentation Patterns and Practices for DX, AX, and UX

**Date:** 2026-05-27
**Depth mode:** deep-dive
**Methodology grounding:** see `skill.json.inspired_by` of the `topic-research` skill

---

## 1. Research question

**What documentation patterns and practices produce effective developer experience (DX), agent experience (AX), and end-user experience (UX) — covering tutorials, reference, how-to, explanation, examples, error copy, in-product help, onboarding, IA, and machine-readability — and where do the three audiences converge, diverge, and conflict?**

- **In scope:** docs-as-code workflow, information architecture, Diátaxis and competing frameworks, style guides (Google / Microsoft / 18F / Mailchimp / GOV.UK), README and quickstart bar, code-sample testing, OpenAPI / typed-schema as docs, in-product help, onboarding flows, error-copy as docs, llms.txt / AGENTS.md / SKILL.md / MCP descriptions, documentation accessibility (WCAG 2.2), plain language, RAG-over-docs design, doc telemetry and feedback loops.
- **Out of scope:** tool bake-offs (Mintlify vs Docusaurus vs Sphinx feature lists), non-software UX writing (marketing copy), localization process detail, paid content strategy frameworks.
- **Audience / use:** practitioners building or evolving documentation across DX, AX, and UX surfaces — particularly those weighing whether AX is a sub-discipline of DX or a distinct design discipline with its own patterns and evidence base. The report is framed with **AX as the centerpiece**; DX and UX patterns are present as comparative reference frames against which the AX claims can be evaluated.

## 2. Search strategy

- **Source types consulted (priority order):**
  1. Canonical framework sources (Diátaxis / Procida; Rosenfeld, Morville, Arango on IA; Bloch on API design as documentation).
  2. Standards bodies (W3C WCAG 2.2, plainlanguage.gov / Plain Writing Act, OpenAPI 3.1, schema.org, Model Context Protocol spec, llms.txt spec).
  3. Peer-reviewed and arXiv academic (CMU Natural Programming / Stylos & Myers on API usability; Gloaguen / Mündler et al. on AGENTS.md evaluation; Hasan et al. on MCP description quality; VersionRAG; meta-policy reflection).
  4. Vendor primary engineering writing (Stripe, Twilio, Vercel, Cloudflare, Anthropic, OpenAI, Google, Microsoft, Mintlify, GitLab, Netlify, WorkOS, Stytch, Speakeasy).
  5. Practitioner long-form (Tom Johnson / *I'd Rather Be Writing*, Simon Willison, Mathias Biilmann, NN/g articles, Nordic APIs AX series, Anne Gentle on docs-as-code).
- **Search terms (sample):** "Diátaxis framework documentation," "llms.txt specification," "AGENTS.md AI agents," "Anthropic Agent Skills SKILL.md," "MCP tool description quality," "agent experience AX documentation," "WCAG 2.2 documentation accessibility," "Stripe error doc_url," "OpenAPI 3.1 examples agents," "RAG chunking documentation structure," "Cloudflare Markdown for Agents," "AGENTS.md evaluation benchmark," "docs as code Anne Gentle," "NN/g help and documentation."
- **Engines / venues:** general web search, GitHub repository search, arXiv direct, ACM Digital Library (cited entries returned 403 for full body — citations made at the abstract / published-summary level where this happened), W3C, OpenAPI Initiative, Linux Foundation Agentic AI Foundation pages, vendor engineering blogs.
- **Snowballing:** forward and backward from anchor sources. Backward from llms.txt → robots.txt / sitemap.xml / Diátaxis; from AGENTS.md → CLAUDE.md / Cursor rules / `.github/copilot-instructions.md`; from Stripe error docs → Brandur on idempotency, Rust diagnostics history. Forward from Procida → Cloudflare style guide, Django, Gatsby adoption examples; from Anthropic Agent Skills → Vercel AGENTS.md vs Skills evals, Speakeasy skills release; from WorkOS AX essay → Biilmann's one-year-of-AX adopter list.
- **Exclusions:**
  - Vendor marketing without engineering substance.
  - Listicles and "Top N tools" comparisons without first-party authorship.
  - Pre-2018 generic technical-writing handbooks (too dated for the AX surface).
  - Non-English sources (English-only bias acknowledged in §8).
- **Stop criterion:** saturation per sub-question (three consecutive sources adding zero net-new claims), with the centerpiece §4.4 lifted to a higher target (~35 sources) given the discipline's novelty. Roughly 75 distinct sources cited across the report after deduplication.

## 3. Background

### 3.1 The three audiences

Documentation is consumed by three structurally different audiences, and the patterns that delight one can actively harm the others. The framing the report uses:

- **DX (Developer Experience)** — the human engineer integrating an SDK, API, CLI, framework, or library into their own application. Cares about install ergonomics, mental-model fit, sensible defaults, IDE surfacing, debuggability of the integration.
- **UX (End-user Experience)** — the human consumer of a software product through its UI. Cares about plain language, learnability in the moment of need, recovery from error, accessibility, and minimal context-switching to help surfaces.
- **AX (Agent Experience)** — LLM-based agents (coding agents like Claude Code, Cursor, Codex; runtime agents like chatbots and autonomous workflows; RAG retrievers) that *consume* documentation as part of their work. Coined by Mathias Biilmann of Netlify on 28 January 2025 and now sits alongside DX and UX as a named design surface in vendor positioning across Anthropic, Vercel, Mintlify, Cloudflare, WorkOS, Stytch, Stripe, and Speakeasy.

WorkOS's framing for the AX/UX gap captures the core asymmetry: "agents cannot read tooltips, infer layout intent, recover from ambiguous errors, or maintain context across sessions without explicit support. They operate at machine speed, retry aggressively, and make decisions solely on surfaced text." Patterns that depend on visual hierarchy, hover state, animation, or implicit convention are AX failures by default.

### 3.2 Why AX is the centerpiece of this report

Three reasons. First, the discipline is the youngest of the three — the original llms.txt proposal landed September 2024, AGENTS.md converged August 2025, Anthropic Agent Skills released October 2025, the canonical "Introducing AX" post landed January 2025. The evidence base is thin enough that synthesis is genuinely needed. Second, the patterns that work for AX are largely orthogonal to and sometimes opposed to the patterns that work for DX and UX (see §4.5 for the conflicts), so a report that treats AX as an afterthought misses the design tensions. Third, two recent academic papers (Gloaguen / Mündler et al. on AGENTS.md, Hasan et al. on MCP descriptions) provide the first rigorous evidence on what works at the AX layer — and both produce counterintuitive findings that contradict naive maximalist instincts.

### 3.3 What counts as "documentation"

The report treats documentation broadly: anything written or structured to communicate how a system works, who it's for, and how to use it. Operationally this includes prose docs (tutorials, reference, how-to, explanation, FAQs), embedded surfaces (READMEs, doc comments, type signatures, IDE hover-text), error messages and validation copy, in-product help (tooltips, walkthroughs, empty states, onboarding tours), machine-readable contracts (OpenAPI, MCP tool descriptions, GraphQL SDL, llms.txt, AGENTS.md, SKILL.md, schema.org markup), and the operational metadata around them (versioning, telemetry, feedback loops, release notes). The unifying claim: all of these are documentation surfaces, and patterns that work on one surface often transfer to others — though never without inspection.

## 4. Current state

### 4.1 Cross-audience documentation foundations

These eight patterns apply to documentation for any audience — developers reading SDK references, end-users following onboarding, or agents consuming SKILL.md frontmatter. Treat them as the substrate the audience-specific patterns in §4.2–4.4 build on. Where one audience pulls a foundation in a different direction (e.g., agents need stricter machine-readability than humans tolerate), the divergence is flagged inline.

#### Diátaxis framework
Daniele Procida's Diátaxis names four documentation modes — **tutorials** (learning-oriented), **how-to guides** (task-oriented), **reference** (information-oriented), and **explanation** (understanding-oriented) — and arranges them on a two-axis frame: **action vs. cognition** and **study vs. work** ([diataxis.fr](https://diataxis.fr/)). The framework's operational claim is not just "there are four types" but that *mixing the modes in a single document is the bug* — a tutorial that drifts into reference, or a how-to that drifts into explanation, fails both jobs.

Adoption is broad and named: Cloudflare's developer-docs team calls Diátaxis their "north star for information architecture" ([Cloudflare Style Guide](https://developers.cloudflare.com/style-guide/documentation-content-strategy/information-architecture/)), Gatsby and Vonage cite it on Procida's site ([diataxis.fr](https://diataxis.fr/)), and Django's documentation explicitly organizes around tutorials, topic guides, how-tos, and reference ([Django docs](https://docs.djangoproject.com/en/6.0/)). For AX specifically, the four modes map cleanly onto what an agent needs to discriminate: agents call SKILL.md "how-to" routes for work, but need separate reference surfaces for argument shape — the same anti-mixing rule applies.
**Sources:** [Diátaxis (Procida)](https://diataxis.fr/), [Cloudflare Style Guide — IA](https://developers.cloudflare.com/style-guide/documentation-content-strategy/information-architecture/), [Django documentation](https://docs.djangoproject.com/en/6.0/)
**Confidence:** H

#### Docs-as-code workflow
Docs-as-code treats documentation with the same tooling as source: plain-text markup in version control, pull-request review, automated build, and CI deploy ([Write the Docs guide](https://www.writethedocs.org/guide/docs-as-code/)). The Write the Docs community lists the canonical chain as Git + Markdown/reST/AsciiDoc + code review + issue trackers + automated tests, and notes the load-bearing benefit: it lets teams "block merging of new features if they don't include documentation, which incentivizes developers to write about features while they are fresh."

The pattern was popularized in book form by Anne Gentle's *Docs Like Code* (1st ed. 2017, 3rd ed. 2022) ([docslikecode.com](https://www.docslikecode.com/)), which is the standard reference Write the Docs points readers to. By 2025–2026, docs-as-code is effectively assumed at engineering-led organizations — Stripe, GitLab, Vercel, and Cloudflare all run their public docs out of repos with PR review. For AX, the implication is sharper than for human audiences: agents *write* the docs they later consume, so the same PR + CI + lint chain that gates code must gate the AGENTS.md / SKILL.md / MCP surfaces too.
**Sources:** [Write the Docs — Docs as Code](https://www.writethedocs.org/guide/docs-as-code/), [Docs Like Code (Anne Gentle)](https://www.docslikecode.com/)
**Confidence:** H

#### Code samples must be tested, runnable, and current
Stale code samples are one of the most common documentation defects, and the foundational fix is to execute samples in CI rather than rely on human review. Python's standard library has shipped `doctest` since the early 2000s, and Sphinx's [`sphinx.ext.doctest`](https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html) extension extracts marked code blocks from docs and runs them as tests on every build — the official guidance is to wire `python -m sphinx -b doctest` into CI so broken samples fail the build.

Stripe took this further by building [Markdoc](https://stripe.dev/blog/markdoc), now open-source, which treats docs as a typed authoring format with schema-validated tags and link-graph checking. Stripe's CI "check[s] to make sure that every link between pages within our documentation points to a valid route," and an internal VS Code extension surfaces validation errors as authors type ([stripe.dev/blog/markdoc](https://stripe.dev/blog/markdoc)). The institutional pattern is consistent across mature doc operations: untested samples decay faster than the docs team can catch by reading. For AX the same rule binds harder — agents copy-paste from samples literally, so a stale snippet becomes a stale tool-call.
**Sources:** [Sphinx doctest extension](https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html), [Stripe — How we build interactive docs with Markdoc](https://stripe.dev/blog/markdoc)
**Confidence:** H

#### Style guides as a foundation
Three style guides anchor English-language technical writing in 2026: the [Google Developer Documentation Style Guide](https://developers.google.com/style), which sets the editorial baseline for "clear and consistent technical documentation for an audience of software developers and other technical practitioners"; the [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/), whose top-line voice principle is "warm and relaxed, crisp and clear, ready to lend a hand"; and the [18F Content Guide](https://guides.18f.gov/content-guide/) from the US federal digital-services team.

Plain-language requirements have legal force in the US: the [Plain Writing Act of 2010](https://www.plainlanguage.gov/) requires federal agencies to write "clear, concise, well-organized" content and follow the [Federal Plain Language Guidelines](https://www.plainlanguage.gov/guidelines/). The Microsoft guide and 18F guide both require bias-free terminology — avoiding gendered defaults, ableist phrasing, and culture-coded idioms — which carries directly to UX copy and onboarding. For AX, style guides matter less for voice and more for *terminology consistency*: an agent that sees "endpoint" in one page and "route" in the next infers two concepts.
**Sources:** [Google Developer Documentation Style Guide](https://developers.google.com/style), [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/), [18F Content Guide](https://guides.18f.gov/content-guide/), [plainlanguage.gov](https://www.plainlanguage.gov/), [Federal Plain Language Guidelines](https://www.plainlanguage.gov/guidelines/)
**Confidence:** H

#### Information architecture
Rosenfeld, Morville, and Arango's *Information Architecture: For the Web and Beyond* (4th ed., O'Reilly 2015 — the "polar bear book") is the canonical IA reference; it codifies the organization / labeling / navigation / search systems that any docs site composes ([O'Reilly](https://www.oreilly.com/library/view/information-architecture-4th/9781491913529/)). The empirical method for grounding a taxonomy is **card sorting**, treated comprehensively in Donna Spencer's *Card Sorting: Designing Usable Categories* (Rosenfeld Media) — open, closed, and hybrid sorts surface how users actually group concepts vs. how authors structure them ([Rosenfeld Media](https://rosenfeldmedia.com/books/card-sorting/)).

A second foundational IA pattern is **progressive disclosure**, introduced by Jakob Nielsen in the mid-1990s: show the few most important options first, defer specialized options to a secondary level ([NN/g](https://www.nngroup.com/articles/progressive-disclosure/)). NN/g argues this improves learnability, efficiency, and error rates simultaneously. Search-first vs. browse-first is a live IA debate for docs sites — Stripe and Cloudflare lean search-first for reference, Diátaxis-shaped sidebars lean browse-first for orientation; mature sites support both.
**Sources:** [Information Architecture: For the Web and Beyond (Rosenfeld/Morville/Arango)](https://www.oreilly.com/library/view/information-architecture-4th/9781491913529/), [Card Sorting (Spencer)](https://rosenfeldmedia.com/books/card-sorting/), [NN/g — Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)
**Confidence:** H

#### Accessibility (WCAG 2.2)
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) became a W3C Recommendation on 5 October 2023, adding nine new success criteria on top of WCAG 2.1 ([W3C WAI](https://www.w3.org/WAI/news/2023-10-05/wcag22rec/), [What's New in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)). For documentation sites specifically, the load-bearing additions are **2.4.11 Focus Not Obscured** (sticky headers can't cover the focused link in a long doc), **2.4.13 Focus Appearance** (focus rings must be visible — critical for keyboard nav through nested TOCs), **2.5.8 Target Size (Minimum)** (sidebar and inline links must be tappable), and **3.2.6 Consistent Help** (help/feedback widgets must sit in the same place on every page).

Baseline WCAG 2.1 obligations carry forward and matter most for docs: semantic heading hierarchy (H1→H2→H3 in order, no skips), descriptive alt text on diagrams, code blocks that screen readers can navigate as preformatted text rather than running prose, and color-contrast in syntax highlighting (a frequent regression — dark themes ship with low-contrast comment colors). Keyboard nav and visible focus are how blind, low-vision, and motor-impaired users move through a docs site at all.
**Sources:** [WCAG 2.2 (W3C Recommendation)](https://www.w3.org/TR/WCAG22/), [W3C — WCAG 2.2 announcement](https://www.w3.org/WAI/news/2023-10-05/wcag22rec/), [What's New in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
**Confidence:** H

#### Versioned docs
Documentation versions must track product versions or they become actively misleading. Stripe maintains long-lived API version pins and ships explicit [API upgrade guides](https://docs.stripe.com/upgrades) per release ([Stripe API versioning](https://docs.stripe.com/api/versioning)). Kubernetes hosts the current release plus the four previous releases on dedicated subdomains (v1.36 at `kubernetes.io/docs/`, v1.35 at `v1-35.docs.kubernetes.io/`, and so on) and explicitly separates "documentation available" from "version supported" ([Kubernetes — Supported Doc Versions](https://kubernetes.io/docs/home/supported-doc-versions/)). React-Native publishes archived versions as "permanent, immutable deployments" ([RFC #3819](https://github.com/facebook/react-native-website/issues/3819)).

The institutional pattern is: an explicit per-version archive, a banner on archived versions pointing to current, and a deprecation/upgrade path. The cost of drift is high — a user landing on an outdated page via search who can't tell they're on an outdated page will file bug reports against the current product. For AX the cost compounds: agents retrieve a version-stale snippet and call a removed API.
**Sources:** [Stripe API versioning](https://docs.stripe.com/api/versioning), [Stripe upgrades](https://docs.stripe.com/upgrades), [Kubernetes — Supported Doc Versions](https://kubernetes.io/docs/home/supported-doc-versions/), [React-Native docs version archiving (RFC #3819)](https://github.com/facebook/react-native-website/issues/3819)
**Confidence:** H

#### Documentation telemetry & feedback loops
Mature documentation operations instrument their sites the way product teams instrument apps. The page-level **"Was this helpful?"** widget is near-universal on docs.gitlab.com, learn.microsoft.com, kubernetes.io, and developer.cloudflare.com; GitLab routes "Nothing on this page helped" responses into its issue tracker as docs-feedback issues that the docs team triages ([GitLab issue #374573](https://gitlab.com/gitlab-org/gitlab/-/issues/374573)). Tom Johnson (Google, *I'd Rather Be Writing*) argues that surveys-and-thumbs alone are weak signals and should be paired with a concrete quality checklist evaluated against the docs site ([Measuring documentation quality](https://idratherbewriting.com/learnapidoc/docapis_measuring_impact.html)).

The stronger telemetry signal is **search-query analysis**: queries that return zero results, or queries followed by an immediate exit, are direct gap evidence — they say "users asked for X and the docs didn't answer." The doc-team-as-product-team framing (Johnson, GitLab's docs handbook) follows from this: docs are a product with users, metrics, a backlog, and a release cadence, not a write-once artifact. (Empirical literature specifically validating "Was this helpful?" widget accuracy is thin — the institutional pattern is widespread but the academic evidence base is weaker than for the other foundations.)
**Sources:** [GitLab docs feedback issue (#374573)](https://gitlab.com/gitlab-org/gitlab/-/issues/374573), [Tom Johnson — Measuring documentation quality](https://idratherbewriting.com/learnapidoc/docapis_measuring_impact.html)
**Confidence:** M

### 4.2 DX (developer experience) documentation patterns

#### README structure and the time-to-first-Hello-World (TTFHW) bar

The README is the load-bearing artifact of developer adoption: it is the first file rendered when a developer lands on a repository, and in many cases it is the only documentation a developer reads before deciding whether to keep evaluating the project. Tom Preston-Werner's 2010 essay "Readme Driven Development" argues that the README should be written *before* the code, on the grounds that "a perfect implementation of the wrong specification is worthless" and "a beautifully crafted library with no documentation is also damn near worthless" ([Preston-Werner, 2010](https://tom.preston-werner.com/2010/08/23/readme-driven-development.html)). RDD treats the README as the single most important document in the codebase — a forcing function on API design and naming, not retroactive prose.

The operational form of this principle is the time-to-first-Hello-World (TTFHW) bar: a developer should be able to install the package and see a meaningful result within minutes of landing on the README. This means the *first* code block above the fold is an install command, and the *second* is a complete minimal working example — not a feature tour, not a comparison table, not a list of badges. Twilio's Programmable Voice quickstart and Stripe's API reference both organize around this pattern, putting a runnable snippet in the first viewport with credentials clearly marked as the only placeholder a reader must edit ([Twilio Programmable Voice Quickstarts](https://www.twilio.com/docs/voice/quickstart), [Stripe API Reference](https://docs.stripe.com/api)). The Rust API Guidelines codify a similar bar for libraries: "the front-page should give an example of how to use the crate in a real world setting" ([Rust API Guidelines: Documentation](https://rust-lang.github.io/api-guidelines/documentation.html)).

**Sources:** [Preston-Werner, "Readme Driven Development"](https://tom.preston-werner.com/2010/08/23/readme-driven-development.html), [Twilio Programmable Voice Quickstarts](https://www.twilio.com/docs/voice/quickstart), [Rust API Guidelines: Documentation](https://rust-lang.github.io/api-guidelines/documentation.html)
**Confidence:** H

#### Quickstarts vs tutorials vs how-to guides (Diátaxis applied to DX)

Daniele Procida's Diátaxis framework partitions documentation into four modes — **tutorials** (learning-oriented), **how-to guides** (task-oriented), **reference** (information-oriented), and **explanation** (understanding-oriented) — and argues that mixing them is the primary structural failure mode of technical documentation ([Diátaxis](https://diataxis.fr/)). The framework "solves problems related to documentation content (what to write), style (how to write it) and architecture (how to organise it)" by holding each mode to a different success criterion: a tutorial succeeds if the reader *learns*, a how-to succeeds if the reader *completes a task*, a reference succeeds if the reader *finds a fact*.

The DX-specific cost of mixing modes is severe. Reference dressed as tutorial forces a beginner to read an exhaustive API surface before they can do anything useful; tutorial dressed as reference makes a working developer hunt through prose to find a parameter signature. The "Quickstart" page is the highest-trafficked DX artifact in most SDKs and is genuinely a *tutorial* in Diátaxis terms — its success metric is that a first-time user ends in a working state, not that the user has been taught every option. Stripe and Twilio both treat their quickstarts as tutorials and route "I need to look up the `payment_intent.confirm` parameters" traffic to a separate reference surface generated from OpenAPI ([Stripe API Reference](https://docs.stripe.com/api), [Twilio Docs Quickstart Hub](https://www.twilio.com/docs/quickstart)). Simon Willison's adoption note captures why the framework spread: it gives writers a forcing question — "which of the four am I writing?" — that surfaces structural drift before publication ([Willison, 2021](https://simonwillison.net/2021/Aug/21/diataxis/)).

**Sources:** [Diátaxis](https://diataxis.fr/), [Willison on Diátaxis](https://simonwillison.net/2021/Aug/21/diataxis/), [Stripe API Reference](https://docs.stripe.com/api), [Twilio Docs Quickstart Hub](https://www.twilio.com/docs/quickstart)
**Confidence:** H

#### API reference: auto-generated vs hand-written

API reference documentation lives on a spectrum from fully auto-generated (extracted from source or schema) to fully hand-written. The auto-generated end is anchored by inline-comment conventions: Go's `godoc` (Andrew Gerrand's 2011 introduction) parses comments immediately preceding declarations and treats them as the documentation source of truth, on the principle that "the comments read by godoc are not language constructs… they are just good comments, the sort you would want to read even if godoc didn't exist" ([Gerrand, "Godoc: documenting Go code"](https://go.dev/blog/godoc), [Go Doc Comments](https://go.dev/doc/comment)). Rust's `rustdoc` follows the same model with stronger conventions — `# Examples`, `# Panics`, `# Errors`, and `# Safety` sections are expected by convention on public items, and code in `# Examples` is compiled by `cargo test` so it cannot rot silently ([Rust API Guidelines: Documentation](https://rust-lang.github.io/api-guidelines/documentation.html)). TSDoc/JSDoc, Python's docstring-as-doc tradition (Sphinx autodoc), and Java's Javadoc all share this DNA.

For HTTP APIs, OpenAPI-driven renderers (Swagger UI, Redoc/Redocly, Mintlify, Scalar, ReadMe, Bump) replace handwritten reference with schema-derived pages. Practitioner write-ups converge on the trade-off: auto-generation eliminates the "documentation drift" problem — the spec *is* the doc — but it can produce uniformly bland reference that misses the *why*. Speakeasy's vendor comparison frames it bluntly: "documentation drift is the real problem, not the rendering of the spec," and the fastest-shipping teams adopt design-first workflows where the OpenAPI document is reviewed as a primary artifact rather than generated as an afterthought ([Speakeasy: Choosing a docs vendor](https://www.speakeasy.com/blog/choosing-a-docs-vendor)). Hand-written reference (Stripe is the canonical example) survives where the team is willing to staff editors who shadow engineering changes — Stripe's three-column layout, in which prose, parameter tables, and runnable code sit side by side, is a hand-curated artifact pinned to a generated schema ([Stripe API Reference](https://docs.stripe.com/api)).

**Sources:** [Gerrand, "Godoc"](https://go.dev/blog/godoc), [Go Doc Comments](https://go.dev/doc/comment), [Rust API Guidelines: Documentation](https://rust-lang.github.io/api-guidelines/documentation.html), [Speakeasy: Choosing a docs vendor](https://www.speakeasy.com/blog/choosing-a-docs-vendor), [Stripe API Reference](https://docs.stripe.com/api)
**Confidence:** H

#### Code samples as first-class artifacts

Stylos and Myers' decade-plus of API-usability work at CMU's Natural Programming group found, across multiple controlled studies, that developers reach for example code first and reference second, and that the *presence and quality* of examples predicts task success more reliably than reference completeness ([Myers & Stylos, "Improving API Usability," *CACM* June 2016](https://cacm.acm.org/research/improving-api-usability/), [CMU NatProg API Usability](http://www.cs.cmu.edu/~NatProg/apiusability.html)). The practitioner consequence is that examples are not adornment — they are the primary teaching surface.

A first-class example has four properties: it is **runnable** (copy-paste produces a working result with only credentials swapped), **complete-and-minimal** (no missing imports, no elided error handling that hides a real failure mode, but no demonstration of unrelated features), **tested in CI** (Rust's doctest in `# Examples` blocks and Go's `Example` test functions in `pkg.go.dev` both compile and execute), and **idiomatic in the target language** (Python examples don't read like translated JavaScript). Google's developer-documentation style guide formalizes much of this — sample introduction sentences, indentation, line-wrap, and the requirement that samples be self-contained where reasonable ([Google Code Samples Style](https://developers.google.com/style/code-samples)). Twilio's reputation rests partly on the "8-line quickstart" pattern: their canonical SMS quickstart fits a working call into roughly that many lines, with the credentials and recipient as the only required edits ([Twilio SMS Quickstart](https://www.twilio.com/docs/sms/quickstart)). Multi-language tabs (Node, Python, Go, Ruby, Java, curl) on a single reference page are now the industry default precisely because they collapse the "is this in my language?" branch developers otherwise have to reason through.

**Sources:** [Myers & Stylos, "Improving API Usability," *CACM*](https://cacm.acm.org/research/improving-api-usability/), [CMU NatProg](http://www.cs.cmu.edu/~NatProg/apiusability.html), [Google Code Samples Style](https://developers.google.com/style/code-samples), [Twilio SMS Quickstart](https://www.twilio.com/docs/sms/quickstart)
**Confidence:** H

#### Error copy as documentation

Error messages are the documentation a developer reads at the moment they most need it, and they are the only documentation a developer encounters involuntarily. Stripe's structured error object — `type`, `code`, `message`, `param`, `doc_url`, and `decline_code` — sets the practical floor: every error carries a machine-readable category, a human-readable message identifying the offending parameter by name, and a deep link to the relevant doc page ([Stripe Errors API](https://docs.stripe.com/api/errors), [Stripe Error Codes](https://docs.stripe.com/error-codes)). The `doc_url` field is load-bearing — it converts an error into a navigable documentation event rather than a dead-end.

Compiler diagnostics show the same principle at the language level. The Rust compiler's diagnostic style was deliberately rebuilt around Elm's approach, anchoring messages on the user's own code with carets and labels, and adding the `--explain <code>` flag for extended explanations of error classes ([Rust RFC 1644: Default and Expanded rustc Errors](https://rust-lang.github.io/rfcs/1644-default-and-expanded-rustc-errors.html), [Rust Blog: "Shape of errors to come"](https://blog.rust-lang.org/2016/08/10/Shape-of-errors-to-come/), [Rust Error Codes Index](https://doc.rust-lang.org/error-index.html)). Esteban Küber, who led much of that work, has summarized the design philosophy as: an error message is often your first and best chance to teach somebody something. The minimum DX bar that follows from both Stripe and Rust: every error must say *what went wrong*, *where it went wrong* (offending value or location), and *what to do next* (next action or doc link). Generic messages like "invalid config" fail all three.

**Sources:** [Stripe Errors API](https://docs.stripe.com/api/errors), [Stripe Error Codes](https://docs.stripe.com/error-codes), [Rust RFC 1644](https://rust-lang.github.io/rfcs/1644-default-and-expanded-rustc-errors.html), [Rust Blog: "Shape of errors to come"](https://blog.rust-lang.org/2016/08/10/Shape-of-errors-to-come/), [Rust Error Codes Index](https://doc.rust-lang.org/error-index.html)
**Confidence:** H

#### Type signatures as documentation

The IDE — not the documentation site — is the primary documentation surface for most working developers, and that surface is populated by type signatures and the prose attached to them. Joshua Bloch's "How to Design a Good API and Why It Matters" elevates this to a maxim: APIs should be *self-documenting* such that "it should rarely require documentation to read code written to a good API… in fact, it should rarely require documentation to write it" ([Bloch, OOPSLA 2006](https://dl.acm.org/doi/pdf/10.1145/1176617.1176622), [InfoQ: Bumper-Sticker API Design](https://www.infoq.com/articles/API-Design-Joshua-Bloch/)). Bloch's corollaries — "easy to use and hard to misuse," "principle of least astonishment," "don't make the client do anything the library could do" — are documentation-design principles disguised as API-design principles, because the API *is* the documentation surface.

TypeScript, Rust, Pydantic, and Go's type systems all amplify this effect by surfacing parameter names, return shapes, and JSDoc/TSDoc prose at the cursor inside the IDE — meaning a developer's first lookup is hover-text, not a browser tab ([Total TypeScript: IDE Superpowers](https://www.totaltypescript.com/books/total-typescript-essentials/ide-superpowers)). The discoverability mechanism this enables — auto-completion — turns the type system into a guided menu of valid next moves. The DX implication is that JSDoc/TSDoc comments on public types are not redundant with website reference: they are the *primary* reference for most reads, with the website serving the long-tail and Diátaxis tutorial/explanation modes that don't fit at the cursor.

**Sources:** [Bloch, "How to Design a Good API and Why It Matters" (OOPSLA 2006)](https://dl.acm.org/doi/pdf/10.1145/1176617.1176622), [InfoQ: Bumper-Sticker API Design](https://www.infoq.com/articles/API-Design-Joshua-Bloch/), [Total TypeScript: IDE Superpowers](https://www.totaltypescript.com/books/total-typescript-essentials/ide-superpowers)
**Confidence:** H

#### Tutorials, cookbooks, and recipes

Cookbooks and recipes sit between Diátaxis tutorials (learning) and how-to guides (task completion): they are task-shaped but pedagogical, structured around problems a developer is likely to actually have rather than around the surface area of the API. Twilio's tutorial library — "build a 2FA flow," "send an appointment reminder," "transcribe a phone call" — is the archetype, and the structural choice is deliberate: tasks are named in the customer's vocabulary ("2FA," "reminder") rather than the API's vocabulary (`POST /Messages`, `Verify v2`) ([Twilio Tutorials](https://www.twilio.com/docs/tutorials)).

Anthropic's and OpenAI's "use cases" / "cookbook" surfaces follow the same pattern, organizing examples by the developer's *intent* (summarization, extraction, classification, agentic loops) rather than by API method. The line between cookbook and tutorial in Diátaxis terms is whether the reader is expected to be a beginner: cookbooks assume working familiarity and optimize for "I have this problem now"; tutorials assume novice status and optimize for "I want to understand the system." Both serve developer search behavior — developers Google for the task ("send 2FA SMS Node.js"), not for the method — so cookbook URLs and headings should be task-named for SEO and intent matching as much as for pedagogy.

**Sources:** [Twilio Tutorials](https://www.twilio.com/docs/tutorials), [Diátaxis](https://diataxis.fr/)
**Confidence:** M

#### Changelogs as developer docs

The "I just upgraded — what broke?" path is a first-class documentation surface and is owned by the changelog. The [Keep a Changelog](https://keepachangelog.com/) specification — versioned sections newest-first, grouped under `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`, paired with SemVer — has become the de facto contract for human-readable change history, precisely because it makes the upgrade-impact question scannable in seconds. SemVer's MAJOR/MINOR/PATCH signaling is the load-bearing companion: a developer reading `2.4.1 → 2.4.2` knows the changelog should contain only fixes; `2.4.1 → 3.0.0` signals that a migration guide is required.

For major versions, dedicated migration guides — Next.js's codemods, React's deprecation cycles, Stripe's API version pinning — convert breaking changes from incidents into planned work. Deprecation copy itself is documentation: a good deprecation warning names the replacement API, the version where removal will happen, and a doc link, in the same shape as a Stripe error. The practitioner standard that has emerged: deprecate first, warn loudly, remove only on a major version boundary, and never silently change behavior inside a patch release.

**Sources:** [Keep a Changelog](https://keepachangelog.com/), [SemVer 2.0.0](https://semver.org/)
**Confidence:** H

#### Search and findability

Algolia DocSearch has become the de facto search layer for developer documentation, crawling sites like React, Tailwind, TypeScript, Twilio, Homebrew, and Chromium Developers and serving sub-20ms results with a dropdown UI that has itself become a visual convention ([Algolia DocSearch](https://docsearch.algolia.com/), [DocSearch GitHub](https://github.com/algolia/docsearch)). Its importance to DX is structural: developer search queries are *intent-shaped* ("how do I X," "why does X error happen") rather than *keyword-shaped*, and a fuzzy, typo-tolerant, synonym-aware index outperforms literal-string search by a wide margin on this traffic. DocSearch v4 added an Ask-AI conversational layer over the same index, reflecting the shift toward natural-language doc queries.

The DX implication is that headings and page titles should be written for search intent — task-named, verb-first ("Send an SMS," not "SMS messages") — because they are the primary signal for both Algolia's ranker and the equivalent ranker inside an LLM-backed search box. Findability is also a function of stable URLs: changing a doc URL silently breaks every external link, Stack Overflow answer, and bookmarked Slack message that pointed at it.

**Sources:** [Algolia DocSearch](https://docsearch.algolia.com/), [DocSearch GitHub](https://github.com/algolia/docsearch)
**Confidence:** H

#### Doc taxonomies that scale (versioning, IA)

Single-page-app docs work for small, stable surfaces (one library, one CLI); multi-page IA becomes mandatory once content grows beyond what a sidebar can hold without scroll-fatigue, and especially once multiple products, SDKs, or versions coexist. Versioned URLs are the load-bearing primitive: if `/docs/v2/auth` and `/docs/v3/auth` are distinct URLs, search engines and AI crawlers can disambiguate; if version is a cookie or a dropdown state, they cannot, and users land on stale pages from Google with no indication they are off-version. Stripe's API version pinning (each request carries an `Stripe-Version` header) and the matching doc-version selector is the practitioner gold standard for this problem.

A second IA pattern is the **status banner**: every doc page surfaces its applicable version, deprecation status, and last-updated date in the page chrome so that a developer arriving from a search result can instantly assess whether the page is canonical. Without this, search results actively mislead, and the doc site develops the same trust problem as a Stack Overflow answer from 2014. (inferred from converging practice across Stripe, AWS, and Cloudflare docs; not from a single citable spec)

**Sources:** [Stripe API Versioning](https://docs.stripe.com/api/versioning)
**Confidence:** M

#### Examples ecosystem (separate repos, sandboxes, hosted notebooks)

A docs site can show snippets; an examples ecosystem lets a developer fork and run a working application. Vercel's [`vercel/examples`](https://github.com/vercel/examples) repository and the curated `next.js/examples` directory model the pattern: each example is an independently deployable project, named for the integration or feature it demonstrates (e.g. `with-typescript`, `with-tailwindcss`), and every example has both a one-click deploy button and a one-click "open in StackBlitz / CodeSandbox" link ([Vercel Templates](https://vercel.com/templates), [Next.js with-typescript on StackBlitz](https://stackblitz.com/github/vercel/next.js/tree/canary/examples/with-typescript)).

The DX gain from runnable sandboxes is that they collapse the install step entirely — a developer can evaluate the framework inside a browser tab in seconds, with no local Node version, no package manager, no environment drift. The trade-off is that sandboxes lie about production characteristics (cold starts, native bindings, environment variables), so the pattern works best for evaluation-time examples; production-shape examples belong in a Git-cloneable repo with a real `package.json` and CI. The convergent industry move is to offer both: an in-page sandbox for evaluation and a deployable template for adoption.

**Sources:** [vercel/examples](https://github.com/vercel/examples), [Vercel Templates](https://vercel.com/templates), [Next.js with-typescript on StackBlitz](https://stackblitz.com/github/vercel/next.js/tree/canary/examples/with-typescript)
**Confidence:** H

### 4.3 UX (end-user experience) documentation patterns

#### Diátaxis modes applied to end-user docs

End-user help content benefits from the same four-mode taxonomy that has become canonical for developer docs. [Diátaxis](https://diataxis.fr/) splits documentation into tutorials (guided learning), how-to guides (task recipes for the competent user), reference (factual lookup), and explanation (context and "why"). For end-user help, those modes map onto familiar artifacts: onboarding tutorials and first-run experiences are *tutorials*; task-based help-center articles ("How to invite a teammate") are *how-tos*; keyboard-shortcut tables, settings glossaries, and feature catalogs are *reference*; and "About permissions" or "How billing works" pages are *explanation*. The framework's authors emphasize that [confusion most often arises when modes are blurred](https://diataxis.fr/) — e.g., a "Getting started" article that tries to teach, list every option, and explain the concept simultaneously. Help-center editors who explicitly tag articles by Diátaxis mode tend to surface gaps (most teams over-produce how-tos and under-produce explanation).

The mapping is not perfect. End users rarely consult reference for its own sake; they fall into it from search. FAQs, the traditional help-center genre, are a hybrid — usually how-to or explanation forced into Q&A shape. Treating an FAQ as a third-class artifact (rewriteable into Diátaxis modes as the topic matures) is a common content-design move at organizations like [GOV.UK content design](https://www.gov.uk/guidance/content-design), which builds around explicit user-need statements rather than legacy doc genres.
**Sources:** [Diátaxis](https://diataxis.fr/), [GOV.UK content design](https://www.gov.uk/guidance/content-design/what-is-content-design)
**Confidence:** H

#### In-product vs out-of-product help — "help in the moment of need"

The dominant principle in modern help design is that assistance should arrive where and when the user needs it, not in a separate destination. NN/g's work on [contextual help and "pull revelations"](https://www.nngroup.com/articles/help-and-documentation/) — tips surfaced when the user is already engaged with the relevant control — outperforms "push revelations" like forced onboarding modals, because pull-style help "provides timely information to help users accomplish a task" and is harder to ignore than interruptive prompts. Practitioner writing converges on the same point: users typically [will not switch context to a manual when they hit trouble](https://pronovix.com/blog/overview-context-sensitive-and-embedded-help-formats); the cognitive cost of leaving the app, opening a help center, formulating a search, and re-orienting is high enough that most users abandon instead.

This produces a layered model in practice. Inline labels, field hints, and well-named buttons carry the first layer; tooltips and popovers carry the second; in-app help widgets (Intercom, Pendo, Beacon) carry the third; and the external help center is the last-resort destination, optimized for search-engine discovery and ticket deflection. The boundary is not arbitrary: critical information must live on the page itself, because [tooltips and contextual overlays are easily missed](https://www.nngroup.com/articles/tooltip-guidelines/) and any task that *requires* finding hidden help is, by definition, broken.
**Sources:** [NN/g — Help and Documentation](https://www.nngroup.com/articles/help-and-documentation/), [NN/g — Tooltip Guidelines](https://www.nngroup.com/articles/tooltip-guidelines/), [Pronovix — Context-sensitive and embedded help](https://pronovix.com/blog/overview-context-sensitive-and-embedded-help-formats)
**Confidence:** H

#### Onboarding patterns — tours, empty states, progressive disclosure, "show me how"

Effective onboarding is not a one-shot tutorial but a structured sequence of in-product affordances that respect [progressive disclosure](https://www.nngroup.com/articles/progressive-disclosure/) — the Nielsen-coined principle that advanced or rarely used options should be deferred to secondary screens, so users see "only a few of the most important options initially." Progressive disclosure is the structural basis on which tours, empty states, and "show me how" affordances rest; without it, every onboarding surface tries to teach everything and teaches nothing.

The dominant frame in product-led growth literature treats onboarding as a funnel from sign-up to a defined "first key action" or [aha moment](https://amplitude.com/blog/aha-moment) — the user's first realization that the product solves their problem. Reforge's three-step Setup → Aha → Habit model is the canonical decomposition; [Amplitude reports a 25% activation lift correlating to ~34% revenue growth](https://amplitude.com/blog/aha-moment), which is the empirical bar most product teams aim at. Help and microcopy contribute by shortening time-to-value: empty-state CTAs that walk users into the first action, "show me how" links that scope a guided micro-tour to one feature, and persistent inline hints for steps that consistently appear in funnel drop-off data. Don Norman's foundational point about signifiers vs. affordances — that interfaces must visibly advertise what users can do — sits behind all of this; an empty state without a primary action is a signifier failure.
**Sources:** [NN/g — Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/), [Amplitude — Aha Moment](https://amplitude.com/blog/aha-moment), [Amplitude — Time to Value](https://amplitude.com/blog/time-to-value-drives-user-retention)
**Confidence:** H

#### Microcopy and UX writing

[Kinneret Yifrah's *Microcopy: The Complete Guide*](https://www.amazon.com/Microcopy-Complete-Guide-Kinneret-Yifrah/dp/B07N1RD7W6) is the closest thing to a canonical reference: it covers brand voice and tone, button labels, error messages, success messages, empty states, sign-up forms, and conversational microcopy as one integrated craft. Yifrah's central argument is that microcopy is not decoration — it is where most usability friction is actually resolved or created, because users read the labels at the moment of decision rather than the docs.

[Mailchimp's *Voice and Tone* guide](https://styleguide.mailchimp.com/voice-and-tone/) is the most-copied public exemplar. Its load-bearing distinction — *voice* is constant, *tone* shifts by context and emotional state — is now a de facto standard in content-design org charts. Mailchimp's core writing rules (plainspoken, active voice, positive language, avoid jargon, "clarity above all" beats entertainment) align with broader UX-writing consensus: button labels should be [verbs describing the outcome, not generic "OK"](https://www.nngroup.com/articles/ui-copy/) ("Save draft", "Delete folder"), so users can scan the action without parsing surrounding context. The "stranger test" — would someone who has never seen this product know what this button does, what just happened, and what to do next? — is widely used in critique sessions; it is folkloric in UX writing circles rather than tied to a single canonical source, but it operationalizes Krug's [first law: "Don't make me think"](https://www.amazon.com/Dont-Make-Think-Revisited-Usability/dp/0321965515).
**Sources:** [Yifrah — Microcopy: The Complete Guide](https://www.amazon.com/Microcopy-Complete-Guide-Kinneret-Yifrah/dp/B07N1RD7W6), [Mailchimp Content Style Guide — Voice and Tone](https://styleguide.mailchimp.com/voice-and-tone/), [NN/g — UI Copy](https://www.nngroup.com/articles/ui-copy/), [Krug — Don't Make Me Think](https://www.amazon.com/Dont-Make-Think-Revisited-Usability/dp/0321965515)
**Confidence:** H

#### Error messages as UX docs

Nielsen's [usability heuristic #9](https://www.nngroup.com/articles/ten-usability-heuristics/) — "help users recognize, diagnose, and recover from errors" — is the canonical reference: error messages must use plain language (no error codes), precisely identify the problem, and constructively suggest a solution, paired with heuristic #5 (prevent the error in the first place). The companion piece, NN/g's [Hostile Patterns in Error Messages](https://www.nngroup.com/articles/hostile-error-messages/), documents the failure modes: premature errors that fire while the user is still typing, aggressive red/warning styling reused for non-errors, and blame-language ("invalid," "illegal," "incorrect") that escalates instead of guides. NN/g's specific timing guidance — [inline validation should appear ~500ms after the user stops typing](https://www.uxpin.com/studio/blog/error-feedback-best-practices-mobile-forms/), and field-level errors should be placed adjacent to the field, not aggregated in a global banner — is widely cited as the operational floor.

End-user error copy diverges from developer error copy in audience model. A developer-facing error is a debugging artifact: the reader can read a stack trace, look up an HTTP code, and inspect a payload, so density of technical detail is a feature. An end-user error is a *recovery instruction*: the reader cannot inspect anything, so the copy must answer "what happened, in your terms" and "what should I do now, here, with one click." This is why "We couldn't reach the server. Try again in a moment, or [check status]." outperforms "Error 503: Service Unavailable" for end users, even though both describe the same fact. The pattern recurs across every modern style guide: [Mailchimp](https://styleguide.mailchimp.com/voice-and-tone/), [Yifrah](https://www.amazon.com/Microcopy-Complete-Guide-Kinneret-Yifrah/dp/B07N1RD7W6), and [GOV.UK](https://www.gov.uk/guidance/content-design/writing-for-gov-uk) all converge on "describe the cause + give the next step + don't blame the user."
**Sources:** [NN/g — 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), [NN/g — Hostile Error Messages](https://www.nngroup.com/articles/hostile-error-messages/), [UXPin — Error Feedback Best Practices](https://www.uxpin.com/studio/blog/error-feedback-best-practices-mobile-forms/)
**Confidence:** H

#### Empty states as teaching surfaces

[NN/g's empty-state research](https://www.nngroup.com/articles/empty-state-interface-design/) names three concrete jobs for a well-designed empty state: communicate system status (is this empty because nothing exists yet, because a filter is hiding everything, or because something failed?), provide learning cues that double as in-context tutorials, and offer a direct pathway to the first key action. NN/g explicitly frames empty states as "pull revelations" — contextual teaching that arrives when the user has already engaged the surface — and notes that "in-context help can often be applied right away and is thus more memorable" than forced tutorials. The empty state is therefore one of the highest-leverage onboarding surfaces in the product, despite being almost always under-invested.

Slack, Linear, and Notion are the commonly cited exemplars. Slack's empty channel-search state gives two scoped recovery paths (refine the search; open the channel directory); Linear's filtered-to-zero states keep the filter chips visible and removable; Notion's blank documents prompt with templates. The pattern these share: the empty state is not blank — it is the first-run state of the feature, designed as docs.
**Sources:** [NN/g — Designing Empty States](https://www.nngroup.com/articles/empty-state-interface-design/), [Carbon Design System — Empty States](https://carbondesignsystem.com/patterns/empty-states-pattern/)
**Confidence:** H

#### Tooltips, walkthroughs, and the modal-carousel failure mode

Tooltips are the highest-density help surface and the most-abused one. [NN/g's tooltip guidelines](https://www.nngroup.com/articles/tooltip-guidelines/) list the failure modes: hiding essential information behind hover (excluding touch and keyboard users), inconsistent coverage (some icons have tooltips, some don't, so users learn to stop hunting), redundant content that duplicates a visible label, and poor positioning that obscures the element being explained. The principle NN/g states bluntly: "important information should always be on the page." Tooltips are for *supplementary* context — unfamiliar icons, unusual form fields, optional clarifications.

The related failure mode is the **modal-carousel walkthrough**: a forced sequence of slide-style overlays at first login. Practitioner data converges on the same finding — passive tours where users [click "Next" through 5+ modals correlate with low feature adoption](https://www.appcues.com/blog/build-effective-product-tours), because nothing was actually performed and nothing was retained. The empirically stronger pattern is the **interactive walkthrough**: users complete one real task with inline guidance, then dismiss. Userpilot reports [contextually tailored in-app tours roughly double completion rates](https://userpilot.com/blog/product-tour-examples/) versus generic ones. The actionable rule: never use a modal carousel for anything users actually need to learn; reserve them for one-time announcements.
**Sources:** [NN/g — Tooltip Guidelines](https://www.nngroup.com/articles/tooltip-guidelines/), [Appcues — Effective Product Tours](https://www.appcues.com/blog/build-effective-product-tours), [Userpilot — Product Tour Examples](https://userpilot.com/blog/product-tour-examples/)
**Confidence:** H

#### Help center IA, search, and deflection

Help centers serve two distinct populations with conflicting needs: urgent problem-solvers who arrive via search (often from Google, not the help center home page) and exploratory browsers learning a feature for the first time. NN/g's heuristic-10 guidance is to support both: [strong search for urgent lookup, plus a clean category structure for browsers](https://www.nngroup.com/articles/help-and-documentation/). In practice most modern help centers (Intercom, Zendesk, Help Scout) are search-first by traffic — the home page is a search bar with categories beneath as a fallback — because Google routes the bulk of arrivals directly to articles, and the on-site browse path is mostly used by readers who have already failed to find what they wanted.

The dominant success metric is **deflection rate**: the fraction of help-seeking sessions that resolve without opening a support ticket. [Industry benchmarks](https://www.eesel.ai/blog/deflection-rate-what-is-it-and-how-to-improve-it) sit around 20–30% for well-tuned knowledge bases; [Zendesk's reporting tooling](https://support.zendesk.com/hc/en-us/articles/4408832867226-Reporting-tools-for-measuring-self-service) tracks self-service ratios as a primary KPI. Deflection optimization is a content-strategy discipline, not just an IA one: surfacing the top-searched terms with no results (or with low article-rating scores) directly identifies the content gaps that produce tickets. This is why mature support orgs treat the help center as a product surface with its own funnel, not as a documentation dumping ground.
**Sources:** [NN/g — Help and Documentation](https://www.nngroup.com/articles/help-and-documentation/), [eesel AI — Deflection Rate](https://www.eesel.ai/blog/deflection-rate-what-is-it-and-how-to-improve-it), [Zendesk — Reporting for Self-Service](https://support.zendesk.com/hc/en-us/articles/4408832867226-Reporting-tools-for-measuring-self-service)
**Confidence:** M

#### Plain language for end users

The institutional reference is the [Plain Writing Act of 2010](https://www.justice.gov/open/plain-writing-act) and the federal [plainlanguage.gov](https://plainlanguage.gov/guidelines/) guidelines, which require federal agencies to write public-facing content the audience can use on first read. The operational rules are concrete: average sentence length 15–20 words, common everyday words over jargon, active voice, personal pronouns, and "you" for the reader. [GOV.UK targets a reading age of 9](https://www.gov.uk/guidance/content-design/writing-for-gov-uk) for all public content, on the grounds that lower reading ages do not insult skilled readers but higher ages exclude unskilled ones — a one-way ratchet. [18F's content guide](https://guides.18f.gov/content-guide/our-approach/plain-language/) operationalizes the same principle for digital services with concrete word swaps ("buy" not "purchase," "help" not "assist").

For consumer products, the typical target is US 6th–8th grade reading level, measurable via Flesch–Kincaid or similar. Cultural and internationalization considerations matter: idioms, figurative language, and US-centric cultural references break translation and exclude non-native readers, so [UX writing that anticipates localization](https://uxcontent.com/what-is-localization-for-ux/) prefers literal phrasing, avoids puns, and leaves room for text expansion (German strings often run 30%+ longer than English).
**Sources:** [plainlanguage.gov — Guidelines](https://plainlanguage.gov/guidelines/), [DOJ — Plain Writing Act](https://www.justice.gov/open/plain-writing-act), [GOV.UK — Writing for GOV.UK](https://www.gov.uk/guidance/content-design/writing-for-gov-uk), [18F Content Guide — Plain Language](https://guides.18f.gov/content-guide/our-approach/plain-language/)
**Confidence:** H

#### Accessibility for help content

Help content has to meet the same [WCAG 2.2 bar](https://www.w3.org/TR/WCAG22/) as the product it documents, and often fails to. The load-bearing success criteria for help articles are: SC 1.1.1 alt text for every screenshot (describing the action being demonstrated, not just "screenshot"), SC 1.2.2 captions on every prerecorded video and SC 1.2.3/1.2.5 audio description or full transcript, semantic heading hierarchy for screen-reader navigation, keyboard operability for any interactive demo, and adequate color contrast for callout annotations. [Penn State's WCAG 2.2 checklist](https://accessibility.psu.edu/guidelines/wcaglist/) and [Document360's WCAG writing guide](https://document360.com/blog/wcag-accessibility-best-practices/) are practical operational references.

A frequent help-center anti-pattern: screencasts with no transcript and no captions, often shipped with marketing-style auto-generated captions that are technically present but unusable. Screen-reader users navigating a help article need the *structure* (descriptive headings, lists, link text that makes sense out of context — never "click here") more than visual users do, because they scan via heading and link rotors rather than visual hierarchy.
**Sources:** [W3C — WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Penn State — WCAG 2.2 Guidelines](https://accessibility.psu.edu/guidelines/wcaglist/), [Document360 — WCAG Accessibility Best Practices](https://document360.com/blog/wcag-accessibility-best-practices/)
**Confidence:** H

#### Help content and feedback loops — "doc team as product team"

Modern help-center platforms (Zendesk, Intercom, HubSpot, KnowledgeOwl) all ship "Was this helpful?" widgets and per-article ratings as a default. The signal is noisy at the article level — most readers don't vote, and "no" votes skew toward already-frustrated users — but at scale it surfaces the right thing: which articles consistently fail to resolve the question they appear for. The richer signal comes from joining article analytics with support-ticket data: which tickets opened *after* the user viewed a specific article (the article did not resolve them), and which top-searched terms return zero or poorly rated results (the content gap). [Aha! and similar product-management write-ups](https://www.aha.io/blog/improve-your-product-knowledge-base-with-user-feedback) treat the knowledge base as a backlog source: support tickets are unfunded help articles waiting to be written.

This is the operational basis for the "doc team as product team" framing now common in mature SaaS orgs: documentation reports against deflection rate, time-to-resolution, and activation-funnel metrics, with the same instrumentation rigor as the product surfaces it documents. It also closes the loop with onboarding-funnel analytics — articles that consistently appear in the path between sign-up and first key action become candidates for promotion into in-product help (tooltips, empty states, contextual sidebars) rather than living only in the help center.
**Sources:** [Aha! — Improve Your Knowledge Base With Feedback](https://www.aha.io/blog/improve-your-product-knowledge-base-with-user-feedback), [Zendesk — Reporting for Self-Service](https://support.zendesk.com/hc/en-us/articles/4408832867226-Reporting-tools-for-measuring-self-service), [Amplitude — Activation Rate](https://amplitude.com/explore/digital-analytics/what-is-activation-rate)
**Confidence:** M

#### Onboarding as a measurable funnel

The dominant frame across [Reforge](https://amplitude.com/blog/aha-moment), Amplitude, and Pendo writing is that onboarding is an instrumented funnel from sign-up to a defined activation event (the "first key action" or "aha moment"), with help and microcopy as the primary intervention surfaces between steps. [Amplitude's activation-rate definition](https://amplitude.com/explore/digital-analytics/what-is-activation-rate) and [time-to-value framing](https://amplitude.com/blog/time-to-value-drives-user-retention) operationalize the idea: define one or two events that correlate strongly with day-7 or day-30 retention, measure conversion from sign-up to those events by cohort, and treat any step with abnormal drop-off as a help-and-microcopy bug first, a UX-flow bug second.

This reframes help content as an activation lever rather than a deflection-only cost center. Articles that consistently appear in the activation path become candidates for inlining (move from help center → in-product tooltip → progressive-disclosure surface). Empty states become the highest-leverage docs surface because they sit on the critical path to first action. Microcopy on the empty state, the "first object created" success message, and the second-session re-engagement prompt collectively move activation more than any single help-center rewrite. [Reforge's 25% activation lift → 34% revenue claim](https://amplitude.com/blog/aha-moment) is the most-cited number for funding doc-team investment in this surface (inferred from secondary reporting of Reforge's framework — original Reforge content is paywalled).
**Sources:** [Amplitude — Activation Rate](https://amplitude.com/explore/digital-analytics/what-is-activation-rate), [Amplitude — Aha Moment](https://amplitude.com/blog/aha-moment), [Amplitude — Time to Value](https://amplitude.com/blog/time-to-value-drives-user-retention)
**Confidence:** M

### 4.4 AX (agent experience) documentation patterns

AX — Agent Experience — is the discipline of designing surfaces (APIs, docs, CLIs, errors, schemas, repo-level context files) so that LLM-based agents can find, parse, and act on them reliably without a human in the loop. The framing was coined by Mathias Biilmann of Netlify on 28 January 2025 and traces a progression: UX (≈1993, human-system interaction), DX (≈2011, developer-platform integration), AX (2025–, agents as a first-class user persona) ([Biilmann, "Introducing AX," Jan 2025](https://biilmann.blog/articles/introducing-ax/); [Netlify, "Agent Experience"](https://www.netlify.com/agent-experience/)). The discipline is young, the literature is mostly vendor-primary, and the evidence base is thin enough that several patterns below are marked M or L. But the shape is clear: documentation for agents is a load-bearing product surface, not a marketing afterthought, and the patterns that work for it are largely orthogonal — sometimes outright opposed — to the patterns that delight human readers.

#### Bucket A — Machine-readable documentation contracts

##### llms.txt and /llms-full.txt

The `/llms.txt` proposal was published by Jeremy Howard of Answer.AI on 3 September 2024 as a way for site authors to give LLMs a curated, markdown-formatted index of their site's most important content at inference time ([Howard, "/llms.txt — a proposal," Answer.AI, Sept 2024](https://www.answer.ai/posts/2024-09-03-llmstxt.html); [llmstxt.org spec](https://llmstxt.org/)). The file format is intentionally minimal: an H1 project title (required), an optional blockquote summary, freeform markdown body, and H2-delimited sections containing curated link lists. A companion convention asks sites to publish a `.md` variant of every page at the same URL with `.md` appended. Howard's stated motivation: "context windows are too small to handle most websites in their entirety," so site authors — not the LLM — should pick what matters. The spec explicitly distinguishes itself from `robots.txt` (which governs *access* for crawlers) and `sitemap.xml` (which enumerates *all* pages, often blowing out context windows).

Two derived files dominate practice. `/llms-full.txt`, co-developed by Mintlify and Anthropic, concatenates the entire documentation set into a single markdown file suitable for direct ingestion ([Mintlify, "Simplifying docs for AI with /llms.txt"](https://www.mintlify.com/blog/simplifying-docs-with-llms-txt)). `/llms-ctx.txt` and `/llms-ctx-full.txt` are generated artifacts that expand the `llms.txt` link list with XML-structured fetched content for direct paste into Claude. Adoption was niche until November 2024, when Mintlify enabled `/llms.txt` and `/llms-full.txt` automatically across every docs site it hosts — overnight, Anthropic, Cursor, Pinecone, Coinbase, and Windsurf began serving the format ([Mintlify on X, Nov 2024](https://x.com/mintlify/status/1859281309878845708); [Mintlify llms.txt docs](https://www.mintlify.com/docs/ai/llmstxt)). Cloudflare went further and publishes per-product `llms-full.txt` files (their site-wide bundle exceeds 3.7 million tokens) so agents can fetch only the slice they need ([Cloudflare developer docs, llms.txt](https://developers.cloudflare.com/llms.txt); [Cloudflare ai-search llms.txt](https://developers.cloudflare.com/ai-search/llms.txt)). Vercel proposed an inline variant on 20 August 2025: `<script type="text/llms.txt">` tags embedded directly in HTML, deployed first on Vercel's default 401 page so an agent encountering an auth wall gets machine-readable instructions on what to do next ([Ubl/Vercel, "A proposal for inline LLM instructions in HTML"](https://vercel.com/blog/a-proposal-for-inline-llm-instructions-in-html)).

The honest caveat: no major LLM provider has formally committed to consuming `/llms.txt` at inference time. The standard has succeeded as a *publishing convention* — agents and tools fetch it deliberately — more than as a *crawled standard* in the robots.txt sense. Treat it as a docs-delivery contract for the agents you can prompt to fetch it, not as a passive SEO surface.

**Sources:** [llmstxt.org](https://llmstxt.org/), [Answer.AI proposal](https://www.answer.ai/posts/2024-09-03-llmstxt.html), [Mintlify blog](https://www.mintlify.com/blog/simplifying-docs-with-llms-txt), [Cloudflare llms.txt](https://developers.cloudflare.com/llms.txt), [Vercel inline-llms proposal](https://vercel.com/blog/a-proposal-for-inline-llm-instructions-in-html)
**Confidence:** H

##### OpenAPI, MCP, and GraphQL schemas as documentation

For agents, a well-maintained OpenAPI 3.1 spec is often a more valuable artifact than the human-readable reference docs around it. OpenAPI 3.1 (Feb 2021) is fully aligned with JSON Schema 2020-12, supports a multi-example `examples` array, and lets CommonMark-rich `description` fields carry the natural-language signal that LLMs use to pick endpoints and construct calls ([OpenAPI Spec v3.1.0](https://spec.openapis.org/oas/v3.1.0.html)). Frameworks like Semantic Kernel, LangChain, the Google Agent Development Kit, and OpenAI's Agents SDK consume OpenAPI documents directly and lower each operation into a callable tool, with the `description` field driving function-calling routing ([Google ADK OpenAPI tools docs](https://google.github.io/adk-docs/tools-custom/openapi-tools/); [Microsoft Semantic Kernel OpenAPI plugins](https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/adding-openapi-plugins)). Speakeasy is explicit: "the best SDK for an agent is often the API documentation itself" — a precise OpenAPI document beats a wrapper SDK because it gives agents direct, structured access ([Speakeasy, "Designing agent experience"](https://www.speakeasy.com/blog/agent-experience-introduction)).

The Model Context Protocol (MCP), released by Anthropic in late 2024 and now under the Linux Foundation's Agentic AI Foundation, formalises tool descriptions as a first-class documentation surface. An MCP server exposes tools, each with a `name`, `description`, and JSON-Schema-typed input schema, and the description is what the model reads to decide whether and how to call the tool ([Model Context Protocol intro](https://modelcontextprotocol.io/docs/getting-started/intro); [MCP spec on GitHub](https://github.com/modelcontextprotocol/modelcontextprotocol)). Quality matters: Hasan et al. ("MCP Tool Descriptions Are Smelly!", arXiv:2602.14878, Feb 2026) analysed 856 tools across 103 MCP servers and found **97.1% contained at least one description "smell," 56% failed to state their purpose clearly**, and augmenting descriptions with their six-component rubric improved task success by a median of 5.85 percentage points and partial-goal completion by 15.12% — but also raised execution steps by 67.46% and regressed performance in 16.67% of cases ([Hasan et al., arXiv:2602.14878](https://arxiv.org/abs/2602.14878)). The takeaway is non-trivial: tool descriptions are documentation, descriptions improve agent behaviour, but more is not always better — they need to be *targeted*.

GraphQL plays a similar role through SDL descriptions and introspection: agents can walk the schema, read per-field descriptions, and assemble queries without trial-and-error probing. The pattern is the same — schema-as-docs, where the description fields are the primary product surface for the agent — and the failure mode is identical: schemas with empty or marketing-style descriptions reduce agent reliability.

**Sources:** [OpenAPI 3.1 spec](https://spec.openapis.org/oas/v3.1.0.html), [MCP intro](https://modelcontextprotocol.io/docs/getting-started/intro), [MCP spec repo](https://github.com/modelcontextprotocol/modelcontextprotocol), [Hasan et al. 2602.14878](https://arxiv.org/abs/2602.14878), [Speakeasy AX guide](https://www.speakeasy.com/blog/agent-experience-introduction), [Google ADK OpenAPI tools](https://google.github.io/adk-docs/tools-custom/openapi-tools/)
**Confidence:** H

##### Structured data and JSON-LD in docs sites

Schema.org markup embedded via JSON-LD script tags gives retrievers and agents an explicit semantic layer over a docs site: entity types (`Article`, `HowTo`, `FAQPage`, `TechArticle`), `@id` references that link entities into a knowledge graph, and properties like `knowsAbout` that disambiguate organizational and topical scope ([schema.org](https://schema.org/), survey via [SEO Strategy JSON-LD guide](https://www.seostrategy.co.uk/schema-structured-data/json-ld-guide/)). For RAG and AI Overview systems, this is the same disambiguation signal a sitemap gives a search crawler, but with explicit type semantics. The pattern of greatest current relevance to AX is `FAQPage` markup, which serves question-answer pairs in exactly the shape LLMs generate, and `HowTo`, which exposes ordered steps that an agent can lift directly. (M: this is established for SEO; the AX adoption story is more recent and largely vendor-asserted.)

**Sources:** [schema.org](https://schema.org/), [JSON-LD SEO guide](https://www.seostrategy.co.uk/schema-structured-data/json-ld-guide/), [Structured Linked Data for agent retrieval, arXiv:2603.10700](https://arxiv.org/pdf/2603.10700)
**Confidence:** M

##### Docs-as-data via APIs

Several documentation platforms now expose docs themselves as queryable APIs. ReadMe.io publishes its docs index at `https://docs.readme.com/llms.txt` and exposes a write-API so agents can update documentation pages programmatically from Claude Code, Cursor, or CI ([ReadMe API reference](https://docs.readme.com/main/reference/intro-to-the-readme-api)). The Notion API exposes pages and databases as schema-aware data sources that can be wired to agents as knowledge bases ([Notion API overview](https://developers.notion.com/)). The pattern matters because it changes docs from a render target into a *queryable substrate*: an agent can search, fetch, and (with the right tokens) write — closing the loop from observation to documentation update without a human edit.

**Sources:** [ReadMe API](https://docs.readme.com/main/reference/intro-to-the-readme-api), [Notion API](https://developers.notion.com/)
**Confidence:** M

#### Bucket B — Documentation written for coding agents

##### AGENTS.md as the converging multi-harness standard

`AGENTS.md` started as an OpenAI Codex convention in August 2025 and has converged into the closest thing the coding-agent ecosystem has to a cross-tool standard. By December 2025 it was placed under the Linux Foundation's Agentic AI Foundation (alongside MCP and Block's Goose) with backing from OpenAI, Anthropic, Google, AWS, Bloomberg, and Cloudflare ([agents.md](https://agents.md/)). Native readers now include OpenAI Codex, GitHub Copilot (coding agent), Cursor, Windsurf, Devin, Amp, Jules, Gemini CLI, Aider, Zed, Warp, JetBrains Junie, and ~15 other harnesses; the agents.md site claims **over 60,000 open-source repositories** carry one ([agents.md](https://agents.md/)). The spec is deliberately minimal — standard Markdown, no required fields — but conventional sections include project overview, build/test commands, code-style rules, testing instructions, security considerations, commit/PR conventions, and deployment steps.

Because per-harness conventions persisted (Claude Code reads `CLAUDE.md`, Copilot reads `.github/copilot-instructions.md`, Gemini reads `GEMINI.md`, Cursor reads `.cursor/rules/`, Windsurf reads `.windsurf/rules/`), the operational pattern is to **symlink them all to a single source of truth**. The canonical example is `vercel/next.js`, whose AGENTS.md opens with `"CLAUDE.md is a symlink to AGENTS.md. They are the same file."` ([vercel/next.js AGENTS.md](https://github.com/vercel/next.js/blob/canary/AGENTS.md)). `create-next-app` now generates both files automatically. The Next.js AGENTS.md itself is 312 lines covering monorepo layout, pnpm build commands, Turbopack-vs-webpack selection, test patterns, lint commands, PR conventions, and a list of specialised skills the agent should consult conditionally — a representative shape for a mature repo-level context file.

A critical counterpoint comes from Gloaguen, Mündler, Müller, Raychev, and Vechev (ETH SRI Lab / LogicStar), "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" (arXiv:2602.11988, Feb 2026) ([paper](https://arxiv.org/abs/2602.11988)). Across four agents (Claude Code with Sonnet-4.5, Codex with GPT-5.2 and GPT-5.1-mini, Qwen Code with Qwen3-30b-coder) and 438 tasks across SWE-bench Lite and a new AGENTbench, **LLM-generated AGENTS.md files reduced task success by ~2% on AGENTbench and 0.5% on SWE-bench Lite while raising inference cost by 20–23%.** Developer-written files gave only a 4% average lift and still inflated cost ~19%. The authors' interpretation: context files "encourage more exploration and testing," and that extra work hurts more than it helps. Their recommendation — **"human-written context files should describe only minimal requirements"** — directly contradicts the maximalist AGENTS.md culture and is the strongest evidence in the AX literature that AGENTS.md is a load-bearing surface where less is more.

**Sources:** [agents.md](https://agents.md/), [vercel/next.js AGENTS.md](https://github.com/vercel/next.js/blob/canary/AGENTS.md), [Gloaguen et al., arXiv:2602.11988](https://arxiv.org/abs/2602.11988), [Augment Code AGENTS.md guide](https://www.augmentcode.com/guides/how-to-build-agents-md), [Speakeasy agent skills release](https://www.speakeasy.com/blog/release-agent-skills)
**Confidence:** H

##### SKILL.md and Anthropic Agent Skills

Anthropic released Agent Skills on 16 October 2025 and they are now the canonical pattern for packaging documentation-plus-code into reusable, load-on-demand modules ([Anthropic engineering blog, Oct 2025](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills); [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)). The contract is a `SKILL.md` file with YAML frontmatter — `name` (≤64 chars, lowercase-hyphens) and `description` (≤1024 chars) — followed by markdown instructions, plus an optional folder of references, templates, and executable scripts.

The discipline of the design is **progressive disclosure** through three loading levels:

1. **Metadata (always loaded, ~100 tokens per skill):** the YAML `name` + `description` enters the system prompt at startup so the agent knows the skill exists.
2. **Instructions (loaded when the skill is triggered, <5 kB):** the SKILL.md body is read into context only when the description matches the user's task.
3. **Resources (loaded on demand, effectively unbounded):** referenced markdown files, schemas, examples, and executable scripts live on the filesystem and only enter context when needed; scripts execute via bash and their *code* never enters context, only their *output*.

This makes routing-via-description the load-bearing AX choice in the entire pattern. Anthropic's official guidance is that descriptions must include *both what the skill does and when to use it*, written in third person, and should err on the "pushy" side because models tend to undertrigger ([Anthropic skill-creator SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md); [Anthropic best-practices guide](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)). The skill-creator skill itself ships an iterative description-optimisation loop that runs queries against candidate descriptions, measures trigger rate, and improves the wording — treating the description as a tunable hyperparameter, not prose.

A useful counterweight: Vercel's Jude Gao published evaluation results on 27 January 2026 showing that for Next.js 16 APIs absent from training data, an 8 kB compressed docs index embedded in `AGENTS.md` scored **100%** vs **53%** for skills (no instruction) and **79%** for skills with explicit instructions ([Vercel, "AGENTS.md outperforms skills in our agent evals"](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)). The mechanism: AGENTS.md content sits in the system prompt every turn, removing the trigger-decision burden, while skills failed to activate in 56% of cases. The honest read: skills win on *unbounded bundled content* and *zero-idle-cost*; AGENTS.md wins on *always-available framework docs*. The patterns are complements, not competitors.

**Sources:** [Anthropic engineering blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [anthropics/skills repo](https://github.com/anthropics/skills), [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md), [Vercel AGENTS.md vs skills evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
**Confidence:** H

##### The per-harness rule-file landscape

The current landscape (May 2026) is: AGENTS.md (cross-harness), CLAUDE.md (Claude Code, usually a symlink to AGENTS.md), `.github/copilot-instructions.md` plus path-scoped `.instructions.md` files with YAML frontmatter and glob matchers (GitHub Copilot), `.cursor/rules/*.mdc` files with metadata (Cursor; legacy `.cursorrules` single file still supported), `.windsurf/rules/` directory (12,000-char limit per file, 6,000-char global; legacy `.windsurfrules` still works), GEMINI.md (Gemini CLI) ([deployhq comparison](https://www.deployhq.com/blog/ai-coding-config-files-guide); [Cursor rules vs CLAUDE.md](https://www.agentrulegen.com/guides/cursorrules-vs-claude-md)). Convergence is happening at the *content* layer — "markdown file at repo root that the AI reads first" — even where filename conventions diverge. The pragmatic AX pattern is: write content once, symlink the filenames per harness, gate the symlinks with CI.

**Sources:** [DeployHQ AI coding config guide](https://www.deployhq.com/blog/ai-coding-config-files-guide), [Agent Rules Builder comparison](https://www.agentrulegen.com/guides/cursorrules-vs-claude-md), [SSW symlink-agents-to-claude rule](https://www.ssw.com.au/rules/symlink-agents-to-claude)
**Confidence:** H

##### Documenting forbidden actions and guardrails

A growing pattern is to document "thou shalt nots" not as prose alone but as machine-enforced gates. The Claude Code PreToolUse hook receives JSON on stdin for every tool call, can inspect Bash commands argv-by-argv, and rejects with exit code 2 (whose stderr is fed back to the model as an error message) ([Claude Code hooks reference](https://code.claude.com/docs/en/hooks); [Building Guardrails for AI Coding Assistants](https://dev.to/mikelane/building-guardrails-for-ai-coding-assistants-a-pretooluse-hook-system-for-claude-code-ilj)). Cursor's `preToolUse` on `Shell`, Codex's `.codex/hooks.json`, and equivalent layers in Windsurf provide harness-specific equivalents. The AX-documentation pattern here is two-layer: a "Forbidden actions" section in AGENTS.md that *describes* the policy in natural language for the model, and a hook script that *enforces* it deterministically when the model ignores the prose — because models do ignore prose, and natural-language guardrails alone are not a control. The dwarvesf/claude-guardrails project and the mattpocock skills git-guardrails skill are representative public implementations ([dwarvesf/claude-guardrails](https://github.com/dwarvesf/claude-guardrails)).

**Sources:** [Claude Code hooks reference](https://code.claude.com/docs/en/hooks), [PreToolUse guardrails how-to](https://dev.to/mikelane/building-guardrails-for-ai-coding-assistants-a-pretooluse-hook-system-for-claude-code-ilj), [dwarvesf/claude-guardrails](https://github.com/dwarvesf/claude-guardrails)
**Confidence:** H

##### Reflection logs and evidence-driven rules

A nascent pattern — visible in this very repository and a handful of others — treats observed agent failures as the *primary evidence base* for what belongs in AGENTS.md or SKILL.md. The shape: one dated markdown entry per observed failure, with fixed frontmatter (date, harness, sub-surface, severity, status) and a `## What to do differently` section; promotion of a recurring pattern into a rule, hook, or CI gate happens only after **three or more entries describe the same gap**. The empirical justification is the Gloaguen/Mündler finding above (arXiv:2602.11988) — scaffolding context files from fewer than three observed failures produces plausible-sounding but performance-hurting boilerplate. The pattern is novel enough that no published academic source treats it directly; the closest adjacent literature is on agent failure attribution and reflective memory (Meta-Policy Reflexion, arXiv:2509.03990; PreFlect, arXiv:2602.07187; AgentRx, arXiv:2602.02475), which establish that *recording-and-reflecting on failures* is a load-bearing primitive for agent reliability, not just an editorial nicety. **(inferred — the three-entry promotion floor is a synthesis of the LogicStar finding plus practitioner convention, not a published result.)**

**Sources:** [Gloaguen et al., arXiv:2602.11988](https://arxiv.org/abs/2602.11988), [Meta-Policy Reflexion, arXiv:2509.03990](https://arxiv.org/pdf/2509.03990), [PreFlect, arXiv:2602.07187](https://arxiv.org/pdf/2602.07187)
**Confidence:** M

#### Bucket C — Documentation written to be retrieved (RAG-friendly)

##### Chunking-aware structure

RAG retrievers split documentation into chunks, embed each chunk independently, and serve back the top-k matches to the agent. This makes chunk-survivability a structural property of the docs themselves: every chunk needs to be readable in isolation. The widely cited heuristic — "a good chunk feels like a self-contained answer or idea, while a bad chunk makes you scroll up and down to understand what it's talking about" — has direct authoring implications: avoid "see above" anaphora, restate the subject of each section, define glossary terms inline or at the top of the page, and treat semantic headings (H2/H3) as chunk boundaries rather than visual decoration ([Pinecone semantic chunking notebook](https://github.com/pinecone-io/examples/blob/main/learn/generation/better-rag/02b-semantic-chunking.ipynb); [Firecrawl RAG chunking strategies](https://www.firecrawl.dev/blog/best-chunking-strategies-rag)). The same logic generalises: structure-aware splitters (LlamaIndex's SemanticSplitterNodeParser, header-based recursive splitters) lean on heading hierarchy as the primary chunk signal, so heading discipline in source documents *is* retrieval quality.

**Sources:** [Pinecone semantic chunking](https://github.com/pinecone-io/examples/blob/main/learn/generation/better-rag/02b-semantic-chunking.ipynb), [Firecrawl chunking guide](https://www.firecrawl.dev/blog/best-chunking-strategies-rag), [LlamaIndex semantic splitter discussion](https://github.com/run-llama/llama_index/issues/12007)
**Confidence:** H

##### Stable, deep-linkable anchors

RAG systems and agents both store URLs as the canonical pointer back to source. That makes anchor stability across versions a load-bearing concern. The pattern is to author every H2/H3 with a stable, hand-defined slug (not auto-generated from text, which drifts when titles are edited), include version and locale in the URL so version-specific citations don't decay, and use canonical link headers when the same content lives at multiple URLs ([VersionRAG, arXiv:2510.08109](https://arxiv.org/pdf/2510.08109); [LLM internal linking practitioner guide](https://zcmarketing.au/seo-tips/llm-internal-linking-2025/)). Cloudflare and Mintlify both expose `index.md` companion URLs at every documentation route so deep-link-plus-`.md` is a one-line transformation an agent can do without configuration ([Cloudflare markdown-for-agents](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/)).

**Sources:** [VersionRAG, arXiv:2510.08109](https://arxiv.org/pdf/2510.08109), [Cloudflare markdown-for-agents](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/), [LLM internal linking guide](https://zcmarketing.au/seo-tips/llm-internal-linking-2025/)
**Confidence:** M

##### Plain-language summaries at the top of pages

The TL;DR-at-the-top pattern serves two AX functions: it gives the retriever a high-signal chunk that summarises the whole page (useful when only that chunk is retrieved), and it gives the model a fast yes/no on whether to keep reading. Diátaxis's "explanation" mode is the closest formal analogue in the human-docs literature ([Diátaxis, Procida](https://diataxis.fr/)). For AX specifically, the pattern compounds with chunking — a self-contained TL;DR chunk is far more likely to be a useful top-k retrieval result than a "this page covers..." sentence. (M: widely advocated, comparatively few controlled evals of the effect on agent task success.)

**Sources:** [Diátaxis](https://diataxis.fr/), [Cloudflare docs-for-agents style guide](https://developers.cloudflare.com/style-guide/ai-tooling/)
**Confidence:** M

##### Embedding-friendly vocabulary and glossaries-as-bridges

Embedding-based retrieval matches on semantic similarity, which means agents find content using the words the *user* used — not necessarily the words the *product team* uses. The bridge pattern is a glossary at the top of the docs (or a dedicated glossary page) that explicitly maps user-facing terms to product-internal terms; queries embed close to the glossary, the glossary chunk gets retrieved, and the agent follows the cross-reference into the canonical content. Practitioner advice from RAG implementors is consistent: pick one term per concept and use it throughout (rename "deployment" and "release" to a single term), and processed-separately glossaries dramatically outperform inline-only definitions because definition chunks are short, high-signal, and embed well ([Observations on Building RAG Systems for Technical Documents, arXiv:2404.00657](https://arxiv.org/pdf/2404.00657); [Cloudflare style guide](https://developers.cloudflare.com/style-guide/ai-tooling/)).

**Sources:** [arXiv:2404.00657](https://arxiv.org/pdf/2404.00657), [Cloudflare docs-for-agents](https://developers.cloudflare.com/style-guide/ai-tooling/)
**Confidence:** M

##### Cross-references and link density

Agents follow links to disambiguate, so a docs site with high link density between related concepts gives the agent more opportunities to converge on the right answer than a well-organised-but-isolated one. The pattern overlaps with HATEOAS in API design — the response carries the next link — and with Schema.org `@id` references that knit entities into a graph. Practitioner advice: every concept name on the page should hyperlink to its canonical definition the *first* time it appears (and ideally every time, since chunks lose first-mention context). Nordic APIs' "HATEOAS: The API design style that was waiting for AI" makes the same argument at the API layer ([Nordic APIs, HATEOAS for AI](https://nordicapis.com/hateoas-the-api-design-style-that-was-waiting-for-ai/)).

**Sources:** [Nordic APIs HATEOAS](https://nordicapis.com/hateoas-the-api-design-style-that-was-waiting-for-ai/), [Cloudflare docs-for-agents](https://developers.cloudflare.com/style-guide/ai-tooling/)
**Confidence:** M

#### Bucket D — Documentation written to be acted on (agent-callable)

##### Stable error codes and machine-parseable error envelopes

The Stripe error envelope is the canonical AX precedent. Every error response carries `type` (one of `api_error`, `card_error`, `idempotency_error`, `invalid_request_error`), a machine-readable `code` field, a `decline_code` where applicable, a human-safe `message`, the offending `param`, a `doc_url` linking to the canonical error-code documentation, and a `request_log_url` deep-linking to the Stripe dashboard ([Stripe API Errors reference](https://docs.stripe.com/api/errors); [Stripe Error codes](https://docs.stripe.com/error-codes)). The `doc_url` pattern in particular is load-bearing for AX: an agent that hits an unfamiliar error code can fetch the URL, read the canonical explanation, and decide whether to retry, ask for clarification, or surface to the user — without string-matching the message.

WorkOS's framing makes the principle explicit: agents need errors that are "machine-readable (a stable error code, not just an HTTP status), specific (what went wrong, not that something did), and actionable (what the caller should do next)" ([WorkOS, "Agent experience: How to design products that agents can actually use," May 2026](https://workos.com/blog/agent-experience-oujuh)). Their cited positive example is Resend, whose errors return a `name` field (`missing_required_field`, `invalid_to`, `daily_sending_quota_exceeded`), a human message, and a doc link — letting an agent branch on `name` without parsing strings. The failure mode WorkOS calls out: free-text error messages that vary by language, locale, or release. Agents pattern-match on those strings and break the moment the wording changes.

**Sources:** [Stripe API errors](https://docs.stripe.com/api/errors), [Stripe error codes](https://docs.stripe.com/error-codes), [WorkOS AX guide](https://workos.com/blog/agent-experience-oujuh), [Nordic APIs "Designing API error messages for AI agents"](https://nordicapis.com/what-is-agent-experience-ax/)
**Confidence:** H

##### Idempotency, retries, and discoverable rate-limit semantics

Agents retry at machine speed. That makes retry-related contracts — idempotency keys, retry-after semantics, rate-limit headers, quota policies — first-class documentation surfaces. Stripe's `Idempotency-Key` header (a client-generated UUID stored server-side for 24 hours) lets agents safely retry network failures without risking duplicate charges ([Stripe Idempotent requests](https://docs.stripe.com/api/idempotent_requests); [Adyen API idempotency](https://docs.adyen.com/development-resources/api-idempotency)). The reciprocal contract — `429 Too Many Requests` with a `Retry-After` header — needs to be documented as a *commitment*, not a suggestion, because agents will follow it literally. The Nordic APIs AX tips guide makes this explicit: "publish expected latencies, rate limits, costs, idempotency guarantees, and error codes so agents can reason about non-functional properties when selecting tools" ([Nordic APIs, 10 Tips for Improving AX, J Simpson, Dec 2025](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/)). Xero documents a `transient-error: true` response header so agents know a 5xx is safe to retry with the same idempotency key ([Xero idempotency docs](https://developer.xero.com/documentation/guides/idempotent-requests/idempotency/)).

**Sources:** [Stripe idempotency](https://docs.stripe.com/api/idempotent_requests), [Adyen idempotency](https://docs.adyen.com/development-resources/api-idempotency), [Xero idempotency](https://developer.xero.com/documentation/guides/idempotent-requests/idempotency/), [Nordic APIs 10 Tips](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/)
**Confidence:** H

##### Operational characteristics as discoverable metadata

Beyond rate limits, AX-friendly docs surface the operational shape of each endpoint as structured metadata: expected p50/p99 latency, dollar cost per call, required scopes, side effects (is this idempotent? does it write?), reversibility, and quota cost. Nordic APIs' tip 7 ("Surface operational characteristics and limits") makes this a discrete pattern ([Nordic APIs](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/)). WorkOS frames it as "match autonomy to reversibility: confirm irreversible actions, preview broad changes, allow narrow-scope tasks freely" — which only works if reversibility is *documented* in a place the planning model can read ([WorkOS](https://workos.com/blog/agent-experience-oujuh)). Cloudflare ships `x-markdown-tokens` response headers so agents can plan context budgets, an early example of operational metadata-as-header rather than metadata-as-prose ([Cloudflare markdown-for-agents](https://blog.cloudflare.com/markdown-for-agents/)).

**Sources:** [Nordic APIs 10 Tips](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/), [WorkOS AX](https://workos.com/blog/agent-experience-oujuh), [Cloudflare markdown-for-agents](https://blog.cloudflare.com/markdown-for-agents/)
**Confidence:** M

##### Code samples written for agents

Human-tolerable code samples often omit imports, environment setup, or error handling on the assumption that the reader can fill in the gaps. Agents can't. Cloudflare's docs-for-agents style guide is explicit: "partial snippets that rely on context from earlier in the page are harder for AI agents to use; self-contained, copy-paste-ready examples work best" ([Cloudflare style guide](https://developers.cloudflare.com/style-guide/ai-tooling/)). Multi-language samples with the imports included, error handling shown, and the success path *and* the failure path documented are the AX-friendly shape. The same logic applies inside Anthropic Skills: the skill-creator skill ships concrete worked examples (input → expected output → assertion) inside the SKILL.md because agents pattern-match on examples as few-shot prompts more reliably than they generalise from rules alone ([Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)).

**Sources:** [Cloudflare docs-for-agents](https://developers.cloudflare.com/style-guide/ai-tooling/), [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
**Confidence:** H

##### Examples as part of the API contract

OpenAPI 3.1's `examples` keyword (an array of named examples, replacing 3.0's single `example`) lets a spec carry multiple worked request/response pairs per operation. Frameworks consuming the spec for tool-calling lift those examples into the model's context as effective few-shot prompts, so example coverage in the spec directly shapes call quality ([OpenAPI 3.1 spec](https://spec.openapis.org/oas/v3.1.0.html); [Speakeasy on examples](https://www.speakeasy.com/blog/agent-experience-introduction)). MCP follows the same pattern: tool descriptions that include input/output examples produce statistically more reliable tool calls than equivalent descriptions without (Hasan et al.'s rubric explicitly counts "examples present" as one of the six components correlated with task-success uplift). Nordic APIs' tip 8 — "annotated JSON payloads, minimal/maximal request examples, and workflow specifications to help agents understand precise expectations and reduce hallucinations" — converges on the same conclusion ([Nordic APIs 10 Tips](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/)).

**Sources:** [OpenAPI 3.1](https://spec.openapis.org/oas/v3.1.0.html), [Hasan et al. arXiv:2602.14878](https://arxiv.org/abs/2602.14878), [Nordic APIs 10 Tips](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/), [Speakeasy AX](https://www.speakeasy.com/blog/agent-experience-introduction)
**Confidence:** H

#### Bucket E — The discipline of AX as design surface

##### WorkOS' "agents don't read tooltips" framing

WorkOS's May 2026 essay by Maria Paktiti is the most condensed statement of the AX framing: "agents cannot read tooltips, infer layout intent, recover from ambiguous errors, or maintain context across sessions without explicit support. They operate at machine speed, retry aggressively, and make decisions solely on surfaced text" ([WorkOS, "Agent experience"](https://workos.com/blog/agent-experience-oujuh)). The implication for documentation is that *any* signal carried by visual hierarchy, hover state, animation, or implicit convention has to be re-surfaced as text the model can read. That includes form-field validation rules buried in JS, error explanations that only appear after a failed submit, and "you know what I mean" conventions in style guides. AX docs make the implicit explicit.

**Sources:** [WorkOS AX](https://workos.com/blog/agent-experience-oujuh)
**Confidence:** H

##### Nordic APIs' practitioner AX series

J Simpson's December 2025 "10 Tips for Improving Agentic Experience (AX)" is the most cited practitioner-shaped checklist in the space ([Nordic APIs 10 Tips](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/)). The ten tips: (1) machine-readable service descriptions via OpenAPI or MCP; (2) discovery endpoint/registry of tools; (3) ship an MCP gateway in front of APIs; (4) replace interactive auth with OAuth client credentials or mTLS; (5) treat authorization as contextual policy; (6) make onboarding automatable (API-first credential minting); (7) surface operational characteristics; (8) provide enriched examples and canonical usage; (9) log/trace/replay; (10) evolve safety iteratively (start with conservative scopes and dry-run modes). Nordic APIs' broader AX series (definition piece by the same outlet, "Designing API Error Messages for AI Agents," "How Arazzo Could Help MCP Servers Orchestrate APIs for AI Consumers," "HATEOAS: The API Design Style That Was Waiting for AI") forms the largest practitioner corpus in the space.

**Sources:** [Nordic APIs 10 Tips](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/), [Nordic APIs definition piece](https://nordicapis.com/what-is-agent-experience-ax/), [Nordic APIs HATEOAS for AI](https://nordicapis.com/hateoas-the-api-design-style-that-was-waiting-for-ai/)
**Confidence:** H

##### The AX-vs-DX-vs-UX three-axis debate

There are two camps. The "AX is a distinct discipline" camp — Biilmann (Netlify), Lamb (Stytch), Paktiti (WorkOS), Sullivan (Speakeasy), Simpson (Nordic APIs) — argues that agents are a new user persona with structurally different needs (machine-readable, stateless, retry-tolerant, error-codified) and that DX patterns optimised for human ergonomics actively harm agent reliability ([Biilmann "Introducing AX"](https://biilmann.blog/articles/introducing-ax/); [Stytch "The age of agent experience"](https://stytch.com/blog/the-age-of-agent-experience/); [Speakeasy AX](https://www.speakeasy.com/blog/agent-experience-introduction)). Biilmann's "One Year of AX" reflection (28 Jan 2026) names the early adopters explicitly: WorkOS, Stytch, Resend, Clerk, Auth0, Neon, Vite, Daytona ([Biilmann, "One Year of AX"](https://biilmann.blog/articles/one-year-of-ax/)).

The "AX is a sub-discipline of DX" camp tends to come from the docs platform and SDK-generation side (Speakeasy notes "AX does not replace DX, it extends it"; Cloudflare's style guide unifies the surfaces with content negotiation rather than splitting them). There is no academic consensus yet — arXiv searches for "agent experience" surface adjacent work on agent memory and reflection (AgentRR, Meta-Policy Reflexion, AgentRx) but no peer-reviewed AX-as-discipline paper. The Gloaguen/Mündler paper is the most rigorous evidence the field has on a *specific* AX surface (AGENTS.md) — and its finding that maximalist context files hurt agents is itself an argument that AX needs its own evaluation methodology distinct from DX intuitions.

**Sources:** [Biilmann Introducing AX](https://biilmann.blog/articles/introducing-ax/), [Biilmann One Year of AX](https://biilmann.blog/articles/one-year-of-ax/), [Stytch age of agent experience](https://stytch.com/blog/the-age-of-agent-experience/), [Speakeasy AX](https://www.speakeasy.com/blog/agent-experience-introduction), [WorkOS AX](https://workos.com/blog/agent-experience-oujuh), [Gloaguen et al. arXiv:2602.11988](https://arxiv.org/abs/2602.11988)
**Confidence:** M

##### Vendor positioning: Anthropic, Vercel, Mintlify, Cloudflare

Four vendors have made AX docs a product feature, not a marketing afterthought. **Anthropic** positions Agent Skills as "domain-specific expertise that transforms general-purpose agents into specialists" with progressive disclosure as the load-bearing design choice ([Anthropic engineering Oct 2025](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)). **Vercel** ships `llms.txt`/`llms-full.txt` for the AI SDK, proposed inline `<script type="text/llms.txt">` HTML embedding, and published controlled evals comparing AGENTS.md against skills ([Vercel inline-llms proposal](https://vercel.com/blog/a-proposal-for-inline-llm-instructions-in-html); [Vercel AGENTS.md eval](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)). **Mintlify** made llms.txt the default for every customer in November 2024 and frames the project as "one day, every company will need two versions of their docs: one for humans and another for LLMs" ([Mintlify](https://www.mintlify.com/blog/simplifying-docs-with-llms-txt)). **Cloudflare** ships Markdown-for-Agents as an HTTP content-negotiation feature on its network (`Accept: text/markdown` returns an auto-converted markdown render, with `x-markdown-tokens` headers and 80% token reduction on the example blog post), plus per-product `llms-full.txt` files ([Cloudflare Markdown for Agents, Feb 2026](https://blog.cloudflare.com/markdown-for-agents/); [Cloudflare style guide](https://developers.cloudflare.com/style-guide/ai-tooling/)). These four vendors collectively define the current production state of AX documentation as a discipline.

**Sources:** [Anthropic engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), [Vercel inline llms](https://vercel.com/blog/a-proposal-for-inline-llm-instructions-in-html), [Vercel AGENTS.md eval](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals), [Mintlify](https://www.mintlify.com/blog/simplifying-docs-with-llms-txt), [Cloudflare Markdown for Agents](https://blog.cloudflare.com/markdown-for-agents/), [Cloudflare docs-for-agents](https://developers.cloudflare.com/style-guide/ai-tooling/)
**Confidence:** H

### 4.5 Common vs unique — what transfers across audiences, what diverges, where they conflict *(inferred from §4.1, §4.2, §4.3, §4.4)*

**Strict shared inheritance.** Five patterns transfer across all three audiences with their structure intact:

- **Diátaxis four-mode taxonomy** — tutorials, how-to, reference, explanation apply equally to DX docs, UX help articles, and (for AX) the routing decision an agent makes when picking between a SKILL.md, a reference URL, or an example.
- **Docs-as-code workflow** — PR review, CI gating, version control. Same chain everywhere; just gated on different lint rules (link-check for DX; reading-level for UX; description-length and trigger-eval for AX).
- **Information architecture and stable URLs** — every audience needs deep-linkable, search-discoverable, version-disambiguated content. The Stripe API version-pinning pattern is load-bearing for all three.
- **Plain language as a floor** — readable prose helps every audience. For UX it's a recovery requirement; for DX it's a comprehension default; for AX it's a parsing default (an agent encountering florid prose embeds it worse than literal phrasing).
- **Errors are documentation** — Stripe's `code` + `message` + `param` + `doc_url` envelope (DX origin) is the same shape WorkOS recommends for AX, and the "describe + give next step + don't blame" rule from UX writing operationalizes both.

**Modified inheritance.** Three patterns transfer but change shape between audiences:

- **Code samples.** DX needs runnable + copy-paste-correct + idiomatic. AX needs *more*: self-contained including imports, both success and failure paths, no "you know what I mean" elisions. UX rarely needs code samples but inherits the "show, don't tell" instinct from the same lineage.
- **Style guides.** Google/Microsoft/Mailchimp set voice and terminology for DX and UX. For AX, *voice* matters less and *terminology consistency* matters far more — a renamed concept across two pages is a UX wobble but an AX bug, because embedding-based retrieval treats inconsistent terms as different concepts.
- **Progressive disclosure.** Nielsen's UX pattern (defer rare options) and the Anthropic Skills three-level loading model (metadata → instructions → resources) are structurally the same idea applied to two audiences — show the minimum, load more on demand. The UX version is about cognitive load; the AX version is about context budget. The principle is shared; the failure mode is different.

**Uniquely required by AX.** Six patterns have no clean parallel in DX or UX:

- **Routing-via-description.** SKILL.md and MCP tool descriptions are not prose — they are the load-bearing trigger for whether the content gets loaded at all. Anthropic's "treat the description as a tunable hyperparameter" framing has no DX or UX analogue, because human users either browse the catalog or arrive via search; agents have neither browse nor search, they have routing-by-description-match.
- **Always-loaded vs load-on-demand budget arithmetic.** The Vercel AGENTS.md-vs-Skills evals (100% vs 53%) are about whether the content sits in the system prompt every turn or only on trigger. Humans don't pay context costs; agents do.
- **Schema-as-docs.** OpenAPI / MCP / GraphQL SDL `description` fields are the primary product surface for agents, with rendered docs sites a secondary derivative. For DX the prose site is primary, the schema is helper; for AX the relationship inverts.
- **Stable error codes over message strings.** DX tolerates message-text reading (developers can read prose); AX needs codes because message text drifts. WorkOS' Resend example (`name: "missing_required_field"`) is the AX-shaped variant of what Stripe does for DX.
- **Chunk-survivability.** No "see above" anaphora, restated subjects, glossary-as-bridge — these are RAG-design constraints that have no UX or DX parallel, because humans read pages and IDEs read symbols, but retrievers read chunks.
- **Forbidden-actions as machine-enforced gates.** AGENTS.md can describe "thou shalt not" in prose, but the load-bearing AX pattern is a hook script that enforces the rule when the model ignores the prose. No equivalent in DX (developers can read a CONTRIBUTING.md) or UX (end users can be guarded by UI affordances).

**Where the audiences conflict.** Six places the optimum for one audience harms another:

- **Hover/tooltip discoverability (good UX) vs always-on-page text (good AX).** WorkOS' "agents can't read tooltips" is a direct conflict with NN/g's tooltip guidance, which encourages tooltips for *supplementary* context. Resolving it requires either dual rendering (visible-for-humans-plus-machine-readable) or moving load-bearing content out of tooltips entirely.
- **Conversational prose (engaging UX) vs structured fields (parsing-friendly AX).** Mailchimp's voice-and-tone advice ("warm, personal, plainspoken") works against the AX preference for terse, structured, code-table content. The Cloudflare Markdown-for-Agents content-negotiation pattern (`Accept: text/markdown` returns a stripped version) is one resolution.
- **Maximalist context files (intuitive for "more help is better") vs minimalist AGENTS.md (better for agents per Mündler et al.).** The 4% lift from developer-written maximalist AGENTS.md plus 19% cost inflation is the cleanest evidence that DX intuitions can actively hurt AX outcomes.
- **Plain language for end users (US 6th–8th grade) vs precise technical terminology for developers and agents.** A glossary that the UX team has approved for "delete" may need to remain `DELETE` (with explicit warning of irreversibility) for agents acting through APIs.
- **Hand-curated reference (Stripe's three-column DX gold standard) vs auto-generated schema-as-docs (AX-preferred).** A hand-written DX reference is more polished; an OpenAPI-derived reference is more reliably current and machine-parseable. Stripe's resolution — hand-curated *on top of* a generated schema — is the most expensive but the most defensible.
- **Pull-revelation UX help (NN/g preferred for end users) vs always-on context (preferred for agents).** The UX prefers help that arrives when needed; agents prefer help that's always loaded so the trigger decision doesn't have to be made.

The clean way to state the contrast: **DX optimises for the human developer's cognitive efficiency; UX optimises for the human end-user's recovery and learnability; AX optimises for the agent's machine-readability, deterministic behaviour, and stable contract.** The three audiences agree on the foundations (Diátaxis, docs-as-code, plain language, errors-as-docs) but diverge sharply on the specifics — and the divergences are where the design tensions live.

## 5. Key debates and open questions

### 5.1 Empirical disagreement (sources disagree on what works)

- **Maximalist vs minimalist AGENTS.md.** The Gloaguen/Mündler ETH paper (arXiv:2602.11988) shows that across 438 tasks and four agents, LLM-generated AGENTS.md *hurts* task success (~2% on AGENTbench) while raising cost 20–23%; developer-written files give only 4% lift with 19% cost inflation. Their recommendation: "describe only minimal requirements." This contradicts the maximalist culture visible in the wild (Next.js's 312-line AGENTS.md, repos with 1000+ line CLAUDE.md). The honest read: the field has not yet adapted to the evidence. **Confidence:** H

- **AGENTS.md vs Anthropic Skills.** Vercel's January 2026 evals showed AGENTS.md scoring 100% vs Skills' 53% (no instruction) / 79% (with explicit instruction) on Next.js 16 APIs absent from training data. The mechanism is the always-loaded-vs-trigger trade-off. Anthropic's framing emphasizes Skills' progressive disclosure as a feature; Vercel's evidence shows it as a liability for content the agent should always have. The two are *complements* — AGENTS.md for always-needed, Skills for unbounded-on-demand — but the framing in vendor positioning sometimes treats them as competitors. **Confidence:** M

- **MCP tool descriptions: more vs targeted.** Hasan et al. (arXiv:2602.14878) found their six-component description rubric improved task success 5.85pp on median but also regressed performance in 16.67% of cases and added 67.46% more execution steps. More description is not strictly better; targeted is. **Confidence:** H

- **Auto-generated vs hand-written API reference.** The Stripe model (hand-curated three-column reference over a generated schema) produces the polished gold standard but requires staffed editors. The OpenAPI-driven model (Mintlify, Redoc, Scalar) eliminates drift but produces uniform prose that misses the *why*. No source claims one wins on every dimension. **Confidence:** M

- **Push vs pull onboarding.** NN/g argues pull-style contextual help outperforms push-style modal carousels. Practitioner data (Appcues, Userpilot) corroborates on completion rates, but vendor selling onboarding tools (Pendo, WalkMe) maintains the case for product tours when scoped to one task. Disagreement is partly definitional — "interactive walkthrough" is push-style if you squint. **Confidence:** M

### 5.2 Interpretive disagreement (sources agree on data but disagree on what it implies)

- **Is AX a distinct design discipline or a sub-discipline of DX?** Biilmann/Stytch/WorkOS/Nordic APIs treat it as distinct because agents have structurally different needs (machine-readable, stateless, retry-aggressive, code-driven decisioning). Speakeasy and Cloudflare frame it as DX extended ("AX does not replace DX, it extends it"). The Mündler evidence cuts toward "distinct" — AGENTS.md needs its own evaluation methodology because DX intuitions actively mislead — but the field hasn't converged. **Confidence:** M

- **Single source of truth vs forked human/agent docs.** Mintlify's framing is that "every company will need two versions of their docs: one for humans and another for LLMs." Cloudflare's Markdown-for-Agents takes the opposite position: one source rendered differently per `Accept:` header. Both reduce the same risk (humans and agents get different things) but solve it differently — Mintlify by maintaining two artifacts, Cloudflare by content negotiation. **Confidence:** M

- **llms.txt as a standard vs a publishing convention.** llmstxt.org positions itself as a spec; in practice no LLM provider has committed to consuming it at inference time, so it functions as a *publishing convention* (agents and tools fetch it on prompt) rather than a *crawled standard* in the robots.txt sense. The disagreement is whether this gap matters — Anthropic, Vercel, Mintlify, Cloudflare ship it anyway because the agents they care about do fetch it; skeptics note the absence of formal commitment from model providers. **Confidence:** H

- **Diátaxis vs alternatives.** Diátaxis is the dominant framework; alternatives include Mark Baker's "Every Page is Page One" (treating every page as a possible entry point, optimizing for findability), DITA (heavy XML-typed authoring), and the Microsoft Modular Writing model. Procida frames Diátaxis as descriptive (the four modes already exist in good docs); critics argue it's prescriptive in a way that fits SDKs better than apps. **Confidence:** M

- **Search-first vs browse-first IA.** NN/g recommends supporting both; practitioner data leans search-first for help centers (Google drives most traffic), browse-first for tutorials and conceptual docs. The disagreement is whether to optimize the home page for search (search-first) or for orientation (browse-first). **Confidence:** M

### 5.3 Open questions (no source addresses these clearly)

- **What is the optimum AGENTS.md length given the Mündler finding?** The paper recommends "minimal requirements" but doesn't define a length. Practitioner files run 50–1500 lines; the Next.js canonical exemplar is 312. No controlled study yet measures the optimum point on the size-cost-benefit curve.

- **How should docs be split between always-loaded (AGENTS.md / system prompt) and load-on-demand (Skills / MCP tools / linked references)?** Vercel's evals say "framework APIs go in AGENTS.md"; Anthropic's positioning says "domain expertise goes in Skills." Where the line falls for the median repo is an open practitioner question.

- **Do `llms-full.txt` files at Cloudflare scale (3.7M tokens) actually help agents, or are they just published?** No public eval measures task-success delta from a fetched `llms-full.txt` vs the live docs site.

- **How should multi-audience docs handle the AX-vs-UX hover-tooltip conflict?** Cloudflare's content-negotiation is one resolution; dual rendering (visible + machine-readable) is another; moving load-bearing content out of tooltips is a third. No source proposes a canonical pattern.

- **Should error message strings remain stable as part of the contract (Hyrum's Law for AX)?** Stripe's `code` field is stable; the `message` field is technically prose. WorkOS notes that agents pattern-match on message strings anyway. The open question is whether vendors should formally commit to message stability (treating it as part of the API contract) or rely on `code` discipline.

- **What is the right reading-age target for AX-facing prose?** UX targets US 6th–8th grade for end users; DX has no codified target. For AX, embedding similarity favors literal phrasing over flowery language, but no source proposes a quantitative target.

- **Does Diátaxis's anti-mixing rule still hold for AX?** The four modes are meant to be kept separate; SKILL.md frequently mixes "when to use" (explanation) with "how to use" (how-to) with "examples" (reference). Whether this is a violation or a productive adaptation is unsettled.

## 6. Implications

### 6.1 If you're building documentation for any audience

- **Sourced implication:** Adopt Diátaxis as the IA backbone. Cloudflare, Django, Gatsby, and gov.uk all converge on it; the anti-mixing rule is the highest-yield discipline a docs team can adopt. (§4.1, §4.2, §4.3, §4.4)
- **Sourced implication:** Treat docs as code: PRs, CI gating, doctest, link checks, lint. Anne Gentle's *Docs Like Code* and Stripe's Markdoc are the canonical references. (§4.1)
- **Sourced implication:** Versioned URLs are non-negotiable. Cookie-based or dropdown-based version selectors lose to versioned URLs at the search-result layer; the cost in stale-page bug reports compounds over time. (§4.1, §4.2)
- **Sourced implication:** Instrument the docs site: "Was this helpful?" + zero-result-search analysis + ticket-to-article gap analysis. The doc team as a product team needs metrics. (§4.1, §4.3)

### 6.2 If you're building DX documentation specifically

- **Sourced implication:** The README is your TTFHW surface. Install + minimum working example above the fold; no badges, no comparison tables, no feature tours before the runnable snippet. (§4.2)
- **Sourced implication:** Structured errors with `code` + `message` + `param` + `doc_url` are the floor. Stripe's pattern is widely imitated because it works. Generic "invalid config" messages are an unforced loss. (§4.2)
- **Sourced implication:** Code samples are first-class — tested in CI, idiomatic, complete-and-minimal. CMU NatProg's empirical evidence is that example quality predicts task success better than reference completeness. (§4.2)
- **Inferred implication (from §4.2 + §4.4):** Type-as-doc is the primary DX surface for working developers and is the AX surface that flows directly into IDE-attached agents. JSDoc/TSDoc on public types pays compounding returns.

### 6.3 If you're building UX documentation specifically

- **Sourced implication:** Help-in-the-moment-of-need beats forced onboarding modals. Pull revelations (contextual help) outperform push revelations (modal carousels) on completion rates. (§4.3)
- **Sourced implication:** Empty states are teaching surfaces. NN/g's three-job framing (status / learning / pathway) is the highest-leverage docs surface you're probably under-investing in. (§4.3)
- **Sourced implication:** Error copy follows the recovery shape: describe what happened in the user's words, give the next step in one click, don't blame the user. Mailchimp/Yifrah/GOV.UK converge on the same pattern. (§4.3)
- **Sourced implication:** Plain language is the floor: 15–20 word sentences, US 6th–8th grade reading level for consumer products, active voice. WCAG 2.2 compliance is non-negotiable for any public-facing help. (§4.1, §4.3)
- **Inferred implication (from §4.3):** Articles consistently appearing in the activation funnel between sign-up and first key action are candidates for promotion from help center into in-product help (tooltips, empty states, contextual sidebars). Treat the help center as a backlog source.

### 6.4 If you're building AX documentation specifically

- **Sourced implication:** Ship `llms.txt` (curated index) and `llms-full.txt` (full content) for any docs site agents will fetch. Mintlify-hosted sites get this automatically; for self-hosted, add it. The cost is low and the reach to fetch-capable agents is real. (§4.4)
- **Sourced implication:** Keep AGENTS.md minimal. The Mündler evidence is that maximalist context files hurt task success and inflate cost; "human-written context files should describe only minimal requirements" is the bar. (§4.4)
- **Sourced implication:** Symlink AGENTS.md ↔ CLAUDE.md ↔ `.github/copilot-instructions.md` ↔ GEMINI.md to a single source of truth, gated by CI. Vercel's Next.js is the canonical exemplar. (§4.4)
- **Sourced implication:** MCP tool descriptions are documentation. Hasan et al.'s six-component rubric (purpose + parameters + return + examples + errors + constraints) is the most rigorous quality bar in the literature. (§4.4)
- **Sourced implication:** Stable error codes (Stripe's `code`, Resend's `name`) over free-text message strings. Agents pattern-match on whatever's there; give them the stable surface to match on. (§4.4)
- **Sourced implication:** Forbidden-actions documentation is two-layer: prose in AGENTS.md describes the rule, hook script enforces it deterministically. Models ignore prose; hooks don't. (§4.4)
- **Inferred implication (from §4.4 + §4.5):** Skills (Anthropic) and AGENTS.md are complementary, not competitive. Use AGENTS.md for always-available framework knowledge the agent needs every turn; use Skills for unbounded bundled expertise that loads on trigger.
- **Inferred implication (from §4.4):** Run an internal eval. The Mündler-style methodology — measure task success and cost on your repo's actual tasks with and without each AX surface — is the only way to know whether your AGENTS.md is in the "helpful" or "actively harmful" zone.

### 6.5 If you're building docs that serve multiple audiences

- **Inferred implication (from §4.5):** Content negotiation (Cloudflare's `Accept: text/markdown` pattern) is a more sustainable resolution than maintaining two parallel artifacts. The closer the human and agent docs stay to one source, the less drift you have to manage.
- **Inferred implication (from §4.5):** The audiences converge on Diátaxis, docs-as-code, plain language, versioned URLs, and structured errors. Build those foundations once for everyone; specialize on top.
- **Inferred implication (from §4.5):** The conflicts are sharper than the convergences. Where tooltips, conversational prose, maximalist context files, and pull-revelation help collide with AX needs, design a resolution explicitly — don't assume the human-optimized choice also serves agents.

## 7. Sources

Annotated bibliography organized by source class. Entries from §4.1 / §4.2 / §4.3 / §4.4 are deduplicated and combined here.

### Canonical frameworks and seminal references

- **[Diátaxis (Procida)](https://diataxis.fr/)** — canonical four-mode framework. Primary, actively maintained, named adopters.
- **[Cloudflare Style Guide — IA](https://developers.cloudflare.com/style-guide/documentation-content-strategy/information-architecture/)** — Diátaxis-based IA from a named adopter. Institutional primary.
- **[Django documentation](https://docs.djangoproject.com/en/6.0/)** — Diátaxis-shaped IA in a major OSS project. Primary.
- **[Write the Docs — Docs as Code](https://www.writethedocs.org/guide/docs-as-code/)** — community-canonical definition and tooling chain. Practitioner-vetted reference.
- **[Docs Like Code (Anne Gentle)](https://www.docslikecode.com/)** — book site for the standard docs-as-code reference. Primary.
- **[Joshua Bloch, "How to Design a Good API and Why It Matters" (OOPSLA 2006)](https://dl.acm.org/doi/pdf/10.1145/1176617.1176622)** — seminal paper on self-documenting APIs. Peer-reviewed.
- **[InfoQ: Bumper-Sticker API Design](https://www.infoq.com/articles/API-Design-Joshua-Bloch/)** — accessible summary of Bloch's maxims. Practitioner-secondary.
- **[Tom Preston-Werner, "Readme Driven Development" (2010)](https://tom.preston-werner.com/2010/08/23/readme-driven-development.html)** — canonical RDD essay. Primary, foundational.
- **[Rust API Guidelines: Documentation](https://rust-lang.github.io/api-guidelines/documentation.html)** — codifies `# Examples` / `# Errors` / `# Panics` conventions. Primary, project-official.
- **[Andrew Gerrand, "Godoc: documenting Go code"](https://go.dev/blog/godoc)** — foundational godoc convention. Primary.
- **[Go Doc Comments](https://go.dev/doc/comment)** — current Go doc-comment spec. Primary.
- **[Information Architecture: For the Web and Beyond (Rosenfeld/Morville/Arango)](https://www.oreilly.com/library/view/information-architecture-4th/9781491913529/)** — canonical IA reference (the "polar bear book"). Primary.
- **[Card Sorting (Donna Spencer)](https://rosenfeldmedia.com/books/card-sorting/)** — canonical IA empirical method. Primary.
- **[Kinneret Yifrah, *Microcopy: The Complete Guide*](https://www.amazon.com/Microcopy-Complete-Guide-Kinneret-Yifrah/dp/B07N1RD7W6)** — canonical UX-writing reference. Primary.
- **[Steve Krug, *Don't Make Me Think* (3rd ed.)](https://www.amazon.com/Dont-Make-Think-Revisited-Usability/dp/0321965515)** — foundational usability book. Primary.

### Style guides and standards

- **[Google Developer Documentation Style Guide](https://developers.google.com/style)** — primary canonical source.
- **[Google Code Samples Style](https://developers.google.com/style/code-samples)** — code-sample subsection. Primary.
- **[Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)** — primary canonical source.
- **[18F Content Guide](https://guides.18f.gov/content-guide/)** — institutional source for plain-language federal practice. Primary.
- **[18F Content Guide — Plain Language](https://guides.18f.gov/content-guide/our-approach/plain-language/)** — operational rules with concrete word swaps. Primary.
- **[plainlanguage.gov](https://www.plainlanguage.gov/)** — federal plain-language hub. Primary government.
- **[Federal Plain Language Guidelines](https://www.plainlanguage.gov/guidelines/)** — operationalized rules behind the Plain Writing Act. Primary government.
- **[DOJ — Plain Writing Act of 2010](https://www.justice.gov/open/plain-writing-act)** — primary institutional source for the legal mandate.
- **[GOV.UK — What is content design](https://www.gov.uk/guidance/content-design/what-is-content-design)** — UK Government Digital Service's content-design guidance. Primary.
- **[GOV.UK — Writing for GOV.UK](https://www.gov.uk/guidance/content-design/writing-for-gov-uk)** — 9-year-old reading-age target. Primary.
- **[Mailchimp Content Style Guide — Voice and Tone](https://styleguide.mailchimp.com/voice-and-tone/)** — most-copied public exemplar. Primary vendor (substantive).
- **[Cloudflare docs-for-agents style guide](https://developers.cloudflare.com/style-guide/ai-tooling/)** — primary vendor patterns source for AX writing.
- **[WCAG 2.2 (W3C Recommendation)](https://www.w3.org/TR/WCAG22/)** — standards-body primary source.
- **[W3C WAI — WCAG 2.2 announcement](https://www.w3.org/WAI/news/2023-10-05/wcag22rec/)** — primary dating source.
- **[What's New in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)** — W3C summary of 9 new criteria. Primary.
- **[Penn State — WCAG 2.2 Guidelines](https://accessibility.psu.edu/guidelines/wcaglist/)** — institutional practical checklist for applying WCAG to authoring.
- **[Document360 — WCAG Accessibility Best Practices](https://document360.com/blog/wcag-accessibility-best-practices/)** — substantive vendor writing on its own system.
- **[OpenAPI 3.1 spec](https://spec.openapis.org/oas/v3.1.0.html)** — schema-as-docs canonical contract. Primary, standards.
- **[schema.org](https://schema.org/)** — vocabulary for structured data in docs. Primary, standards.
- **[Keep a Changelog](https://keepachangelog.com/)** — primary, widely-adopted changelog spec.
- **[SemVer 2.0.0](https://semver.org/)** — primary versioning spec.

### Peer-reviewed and arXiv academic

- **[Myers & Stylos, "Improving API Usability," *CACM* June 2016](https://cacm.acm.org/research/improving-api-usability/)** — peer-reviewed synthesis of CMU NatProg's decade of empirical work on API/doc usability.
- **[CMU NatProg API Usability project](http://www.cs.cmu.edu/~NatProg/apiusability.html)** — institutional, primary; indexes the underlying empirical studies.
- **[NN/g — 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)** — Nielsen's canonical heuristics including error prevention/recovery.
- **[NN/g — Help and Documentation](https://www.nngroup.com/articles/help-and-documentation/)** — primary canonical source for heuristic #10, pull-vs-push help, search/browse guidance.
- **[NN/g — Tooltip Guidelines](https://www.nngroup.com/articles/tooltip-guidelines/)** — primary canonical source for tooltip failure modes and best practices.
- **[NN/g — Designing Empty States](https://www.nngroup.com/articles/empty-state-interface-design/)** — primary canonical source for the three-job empty-state framing.
- **[NN/g — Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)** — Nielsen's foundational article on progressive disclosure.
- **[NN/g — Hostile Error Messages](https://www.nngroup.com/articles/hostile-error-messages/)** — primary, recent failure-mode catalog for error copy.
- **[NN/g — UI Copy](https://www.nngroup.com/articles/ui-copy/)** — primary canonical source on UI command-name guidelines.
- **[Gloaguen et al., "Evaluating AGENTS.md," arXiv:2602.11988 (Feb 2026)](https://arxiv.org/abs/2602.11988)** — central evidence that maximalist AGENTS.md hurts agents; LogicStar/ETH SRI. Primary academic.
- **[Hasan et al., "MCP Tool Descriptions Are Smelly!", arXiv:2602.14878 (Feb 2026)](https://arxiv.org/abs/2602.14878)** — 856 tools, 97.1% smell rate, +5.85pp uplift from six-component rubric. Primary academic.
- **[VersionRAG, arXiv:2510.08109](https://arxiv.org/pdf/2510.08109)** — version-aware retrieval; supports stable-anchor pattern. Academic.
- **["Observations on Building RAG Systems for Technical Documents," arXiv:2404.00657](https://arxiv.org/pdf/2404.00657)** — supports glossary-as-separate-processing. Academic.
- **["Structured Linked Data as a Memory Layer for Agent-Orchestrated Retrieval," arXiv:2603.10700](https://arxiv.org/pdf/2603.10700)** — supports schema.org-for-agents claim. Academic.
- **[Meta-Policy Reflexion, arXiv:2509.03990](https://arxiv.org/pdf/2509.03990)** — academic, adjacent support for reflective-memory pattern.
- **[PreFlect, arXiv:2602.07187](https://arxiv.org/pdf/2602.07187)** — academic, adjacent.
- **[AgentRx, arXiv:2602.02475](https://arxiv.org/pdf/2602.02475)** — academic, adjacent support for reflection-log pattern.

### Vendor primary (substantive engineering writing on own systems)

- **[Stripe API Reference](https://docs.stripe.com/api)** — canonical hand-curated three-column reference layout. Primary.
- **[Stripe API errors](https://docs.stripe.com/api/errors)** — canonical structured-errors precedent. Primary.
- **[Stripe Error codes](https://docs.stripe.com/error-codes)** — error-codes table linked from `doc_url`. Primary.
- **[Stripe Idempotent requests](https://docs.stripe.com/api/idempotent_requests)** — canonical agent-safe retries precedent. Primary.
- **[Stripe API Versioning](https://docs.stripe.com/api/versioning)** — primary, benchmark doc operation.
- **[Stripe upgrades](https://docs.stripe.com/upgrades)** — per-version migration docs. Primary.
- **[Stripe — Markdoc](https://stripe.dev/blog/markdoc)** — first-party engineering on docs validation CI. Primary.
- **[Twilio Programmable Voice Quickstarts](https://www.twilio.com/docs/voice/quickstart)** — canonical minimum-lines-to-working-call pattern. Primary.
- **[Twilio SMS Quickstart](https://www.twilio.com/docs/sms/quickstart)** — closest extant relative of the "8 lines" pattern. Primary.
- **[Twilio Tutorials](https://www.twilio.com/docs/tutorials)** — task-named cookbook surface. Primary.
- **[Twilio Docs Quickstart Hub](https://www.twilio.com/docs/quickstart)** — tutorial-shaped landing page. Primary.
- **[Anthropic — Equipping agents with Agent Skills (Oct 2025)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)** — primary vendor framing; progressive disclosure rationale.
- **[Anthropic Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)** — official Skills documentation. Primary.
- **[anthropics/skills repo](https://github.com/anthropics/skills)** — primary open-source Skills repo.
- **[Anthropic skill-creator SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)** — concrete SKILL.md example with description-optimization loop. Primary.
- **[Anthropic — Complete Guide to Building Skills](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)** — official authoring guide. Primary.
- **[Claude Code hooks reference](https://code.claude.com/docs/en/hooks)** — official hooks reference (PreToolUse, exit codes). Primary vendor.
- **[Vercel — AGENTS.md outperforms Skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)** — Jan 2026 controlled eval. Primary vendor.
- **[Vercel — A proposal for inline LLM instructions in HTML](https://vercel.com/blog/a-proposal-for-inline-llm-instructions-in-html)** — Aug 2025 inline-llms-txt proposal. Primary vendor.
- **[vercel/examples](https://github.com/vercel/examples)** — canonical separate-examples-repo pattern. Primary.
- **[Vercel Templates](https://vercel.com/templates)** — templates marketplace with one-click deploy. Primary.
- **[Next.js with-typescript on StackBlitz](https://stackblitz.com/github/vercel/next.js/tree/canary/examples/with-typescript)** — primary in-browser-fork example.
- **[vercel/next.js AGENTS.md](https://github.com/vercel/next.js/blob/canary/AGENTS.md)** — canonical AGENTS.md ↔ CLAUDE.md symlink reference. Primary.
- **[Mintlify — Simplifying docs for AI with /llms.txt](https://www.mintlify.com/blog/simplifying-docs-with-llms-txt)** — primary vendor announcement of platform-wide llms.txt support.
- **[Mintlify llms.txt docs](https://www.mintlify.com/docs/ai/llmstxt)** — reference docs for llms.txt generation. Primary.
- **[Mintlify on X, Nov 2024](https://x.com/mintlify/status/1859281309878845708)** — primary, dated social announcement.
- **[Cloudflare developer docs, llms.txt](https://developers.cloudflare.com/llms.txt)** — primary artifact.
- **[Cloudflare ai-search llms.txt](https://developers.cloudflare.com/ai-search/llms.txt)** — primary artifact.
- **[Cloudflare blog — Markdown for Agents (Feb 2026)](https://blog.cloudflare.com/markdown-for-agents/)** — primary vendor source by Celso Martinho & Will Allen.
- **[Cloudflare reference docs — markdown-for-agents](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/)** — primary content-negotiation reference.
- **[Algolia DocSearch](https://docsearch.algolia.com/)** — primary source for de-facto doc-search standard.
- **[DocSearch GitHub](https://github.com/algolia/docsearch)** — primary OSS implementation.
- **[ReadMe API reference](https://docs.readme.com/main/reference/intro-to-the-readme-api)** — primary vendor docs-as-data source.
- **[Notion API overview](https://developers.notion.com/)** — primary vendor docs-as-data source.
- **[Google ADK OpenAPI tools docs](https://google.github.io/adk-docs/tools-custom/openapi-tools/)** — primary vendor source for OpenAPI-as-tools.
- **[Microsoft Semantic Kernel OpenAPI plugins](https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/adding-openapi-plugins)** — primary vendor source.
- **[Speakeasy — Designing agent experience](https://www.speakeasy.com/blog/agent-experience-introduction)** — primary practitioner-vendor guide; OpenAPI-as-AX-surface.
- **[Speakeasy — release agent skills](https://www.speakeasy.com/blog/release-agent-skills)** — primary vendor source.
- **[Speakeasy — Choosing a docs vendor](https://www.speakeasy.com/blog/choosing-a-docs-vendor)** — practitioner-comparison framing for drift-vs-render trade-off.
- **[Pinecone semantic chunking](https://github.com/pinecone-io/examples/blob/main/learn/generation/better-rag/02b-semantic-chunking.ipynb)** — primary vendor.
- **[LlamaIndex semantic splitter discussion](https://github.com/run-llama/llama_index/issues/12007)** — primary repo issue.
- **[Adyen API idempotency](https://docs.adyen.com/development-resources/api-idempotency)** — primary, secondary adoption of Stripe pattern.
- **[Xero idempotency docs](https://developer.xero.com/documentation/guides/idempotent-requests/idempotency/)** — primary, with `transient-error` header pattern.
- **[Stripe Blog — Idempotency](https://stripe.com/blog/idempotency)** — primary engineering writing on idempotent retries.
- **[Rust RFC 1644: Default and Expanded rustc Errors](https://rust-lang.github.io/rfcs/1644-default-and-expanded-rustc-errors.html)** — primary, peer-reviewed by Rust core.
- **[Rust Blog: "Shape of errors to come"](https://blog.rust-lang.org/2016/08/10/Shape-of-errors-to-come/)** — primary official Rust blog.
- **[Rust Error Codes Index](https://doc.rust-lang.org/error-index.html)** — primary, official `--explain` error-code index.
- **[Sphinx doctest extension](https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html)** — primary tooling source for executable samples.
- **[Kubernetes — Supported Doc Versions](https://kubernetes.io/docs/home/supported-doc-versions/)** — primary institutional source on doc versioning.
- **[React-Native docs version archiving (RFC #3819)](https://github.com/facebook/react-native-website/issues/3819)** — primary, named adopter.
- **[Carbon Design System — Empty States](https://carbondesignsystem.com/patterns/empty-states-pattern/)** — primary IBM design-system source.

### AX-discipline practitioner sources

- **[Biilmann — Introducing AX (Jan 2025)](https://biilmann.blog/articles/introducing-ax/)** — load-bearing origin source for the AX term. Primary.
- **[Biilmann — One Year of AX (Jan 2026)](https://biilmann.blog/articles/one-year-of-ax/)** — adopter list reflection. Primary.
- **[Netlify — Agent Experience](https://www.netlify.com/agent-experience/)** — primary vendor positioning.
- **[WorkOS — Agent experience](https://workos.com/blog/agent-experience-oujuh)** — canonical "agents can't read tooltips" framing. Primary practitioner.
- **[Stytch — The age of agent experience](https://stytch.com/blog/the-age-of-agent-experience/)** — OAuth-for-agents framing. Primary practitioner.
- **[Nordic APIs — 10 Tips for Improving AX](https://nordicapis.com/10-tips-for-improving-agentic-experience-ax/)** — established practitioner checklist. Primary.
- **[Nordic APIs — What is AX](https://nordicapis.com/what-is-agent-experience-ax/)** — definition piece. Practitioner.
- **[Nordic APIs — HATEOAS for AI](https://nordicapis.com/hateoas-the-api-design-style-that-was-waiting-for-ai/)** — practitioner.
- **[agents.md](https://agents.md/)** — canonical site, Linux Foundation Agentic AI Foundation. Primary.
- **[llmstxt.org](https://llmstxt.org/)** — canonical llms.txt specification. Primary.
- **[Answer.AI — llms.txt proposal](https://www.answer.ai/posts/2024-09-03-llmstxt.html)** — Howard's original proposal, Sept 2024. Primary.
- **[Model Context Protocol — intro](https://modelcontextprotocol.io/docs/getting-started/intro)** — canonical MCP entry point. Primary.
- **[Model Context Protocol — spec repo](https://github.com/modelcontextprotocol/modelcontextprotocol)** — primary spec docs.
- **[Building Guardrails for AI Coding Assistants](https://dev.to/mikelane/building-guardrails-for-ai-coding-assistants-a-pretooluse-hook-system-for-claude-code-ilj)** — practitioner walkthrough of PreToolUse pattern.
- **[dwarvesf/claude-guardrails](https://github.com/dwarvesf/claude-guardrails)** — practitioner reference implementation.
- **[DeployHQ — AI coding config guide](https://www.deployhq.com/blog/ai-coding-config-files-guide)** — practitioner comparison of CLAUDE.md / AGENTS.md / Copilot Instructions.
- **[Agent Rules Builder — Cursor rules vs CLAUDE.md](https://www.agentrulegen.com/guides/cursorrules-vs-claude-md)** — practitioner.
- **[SSW — symlink-agents-to-claude rule](https://www.ssw.com.au/rules/symlink-agents-to-claude)** — practitioner rule documenting the symlink convention.
- **[Augment Code — How to build AGENTS.md](https://www.augmentcode.com/guides/how-to-build-agents-md)** — practitioner.
- **[Firecrawl — Best chunking strategies for RAG](https://www.firecrawl.dev/blog/best-chunking-strategies-rag)** — practitioner.
- **[LLM internal linking guide (zcmarketing)](https://zcmarketing.au/seo-tips/llm-internal-linking-2025/)** — practitioner on stable anchor IDs.
- **[JSON-LD SEO guide](https://www.seostrategy.co.uk/schema-structured-data/json-ld-guide/)** — practitioner survey of JSON-LD use.

### DX/UX practitioner sources

- **[Total TypeScript — IDE Superpowers](https://www.totaltypescript.com/books/total-typescript-essentials/ide-superpowers)** — Pocock's chapter on TypeScript-as-IDE-doc-surface. Practitioner.
- **[Simon Willison on Diátaxis](https://simonwillison.net/2021/Aug/21/diataxis/)** — practitioner adoption note.
- **[Pronovix — Context-sensitive embedded help](https://pronovix.com/blog/overview-context-sensitive-and-embedded-help-formats)** — substantive practitioner from doc-tooling specialist.
- **[Appcues — Build Effective Product Tours](https://www.appcues.com/blog/build-effective-product-tours)** — substantive vendor writing on tour anti-patterns.
- **[Userpilot — Product Tour Examples](https://userpilot.com/blog/product-tour-examples/)** — vendor primary on contextual-tour completion-rate data.
- **[UXPin — Error Feedback Best Practices](https://www.uxpin.com/studio/blog/error-feedback-best-practices-mobile-forms/)** — practitioner reference for 500ms inline-validation timing.
- **[Amplitude — Aha Moment](https://amplitude.com/blog/aha-moment)** — Reforge Setup→Aha→Habit framing; 25%/34% figures.
- **[Amplitude — Time to Value](https://amplitude.com/blog/time-to-value-drives-user-retention)** — vendor primary, substantive.
- **[Amplitude — Activation Rate](https://amplitude.com/explore/digital-analytics/what-is-activation-rate)** — vendor primary; operational definition.
- **[eesel AI — Deflection Rate](https://www.eesel.ai/blog/deflection-rate-what-is-it-and-how-to-improve-it)** — vendor secondary on benchmarks.
- **[Zendesk — Reporting for Self-Service](https://support.zendesk.com/hc/en-us/articles/4408832867226-Reporting-tools-for-measuring-self-service)** — vendor primary on its own system.
- **[Aha! — Improve Your Knowledge Base With Feedback](https://www.aha.io/blog/improve-your-product-knowledge-base-with-user-feedback)** — vendor secondary, substantive.
- **[UX Content Collective — What is localization for UX](https://uxcontent.com/what-is-localization-for-ux/)** — practitioner secondary on internationalization.
- **[GitLab docs feedback issue (#374573)](https://gitlab.com/gitlab-org/gitlab/-/issues/374573)** — primary evidence of the feedback-loop pattern in practice.
- **[Tom Johnson — Measuring documentation quality](https://idratherbewriting.com/learnapidoc/docapis_measuring_impact.html)** — practitioner long-form on doc telemetry.

## 8. Limitations

**Coverage gaps:**

- **Sub-discipline depth tradeoffs.** Because AX was the centerpiece, DX and UX coverage is at "reference frame" depth rather than exhaustive. Pattern catalogs for either could be substantially deeper — e.g., the UX section under-covers internationalization, motion-design as documentation, and accessibility-for-cognitive-differences; the DX section under-covers SDK contributor experience, doc-team org structure, and language-specific idiomatic doc style.
- **Quantitative comparative studies are thin.** The only rigorous controlled evals in the report are Gloaguen/Mündler on AGENTS.md and Hasan et al. on MCP descriptions. No comparable empirical work exists for llms.txt effectiveness, SKILL.md activation rates, or the value of `llms-full.txt` at Cloudflare scale. Most patterns are supported by institutional convergence + practitioner consensus, not controlled experiments.
- **Vendor-primary dominates AX.** The AX literature is heavily vendor-primary (Anthropic, Vercel, Mintlify, Cloudflare, WorkOS, Stytch, Speakeasy). Even the most rigorous academic source (Mündler) only landed in February 2026. Treat AX patterns as a working hypothesis space, not a settled discipline.
- **English-only and US/EU bias.** Most cited sources are English-language and US/EU-based. The international plain-language and content-design literature (e.g., Plain Language Association International, non-English style guides) is unsurveyed.
- **No mobile-app documentation patterns.** iOS, Android, React Native help-content patterns are excluded; the UX section is web-centric.
- **No video, voice, or multimedia documentation.** Modern docs surfaces include screencasts, voice agents, and interactive demos that aren't covered.
- **No documentation-as-product KPIs literature.** The "doc team as product team" framing is asserted but the quantitative literature on how to instrument and measure that org structure was not surveyed.

**Source-type gaps:**

- **Peer-reviewed UX onboarding evidence.** The 25%/34% Reforge activation-to-revenue numbers are widely cited but trace to Reforge's own paywalled framework; the report cites Amplitude's secondary reporting of those numbers but the underlying methodology is not independently verifiable from public sources.
- **CHI / SIGCHI / CSCW on doc usability.** The CMU NatProg work (cited via the *CACM* synthesis) is the primary peer-reviewed anchor for DX-docs claims. More recent academic work was not exhaustively surveyed; the field has been comparatively quiet in the post-2018 window on developer doc usability specifically.
- **No first-party engineering writing from Apple, Atlassian, or Microsoft on their doc practices.** Each has substantial public guidance not surveyed (Microsoft's `learn.microsoft.com` is cited only as style guide, not architecture).
- **No standards-body sources on AX outside the OpenAPI Initiative and Model Context Protocol.** No IEEE / ISO / NIST coverage on agent-readable documentation patterns surfaced; the AX literature is too young.

**Confidence floor:**

- Lowest-confidence claims: the reflection-log promotion floor (synthesis, not a published result); the "AX is a distinct discipline vs sub-discipline of DX" framing (live debate, no academic consensus); the optimum AGENTS.md length (open question — Mündler shows maximalist hurts but doesn't quantify the minimum); the activation-rate / aha-moment lift numbers (vendor-reported, paywalled source).
- What would raise these to H: peer-reviewed empirical work specifically on AX surfaces (one paper exists for AGENTS.md; nothing comparable for llms.txt, SKILL.md activation, or content-negotiation); an independent replication of Mündler's findings on a different agent / repo set; controlled studies of the "describe minimal requirements" recommendation at varying granularities.

**What would change this report:**

- A peer-reviewed comparative study of DX, UX, and AX doc patterns sharing measurable outcomes (developer time-to-first-success, end-user activation rate, agent task success) would substantially sharpen §4.5 and §5.
- A second peer-reviewed AX-evaluation paper from a non-LogicStar team would strengthen confidence in the Mündler-style minimalism finding.
- A formal commitment from a major LLM provider to consume `/llms.txt` at inference time (not just on prompt) would change §4.4 Bucket A from "publishing convention" to "standard."
- A canonical resolution to the AGENTS.md-vs-Skills positioning question — whether they are complements or competitors at the design level — would resolve §5.1 and §5.3.
- A major MCP version revision (the spec is actively evolving) could change the §4.4 "schema-as-docs" framing materially.

---

*Generated using the topic-research skill (deep-dive depth, Guided Draft mode). Methodology grounded in the sources listed in `skill.json.inspired_by`.*
