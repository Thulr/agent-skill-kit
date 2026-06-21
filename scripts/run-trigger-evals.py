#!/usr/bin/env python3
"""Model-graded activation-routing evals for the skill catalog (the "Stage 1.5" runner).

`just check` only validates the SHAPE of each `evals/trigger-evals.json`. This runner
actually grades ACTIVATION: it shows a judge the real activation surface — every
published skill's `description`, which is all a downstream agent sees at startup — and
asks which skill (if any) each labeled query routes to, then scores routing against the
trigger-evals labels.

Judge backend: `pi` (the local AI CLI). Its default provider is `openai-codex`
(GPT-5.5) — i.e. "Codex via pi". The backend is an adapter (see `Judge`); a
deterministic `MockJudge` runs the whole pipeline offline so `scripts/test-run-trigger-evals.py`
can cover it in `just check` without a network call.

Methodology mirrors a hand-run sweep: one judge pass per shard, then every misroute is
re-judged `--escalate-rounds` times and decided by majority vote — so a single flaky
judgment doesn't fail the build.

Usage:
  python3 scripts/run-trigger-evals.py                      # full catalog, pi judge
  python3 scripts/run-trigger-evals.py --skills artifact-host-integration,ui-design
  python3 scripts/run-trigger-evals.py --judge mock         # offline pipeline smoke
  python3 scripts/run-trigger-evals.py --json /tmp/out.json # also write full results

Exit code is non-zero if any query still misroutes after escalation.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# All three install lanes (Rule 1). `.agents/` is excluded — it is not the published
# catalog an end user installs. `.experimental/` is currently empty but enumerated so
# the runner picks it up the moment a skill lands there.
SKILL_GLOBS = ("skills/*/skill.json", "skills/.experimental/*/skill.json")

JUDGE_SYSTEM = (
    "You are grading skill ACTIVATION ROUTING for a catalog of Agent Skills. A coding "
    "agent sees ONLY the skill descriptions below at startup; for a user message it "
    "invokes the SINGLE most appropriate skill, or none if nothing clearly fits.\n\n"
    "Decide which one skill each message routes to, based PURELY on the descriptions "
    "(honor any explicit 'Do NOT use ... use X' fences inside them). Use \"none\" only "
    "when genuinely nothing fits. A message that is essentially a skill's name is an "
    "explicit invocation of that skill.\n\n"
    "Output STRICT JSON only — a single array, no prose, no markdown fences. Each "
    'element: {"id": "<id>", "predicted_skill": "<skill-name-or-none>", '
    '"confidence": "high|medium|low", "reason": "<=12 words"}. Cover every message once.'
)

_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


# --------------------------------------------------------------------------- discovery
def discover_pool(root: Path) -> dict[str, str]:
    """name -> description for every published, non-internal skill (the candidate pool)."""
    pool: dict[str, str] = {}
    for pattern in SKILL_GLOBS:
        for path in sorted(root.glob(pattern)):
            manifest = json.loads(path.read_text())
            meta = manifest.get("metadata", {})
            if manifest.get("status") != "published" or meta.get("internal"):
                continue
            pool[manifest["name"]] = manifest["description"]
    return pool


def collect_queries(root: Path, names: list[str]) -> list[dict]:
    """Labeled queries from each named skill's trigger-evals.json."""
    queries: list[dict] = []
    for name in names:
        te_path = next(
            (root / pat.split("*")[0] / name / "evals" / "trigger-evals.json"
             for pat in SKILL_GLOBS
             if (root / pat.split("*")[0] / name / "evals" / "trigger-evals.json").is_file()),
            None,
        )
        if te_path is None:
            continue
        te = json.loads(te_path.read_text())
        for i, q in enumerate(te.get("queries", []), 1):
            queries.append({
                "id": f"{name}#{i}",
                "skill_under_test": name,
                "category": q["category"],
                "should_activate": q["should_activate"],
                "query": q["query"],
            })
    return queries


# ------------------------------------------------------------------------------ judges
class Judge:
    """Routing-judge interface. route() returns {id: predicted_skill} for the batch."""

    name = "judge"

    def route(self, queries: list[dict], pool: dict[str, str], *, nonce: str = "") -> dict[str, str]:
        raise NotImplementedError


