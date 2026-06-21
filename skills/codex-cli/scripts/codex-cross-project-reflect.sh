#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage:
  codex-cross-project-reflect.sh [options]

Options:
  --since <date-or-window>              Date/window to inspect, e.g. 2026-05-01
  --cd <dir>                            Neutral starting directory (default: $HOME)
  --context-file <file>                 Include a compact context file (repeatable)
  --model <model>                       Codex model override
  --profile <profile>                   Codex config profile
  --config <key=value>                  Codex config override (repeatable)
  --sandbox <mode>                      read-only, workspace-write, or danger-full-access
  --ask-for-approval <policy>           untrusted, on-request, on-failure, or never
  --output <file>                       Write Codex output to a file as well
  --dry-run                             Print command and prompt; do not invoke Codex
  -h, --help                            Show help

Example:
  codex-cross-project-reflect.sh --since "last 30 days" --dry-run
USAGE
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
run_dir="${HOME:-$(pwd)}"
since="last 30 days"
args=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --since)
      since="${2:-}"
      shift 2
      ;;
    --cd)
      run_dir="${2:-}"
      shift 2
      ;;
    --context-file|--model|--profile|--config|--sandbox|--ask-for-approval|--output)
      args+=("$1" "${2:-}")
      shift 2
      ;;
    --dry-run)
      args+=("$1")
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

task="Reflect on Codex work across projects for ${since}. Identify repeated mistakes you have made, common feedback Justin gives, patterns in how he works or reviews, and durable workflow improvements. Treat this as global/cross-project evidence, not a review of the repository that launched the command."

exec "$script_dir/codex-ask.sh" \
  --template templates/cross-project-reflection-prompt.md \
  --cd "$run_dir" \
  --skip-git-repo-check \
  "${args[@]}" \
  "$task"
