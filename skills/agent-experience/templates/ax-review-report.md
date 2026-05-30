# Agent Experience Review — <scope>

## Summary

- **Route:** <ax-docs | ai-sdk | repo-readiness | audience-conflicts>
- **Intent:** <audit | design | debug>
- **Surface inspected:** <llms.txt / AGENTS.md / SDK / docs tree / …>
- **Primary audience:** agent (<which harnesses: Claude Code / Cursor / Codex / …>)
- **Secondary / harmed audiences:** <human personas or none>
- **Overall risk:** <low | medium | high | critical>

## Evidence inspected

- <file / source / path / link inspected>
- <eval / trace / agent-run / support report, if any>
- **Evidence gaps:** <unknowns that limit confidence>

## Findings

| ID | Severity | Surface | Finding | Evidence | Recommendation | Verification |
|---|---:|---|---|---|---|---|
| AX-001 | <0-4> | <surface> | <mechanism an agent trips on> | <quote/path/signal> | <fix> | <test/check/eval> |

## Audience conflicts

- <conflict if any: audience helped, audience harmed, proposed resolution per
  audience-matrix conflict rule>

## Hand-offs

- <if the fix is build/harden/measure, name the arm skill and the scoped task:
  project-agentification (harden) / evidence-driven-agent-rules (promote) /
  eval-flywheel (instrument)>

## Prioritized fixes

1. <highest-leverage fix and owner>
2. <next fix>
3. <measurement, gate, or eval>

## Verification plan

- <retrieval eval / trigger-rate check / cold-start example run / schema
  validation / agent task-success measurement>

## Grounding

- <source names from skill.json.inspired_by relevant to the applied playbook(s)>
