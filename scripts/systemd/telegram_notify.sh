#!/bin/bash
# scripts/systemd/telegram_notify.sh

# Default Project Root
PROJECT_ROOT="/home/samson/apex"

# Load environment variables
if [ -f "$PROJECT_ROOT/.env" ]; then
    # Use export to make variables available
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | grep -v '^\s*$' | xargs)
else
    echo "Error: .env file not found at $PROJECT_ROOT/.env"
    exit 1
fi

MESSAGE="$1"

if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_USER_ID" ]; then
    echo "Error: TELEGRAM_BOT_TOKEN or TELEGRAM_USER_ID not set."
    exit 1
fi

# Send message
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="${TELEGRAM_USER_ID}" \
    -d text="${MESSAGE}" \
    > /dev/null
