# Source Safety Review

## Core Question

Does the skill transform source ideas into reusable behavior, or does it
reproduce the source?

## Pass Conditions

- `skill.json.inspired_by` carries concise provenance.
- `SKILL.md` contains runtime instructions, not source marketing.
- References paraphrase ideas into frameworks, rubrics, workflows, or examples.
- Public grounding references are concise and operational: they map source
  families to heuristics, caveats, intents, or validation criteria.
- Public grounding references are reachable through
  `references/intent-router.csv` and loaded only for relevant intents.
- The skill does not provide a substitute for the book, movie, article, or talk.
- Research claims have enough provenance in local dossiers or user-provided
  notes.

## Block Conditions

- Long quotes, dialogue, lyrics, scripts, worksheets, or chapter summaries.
- Distinctive source phrasing copied into runtime instructions.
- Author biographies, further-reading sections, long bibliographies, or
  source-by-source explainers in `SKILL.md`.
- Public grounding files that summarize the source rather than helping the
  agent execute the skill.
- A skill organized around source fandom rather than user capability.
- Medical, legal, financial, or mental-health overclaiming without boundaries.
- A claim of official endorsement without evidence.

## Sensitive Domains

For mental health, medical, legal, financial, or other high-stakes domains:

- frame the skill as support, reflection, preparation, or education
- avoid diagnosis, treatment, legal advice, or financial advice
- include escalation boundaries when harm, crisis, or professional judgment is
  involved
- prefer conservative wording and validation
