# Source Dossier: Customer Interviewing (Mom Test · Interviewing Users · Continuous Discovery Habits)

Phase 2 artifact. Private research trail. Public skill files paraphrase only — never reproduce this verbatim.

## Dossier ID

- Slug: `customer-interviewing`
- Linked intake brief: `.agents/state/intake-briefs/customer-interviewing.md`

## Source Identity

- Titles / Creators:
  - *The Mom Test* — Rob Fitzpatrick (2013), book
  - *Interviewing Users* (1st 2013 / 2nd ed. 2023) — Steve Portigal, book
  - *Continuous Discovery Habits* — Teresa Torres (2021), book (interview & synthesis chapters)
- Type: books (+ author sites, talks, practitioner write-ups)
- Source slug: `customer-interviewing`
- Research date: 2026-06-05

## Research Sources

| Type | URL | Notes | Confidence |
|---|---|---|---|
| official | momtestbook.com | Fitzpatrick's official book site (factual ID, framing). | H |
| official | portigal.com/Books/interviewing-users-2/ | Portigal's official page for the 2nd edition. | H |
| official | producttalk.org/2022/12/customer-interviews/ ; producttalk.org/glossary-discovery-interview-participants/ | Torres' own site: recruit → ask → synthesize; participant definitions. | H |
| interpretive | mtlynch.io/book-reports/the-mom-test/ ; readingraphics.com/book-summary-the-mom-test/ ; dev.to/egepakten Ch.5 | Practitioner notes: 3 rules; bad-data types; commitment & advancement. | H |
| interpretive | medium.com design-bootcamp "What I Learned from Interviewing Users"; theproductmanager.com Portigal | Portigal techniques: rapport, silence, broad→specific, follow-ups, listening. | H |
| interpretive | evansamek substack; shortform.com/blog/continuous-discovery-habits; martinlugton.com | Torres: story-based interviewing, interview snapshot, experience map, weekly cadence. | H |
| critical | saasvalidation.tech "...optimize for confidence, not accuracy" | Structural critique: interviews simulate decisions; say≠do; interviewer effect; confirmation bias. | M |
| critical | layer3pm.com / userinterviews.com continuous-discovery-research-report | Practical critique of weekly cadence: hardest part is sustainably finding people; time cost. | M |
| applied | userinterviews.com (Portigal applied to remote research); kromatic.com real-startup-book generative research | Applied interviewing/recruiting in real research ops. | M |
| applied | producttalk.org automating-customer-interviews (Zonar); ethn.io (screeners) | Applied: participant pipeline automation; screener surveys to find/qualify the right people. | M |

**Confidence rules.** No **L** rows on load-bearing claims. Critical/applied rows are **M** (secondary synthesis, not primary text) but none is the sole support for a load-bearing heuristic — each is corroborated by ≥1 H interpretive row.

## Paraphrased Concepts

