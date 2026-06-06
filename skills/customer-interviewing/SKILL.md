---
name: customer-interviewing
description: Use to plan, sharpen, run, or make sense of customer discovery interviews — plan an interview (set a learning goal, choose who to talk to, write a screener, build a recruiting cadence), critique and rewrite questions that lead, pitch, or fish for compliments, coach the live conversation (rapport, silence, probing, asking for a real commitment), or synthesize raw notes into an evidence-backed interview snapshot. Triggers on 'are these good interview questions', 'plan customer/discovery interviews', 'how do I run a user interview', 'who should I talk to', 'how do I make sense of my interviews', 'rewrite this leading question'. Do NOT use to validate a market or decide whether to build something (use research), to usability-test a built interface or flow (use ux-audit), or to write up findings as a polished memo or report (use writing-design).
license: MIT
---

# Customer Interviewing

Generative, one-to-one discovery conversations — planning who to talk to and why,
keeping questions honest, running the live session, and turning what you heard into
evidence. Provenance and grounding sources live in `skill.json`; this file is
runtime routing only.

**Produces:** an `interview-plan.md` (prep) or an `interview-snapshot.md`
(synthesize); the `critique-questions` and `conduct` intents transform the user's
own questions, transcript, or plan in place.

## Core principle

**Trust what people did, not what they say they'll do.** A discovery interview is a
generative instrument: it is good for surfacing real problems, the words people use,
and the context around a behavior — and weak as proof. Past-behavior detail is
evidence; predictions, compliments, and feature wishes are not. The interviewer's
job is to stay out of the way of the truth.

## Activation

- **Bare invocation** (`"use customer-interviewing"`, `"help me with user
  interviews"`): load `references/intent-router.csv` and show the intent menu
  (prep / critique-questions / conduct / synthesize), then offer the mode choice.
  Wait. No file inspection, network calls, or writes.
- **Concrete invocation** with an intent inferable: skip to Workflow step 2.
- **Ambiguous concrete invocation**: ask one question to fix the intent (are we
  planning, fixing questions, running it, or making sense of it?) before anything else.

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`. Route the prompt to one of:
   `prep`, `critique-questions`, `conduct`, `synthesize`. Ambiguous → ask once.
2. **Load only that row.** Read the chosen row's `detail_files` (one playbook) and
   `templates`. Do not load the other playbooks.
3. **Anchor the work.** Name the learning goal tied to a real decision and the target
   segment. If neither is known and the intent is `prep`, establish them first; for
   the other intents, ask only if their absence blocks the move.
4. **Apply the playbook.** Use its heuristics; prefer a concrete rewrite, probe, or
   move over generic advice. Watch the playbook's named common failures.
5. **Emit output.** `prep` → `templates/interview-plan.md`. `synthesize` →
   `templates/interview-snapshot.md`. `critique-questions` and `conduct` return the
   reworked material inline with the reasoning, no template.
6. **Hold the evidence boundary.** Separate what a person *did* (behavioral evidence)
   from what they *said they would do* (a claim). Do not present interview enthusiasm
   as validation; for a real bet, recommend triangulating with an experiment or
   behavioral data (that is `product-discovery`/`research` territory, not this skill).

## Modes

Guided Draft (default — propose, then refine with the user), Autopilot (make
conservative assumptions; stop only for missing inputs), Grill Me (one question at a
time when the goal, segment, or material is unclear). Offer the mode at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the learning goal and the segment, keeps the participant doing
most of the talking, and keeps evidence separate from claims. Question work shows the
before and the rewritten version with the reason. Synthesis points at specific
behavior, names at least one disconfirming signal where one exists, and never asks a
reader to re-derive the insight from raw notes.

## Reference map

- `references/intent-router.csv` — one-layer router (intent → playbook + templates).
- `references/playbooks/prep.md` — learning goal, segment, screener, recruiting, cadence.
- `references/playbooks/critique-questions.md` — diagnose and rewrite questions; spot misleading data.
- `references/playbooks/conduct.md` — rapport, silence, probing, asking for commitment.
- `references/playbooks/synthesize.md` — interview snapshot and cross-interview patterning.
- `templates/interview-plan.md` — `prep` output shape.
- `templates/interview-snapshot.md` — `synthesize` output shape.
- `evals/` — activation cases, static checks, trigger evals.
- `skill.json` — provenance, grounding sources, version, status.
