# Candidate Skill Plan: customer-interviewing

Phase 3 artifact. Gate between research and any file write.

## Back-links

- Intake brief: `.agents/state/intake-briefs/customer-interviewing.md`
- Source dossier: `.agents/state/source-dossiers/customer-interviewing.md`

## Source

- Title and creator: *The Mom Test* (Rob Fitzpatrick), *Interviewing Users* (Steve Portigal), *Continuous Discovery Habits* (Teresa Torres, interview/synthesis chapters)
- Why now: skill #1 of the new `discovery` family; the catalog has no interview-craft skill.

## Recommended Pack Decisions

- Pack tag(s) used: `discovery` (also `tags`: `discovery`, `user-research`, `customer-interviews`)
- New pack created? **Yes.** Justified per pack-placement-rubric: the name is a capability domain (product discovery), not a source; it survives if any book disappears; it clusters ≥3 candidates (`customer-interviewing`, `product-discovery`, `journey-storymapping`); and it can accept future sources (talks, articles). Catalog **family** `discovery` (the README grouping) is wired in Reference Additions below — distinct from the `tags` pack.

## Draft Skill Candidates

```text
candidate:                  customer-interviewing
pack:                       discovery
shape:                      single-layer
depth:                      1
action:                     create
public_path:                skills/customer-interviewing/
dossier_ref:                customer-interviewing
audience_ref:               customer-interviewing
shape_decision:
  rubric_evidence:          Q1 = 4 distinct invocations (3–8 → single-layer). Q2 = 1 orthogonal axis (intent only; no second axis like surface/persona). Q3 = each leaf ~250–450 words (200–500 → single-layer). Q4 = shared vocabulary (evidence, past-behavior, commitment) + two reusable output templates → centralize, not flat.
  promotion_path:           Promote to two-level only if an audience axis emerges (e.g. B2B vs consumer vs internal-stakeholder interviews each needing distinct content per intent), or if `synthesize` outgrows ~1500 words splitting single-interview vs cross-interview patterning into their own routing.
  axes:                     intent  (prep | critique-questions | conduct | synthesize)
anti_pattern_check:
  - one_dim_collapsed:      yes  (4 differentiated rows, ≥3)
  - registry_routes:        yes  (each row loads a distinct detail file; templates differ — prep/synthesize carry one, critique/conduct carry none)
  - cargo_culting:          yes  (single-layer chosen on content: 4 intents × 200–500 words sharing vocabulary — not for prestige)
  - bloat_check:            yes  (SKILL.md projected <800 words; each playbook 250–450 < 1500)
  - depth_orthogonality:    N/A  (depth 1, single axis — no orthogonality claim to defend)
playbook_outline:
  - prep:
      heuristic_seeds:
        - Start from ONE learning goal tied to a real decision, plus a target segment, before writing any question.
        - Build a participant pipeline (in-product opt-in, advisory panel, sales/CS handoff) + a short disqualifying screener; set a sustainable recurring cadence, not a one-off batch.
      common_failure_seeds:
        - Recruiting whoever is easiest (friends, fans, power users) → unrepresentative, agreeable signal.
        - No learning goal, so the session drifts into a feature wishlist.
  - critique-questions:
      heuristic_seeds:
        - Rewrite idea-leaking / hypothetical / compliment-seeking questions into questions about a specific recent event ("walk me through the last time you…").
        - Tag responses that are compliments, generalities ("I usually…"), or unprompted feature requests as non-evidence and redirect to actual behavior.
      common_failure_seeds:
        - Asking "would you use / pay for this?" and treating a polite "yes" as validation.
        - Leading the witness — embedding the hoped-for answer in the question.
  - conduct:
      heuristic_seeds:
        - Open broad, then follow the thread with probes; leave silences unfilled instead of offering multiple-choice answers.
        - Aim for the participant to hold most of the airtime; close by asking for a real commitment (time / reputation / money) or a concrete next step, not "keep me posted."
      common_failure_seeds:
        - Marching through a fixed list / interviewer talking too much / rescuing every pause → shallow, agreeable answers.
        - Pitching the idea mid-interview and contaminating the signal.
  - synthesize:
      heuristic_seeds:
        - Reduce each interview to a one-page snapshot — key context, an experience map of that specific story, a few evidence-tagged takeaways — rather than forwarding raw notes/recordings.
        - When patterning across interviews, separate what people DID (behavioral evidence) from what they SAID they'd do (claims); surface disconfirming cases, don't cherry-pick supporting quotes.
      common_failure_seeds:
        - Confirmation bias — mining transcripts for quotes that support the idea you already had.
        - Dumping unsynthesized notes and expecting teammates to do the synthesis.
registry_sketch:
  layers:
    - layer: intent-router
      rows:
        - row: prep
          loads: references/prep.md ; templates/interview-plan.md
          notes: Planning BEFORE the conversation — goal, segment, recruiting, screener, cadence. Only row with the plan template.
        - row: critique-questions
          loads: references/critique-questions.md
          notes: Diagnose/rewrite a question list or transcript. No template (it transforms user input in place).
        - row: conduct
          loads: references/conduct.md
          notes: Running the live session — rapport, silence, probing, commitment. No template (in-session guidance).
        - row: synthesize
          loads: references/synthesize.md ; templates/interview-snapshot.md
          notes: AFTER the conversation — snapshot + cross-interview patterning. Only row with the snapshot template.
activation_case_seeds:
  positive:
    - prompt: "Here's my customer-interview question list — are these good questions?" -> route: critique-questions
    - prompt: "Rewrite 'would you pay for this?' into something that gives real signal." -> route: critique-questions
    - prompt: "Help me plan discovery interviews for a churn problem — who do I talk to and how many?" -> route: prep
    - prompt: "I freeze in interviews and end up pitching. How do I actually run the conversation?" -> route: conduct
    - prompt: "I did six user interviews — now what? How do I make sense of them?" -> route: synthesize
  negative:
    - prompt: "Should we build this B2B SaaS idea? Validate the market and give me a go/no-go." -> use sibling: research  because that's desk/opportunity validation ending in a decision memo, not live interview craft.
    - prompt: "Run a usability test on our checkout flow and find where users get stuck." -> use sibling: ux-audit  because that's evaluative testing of a built interface, not generative problem discovery.
    - prompt: "Turn our research findings into a polished stakeholder memo." -> use sibling: writing-design  because that's authoring/structuring a narrative document, not synthesizing interviews into evidence.
  edge:
    - prompt: "I'm about to talk to 5 users about why they churned — help me." -> activates (generative discovery); but if they actually want to evaluate a specific built flow, hand off to ux-audit.
    - prompt: "How should I interview internal stakeholders about requirements?" -> activates only if treated as discovery-style conversation craft (conduct/critique-questions); flag that respondent is internal, not a customer.
grounding_map:
  - source: The Mom Test, year: 2013
    playbooks: [critique-questions, conduct]
    contribution: Question hygiene (life-not-idea, past-not-hypothetical, listen more); commitment & advancement as the real signal.
  - source: Interviewing Users, year: 2013
    playbooks: [conduct, critique-questions]
    contribution: Conducting craft — rapport over interrogation, embracing silence, broad-to-specific probing, active listening.
  - source: Continuous Discovery Habits, year: 2021
    playbooks: [prep, synthesize]
    contribution: Recruiting a participant pipeline + sustainable cadence; story-based questions; interview snapshots & evidence-based synthesis.
reason:                     Fills a clear catalog gap (no interview skill); high-leverage, well-bounded, three canonical mutually-reinforcing sources; anchors the new discovery family.
inspired_by:                [mom-test, interviewing-users, continuous-discovery-habits]
```

