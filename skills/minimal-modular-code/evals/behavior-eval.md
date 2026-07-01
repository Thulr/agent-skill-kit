# Minimal Modular Code Behavior Eval

These cases test the semantic contract that "minimal" means concise, reused,
modular, and safe rather than shortcut-driven. `trigger-evals.json` checks
activation routing; this fixture checks output behavior.

## Files

- `behavior-cases.json` defines the prompts, expected behavior, thulr criteria,
  and paired good/bad examples for calibration.
- `scripts/run-minimal-modular-behavior-eval.py` emits thulr JSONL traces from
  either fixture answers or Codex-via-pi answers. The `with-skill` arm injects
  `SKILL.md` plus the relevant playbooks as runtime context so the comparison
  measures Codex using the skill, not merely having it installed.
- `scripts/check-minimal-modular-behavior-evals.py` validates the fixture shape
  in this skill's static check.

## Criteria

- `reuse_first`
- `shortcut_resistance`
- `deletion_safety`
- `legibility`
- `scope_control`
- `boundary_discipline`
- `right_sizing`

## Cheap Fixture Check

Run without model calls:

```sh
python3 scripts/check-minimal-modular-behavior-evals.py
python3 scripts/run-minimal-modular-behavior-eval.py --agent calibration --out /tmp/minimal-modular-calibration.jsonl
thulr inspect-trace --trace /tmp/minimal-modular-calibration.jsonl
```

The calibration trace includes one known-good and one known-bad output per case,
so thulr can measure true negatives instead of hiding an always-pass judge.

## Codex Skill A/B

Run the same prompts without the skill and with the skill:

```sh
python3 scripts/run-minimal-modular-behavior-eval.py \
  --agent without-skill \
  --out .thulr/traces/minimal-modular-without-skill.jsonl
thulr inspect-trace --trace .thulr/traces/minimal-modular-without-skill.jsonl
thulr judge \
  --trace .thulr/traces/minimal-modular-without-skill.jsonl \
  --out .thulr/runs/minimal-modular-without-skill.json

python3 scripts/run-minimal-modular-behavior-eval.py \
  --agent with-skill \
  --out .thulr/traces/minimal-modular-with-skill.jsonl
thulr inspect-trace --trace .thulr/traces/minimal-modular-with-skill.jsonl
thulr judge \
  --trace .thulr/traces/minimal-modular-with-skill.jsonl \
  --out .thulr/runs/minimal-modular-with-skill.json
```

Compare deltas:

```sh
thulr compare \
  .thulr/runs/minimal-modular-without-skill.json \
  .thulr/runs/minimal-modular-with-skill.json
```

## Latest A/B Result

Run on 2026-07-01 with the same 8 behavior cases:

- **Control:** Codex via `pi`, `--no-skills`, trace
  `.thulr/traces/minimal-modular-without-skill-v8.jsonl`, judged run
  `.thulr/runs/minimal-modular-without-skill-v8.json`.
- **Candidate:** Codex via `pi` with `minimal-modular-code`, trace
  `.thulr/traces/minimal-modular-with-skill-v12.jsonl`, judged run
  `.thulr/runs/minimal-modular-with-skill-v12.json`.
- **Subject model:** `openai-codex` / `gpt-5.5`, `--thinking off`, no tools,
  no context files.
- **Judge:** `thulr judge` using embedded `pi`, model
  `openai-codex/gpt-5.4-mini`, single sample.

`thulr compare` result:

| Dimension | No skill | With skill | Delta |
| --- | ---: | ---: | ---: |
| Aggregate pass rate | 82.8% | 100.0% | +17.2% |
| Aggregate score | 0.84 | 0.99 | +0.15 |
| `criterion` | 75.0% / 0.83 | 100.0% / 0.99 | +25.0% / +0.15 |
| `deletion_safety` | 0.0% / 0.00 | 100.0% / 1.00 | +100.0% / +1.00 |
| `shortcut_resistance` | 75.0% / 0.73 | 100.0% / 0.99 | +25.0% / +0.25 |
| `right_sizing` | 85.7% / 0.84 | 100.0% / 0.98 | +14.3% / +0.14 |
| `boundary_discipline` | 100.0% / 0.99 | 100.0% / 1.00 | +0.0% / +0.01 |
| `legibility` | 100.0% / 1.00 | 100.0% / 0.99 | +0.0% / -0.01 |
| `reuse_first` | 100.0% / 0.98 | 100.0% / 0.99 | +0.0% / +0.01 |
| `scope_control` | 100.0% / 0.96 | 100.0% / 0.98 | +0.0% / +0.02 |

The control failed the safety-net deletion case and overbuilt one notifier boundary case.
The with-skill run passed all 29 judged verdicts. Treat this as a live, single-sample
model-graded result rather than a deterministic benchmark; both traces were judge-grade,
but they do not yet include token/cost telemetry.

For the first A/B, read the deltas rather than treating this as a regression
gate: the no-skill run is the control, not the champion. Once the with-skill run
is trusted, baseline it and gate future skill changes against that champion:

```sh
thulr baseline \
  .thulr/runs/minimal-modular-with-skill.json \
  .thulr/runs/minimal-modular-baseline.json

thulr \
  --score-guardrail reuse_first \
  --score-guardrail shortcut_resistance \
  --score-guardrail deletion_safety \
  --score-guardrail legibility \
  --score-guardrail scope_control \
  --score-guardrail boundary_discipline \
  --score-guardrail right_sizing \
  gate \
  .thulr/runs/minimal-modular-baseline.json \
  .thulr/runs/minimal-modular-candidate.json
```
