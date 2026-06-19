"""Shared Anthropic SDK boilerplate for skill-local eval graders.

Originally used by: skills/agent-evals/evals/phase2-grader.py (retired in
ADR 0011). Kept deliberately minimal — three functions — until a skill adopts it.
At that point the API can be refactored without breaking external users
since this lives under scripts/, not skills/.

Not invoked from `just check`. Imported by skill-local graders that are
opt-in by design.

Usage:
    from anthropic_eval_lib import pick_model, make_client, complete

    client = make_client()                       # raises if key missing
    model = pick_model("sonnet")                 # 'claude-sonnet-4-6'
    text = complete(client, system="...", user="...", model=model)

Self-test:
    python3 scripts/anthropic_eval_lib.py --self-test
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any


MODELS = {
    "opus": "claude-opus-4-7",
    "sonnet": "claude-sonnet-4-6",
    "haiku": "claude-haiku-4-5-20251001",
}
DEFAULT_MODEL = "sonnet"
DEFAULT_MAX_TOKENS = 4096


class MissingApiKey(RuntimeError):
    """Raised when ANTHROPIC_API_KEY is not set and the caller asked for a
    real client."""


def _find_repo_root(start: Path) -> Path | None:
    cur = start.resolve()
    for parent in (cur, *cur.parents):
        if (parent / "AGENTS.md").is_file() and (parent / "schemas").is_dir():
            return parent
    return None


def load_dotenv(env_path: Path | None = None) -> dict[str, str]:
    """Populate `os.environ` from a `.env` file without clobbering existing
    values. Returns the dict of keys that were newly set.

    Strict parser: only `KEY=VALUE` lines (optionally quoted). No shell
    expansion, no $VAR substitution, no `export` prefix handling. Lines
    starting with `#` and blank lines are ignored. For richer behavior
    install `python-dotenv` and import it explicitly.

    Search order if `env_path` is None:
      1. $REPO_ROOT/.env (where REPO_ROOT contains AGENTS.md + schemas/)
      2. cwd/.env
    First file found wins; missing file is silently OK.
    """
    if env_path is None:
        candidates: list[Path] = []
        root = _find_repo_root(Path(__file__).parent)
        if root is not None:
            candidates.append(root / ".env")
        candidates.append(Path.cwd() / ".env")
        env_path = next((c for c in candidates if c.is_file()), None)
        if env_path is None:
            return {}
    elif not env_path.is_file():
        return {}

    loaded: dict[str, str] = {}
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key.isidentifier():
            continue
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        if key in os.environ:
            continue  # respect already-set environment
        os.environ[key] = value
        loaded[key] = value
    return loaded


def pick_model(name: str) -> str:
    """Resolve a friendly model alias (opus/sonnet/haiku) to a model ID.

    Accepts a raw model ID as a passthrough so callers can pin a specific
    Claude version without going through this mapping.
    """
    if name in MODELS:
        return MODELS[name]
    if name.startswith("claude-"):
        return name
    raise ValueError(
        f"Unknown model {name!r}. Choose from {sorted(MODELS)} or pass a 'claude-*' ID."
    )


def make_client(api_key: str | None = None) -> Any:
    """Construct an anthropic.Anthropic client. Imported lazily so this
    module is importable in environments without `anthropic` installed
    (e.g., CI just verifying `py_compile`).

    If `ANTHROPIC_API_KEY` is not already in the environment, attempts to
    load it from a `.env` at the repo root or cwd before failing.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        load_dotenv()
        key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise MissingApiKey(
            "ANTHROPIC_API_KEY not set. Add it to a .env at the repo root, "
            "export it in your shell, or call with --dry-run to print the "
            "prompts without hitting the API."
        )
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError(
            "anthropic SDK not installed. Run `pip install anthropic` first."
        ) from e
    return anthropic.Anthropic(api_key=key)


def complete(
    client: Any,
    *,
    system: str,
    user: str,
    model: str,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """Single-turn message completion. Returns the concatenated assistant
    text. No tool use, no streaming — intentionally minimal."""
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    parts: list[str] = []
    for block in response.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    return "".join(parts)


def _self_test() -> int:
    print(f"Available models: {sorted(MODELS)}")
    print(f"  opus   -> {pick_model('opus')}")
    print(f"  sonnet -> {pick_model('sonnet')}")
    print(f"  haiku  -> {pick_model('haiku')}")
    try:
        pick_model("gpt-4")
    except ValueError as e:
        print(f"Rejects unknown aliases: {e}")
    pre = "ANTHROPIC_API_KEY" in os.environ
    loaded = load_dotenv()
    post = "ANTHROPIC_API_KEY" in os.environ
    if pre:
        print("ANTHROPIC_API_KEY already in env (not from .env)")
    elif "ANTHROPIC_API_KEY" in loaded:
        print("ANTHROPIC_API_KEY loaded from .env")
    elif loaded:
        print(f".env loaded but no ANTHROPIC_API_KEY (loaded: {sorted(loaded)})")
    elif post:
        print("ANTHROPIC_API_KEY set during this run")
    else:
        print("ANTHROPIC_API_KEY NOT set (no .env found either)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--self-test", action="store_true", help="Run a dry self-test.")
    args = parser.parse_args()
    if args.self_test:
        return _self_test()
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
