#!/usr/bin/env bash

set -u

ENV_FILE="$HOME/.config/sineos/monitoring/open-webui.env"
HEALTH_URL="http://127.0.0.1:3000/health"

[[ -r "$ENV_FILE" ]] || exit 1

source "$ENV_FILE"

[[ -n "${PUSH_URL:-}" ]] || exit 1

if curl --silent --fail --max-time 5 "$HEALTH_URL" >/dev/null; then
    curl --silent --fail --max-time 5 "$PUSH_URL" >/dev/null
fi
