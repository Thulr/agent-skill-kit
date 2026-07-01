#!/usr/bin/env python3
"""Run minimal-modular-code behavior evals and emit a thulr JSONL trace.

The runner supports two cheap fixture agents for calibration/smoke tests and two
Codex-via-pi agents for the actual A/B comparison:

  fixture-good   emits the known-good examples from behavior-cases.json
  fixture-bad    emits the known-bad examples from behavior-cases.json
  with-skill     runs pi with --skill skills/minimal-modular-code
  without-skill  runs pi with --no-skills
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "skills/minimal-modular-code/evals/behavior-cases.json"
DEFAULT_SKILL_DIR = ROOT / "skills/minimal-modular-code"

AGENT_MODES = ("fixture-good", "fixture-bad", "calibration", "with-skill", "without-skill")

PI_SYSTEM_APPEND = (
    "Answer the user's code review or design prompt directly. "
    "Give concise, actionable guidance. Do not modify files."
)

RUNTIME_REFERENCES = (
    "SKILL.md",
    "references/playbooks/minimalism.md",
    "references/playbooks/legibility.md",
    "references/playbooks/boundaries.md",
)


def load_cases(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def select_cases(data: dict[str, Any], case_id: str | None) -> list[dict[str, Any]]:
    cases = data["cases"]
    if case_id is None:
        return cases
    matches = [case for case in cases if case["id"] == case_id]
    if not matches:
        raise SystemExit(f"unknown case id: {case_id}")
    return matches


def run_pi(prompt: str, args: argparse.Namespace) -> str:
    pi = shutil.which("pi")
    if pi is None:
        raise SystemExit("pi is not on PATH; install/configure pi before running Codex behavior evals")

    system_prompt = PI_SYSTEM_APPEND
    if args.agent == "with-skill":
        system_prompt = f"{system_prompt}\n\n{skill_runtime_prompt(args.skill_dir)}"

    cmd = [
        pi,
        "-p",
        "--no-session",
        "--no-context-files",
        "--no-extensions",
        "--no-prompt-templates",
        "--no-tools",
        "--provider",
        args.provider,
        "--model",
        args.model,
        "--thinking",
        args.thinking,
        "--append-system-prompt",
        system_prompt,
    ]
    if args.agent == "with-skill":
        cmd.extend(["--skill", str(args.skill_dir)])
    else:
        cmd.append("--no-skills")
    cmd.append(prompt)

    result = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=args.timeout,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise SystemExit(f"pi failed for behavior eval: {detail}")
    return result.stdout.strip()


def skill_runtime_prompt(skill_dir: Path) -> str:
    parts = [
        "Use the minimal-modular-code skill runtime below. Apply it directly; do not answer from generic coding advice."
    ]
    for rel_path in RUNTIME_REFERENCES:
        path = skill_dir / rel_path
        if path.is_file():
            parts.append(f"\n--- {rel_path} ---\n{path.read_text()}")
    return "\n".join(parts)


def criterion_text(case: dict[str, Any], all_criteria: dict[str, str]) -> str:
    return "\n".join(
        f"{criterion_id}: {all_criteria[criterion_id]}" for criterion_id in case["criteria"]
    )


def build_span(
    *,
    data: dict[str, Any],
    case: dict[str, Any],
    output: str,
    agent: str,
    model: str,
    label: bool | None,
    index: int,
    case_input: str | None = None,
    case_id: str | None = None,
) -> dict[str, Any]:
    effective_case_id = case_id or case["id"]
    prompt = case_input or case["prompt"]
    start = int(time.time() * 1000) + index
    attrs: dict[str, Any] = {
        "service.name": "agent-skill-kit",
        "agent.name": f"minimal-modular-code-{agent}",
        "agent.framework": "pi" if agent in {"with-skill", "without-skill"} else "fixture",
        "input.value": prompt,
        "output.value": output,
        "llm.model_name": model,
        "thulr.case_id": effective_case_id,
        "thulr.task.input": prompt,
        "thulr.expected_behavior": case["expected_behavior"],
        "thulr.failure_modes": case["failure_modes"],
        "thulr.criterion": criterion_text(case, data["criteria"]),
        "thulr.prompt_version": f"{data['skill']}-{data['version']}",
        "thulr.config_version": agent,
        "minimal_modular.expected_route": case["expected_route"],
    }
    for criterion_id in case["criteria"]:
        attrs[f"thulr.criteria.{criterion_id}"] = data["criteria"][criterion_id]
        if label is None:
            attrs[f"thulr.judge_only.{criterion_id}"] = True
        else:
            attrs[f"thulr.label.{criterion_id}"] = label
    if label is not None:
        attrs["thulr.deterministic_label"] = label

    return {
        "trace_id": f"minimal-modular-code-{agent}",
        "span_id": f"{effective_case_id}-answer",
        "name": "agent.final_answer",
        "start_time_unix_ms": start,
        "end_time_unix_ms": start + 1,
        "attributes": attrs,
    }


def output_for_case(case: dict[str, Any], args: argparse.Namespace) -> tuple[str, bool | None, str]:
    if args.agent == "fixture-good":
        return case["example_pass"], True, case["id"]
    if args.agent == "fixture-bad":
        return case["example_fail"], False, case["id"]
    prompt = args.case_input or case["prompt"]
    return run_pi(prompt, args), None, case["id"]


def write_spans(spans: list[dict[str, Any]], out: str) -> None:
    text = "".join(json.dumps(span, separators=(",", ":")) + "\n" for span in spans)
    if out == "-":
        sys.stdout.write(text)
        return
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(text)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--agent", choices=AGENT_MODES, default="with-skill")
    parser.add_argument("--out", default="-", help="trace JSONL path, or '-' for stdout")
    parser.add_argument("--case-id", help="single case id; used by thulr --runner")
    parser.add_argument("--case-input", help="single case prompt override; used by thulr --runner")
    parser.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR)
    parser.add_argument("--provider", default="openai-codex")
    parser.add_argument("--model", default="gpt-5.5")
    parser.add_argument("--thinking", default="off")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args(argv)

    if args.case_input and not args.case_id:
        parser.error("--case-input requires --case-id")

    data = load_cases(args.cases)
    cases = select_cases(data, args.case_id)
    spans: list[dict[str, Any]] = []

    if args.agent == "calibration":
        for index, case in enumerate(cases, 1):
            spans.append(
                build_span(
                    data=data,
                    case=case,
                    output=case["example_pass"],
                    agent=args.agent,
                    model="fixture",
                    label=True,
                    index=index * 2,
                    case_id=f"{case['id']}-pass",
                )
            )
            spans.append(
                build_span(
                    data=data,
                    case=case,
                    output=case["example_fail"],
                    agent=args.agent,
                    model="fixture",
                    label=False,
                    index=index * 2 + 1,
                    case_id=f"{case['id']}-fail",
                )
            )
    else:
        for index, case in enumerate(cases, 1):
            output, label, effective_case_id = output_for_case(case, args)
            spans.append(
                build_span(
                    data=data,
                    case=case,
                    output=output,
                    agent=args.agent,
                    model=args.model if args.agent in {"with-skill", "without-skill"} else "fixture",
                    label=label,
                    index=index,
                    case_input=args.case_input,
                    case_id=effective_case_id,
                )
            )

    write_spans(spans, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
