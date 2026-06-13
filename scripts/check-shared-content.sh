#!/usr/bin/env bash
#
# Compatibility adapter for the shared-content inventory checker.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/scripts/check-shared-content.py"
