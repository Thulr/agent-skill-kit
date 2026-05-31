"""Level 4 System Benchmarking template.

Use when the product needs release-grade regression protection: model swaps,
prompt bundle changes, tool changes, or platform-wide agent upgrades. The loop
replays fixed tasks, compares against a baseline, and fails the release if
guardrail metrics regress.

CI parses this with `python3 -m py_compile`; no external imports required.
"""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean


CASES_PATH = Path("ai-ops/benchmark-cases.json")
BASELINE_PATH = Path("ai-ops/baseline-results.json")
CURRENT_PATH = Path("ai-ops/current-results.json")
REPORT_PATH = Path("ai-ops/benchmark-report.md")

MIN_PASS_RATE = 0.95
MAX_COST_MULTIPLIER = 1.10
MAX_LATENCY_MULTIPLIER = 1.15


def run_system_on_case(case: dict) -> dict:
    """TODO: invoke the real agent/application for one fixed task.

    Return:
    {
      "id": case["id"],
      "passed": bool,
      "cost_usd": float,
      "latency_s": float,
      "notes": "short failure/trace pointer"
    }
    """
    raise NotImplementedError("Wire to the host agent or app entrypoint")


def summarize(results: list[dict]) -> dict:
    return {
        "pass_rate": sum(1 for r in results if r["passed"]) / max(len(results), 1),
        "avg_cost_usd": mean([r["cost_usd"] for r in results]) if results else 0.0,
        "avg_latency_s": mean([r["latency_s"] for r in results]) if results else 0.0,
    }


def compare_to_baseline(current: dict, baseline: dict) -> dict:
    cost_ratio = current["avg_cost_usd"] / max(baseline["avg_cost_usd"], 0.000001)
    latency_ratio = current["avg_latency_s"] / max(baseline["avg_latency_s"], 0.000001)
    return {
        "pass_rate_ok": current["pass_rate"] >= MIN_PASS_RATE,
        "cost_ok": cost_ratio <= MAX_COST_MULTIPLIER,
        "latency_ok": latency_ratio <= MAX_LATENCY_MULTIPLIER,
        "cost_ratio": cost_ratio,
        "latency_ratio": latency_ratio,
    }


def write_report(current: dict, baseline: dict, verdict: dict) -> None:
    gate_pass = (
        verdict["pass_rate_ok"] and verdict["cost_ok"] and verdict["latency_ok"]
    )
    REPORT_PATH.write_text(
        "\n".join(
            [
                "# System Benchmark Report",
                "",
                f"- Current pass rate: {current['pass_rate']:.2%}",
                f"- Baseline pass rate: {baseline['pass_rate']:.2%}",
                f"- Cost ratio: {verdict['cost_ratio']:.2f}x",
                f"- Latency ratio: {verdict['latency_ratio']:.2f}x",
                f"- Release gate: {'PASS' if gate_pass else 'FAIL'}",
                "",
                "Rollback if pass rate, cost, or latency exceeds gate thresholds.",
            ]
        )
    )


def run_benchmark() -> None:
    cases = json.loads(CASES_PATH.read_text())
    results = [run_system_on_case(case) for case in cases]
    CURRENT_PATH.write_text(json.dumps(results, indent=2))

    current_summary = summarize(results)
    baseline_summary = json.loads(BASELINE_PATH.read_text())
    verdict = compare_to_baseline(current_summary, baseline_summary)
    write_report(current_summary, baseline_summary, verdict)

    if not (verdict["pass_rate_ok"] and verdict["cost_ok"] and verdict["latency_ok"]):
        raise SystemExit("Benchmark gate failed. See ai-ops/benchmark-report.md")

    print("Benchmark gate passed.")


if __name__ == "__main__":
    run_benchmark()
