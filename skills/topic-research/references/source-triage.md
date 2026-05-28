# Source triage

Not all sources are equal. Triage filters the search output into
sources worth citing, sources worth reading-but-not-citing, and
sources to discard. The goal is to make the report's citation list
load-bearing — every cited source should survive scrutiny.

## Triage dimensions

Rank each candidate source on four axes. None alone disqualifies a
source; together they shape the citation list.

### 1. Primacy — how close is the source to the original observation?

- **Primary:** the original empirical study, original dataset,
  original code, original specification, original financial filing,
  original interview transcript, original product documentation.
- **Secondary:** a review, synthesis, summary, news article, or
  textbook reporting on primary sources.
- **Tertiary:** encyclopedic content — Wikipedia, glossaries,
  textbook glossaries. Useful for orientation and terminology, rarely
  for load-bearing claims.

**Prefer primary** for empirical or factual claims. Secondary is
acceptable for orientation, current-state summaries, and synthesis
context. Tertiary is acceptable for terminology and background only.

### 2. Recency — how dated is the source relative to the topic?

- **Fresh:** within the last 1–2 years for fast-moving fields
  (LLMs, web dev, cryptography), 3–5 years for slower fields, 10+
  years for stable fields (most pure math, classical sociology).
- **Recent:** within the typical cycle of the field above.
- **Dated:** older than the typical cycle, but the claim still holds.
- **Seminal:** old but foundational; the claim depends on it
  regardless of date.

Recent ≠ better. Seminal sources are load-bearing even if dated.
Dated sources on a fast-moving topic are a red flag.

### 3. Independence — is the source aligned with what it's reporting on?

- **Independent:** no financial, professional, or political stake
  in the claim being true.
- **Semi-independent:** some alignment (e.g., academic researcher
  whose career thesis depends on the claim) but published under
  peer review or other oversight.
- **Vendor-aligned:** the source has a direct stake in the claim —
  product vendor describing their own product, analyst firm paid by
  the vendor, advocacy group on its own issue. Useful for primary
  facts about the vendor's product; not load-bearing for claims
  about *comparative* performance, *market* trends, or *broader*
  implications.

Mark vendor-aligned sources explicitly. The report should never let
a vendor-aligned source be the only support for a claim *about*
that vendor's category.

### 4. Vetting — what review did the source go through before publication?

- **Peer-reviewed:** journal or peer-reviewed conference. Highest vetting.
- **Institutional:** standards bodies, agency reports, conference
  proceedings without formal peer review. Strong vetting.
- **Editorial:** trade publications, industry reports from
  established analyst firms, major newspapers. Some vetting.
- **Editor-only:** professional blogs, op-eds, expert commentary
  on personal sites. Author's reputation is the vetting.
- **Unvetted:** anonymous forum posts, social media, AI-generated
  content. Generally not citable, but occasionally useful as a primary
  source on community sentiment.

## Triage decisions

After ranking each source on all four axes:

- **Cite:** primary or secondary, recent or seminal, independent or
  marked-vendor-aligned, peer-reviewed or institutional.
- **Read but don't cite as load-bearing:** anything weaker on one
  or more axes that still provides orientation, context, or
  alternative perspective. Use for synthesis, mark as background.
- **Discard:** unvetted, vendor-aligned-and-not-primary, tertiary
  for empirical claims, dated-on-fast-moving-topic.

## When sources conflict

When two well-triaged sources disagree, both belong in the report.
Surface the disagreement explicitly in the "Key debates" section.
Picking one and burying the other is editorializing.

## Quantity vs quality

A 10-source report with 10 well-triaged citations beats a 40-source
report padded with tertiary and vendor-aligned filler. Target the
source-count for the depth mode (5 / 15–20 / 30+), but every cited
source must pass triage. Cut padding rather than ship weak citations.