- **Talk about their life, not your idea** (Mom Test rule 1): keep questions on the person's real world and experience; your concept stays out of the conversation so you don't fish for approval. (official/interpretive)
- **Specific past events, not hypothetical futures** (rule 2): ask what actually happened the last time, not what someone imagines they'd do. (interpretive)
- **Listen more than you talk** (rule 3): the participant should hold most of the airtime; the interviewer's job is to draw them out. (interpretive)
- **Three kinds of misleading data**: compliments, vague generalities ("I always/usually…"), and the person's own feature ideas/opinions — none is evidence; only concrete behavior and committed action are. (interpretive)
- **Commitment & advancement**: a conversation is going somewhere only when the person gives up something they value — time, reputation, or money — or takes a real next step in your funnel; verbal enthusiasm with no commitment is noise. (interpretive — dev.to Ch.5, readingraphics)
- **Rapport over interrogation** (Portigal): make it a conversation that grows, create space the person wants to fill, rather than marching through a fixed question list. (interpretive)
- **Embrace silence** (Portigal): after a question, wait; don't rescue the pause with suggested answers or multiple-choice prompts — the reflective gap is where the richer answer surfaces. (interpretive)
- **Broad to specific + follow the thread** (Portigal): open wide, then probe; a follow-up signals "that matters, tell me more" and keeps the person engaged. (interpretive)
- **Story-based / "excavate the story"** (Torres): instead of asking about behavior in general, anchor on one recent instance ("tell me about the last time…") and walk it chronologically to get behavioral detail rather than self-report. (official/interpretive)
- **Interview snapshot** (Torres): a one-page synthesis of a single interview (including an experience map of that person's specific story) so colleagues can absorb the learning without reading raw notes; raw-notes/recording dumps are an anti-pattern. (official/interpretive)
- **Recruit a pipeline, don't re-recruit each time** (Torres applied): sustain a weekly cadence by automating sourcing — in-product research opt-ins, an advisory panel, partnering with sales/CS — and use screeners to qualify the right participants. (official/applied)

## Reusable Behaviors

- Behavior: **Diagnose and rewrite a draft question** that leaks the idea, asks for a hypothetical, or fishes for a compliment into a question about a specific past event. Derived from: Mom Test rules 1–2 (interpretive).
- Behavior: **Flag misleading-data responses** (compliments / generalities / unprompted feature requests) in notes or a transcript and redirect to "when did this last happen?" Derived from: three-kinds-of-misleading-data (interpretive).
- Behavior: **Score whether a conversation advanced** by checking for a real commitment (time/reputation/money) or funnel next step, not verbal enthusiasm. Derived from: commitment & advancement (interpretive).
- Behavior: **Plan a session for silence and probing** — open broad, prepare follow-up prompts, and explicitly leave pauses unfilled. Derived from: Portigal rapport/silence/broad-to-specific (interpretive).
- Behavior: **Convert a question list into a story prompt** — replace "what do you look for in X" with "walk me through the last time you did X." Derived from: Torres story-based interviewing (official/interpretive).
- Behavior: **Synthesize one interview into a snapshot** with an experience map and a few evidence-tagged takeaways instead of forwarding raw notes. Derived from: Torres interview snapshot (official/interpretive).
- Behavior: **Stand up a recruiting plan** — pick a source (opt-in, panel, sales/CS), write a short screener with disqualifying criteria, and set a sustainable cadence target. Derived from: Torres recruiting applied (official/applied).
- Behavior: **Set a learning goal and segment before writing questions** so the session targets a decision, not a grab-bag of curiosity. Derived from: discovery-interview framing across all three (interpretive).

## Critical / Dissenting Takes

- Critique: interviews can **optimize for confidence, not accuracy** — they ask people to simulate a decision rather than make one, so a confident "I'd use that" may not predict behavior. (saasvalidation.tech, M)
- Limitation: **interviewer effect & confirmation bias** — question wording, order, and the interviewer's nods/framing partly generate the signal; an invested founder hears what they hoped to hear. (saasvalidation.tech, M)
- Limitation: **say ≠ do** — humans are poor predictors of their own future behavior and tend toward agreeableness, especially with strangers; this is exactly why the sources push past-behavior questions, but it bounds what interviews can prove. (critical search, M)
- Failed application / cost: the **weekly continuous cadence is hard to sustain** — the binding constraint is sourcing participants reliably, and small teams often can't hold it without recruiting automation. (layer3pm/userinterviews, M)
- Steelman boundary (hypothesis): interviews are a **generative** instrument — good for surfacing problems, language, and context; weak as a **confirmatory/quantitative** instrument. Triangulate big bets with behavioral data or an experiment (→ future `product-discovery`), don't treat interview enthusiasm as validation.

## Paraphrase Audit

- Behavior "rewrite a leaky/hypothetical question" — source idea "talk about their life, not your idea / ask about specifics in the past" — paraphrased to "question about a specific past event" — distinctive? **no** (framework named, own wording).
- Behavior "flag misleading-data responses" — source idea "compliments, fluff, ideas" — paraphrased to "compliments / generalities / unprompted feature requests" — distinctive? **no**.
- Behavior "score whether a conversation advanced" — source idea "commitment and advancement / time, reputation, money" — paraphrased, concept names retained as factual framework labels — distinctive? **no**.
- Behavior "plan for silence and probing" — source idea "embrace silence / broad to specific" — paraphrased to "leave pauses unfilled; open broad then probe" — distinctive? **no**.
- Behavior "convert to story prompt" — source idea "tell me about the last time / excavate the story" — the trigger phrase "tell me about the last time" is a short, common, factual technique label, used once as illustration, not reproduced as a script — distinctive? **no** (kept minimal).
- Behavior "snapshot synthesis" — source idea "interview snapshot / experience map" — paraphrased as "one-page per-interview synthesis with an experience map" — distinctive? **no** (these are named artifacts/terms, identified factually).
- No reproduced question lists, worksheets, chapter summaries, or long quotes. Distinctive coined terms (interview snapshot, the Mom Test, commitment & advancement) are *named and attributed*, not redefined as our own.

## Candidate Skills

| Candidate | Pack | Shape | Action | Reason |
|---|---|---|---|---|
| `customer-interviewing` | discovery | single-layer | create skill | 4 orthogonal intents (prep / critique-questions / conduct / synthesize), ~200–500 words each, shared vocabulary (evidence, past behavior, commitment). |
| (deferred) opportunity/experiment work | discovery | two-level | defer → `product-discovery` | OST, assumption testing, MVP — separate skill #2, not interviewing craft. |

## Copyright And Safety Notes

- Copyright posture: paraphrasing into operational methods is sufficient; the sources' distinctive value is their phrasing/exercises, which we do **not** reproduce. Named coined terms are attributed in `skill.json.inspired_by`, not redefined verbatim. No reproduced question banks or scripts.
- Sensitive-domain: not regulated. One ethics heuristic worth surfacing: human-subjects basics — informed consent, recording permission, no manipulation/coercion of respondents. Guidance, not a blocker.
- Narrowing: keep this skill to live 1:1 generative discovery conversations; surveys, usability task-testing (`ux-audit`), and desk/opportunity research (`research`) stay out.

## Open Questions

- None blocking. (Critical/applied rows are M but corroborated; no L on a load-bearing claim.)
- Phase 3 decision to confirm: does `synthesize` stay one intent, or split into "single-interview snapshot" vs "across-interviews patterning"? Lean: one intent, both as heuristics, to honor the user's "fewer/broader" preference and avoid a thin 5th intent.

## Gate

> **Phase 2 → Phase 3 gate.** Does the research cover the sources faithfully? Any missing source types, weak confidence, or open questions to resolve before we plan? Reply `go` to advance to Phase 3 (Plan).
