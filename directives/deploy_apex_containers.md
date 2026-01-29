# Directive: Deploy Apex Containers

## Goal

Deploy and manage the 6-container Project Apex stack on Mac Pro Ubuntu server.

## Inputs

- Server IP: 192.168.0.140
- Docker Compose files in `~/apex/`
- Environment file `.env` configured with secrets

## Tools/Scripts to Use

- `execution/docker-compose/docker-compose.yml` - Production stack
- `execution/docker-compose/docker-compose.dev.yml` - Development overrides

## Process

### 1. Pre-flight Checks

```bash
# Verify Docker is running
ssh macpro "systemctl status docker"

# Verify volumes exist
ssh macpro "ls -la ~/apex/data ~/apex/config ~/apex/backups"

# Verify .env is configured
ssh macpro "test -f ~/apex/.env && echo 'OK' || echo 'MISSING'"
```

**Expected**: Docker active, directories exist, .env present

### 2. Deploy Production Stack

```bash
ssh macpro "cd ~/apex && docker compose up -d"
```

**Expected**: All 6 containers start

### 3. Verify Deployment

```bash
# Check all containers running
ssh macpro "docker compose -f ~/apex/docker-compose.yml ps"

# Check health status
ssh macpro "docker ps --format 'table {{.Names}}\t{{.Status}}'"
```

**Expected**: All containers "Up" with healthy status

### 4. Deploy Development Stack (if needed)

```bash
ssh macpro "cd ~/apex && docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d"
```

## Rollback Procedure

### Stop All Containers

```bash
ssh macpro "cd ~/apex && docker compose down"
```

### Rollback to Previous Version

```bash
ssh macpro "cd ~/apex && git checkout HEAD~1 -- docker-compose.yml && docker compose up -d"
```

### Full Reset (Caution: Data Loss)

```bash
ssh macpro "cd ~/apex && docker compose down -v"  # Removes volumes!
```

## Outputs

- 6 running containers in healthy state
- Internal network `apex-net` active
- Volumes mounted at `/data`, `/config`, `/backups`

## Edge Cases

**Container won't start:**

```bash
# Check logs
ssh macpro "docker compose logs SERVICE_NAME"
# Check resource availability
ssh macpro "docker stats --no-stream"
```

**Health check failing:**

```bash
# Inspect health details
ssh macpro "docker inspect --format='{{json .State.Health}}' CONTAINER_NAME | jq"
```

**Out of memory:**

```bash
# Check memory usage
ssh macpro "free -h && docker stats --no-stream"
# Reduce limits in docker-compose.yml if needed
```

**Network issues between containers:**

```bash
# Verify network exists
ssh macpro "docker network ls | grep apex-net"
# Inspect network
ssh macpro "docker network inspect apex-net"
```

## Timing

- Initial deployment: ~2-5 minutes (first image pull)
- Subsequent restarts: ~30 seconds
- Full rebuild: ~5-10 minutes

## Notes

- Redis and Ollama are internal services, not exposed to host
- Only Telegram gateway (sled-commander) handles external traffic
- Resource limits prevent any single container from exhausting Mac Pro
- Systemd service ensures auto-restart on reboot
