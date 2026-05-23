"""Phase 2 grader for loop-architect.

Implements TEST_PLAN.md Phase 2: feeds mock workspace files (fixtures/) to
Claude under loop-architect's SKILL.md instructions, then uses a separate
Claude call as a judge to score the diagnosis against ground truth.

NOT invoked from `just check`. Opt-in. Costs ~$0.05 per --live run with
the default Sonnet model.

Usage:
    python3 skills/loop-architect/evals/phase2-grader.py --dry-run
    python3 skills/loop-architect/evals/phase2-grader.py --live
    python3 skills/loop-architect/evals/phase2-grader.py --live --case agent-needs-sandbox
    python3 skills/loop-architect/evals/phase2-grader.py --live --model opus

Exit codes:
    0  all cases PASS
    1  any case FAIL (wrong tier diagnosis)
    2  any case PARTIAL (right tier, wrong scaffold keywords), or missing
       ANTHROPIC_API_KEY under --live
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
VENV_DIR = REPO_ROOT / ".venv-loop-architect"  # shared with integration-test.sh
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from anthropic_eval_lib import (  # noqa: E402
    DEFAULT_MAX_TOKENS,
    MissingApiKey,
    complete,
    load_dotenv,
    make_client,
    pick_model,
)

SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_DIR / "SKILL.md"
FIXTURES_DIR = SKILL_DIR / "evals" / "fixtures"

CASES: list[dict[str, Any]] = [
    {
        "id": "translator-level-0-to-2",
        "fixtures": ["translator.py"],
        "expected_tier": "Level 0",
        "expected_target_tier": "Level 2",
        "expected_scaffold_keywords": [
            "DSPy",
            "Signature",
            "MIPROv2",
            "BootstrapFewShot",
        ],
        "description": (
            "Hardcoded translation prompt with no validation. Should be "
            "diagnosed as Level 0 (Zero-Shot) and recommended for Level 2 "
            "(Subroutine Compilation)."
        ),
    },
    {
        "id": "agent-needs-sandbox",
        "fixtures": ["agent.py", "rules.md"],
        "expected_tier": "Level 0",
        "expected_target_tier": "Level 3",
        "expected_scaffold_keywords": [
            "sandbox",
            "Docker",
            "iteration",
            "cost",
        ],
        "description": (
            "Un-sandboxed CLI agent with subprocess shell execution and no "
            "iteration or cost caps. Should be flagged for a Level 3 "
            "Sandbox Harness BEFORE any prompt optimization."
        ),
    },
]


AGENT_USER_TEMPLATE = """\
A user has asked you to audit the AI integration points in their workspace.
Below are the files in that workspace. Apply the loop-architect skill: scan,
diagnose each integration's tier on the AI Optimization Staircase, and
recommend the appropriate scaffolding template.

{file_blocks}

Now produce the Step 2 Diagnostic Report. Be specific about:
- Which AI Optimization Staircase tier each integration currently occupies.
- Which tier you recommend the developer scaffold next, and why.
- Which template (Level 1 / 2 / 3) you would copy into the workspace.
"""

JUDGE_SYSTEM = """\
You are a strict grader for an AI workspace diagnosis. You will receive a
GROUND TRUTH spec describing the expected tier diagnosis and a list of
keywords that should appear in the agent's recommendation. Score the
AGENT OUTPUT on three axes and output JSON only.
"""

JUDGE_USER_TEMPLATE = """\
GROUND TRUTH:
- Current tier of the integration: {expected_tier}
- Recommended target tier: {expected_target_tier}
- Recommendation should reference at least 2 of these keywords (case-insensitive): {keywords}

AGENT OUTPUT:
\"\"\"
{agent_output}
\"\"\"

