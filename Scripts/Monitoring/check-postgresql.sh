#!/usr/bin/env bash

set -u

ENV_FILE="$HOME/.config/sineos/monitoring/postgresql.env"
CONTAINER="sineos-postgres"

[[ -r "$ENV_FILE" ]] || exit 1

source "$ENV_FILE"

[[ -n "${PUSH_URL:-}" ]] || exit 1

if podman exec "$CONTAINER" \
    pg_isready -U sineos -d sineos >/dev/null 2>&1; then

    curl --silent --fail --max-time 5 "$PUSH_URL" >/dev/null
fi
