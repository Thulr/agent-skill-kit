# Pack Placement Rubric

## Core Model

`source -> reusable behaviors -> candidate skills -> organic capability pack`

The source suggests the behavior. The pack describes what the user needs the
agent to do.

A capability pack is a **categorization tag**, recorded in
`skill.json.tags`. It is NOT a directory layer in this repo — all skills
live at `skills/<skill-name>/` regardless of their pack. Use this rubric to
decide what to put in the `tags` field, not where the skill goes on disk.

## Candidate Shapes

- **Small focused skill**: one repeatable move, review, reframing, checklist,
  generator, or intervention.
- **Workflow skill**: multi-phase task with preparation, execution, review,
  state, templates, or checkpoints.
- **Reference addition**: improves an existing skill but does not justify a new
  skill.
- **Pack-level pattern**: shared rubric, vocabulary, template, or safety rule
  used by multiple skills in a pack.

## Create A New Pack When

- the name describes a capability domain, not a source
- the domain would still make sense if the source disappeared
- one strong skill has obvious room to grow, or two to three candidates cluster
  together
- the pack can accept future sources from books, movies, notes, talks, or
  articles

## Use An Existing Pack When

- a current pack already describes the user need
- the candidate extends an existing skill's references, rubric, or templates
- a new pack would differ only by wording

## Reject Or Defer When

- the candidate is just a source summary
- the pack name is a book, movie, person, character, title, or franchise
- the behavior is too vague to validate
- the concept would require professional advice beyond the skill's safe scope

## Decision Output

For each candidate, record:

```text
candidate:
pack:
shape:
action: create skill | update existing skill | add reference | defer | reject
reason:
source influence:
risks:
```

