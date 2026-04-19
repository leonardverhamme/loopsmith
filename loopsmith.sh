#!/usr/bin/env sh
set -eu
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
export CODEX_HOME="${CODEX_HOME:-$SCRIPT_DIR}"
exec python3 "$SCRIPT_DIR/agentctl/agentctl.py" "$@"
