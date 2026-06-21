#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage:
  cursor-doctor-check.sh [options]

Options:
  --models     Also list available models (requires auth)
  --dry-run    Print the command; do not invoke cursor-agent
  -h, --help   Show help

Notes:
  cursor-agent has no `doctor` subcommand. This runs `cursor-agent --version`
  (and optionally --list-models) as a health probe. cursor-agent also requires
  the working directory to be trusted before non-interactive (`-p`) runs; if a
  review errors with a workspace-trust prompt, trust the repo once interactively.
USAGE
}

models=0
dry_run=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --models) models=1; shift ;;
    --dry-run) dry_run=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

if (( models == 1 )); then
  cmd=(cursor-agent --list-models)
else
  cmd=(cursor-agent --version)
fi

if (( dry_run == 1 )); then
  printf 'Command:'; printf ' %q' "${cmd[@]}"; printf '\n'
  exit 0
fi

if ! command -v cursor-agent >/dev/null 2>&1; then
  echo "Cursor CLI (cursor-agent) not found on PATH. Install it (https://cursor.com/cli) and authenticate, then retry." >&2
  exit 1
fi

"${cmd[@]}"