## Reference Additions (cross-skill / repo infra)

This candidate introduces the new `discovery` **catalog family**, which is repo
infrastructure (not a per-skill file). Land these alongside `skills/customer-interviewing/`:

- Target: `schemas/skill.schema.json`. Add: `"discovery"` to the `metadata.family` enum. Reason: schema rejects an unknown family.
- Target: `scripts/build-catalog.py`. Add: `"discovery"` to the `FAMILIES` tuple (line ~32). Reason: build-catalog fails on a family not in the tuple, and the README generator must emit the new group.
- Target: `catalog/catalog.json`. Add: a `families` block `{id: "discovery", title: "Product discovery & planning", intro: [...]}` AND a secondary "Pick a skill" needs→skill row pointing at `customer-interviewing`. Reason: build-catalog cross-checks every catalog family has ≥1 skill and every matrix skill exists; the family block can only land once this skill exists.
- (Optional, deferred) `skills/research/skill.json` & `skills/ux-audit/skill.json`: consider a "Do NOT use for live discovery interviews → customer-interviewing" clause when those are next touched. Not required now — fencing lives in this skill's own description + negative activation cases.

## Anti-pattern self-check (rubric walk)

- [x] No CSV layer has fewer than 3 differentiated rows. (4 rows)
- [x] No registry layer whose rows all load the same files. (4 distinct detail files; templates differ)
- [x] SKILL.md projected <800 words; no playbook projected >1500 words. (~250–450 each)
- [x] Depth ≥2 orthogonality — N/A (depth 1).
- [x] Every `grounding_map.playbooks` is non-empty. (each source → ≥1 playbook; all 4 playbooks covered)
- [x] Every negative activation case names a specific sibling skill. (research, ux-audit, writing-design)
- [x] Every playbook has ≥2 heuristic seeds and ≥1 common-failure seed. (each has 2 + 2)

## Review Handoff (filled at end of Phase 5)

- Draft paths: `skills/customer-interviewing/` (SKILL.md, skill.json, references/intent-router.csv, references/playbooks/{prep,critique-questions,conduct,synthesize}.md, templates/{interview-plan,interview-snapshot}.md, evals/*); repo infra: `schemas/skill.schema.json`, `scripts/build-catalog.py`, `catalog/catalog.json`, `README.md`.
- Known risks: (1) new `discovery` family is the first non-original family — verify README renders it in order (heuristics → research → discovery → ax). (2) Boundary with `research` (opportunity validation) and `ux-audit` (usability testing) relies on description fencing + 4 negative activation cases; watch for mis-fires in practice. (3) SKILL.md author/title leak guard is per-skill; playbooks intentionally name sources in `## Grounding`.
- Suggested reviewer focus: source-safety (paraphrase audit already run — no reproduced question banks/scripts); fencing strength vs `research`/`ux-audit`; whether `synthesize` should later split single-interview vs cross-interview.
- Validation report: `.agents/state/validation-reports/customer-interviewing-phase5.md` (deterministic validator exit 0; `just check` exit 0).

## Gate

> **Phase 3 → Phase 4 gate.** Approve the plan, or revise? Reply `go` to advance to Phase 4 (Scaffold). Any rejection sends us back to Phase 2 (Research) or Phase 1 (Intake) depending on the reason.
