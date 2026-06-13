#!/usr/bin/env bash
#
# Compatibility adapter for the executable routing graph checker.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/scripts/check-routing-csv.py"