Output JSON only with this exact shape:
{{
  "tier_correct": <boolean — did the agent diagnose the current tier as {expected_tier}?>,
  "recommendation_correct": <boolean — did the agent recommend {expected_target_tier} scaffolding?>,
  "keywords_present": [<list of keywords from the ground truth that appear in AGENT OUTPUT>],
  "rationale": "<one sentence>"
}}
"""


def _ensure_anthropic() -> None:
    """If `anthropic` isn't importable in the current interpreter,
    bootstrap `.venv-loop-architect/`, pip-install anthropic into it, and
    re-exec this script using the venv's python.

    Idempotent: a no-op when anthropic is already importable. Skip with
    `--no-bootstrap` if you want the original ImportError to surface
    (e.g., you're already inside your own venv).

    The venv is shared with `integration-test.sh execute`, which installs
    `dspy-ai` into the same directory.
    """
    try:
        import anthropic  # noqa: F401
        return
    except ImportError:
        pass

    venv_python = VENV_DIR / "bin" / "python"

    if not venv_python.exists():
        print(f"[bootstrap] creating venv at {VENV_DIR}", flush=True)
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
        subprocess.check_call(
            [str(venv_python), "-m", "pip", "install", "--quiet", "--upgrade", "pip"]
        )

    check = subprocess.run(
        [str(venv_python), "-c", "import anthropic"],
        capture_output=True,
    )
    if check.returncode != 0:
        print(f"[bootstrap] installing anthropic into {VENV_DIR}", flush=True)
        subprocess.check_call(
            [str(venv_python), "-m", "pip", "install", "--quiet", "anthropic"]
        )

    # If we're already inside the venv, importing should have worked the
    # first time. We're here only if the outer interpreter lacked the
    # package, so re-exec inside the venv.
    print(f"[bootstrap] re-executing in {venv_python}", flush=True)
    os.execv(str(venv_python), [str(venv_python), *sys.argv])


def build_user_message(case: dict[str, Any]) -> str:
    blocks: list[str] = []
    for fname in case["fixtures"]:
        path = FIXTURES_DIR / fname
        content = path.read_text()
        blocks.append(f"=== {fname} ===\n{content}")
    return AGENT_USER_TEMPLATE.format(file_blocks="\n\n".join(blocks))


def build_judge_user(case: dict[str, Any], agent_output: str) -> str:
    return JUDGE_USER_TEMPLATE.format(
        expected_tier=case["expected_tier"],
        expected_target_tier=case["expected_target_tier"],
        keywords=", ".join(case["expected_scaffold_keywords"]),
        agent_output=agent_output,
    )


def parse_judge_verdict(raw: str) -> dict[str, Any]:
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"judge did not return JSON: {raw[:200]}")
    return json.loads(raw[start : end + 1])


def score(verdict: dict[str, Any], case: dict[str, Any]) -> str:
    if not verdict.get("tier_correct"):
        return "FAIL"
    if not verdict.get("recommendation_correct"):
        return "PARTIAL"
    keywords_hit = len(verdict.get("keywords_present", []))
    if keywords_hit < 2:
        return "PARTIAL"
    return "PASS"


def run_case(
    case: dict[str, Any],
    *,
    client: Any,
    model: str,
    skill_md: str,
    dry_run: bool,
) -> tuple[str, dict[str, Any] | None]:
    user = build_user_message(case)
    if dry_run:
        print(f"--- {case['id']}: agent prompt ---")
        print(f"SYSTEM ({len(skill_md)} chars from SKILL.md)")
        print(f"USER:\n{user[:1200]}{'...' if len(user) > 1200 else ''}")
        print()
        return "DRY-RUN", None

    agent_output = complete(
        client, system=skill_md, user=user, model=model, max_tokens=DEFAULT_MAX_TOKENS
    )
    judge_user = build_judge_user(case, agent_output)
    judge_raw = complete(
        client, system=JUDGE_SYSTEM, user=judge_user, model=model, max_tokens=1024
    )
    verdict = parse_judge_verdict(judge_raw)
    return score(verdict, case), {"agent": agent_output, "verdict": verdict}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the prompts that would be sent and exit. Default.",
    )
    mode.add_argument(
        "--live",
        action="store_true",
        help="Actually call the Anthropic API. Costs money.",
    )
    parser.add_argument(
        "--model",
        default="sonnet",
        help="Model alias (opus/sonnet/haiku) or full claude-* ID. Default: sonnet.",
    )
    parser.add_argument(
        "--case",
        help="Run a single case by id. Default: all.",
    )
    parser.add_argument(
        "--no-bootstrap",
        action="store_true",
        help="Don't auto-create .venv-loop-architect/ if anthropic is missing. "
        "Use when you're already inside your own venv with the SDK installed.",
    )
    args = parser.parse_args()

    dry_run = not args.live  # dry-run is the default
    if args.live and not args.no_bootstrap:
        _ensure_anthropic()
    model = pick_model(args.model)
    skill_md = SKILL_MD.read_text()
    loaded = load_dotenv()
    if loaded:
        print(f"[.env] loaded: {sorted(loaded)}")

    cases = CASES
    if args.case:
        cases = [c for c in CASES if c["id"] == args.case]
        if not cases:
            print(f"unknown case: {args.case}. Available: {[c['id'] for c in CASES]}")
            return 2

    if dry_run:
        client = None
        print(f"[DRY-RUN] would use model {model}")
        print(f"[DRY-RUN] would grade {len(cases)} case(s):")
        for c in cases:
            print(f"  - {c['id']}: {c['description']}")
        print()
    else:
        try:
            client = make_client()
        except MissingApiKey as e:
            print(f"SKIP: {e}", file=sys.stderr)
            return 2
        print(f"[LIVE] model={model}, cases={len(cases)}")

    results: list[tuple[str, str]] = []
    for case in cases:
        outcome, _detail = run_case(
            case, client=client, model=model, skill_md=skill_md, dry_run=dry_run
        )
        results.append((case["id"], outcome))
        if not dry_run and _detail is not None:
            print(f"  {case['id']}: {outcome} — {_detail['verdict'].get('rationale', '')}")

    print()
    print("Summary:")
    for cid, outcome in results:
        print(f"  {outcome:9}  {cid}")

    if dry_run:
        return 0
    if any(o == "FAIL" for _, o in results):
        return 1
    if any(o == "PARTIAL" for _, o in results):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
