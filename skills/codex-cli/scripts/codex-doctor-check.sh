#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage:
  codex-doctor-check.sh [options]

Options:
  --json       Emit Codex doctor JSON
  --all        Expand detailed human output
  --dry-run    Print command; do not invoke Codex
  -h, --help   Show help
USAGE
}

json=0
all=0
dry_run=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json)
      json=1
      shift
      ;;
    --all)
      all=1
      shift
      ;;
    --dry-run)
      dry_run=1
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

cmd=(codex doctor)
if (( json == 1 )); then
  cmd+=(--json)
else
  cmd+=(--summary --ascii)
  (( all == 1 )) && cmd+=(--all)
fi

if (( dry_run == 1 )); then
  printf 'Command:'
  printf ' %q' "${cmd[@]}"
  printf '\n'
  exit 0
fi

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI not found on PATH. Install or authenticate Codex, then retry." >&2
  exit 1
fi

"${cmd[@]}"
