"""Level 4 System Benchmarking template.

Use when the product needs release-grade regression protection: model swaps,
prompt bundle changes, tool changes, or platform-wide agent upgrades. The loop
replays fixed tasks, compares against a baseline, and fails the release when a
GUARDRAIL slice regresses.

Two design rules from the eval literature are wired in:

1. No single "god metric". Cases are tagged with a `failure_mode` (slice) and a
   `metric_role` of "guardrail" (must not regress -> blocks the release) or
   "north_star" (capability/aspirational -> reported, never blocks). A red
   north-star slice is information; a red guardrail slice is a ship-blocker.
   (god-metric-vs-decomposed-evaluators; capability-eval-vs-regression-eval)
2. Per-case pass rate is NOT end-to-end reliability. Because per-step
   reliability multiplies across a multi-step agent (the "march of nines"), a
   0.95 per-case bar can still mean a low end-to-end success rate. Calibrate
   GUARDRAIL_MIN_PASS against trajectory-level reliability, not per-case.

CI parses this with `python3 -m py_compile`; no external imports required.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean


CASES_PATH = Path("ai-ops/benchmark-cases.json")
BASELINE_PATH = Path("ai-ops/baseline-results.json")
CURRENT_PATH = Path("ai-ops/current-results.json")
REPORT_PATH = Path("ai-ops/benchmark-report.md")

# Guardrail slices must clear this floor AND not regress vs baseline. Calibrate
# against END-TO-END reliability, not per-case (march of nines).
GUARDRAIL_MIN_PASS = 0.95
MAX_COST_MULTIPLIER = 1.10
MAX_LATENCY_MULTIPLIER = 1.15


def run_system_on_case(case: dict) -> dict:
    """TODO: invoke the real agent/application for one fixed task.

    Carry the case's slice + role through to the result so scoring can
    decompose by failure mode instead of collapsing to one number.

    Return:
    {
      "id": case["id"],
      "failure_mode": case.get("failure_mode", "unspecified"),
      "metric_role": case.get("metric_role", "guardrail"),  # or "north_star"
      "passed": bool,
      "cost_usd": float,
      "latency_s": float,
      "notes": "short failure/trace pointer"
    }
    """
    raise NotImplementedError("Wire to the host agent or app entrypoint")


def _pass_rate(rows: list[dict]) -> float:
    return sum(1 for r in rows if r["passed"]) / max(len(rows), 1)


def summarize(results: list[dict]) -> dict:
    by_slice: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        by_slice[r.get("failure_mode", "unspecified")].append(r)
    slices = {
        name: {
            "metric_role": rows[0].get("metric_role", "guardrail"),
            "pass_rate": _pass_rate(rows),
            "n": len(rows),
        }
        for name, rows in by_slice.items()
    }
    return {
        "pass_rate": _pass_rate(results),
        "avg_cost_usd": mean([r["cost_usd"] for r in results]) if results else 0.0,
        "avg_latency_s": mean([r["latency_s"] for r in results]) if results else 0.0,
        "slices": slices,
    }


def compare_to_baseline(current: dict, baseline: dict) -> dict:
    cost_ratio = current["avg_cost_usd"] / max(baseline["avg_cost_usd"], 0.000001)
    latency_ratio = current["avg_latency_s"] / max(baseline["avg_latency_s"], 0.000001)

    base_slices = baseline.get("slices", {})
    guardrail_regressions: list[dict] = []
    north_star_deltas: list[dict] = []
    for name, cur in current.get("slices", {}).items():
        base_rate = base_slices.get(name, {}).get("pass_rate", 0.0)
        delta = cur["pass_rate"] - base_rate
        record = {"slice": name, "pass_rate": cur["pass_rate"], "delta": delta}
        if cur["metric_role"] == "north_star":
            north_star_deltas.append(record)  # reported, never blocks
        # Guardrail: block on the absolute floor OR a regression vs baseline.
        elif cur["pass_rate"] < GUARDRAIL_MIN_PASS or delta < 0:
            guardrail_regressions.append(record)

    return {
        "guardrail_ok": not guardrail_regressions,
        "guardrail_regressions": guardrail_regressions,
        "north_star_deltas": north_star_deltas,
        "cost_ok": cost_ratio <= MAX_COST_MULTIPLIER,
        "latency_ok": latency_ratio <= MAX_LATENCY_MULTIPLIER,
        "cost_ratio": cost_ratio,
        "latency_ratio": latency_ratio,
    }


def write_report(current: dict, baseline: dict, verdict: dict) -> None:
    gate_pass = verdict["guardrail_ok"] and verdict["cost_ok"] and verdict["latency_ok"]
    lines = [
        "# System Benchmark Report",
        "",
        f"- Overall pass rate: {current['pass_rate']:.2%} (informational, not the gate)",
        f"- Cost ratio: {verdict['cost_ratio']:.2f}x",
        f"- Latency ratio: {verdict['latency_ratio']:.2f}x",
        f"- Release gate (guardrail slices): {'PASS' if gate_pass else 'FAIL'}",
        "",
        "## Guardrail regressions (block release)",
    ]
    if verdict["guardrail_regressions"]:
        for r in verdict["guardrail_regressions"]:
            lines.append(f"- {r['slice']}: {r['pass_rate']:.2%} (delta {r['delta']:+.2%})")
    else:
        lines.append("- none")
    lines += ["", "## North-star slices (reported, do not block)"]
    if verdict["north_star_deltas"]:
        for r in verdict["north_star_deltas"]:
            lines.append(f"- {r['slice']}: {r['pass_rate']:.2%} (delta {r['delta']:+.2%})")
    else:
        lines.append("- none")
    lines += [
        "",
        "Block the release only on guardrail regressions; treat north-star deltas as signal.",
    ]
    REPORT_PATH.write_text("\n".join(lines))


def run_benchmark() -> None:
    cases = json.loads(CASES_PATH.read_text())
    results = [run_system_on_case(case) for case in cases]
    CURRENT_PATH.write_text(json.dumps(results, indent=2))

    current_summary = summarize(results)
    baseline_summary = json.loads(BASELINE_PATH.read_text())
    verdict = compare_to_baseline(current_summary, baseline_summary)
    write_report(current_summary, baseline_summary, verdict)

    if not (verdict["guardrail_ok"] and verdict["cost_ok"] and verdict["latency_ok"]):
        raise SystemExit("Benchmark gate failed. See ai-ops/benchmark-report.md")

    print("Benchmark gate passed.")


if __name__ == "__main__":
    run_benchmark()
