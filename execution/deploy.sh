#!/bin/bash
# Project Apex - Deployment Script
# Deploys the Docker Compose stack to Mac Pro Ubuntu server
#
# Usage:
#   ./deploy.sh          # Deploy production
#   ./deploy.sh --dev    # Deploy development
#   ./deploy.sh --build  # Rebuild images before deploy

set -e

# Configuration
SERVER="macpro"
REMOTE_PATH="/home/samson/apex"
LOCAL_PATH="$(dirname "$0")/docker-compose"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse arguments
DEV_MODE=false
REBUILD=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dev)
            DEV_MODE=true
            shift
            ;;
        --build)
            REBUILD=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}=== Project Apex Deployment ===${NC}"
echo ""

# 1. Check SSH connectivity
echo -e "${BLUE}[1/5] Checking SSH connectivity...${NC}"
if ! ssh -q $SERVER exit; then
    echo -e "${RED}Error: Cannot connect to $SERVER${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Connected to $SERVER${NC}"

# 2. Create remote directories
echo -e "${BLUE}[2/5] Creating remote directories...${NC}"
ssh $SERVER "mkdir -p $REMOTE_PATH/{data,backups,config,bots/{shared,sled-commander,tatt-architect,security-warden,sync-service}}"
echo -e "${GREEN}✓ Directories created${NC}"

# 2.5 Copy Bot Application Code
echo -e "${BLUE}[2.5/5] Copying application code...${NC}"
LOC_BOTS="$(dirname "$0")/../bots"
scp -r "$LOC_BOTS" "$SERVER:$REMOTE_PATH/"
echo -e "${GREEN}✓ Application code copied${NC}"

# 3. Copy Docker Compose files
echo -e "${BLUE}[3/5] Copying Docker Compose files...${NC}"
scp -r "$LOCAL_PATH/"* "$SERVER:$REMOTE_PATH/"
echo -e "${GREEN}✓ Files copied${NC}"

# 4. Check for .env file
echo -e "${BLUE}[4/5] Checking environment configuration...${NC}"
if ! ssh $SERVER "test -f $REMOTE_PATH/config/.env"; then
    echo -e "${YELLOW}Warning: .env file not found at $REMOTE_PATH/config/.env${NC}"
    echo -e "${YELLOW}Creating from template...${NC}"
    ssh $SERVER "cp $REMOTE_PATH/.env.example $REMOTE_PATH/config/.env"
    echo -e "${YELLOW}Please configure $REMOTE_PATH/config/.env before running containers${NC}"
fi
echo -e "${GREEN}✓ Environment checked${NC}"

# 5. Deploy containers
echo -e "${BLUE}[5/5] Deploying containers...${NC}"

COMPOSE_CMD="docker compose"
if [ "$DEV_MODE" = true ]; then
    COMPOSE_CMD="$COMPOSE_CMD -f docker-compose.yml -f docker-compose.dev.yml"
    echo -e "${YELLOW}Deploying in DEVELOPMENT mode${NC}"
else
    echo -e "${GREEN}Deploying in PRODUCTION mode${NC}"
fi

if [ "$REBUILD" = true ]; then
    COMPOSE_CMD="$COMPOSE_CMD up -d --build --remove-orphans"
else
    COMPOSE_CMD="$COMPOSE_CMD up -d --remove-orphans"
fi

ssh $SERVER "cd $REMOTE_PATH && $COMPOSE_CMD"

echo ""
echo -e "${GREEN}=== Deployment Complete ===${NC}"
echo ""

# Show status
echo -e "${BLUE}Container Status:${NC}"
ssh $SERVER "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep -E '^NAMES|apex'"

echo ""
echo -e "${GREEN}Deployment successful!${NC}"
echo ""
echo "Next steps:"
echo "  • Configure secrets: ssh $SERVER 'nano $REMOTE_PATH/config/.env'"
echo "  • View logs: ssh $SERVER 'docker compose -f $REMOTE_PATH/docker-compose.yml logs -f'"
echo "  • Enable auto-start: ssh $SERVER 'sudo cp $REMOTE_PATH/docker-compose-apex.service /etc/systemd/system/ && sudo systemctl enable docker-compose-apex'"
