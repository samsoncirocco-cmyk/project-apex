#!/bin/bash
# Project Apex - Task Verification Script
# Run this on the Mac Pro to validate Tasks 1-4 status

set -e

echo "=== Verifying Project Apex Infrastructure & Tasks ==="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_result() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}PASS${NC} $1"
    else
        echo -e "${RED}FAIL${NC} $1"
        if [ ! -z "$2" ]; then echo -e "  ${YELLOW}Hint: $2${NC}"; fi
    fi
}

# ------------------------------------------------------------------------------
# Task 1: Docker Compose Infrastructure
# ------------------------------------------------------------------------------
echo "--- Task 1: Infrastructure ---"
docker ps | grep -q "apex-redis"
check_result "Container: Redis" "Run ./deploy.sh"

docker ps | grep -q "apex-ollama"
check_result "Container: Ollama"

docker ps | grep -q "apex-sled-commander"
check_result "Container: Sled Commander"

# ------------------------------------------------------------------------------
# Task 2: Ollama + LiteLLM
# ------------------------------------------------------------------------------
echo "--- Task 2: AI Layer ---"
docker ps | grep -q "apex-litellm"
check_result "Container: LiteLLM" "Add 'litellm' service to docker-compose.yml"

if curl -s http://localhost:4000/health | grep -q "healthy"; then
    echo -e "${GREEN}PASS${NC} LiteLLM Health Check"
else
    echo -e "${RED}FAIL${NC} LiteLLM Health Check"
fi

# ------------------------------------------------------------------------------
# Task 3: SQLite + WAL Mode
# ------------------------------------------------------------------------------
echo "--- Task 3: SQLite Database ---"
DB_PATH="$HOME/apex/data/apex.db"

if [ -f "$DB_PATH" ]; then
    echo -e "${GREEN}PASS${NC} Database file exists"
    
    # Check WAL mode
    WAL_MODE=$(sqlite3 "$DB_PATH" "PRAGMA journal_mode;")
    if [ "$WAL_MODE" == "wal" ]; then
        echo -e "${GREEN}PASS${NC} WAL mode enabled"
    else
        echo -e "${RED}FAIL${NC} WAL mode is '$WAL_MODE' (expected 'wal')"
    fi
else
    echo -e "${RED}FAIL${NC} Database file missing at $DB_PATH"
fi

# ------------------------------------------------------------------------------
# Task 4: Telegram Gateway
# ------------------------------------------------------------------------------
echo "--- Task 4: Telegram Gateway ---"
# Check if python code exists in the container volume or mapped path
# Assuming standard path from deploy.sh
BOT_PATH="$HOME/apex/bots/sled-commander/bot.py" # Adjust filename as needed

if [ -f "$BOT_PATH" ]; then
    echo -e "${GREEN}PASS${NC} Bot code found ($BOT_PATH)"
    
    # Simple check for python-telegram-bot import in the file
    if grep -q "telegram" "$BOT_PATH"; then
        echo -e "${GREEN}PASS${NC} Telegram references found in code"
    else
        echo -e "${YELLOW}WARN${NC} No 'telegram' string found in bot code - is it implemented?"
    fi
else
    echo -e "${RED}FAIL${NC} Bot code missing at $BOT_PATH"
fi

# ------------------------------------------------------------------------------
# Task 15: Systemd
# ------------------------------------------------------------------------------
echo "--- Task 15: Auto-start ---"
if systemctl is-enabled docker-compose-apex &>/dev/null; then
    echo -e "${GREEN}PASS${NC} Service 'docker-compose-apex' enabled"
else
    echo -e "${RED}FAIL${NC} Service 'docker-compose-apex' not enabled"
fi

if systemctl is-active docker-compose-apex &>/dev/null; then
    echo -e "${GREEN}PASS${NC} Service 'docker-compose-apex' active"
else
    echo -e "${RED}FAIL${NC} Service 'docker-compose-apex' not active"
fi

echo ""
echo "=== Verification Complete ==="
