#!/usr/bin/env python3
"""Offline unit + smoke test for scripts/run-trigger-evals.py.

Covers the scorer, discovery, and both pipeline outcomes (clean vs. failing) through
the deterministic MockJudge — no `pi`, no network — so it runs in `just check`. The
real model-graded run (`--judge pi`) is exercised separately via `just eval`.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run-trigger-evals.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("run_trigger_evals", RUNNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    m = load_runner()
    failures = 0

    def check(name: str, cond: bool) -> None:
        nonlocal failures
        if cond:
            print(f"OK   {name}")
        else:
            print(f"FAIL {name}", file=sys.stderr)
            failures += 1

    # ----- grade(): routing outcomes + invalid-label rejection -----
    pos = {"skill_under_test": "x", "should_activate": True}
    neg = {"skill_under_test": "x", "should_activate": False}
    labels = {"x", "y", "none"}
    check("grade: positive fires its skill", m.grade(pos, "x", labels) is True)
    check("grade: positive routed elsewhere fails", m.grade(pos, "y", labels) is False)
    check("grade: negative routed to SUT fails (over-trigger)", m.grade(neg, "x", labels) is False)
    check("grade: negative routed away passes", m.grade(neg, "y", labels) is True)
    check("grade: unknown label on a negative fails (not a silent pass)", m.grade(neg, "ui design", labels) is False)
    check("grade: <error> always fails", m.grade(neg, "<error>", labels) is False)

    # ----- discovery: pool excludes the internal template, includes real skills -----
    pool = m.discover_pool(ROOT)
    check("discover_pool: non-empty", len(pool) > 0)
    check("discover_pool: excludes example-minimal (internal)", "example-minimal" not in pool)
    check("discover_pool: includes ui-design (absorbed artifact-host-integration)", "ui-design" in pool)

    queries = m.collect_queries(ROOT, sorted(pool))
    required = {"id", "skill_under_test", "category", "should_activate", "query"}
    check("collect_queries: non-empty", len(queries) > 0)
    check("collect_queries: every row well-formed", all(required <= set(q) for q in queries))
    pool_labels = set(pool) | {"none"}

    # ----- pipeline (oracle): full coverage, zero failures -----
    oracle = m.MockJudge("oracle")
    preds = m.route_sharded(oracle, queries, pool, 25, 4)
    rows = m.build_rows(queries, preds, pool_labels)
    check("oracle: complete coverage", all(r["predicted"] != "<missing>" for r in rows))
    check("oracle: zero failures", all(r["ok"] for r in rows))
    m.render_report(rows)  # must not raise

    # ----- pipeline (adversary): scorer detects failures; they survive escalation -----
    adversary = m.MockJudge("adversary")
    adv_preds = m.route_sharded(adversary, queries, pool, 25, 4)
    adv_failed = [r for r in m.build_rows(queries, adv_preds, pool_labels) if not r["ok"]]
    check("adversary: failures detected", len(adv_failed) > 0)
    escalated = m.escalate(adversary, adv_failed, pool, 2)
    adv_rows = m.build_rows(queries, {**adv_preds, **escalated}, pool_labels)
    check("adversary: failures survive escalation", any(not r["ok"] for r in adv_rows))

    # ----- end-to-end exit codes via the CLI (offline mock backend) -----
    clean = subprocess.run(
        [sys.executable, str(RUNNER), "--judge", "mock",
         "--skills", "ui-design"],
        cwd=ROOT, capture_output=True, text=True,
    )
    check("e2e --judge mock (oracle) exits 0", clean.returncode == 0)

    failing = subprocess.run(
        [sys.executable, str(RUNNER), "--judge", "mock", "--mock-mode", "adversary",
         "--skills", "ui-design", "--escalate-rounds", "1"],
        cwd=ROOT, capture_output=True, text=True,
    )
    check("e2e --judge mock (adversary) exits non-zero", failing.returncode != 0)

    if failures:
        print(f"\nrun-trigger-evals test failed with {failures} issue(s).", file=sys.stderr)
        return 1
    print("\nrun-trigger-evals test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
