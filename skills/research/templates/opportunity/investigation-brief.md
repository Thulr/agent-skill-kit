# Investigation Brief — <area> for <opportunity-slug>

> Output of the `investigate` intent. One brief per area; the area's
> artifact (e.g., `market-sizing.md`, `competitor-map.md`) is
> embedded or linked at the bottom. When `investigate` runs with
> surface = `all`, one of these is produced per area.

## Opportunity statement

<one-line statement>

## Area

<one of: market | customer | competitive | domain | technical | data
| operational | financial | legal | channel | gtm | stakeholder |
risk | trend>

## Persona lens

<single lens: founder | operator | investor | skeptic, OR
multi-lens with each lens's findings preserved>

## Sources cited

| # | Source | Type (official / interpretive / critical / applied) | Confidence (H/M/L) |
|---|---|---|---|
| 1 | <source, link> | <type> | <H/M/L> |
| 2 | … |  |  |
| 3 | … |  |  |

(Aim for ≥3 sources spanning at least 2 types. If a source type is
empty, explain why in Open Questions.)

## Heuristics applied

From `references/opportunity/playbooks/<area>.md` — list which heuristics were
applied and what each surfaced.

- **<heuristic from playbook>** — finding (severity / confidence)
- **<heuristic from playbook>** — finding (severity / confidence)
- …

## Findings

Numbered findings with confidence tags and source citations.

- F-1 (H): <finding>. Source: <#1 above>. Implication: <what changes
  downstream>.
- F-2 (M): <finding>. Source: <#2 above>. Implication: <…>.
- F-3 (L): <finding>. Source: <#3 above>. Implication: <…>. **Auto-
  promoted to Assumption + test in the F/A/D/R fold below.**

## Stated vs revealed (customer / market only)

If applicable: tag each behavioral claim.

| Claim | Stated / Revealed | Source | Confidence |
|---|---|---|---|
| <claim> | <stated / revealed> | <source> | <H/M/L> |

Any stated-only claim is M-ceiling; auto-promotes to Assumption + test
in F/A/D/R if load-bearing.

## Lens disagreements (multi-lens runs only)

| Claim | Founder lens | Operator lens | Investor lens | Skeptic lens |
|---|---|---|---|---|
| <claim> | <view> | <view> | <view> | <view> |

Preserve disagreements; do not average.

## F/A/D/R fold (for this area)

### Facts

- <observed fact, source, confidence H/M/L>
- …

### Assumptions

- <assumption, leverage (low/med/high), falsifiable test, deadline>
- …

### Decisions

- <decision this area's findings force on the broader opportunity:
  scope-cut / re-segment / re-price / re-channel / re-architect>
- …

### Risks

- <risk, category (assumption/market/execution/technical/operational/
  financial/legal/platform/fraud/reputation/concentration), severity
  (0–4), likelihood (L/M/H), mitigation, owner>
- …

## Next falsifiable test

<one experiment, ideally <1 week, that closes the highest-leverage
assumption above. Name the success threshold, deadline, owner.>

## Open questions

- <question that surfaced but was not resolved in this pass>

## Embedded artifact

See `<artifacts/<area-artifact>.md>` for the structured deliverable.
Or paste it inline below if a single output is desired.

---

<paste filled-in area artifact here if combining brief + artifact>
