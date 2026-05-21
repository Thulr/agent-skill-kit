#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

: "${SKILLS_CLI_VERSION:=1.5.7}"
: "${DISABLE_TELEMETRY:=1}"
: "${NPM_CONFIG_CACHE:=${XDG_CACHE_HOME:-$HOME/.cache}/npm}"
: "${NO_UPDATE_NOTIFIER:=1}"

export DISABLE_TELEMETRY NPM_CONFIG_CACHE NO_UPDATE_NOTIFIER
export npm_config_cache="$NPM_CONFIG_CACHE"
export npm_config_update_notifier=false

exec npx -y "skills@${SKILLS_CLI_VERSION}" add . --list
