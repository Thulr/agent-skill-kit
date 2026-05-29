# Search strategy

How to plan and execute the literature search before synthesis.
Without an explicit plan, the report drifts toward whatever sources
the first few queries happened to surface — biased toward popular,
recent, and vendor-aligned content.

## 1. Convert the topic into search-ready form

Start from the one-sentence research question. Extract:

- **Concept terms:** the nouns that name what the topic is *about*
  (e.g., "developer documentation," "API onboarding").
- **Synonyms and variants:** what other terms might index the same
  topic (e.g., "docs UX," "DX," "technical writing," "tech writer").
- **Adjacent terms:** related concepts that often co-occur (e.g.,
  "DevRel," "developer marketing," "API design").
- **Excluded terms:** terms that look related but aren't (e.g.,
  "documentation" alone is too broad — exclude HR/legal docs).

## 2. Choose source types by topic shape

Not every topic is best served by the same source mix.

| Topic shape | Source mix |
|---|---|
| Empirical, established field | Peer-reviewed first, then secondary literature, then practitioner accounts. |
| Emerging tech / practice | Industry reports, conference talks, expert blogs, primary docs from vendors — peer-reviewed lags. |
| Policy / regulation | Standards bodies, agency publications, legal commentary, primary statute/regulation text. |
| Craft / design discipline | Books, long-form essays, practitioner case studies, prominent practitioners' blogs. |
| Quantitative / market | Reports from independent analysts (e.g., Gartner, Forrester), primary financial filings, government statistics. |

When in doubt, mix source types and surface the mix in the search
strategy section of the report — it lets readers judge bias.

## 3. Pick search venues

- **Web search** — broad coverage, includes industry sources and
  practitioner content. Use multiple search engines if availability
  allows; results overlap less than expected.
- **Citation graphs** — Google Scholar, Semantic Scholar — for forward
  and backward citation chasing (snowballing).
- **Direct archives** — arXiv for ML/CS, SSRN for econ/policy,
  PubMed for medical, IEEE/ACM for engineering.
- **Standards bodies** — IEEE, ISO, IETF, W3C for technical standards.
- **Primary sources** — vendor docs, source-code repos, conference
  proceedings — when the topic is about a specific technology or product.

## 4. Snowball for deep-dive

Database queries miss sources. Citation chasing catches them.

- **Backward snowballing:** for each high-quality anchor source, scan
  its references for relevant cited works. Follow citations one or
  two hops deep until the surfacing rate of new relevant sources drops.
- **Forward snowballing:** for each anchor source, find papers that
  *cite it* (via Google Scholar, Semantic Scholar). This surfaces
  newer work building on the anchor.
- **Stop when:** new sources start citing already-found sources and
  stop adding new claims. This is the "saturation" stop criterion.

## 5. Document exclusions explicitly

Every exclusion is a coverage choice. Surface it in the report's
search strategy section so readers can judge the bias:

- **Time-bounded:** "only sources from the last 5 years" — what
  seminal earlier work was excluded?
- **Language-bounded:** "English-only" — what non-English work was
  excluded?
- **Type-bounded:** "peer-reviewed only" — what practitioner knowledge
  was excluded?
- **Vendor-bounded:** "no vendor marketing" — but vendor docs that
  describe primary product behavior are often the best primary source.

## 6. Set a stop criterion before searching

Open-ended search expands forever. Pick one before starting:

- **Source count:** target ~5 (brief), ~15-20 (survey), ~30+ (deep-dive).
- **Time budget:** N minutes/hours of searching, then synthesize.
- **Saturation:** stop when new searches return already-found sources
  more than 80% of the time.
- **Decision deadline:** stop when the report has to be shipped.

State which criterion was used in the report.