class PiJudge(Judge):
    """Shells out to `pi` (non-interactive, no tools). Default provider = Codex via pi."""

    name = "pi"

    def __init__(self, provider: str, model: str, thinking: str, timeout: int):
        self.provider, self.model, self.thinking, self.timeout = provider, model, thinking, timeout

    def _payload(self, queries: list[dict], pool: dict[str, str], nonce: str) -> str:
        skills = "\n".join(f"- {n}: {d}" for n, d in sorted(pool.items()))
        msgs = "\n".join(f"{q['id']}\t{q['query']}" for q in queries)
        head = f"(round {nonce})\n" if nonce else ""
        return f"{head}SKILLS (name: description):\n{skills}\n\nMESSAGES (id<TAB>text):\n{msgs}"

    def route(self, queries: list[dict], pool: dict[str, str], *, nonce: str = "") -> dict[str, str]:
        # Hermetic judge. -nt disables tools; -nc/-ns/-np/-ne stop pi from appending the
        # repo's AGENTS.md/CLAUDE.md, installed skills, prompt templates, and extensions to
        # the (replacement) system prompt. Without these the judge would see the repo's own
        # routing docs — biasing results and making the audit non-reproducible off this checkout.
        cmd = [
            "pi", "-p", "-nt", "-nc", "-ns", "-np", "-ne", "--no-session",
            "--provider", self.provider, "--model", self.model,
            "--thinking", self.thinking, "--mode", "text",
            "--system-prompt", JUDGE_SYSTEM,
            self._payload(queries, pool, nonce),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
        if proc.returncode != 0:
            raise RuntimeError(f"pi exited {proc.returncode}: {proc.stderr.strip()[:200]}")
        return _parse_predictions(proc.stdout)


class MockJudge(Judge):
    """Deterministic, offline. 'oracle' routes every query correctly; 'adversary'
    deliberately misroutes (for the scorer's own unit test)."""

    name = "mock"

    def __init__(self, mode: str = "oracle"):
        self.mode = mode

    def route(self, queries: list[dict], pool: dict[str, str], *, nonce: str = "") -> dict[str, str]:
        out: dict[str, str] = {}
        for q in queries:
            sut = q["skill_under_test"]
            if self.mode == "adversary":
                out[q["id"]] = sut if not q["should_activate"] else "none"
            else:  # oracle
                out[q["id"]] = sut if q["should_activate"] else "none"
        return out


def _parse_predictions(text: str) -> dict[str, str]:
    cleaned = _FENCE_RE.sub("", text).strip()
    start, end = cleaned.find("["), cleaned.rfind("]")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON array in judge output: {cleaned[:200]!r}")
    arr = json.loads(cleaned[start:end + 1])
    return {e["id"]: (e.get("predicted_skill") or "none").strip() for e in arr}


# --------------------------------------------------------------------------- run/score
def route_sharded(judge: Judge, queries: list[dict], pool: dict[str, str],
                  shard_size: int, jobs: int) -> dict[str, str]:
    shards = [queries[i:i + shard_size] for i in range(0, len(queries), shard_size)]

    def run_shard(shard: list[dict]) -> dict[str, str]:
        try:
            return judge.route(shard, pool)
        except Exception as exc:  # noqa: BLE001 — one bad shard must not sink the sweep
            sys.stderr.write(f"  [warn] shard of {len(shard)} failed: {exc}\n")
            return {q["id"]: "<error>" for q in shard}  # escalation retries these

    preds: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool_ex:
        for result in pool_ex.map(run_shard, shards):
            preds.update(result)
    return preds


def grade(query: dict, predicted: str) -> bool:
    """Positive/edge-true: must fire its skill. Negative/edge-false: must NOT fire it.
    An unknown/errored prediction is always a failure (never a silent negative pass)."""
    if predicted in ("<error>", "<missing>"):
        return False
    sut = query["skill_under_test"]
    return predicted == sut if query["should_activate"] else predicted != sut


def escalate(judge: Judge, failed: list[dict], pool: dict[str, str], rounds: int) -> dict[str, str]:
    """Re-judge each failed query `rounds` times; return the majority prediction."""
    final: dict[str, str] = {}
    for q in failed:
        votes = []
        for r in range(rounds):
            try:
                votes.append(judge.route([q], pool, nonce=str(r + 1))[q["id"]])
            except Exception:
                continue
        final[q["id"]] = Counter(votes).most_common(1)[0][0] if votes else "<error>"
    return final


def build_rows(queries: list[dict], preds: dict[str, str]) -> list[dict]:
    rows = []
    for q in queries:
        predicted = preds.get(q["id"], "<missing>")
        rows.append({**q, "predicted": predicted, "ok": grade(q, predicted)})
    return rows


# ------------------------------------------------------------------------------ report
def render_report(rows: list[dict]) -> str:
    total = len(rows)
    passes = sum(r["ok"] for r in rows)
    lines = [f"OVERALL: {passes}/{total} pass ({100 * passes / total:.1f}%)" if total else "no queries"]

    by_sut: dict[str, list[int]] = {}
    for r in rows:
        bucket = by_sut.setdefault(r["skill_under_test"], [0, 0])
        bucket[1] += 1
        bucket[0] += int(r["ok"])
    lines.append("")
    lines.append(f"{'skill':<34}{'pass':<10}{'status'}")
    lines.append("-" * 56)
    for name in sorted(by_sut):
        ok, n = by_sut[name]
        lines.append(f"{name:<34}{f'{ok}/{n}':<10}{'' if ok == n else '<-- CHECK'}")

    under = [r for r in rows if r["should_activate"] and not r["ok"]]
    over = [r for r in rows if not r["should_activate"] and not r["ok"]]
    lines += ["", f"UNDER-TRIGGER (own positive routed elsewhere): {len(under)}",
              f"OVER-TRIGGER  (stole a query that should route away): {len(over)}"]
    for label, rs in (("UNDER-TRIGGER", under), ("OVER-TRIGGER", over)):
        if not rs:
            continue
        lines.append(f"\n--- {label} ---")
        for r in rs:
            exp = r["skill_under_test"] if r["should_activate"] else f"NOT {r['skill_under_test']}"
            q = r["query"] if len(r["query"]) <= 64 else r["query"][:63] + "…"
            lines.append(f"  expected={exp:<28} got={r['predicted']:<26} | {q}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skills", help="comma-separated skills under test (default: all published)")
    ap.add_argument("--judge", choices=["pi", "mock"], default="pi", help="judge backend (default: pi)")
    ap.add_argument("--provider", default="openai-codex", help="pi provider (default: openai-codex)")
    ap.add_argument("--model", default="gpt-5.5", help="pi model (default: gpt-5.5)")
    ap.add_argument("--thinking", default="off", help="pi thinking level (default: off)")
    ap.add_argument("--shard-size", type=int, default=25, help="queries per judge call (default: 25)")
    ap.add_argument("--jobs", type=int, default=4, help="concurrent judge calls (default: 4)")
    ap.add_argument("--escalate-rounds", type=int, default=3, help="re-judge rounds per failure (default: 3)")
    ap.add_argument("--timeout", type=int, default=300, help="per-judge-call timeout seconds (default: 300)")
    ap.add_argument("--mock-mode", choices=["oracle", "adversary"], default="oracle", help=argparse.SUPPRESS)
    ap.add_argument("--json", dest="json_out", help="write full results to this path")
    args = ap.parse_args()

    pool = discover_pool(ROOT)
    if not pool:
        print("FAIL: no published skills discovered", file=sys.stderr)
        return 1
    names = [s.strip() for s in args.skills.split(",")] if args.skills else sorted(pool)
    unknown = [n for n in names if n not in pool]
    if unknown:
        print(f"FAIL: unknown skill(s): {', '.join(unknown)}", file=sys.stderr)
        return 1

    queries = collect_queries(ROOT, names)
    if not queries:
        print("FAIL: no queries collected", file=sys.stderr)
        return 1

    judge: Judge = (MockJudge(args.mock_mode) if args.judge == "mock"
                    else PiJudge(args.provider, args.model, args.thinking, args.timeout))
    label = f"{judge.name}" + (f" ({args.provider}/{args.model})" if args.judge == "pi" else f" ({args.mock_mode})")
    print(f"Routing {len(queries)} queries from {len(names)} skill(s) "
          f"against {len(pool)} descriptions — judge: {label}\n")

    try:
        preds = route_sharded(judge, queries, pool, args.shard_size, args.jobs)
    except Exception as exc:  # noqa: BLE001 — surface any judge failure cleanly
        print(f"FAIL: judge error during sweep: {exc}", file=sys.stderr)
        return 1

    rows = build_rows(queries, preds)
    failed = [r for r in rows if not r["ok"]]
    if failed and args.escalate_rounds > 0:
        print(f"Escalating {len(failed)} misroute(s) to {args.escalate_rounds}-round majority vote...\n")
        escalated = escalate(judge, failed, pool, args.escalate_rounds)
        preds.update(escalated)
        rows = build_rows(queries, preds)

    report = render_report(rows)
    print(report)

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(
            {"pool": sorted(pool), "rows": rows}, indent=2) + "\n")
        print(f"\nWrote results: {args.json_out}")

    remaining = [r for r in rows if not r["ok"]]
    if remaining:
        print(f"\nFAIL: {len(remaining)} query/queries misroute after escalation.", file=sys.stderr)
        return 1
    print("\nOK: every query routes to the expected skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
