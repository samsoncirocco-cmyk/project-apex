# Mac Pro Server Deployment Checklist
**Updated:** 2026-01-29
**Server:** 192.168.0.140 (mcpro-server)
**Status:** 🔴 Server Offline - Cannot Connect

---

## 🚨 IMMEDIATE BLOCKER

**SSH Connection Failed:**
```bash
ssh samson@192.168.0.140
# Result: Operation timed out
```

**Before proceeding with ANY deployment steps:**
1. ✅ Power on Mac Pro server
2. ✅ Verify network connection
3. ✅ Test connectivity: `ping 192.168.0.140`
4. ✅ Test SSH: `ssh samson@192.168.0.140`

**Once server is accessible, proceed below.**

---

## 📋 Phase 1: Initial Server Setup (One-Time)

### ✅ Prerequisites Check

Run from your local machine:
```bash
# Check if setup script exists
ls -la ~/macpro-ubuntu-server/macpro_ubuntu_setup.sh

# Check if deployment scripts exist
ls -la ~/macpro-ubuntu-server/execution/deploy.sh
ls -la ~/macpro-ubuntu-server/execution/validate_setup.sh
ls -la ~/macpro-ubuntu-server/execution/health_check.sh
```

**Expected:** All files should exist ✅

---

### Step 1.1: Copy Setup Script to Server

```bash
# Copy setup script
scp ~/macpro-ubuntu-server/macpro_ubuntu_setup.sh samson@192.168.0.140:~/

# Verify copied
ssh samson@192.168.0.140 "ls -la ~/macpro_ubuntu_setup.sh"
```

**Expected Output:**
```
-rwxr-xr-x 1 samson samson 12847 Jan 29 macpro_ubuntu_setup.sh
```

---

### Step 1.2: Run Setup Script on Server

```bash
# SSH to server
ssh samson@192.168.0.140

# Make executable (if needed)
chmod +x ~/macpro_ubuntu_setup.sh

# Run setup
./macpro_ubuntu_setup.sh
```

**What This Installs:**
- Docker Engine + Docker Compose
- Portainer (Docker UI) on port 9000
- Ollama (AI runtime)
- Node.js 24 LTS (via nvm)
- Python 3.12+ (via apt)
- pipx for Python tools
- Salesforce CLI (`sf`)
- VS Code Server (web IDE) on port 8080
- Cockpit (system monitor) on port 9090
- Samba file sharing
- UFW firewall (configured)
- ffmpeg and media tools
- Automatic security updates

**Estimated Time:** 20-30 minutes
**Internet Required:** Yes (downloads ~2GB)

**Monitor Progress:**
- Watch for green ✅ checkmarks
- Script will pause for user confirmation at key steps
- If errors occur, script will show red ❌ and stop

**Success Indicators:**
```
✅ Docker installed successfully
✅ Portainer started on port 9000
✅ Ollama installed successfully
✅ Node.js 24 LTS installed
✅ VS Code Server started on port 8080
```

---

### Step 1.3: Verify Base Installation

Still on server (SSH session):

```bash
# Check Docker
docker --version
docker ps

# Check Ollama
ollama --version

# Check Python
python3 --version

# Check Node.js
node --version

# Check Salesforce CLI
sf --version
```

**Expected Output:**
```
Docker version 24.0+
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS
Ollama version 0.1+
Python 3.12+
v24.x.x
@salesforce/cli/2.x
```

**If any command fails, check setup script logs:**
```bash
tail -50 ~/macpro_ubuntu_setup.log
```

---

## 📋 Phase 2: Pull AI Models

**Still on server (SSH):**

### Step 2.1: Pull Ollama Models

```bash
# Primary model (large, powerful)
ollama pull gemma2:27b

# Fast jargon checking
ollama pull llama3.3:8b

# Alternative for code tasks
ollama pull qwen2.5:14b
```

**Download Sizes:**
- `gemma2:27b` → ~16GB
- `llama3.3:8b` → ~5GB
- `qwen2.5:14b` → ~9GB
- **Total:** ~30GB

**Estimated Time:**
- Fast internet (100+ Mbps): 15-30 minutes
- Medium internet (25-50 Mbps): 1-2 hours
- Slow internet (<10 Mbps): 3-4 hours

**Monitor Progress:**
```bash
# Check download status
ollama list

# Watch disk space
df -h
```

---

### Step 2.2: Verify Models

```bash
# List installed models
ollama list

# Test a model
ollama run llama3.3:8b "Hello, test"
```

**Expected Output:**
```
NAME              ID           SIZE
gemma2:27b        abc123       16GB
llama3.3:8b       def456       5GB
qwen2.5:14b       ghi789       9GB

Hello! How can I help you today?
```

**Exit test:** Type `/bye` or press Ctrl+D

---

## 📋 Phase 3: Deploy Project Apex Stack

**Return to your local machine (exit SSH):**

### Step 3.1: Verify Local Files

```bash
# Check Docker Compose files exist
ls -la ~/macpro-ubuntu-server/execution/docker-compose/

# Should see:
# - docker-compose.yml
# - docker-compose.dev.yml
# - Dockerfile.sled-commander
# - Dockerfile.tatt-architect
# - Dockerfile.security-warden
# - Dockerfile.sync-service
# - .env.example
```

---

### Step 3.2: Create Server .env File

**CRITICAL:** The deployment script copies `.env.example` to the server, but you need to configure it.

**Option A: Configure BEFORE deploying (Recommended):**

1. Copy example to working config:
```bash
cd ~/macpro-ubuntu-server/execution/docker-compose
cp .env.example config.env
```

2. Edit `config.env` with your credentials:
```bash
nano config.env
```

3. Add your Telegram tokens:
```bash
TELEGRAM_BOT_TOKEN=8415305740:AAHP2nbUROPxkWzXFu0OxbiKnxMv1wtVnI0
TELEGRAM_ALLOWED_USERS=8572676988
```

4. Add Notion token:
```bash
NOTION_API_KEY=<your_notion_integration_token>
```

5. Add Salesforce credentials (if using OAuth):
```bash
SF_CLIENT_ID=your_connected_app_client_id
SF_CLIENT_SECRET=your_connected_app_secret
SF_REFRESH_TOKEN=your_refresh_token
SF_INSTANCE_URL=https://login.salesforce.com
```

**Option B: Configure AFTER deploying:**
- Deploy first (containers will fail to start)
- SSH to server
- Edit `/home/samson/apex/config/.env`
- Restart containers

**Recommendation:** Use Option A to avoid failed container starts.

---

### Step 3.3: Run Deployment

```bash
cd ~/macpro-ubuntu-server/execution

# First deployment (builds images)
./deploy.sh --build
```

**What This Does:**
1. ✅ Checks SSH connectivity to Mac Pro
2. ✅ Creates remote directories at `/home/samson/apex`
3. ✅ Copies all Docker Compose files to server
4. ✅ Copies bot application code to server
5. ✅ Copies `.env` file (or creates from example)
6. ✅ Builds 4 Docker images (sled-commander, tatt-architect, security-warden, sync-service)
7. ✅ Starts 7 containers (4 bots + redis + ollama + litellm)
8. ✅ Shows container status

**Estimated Time:** 10-15 minutes (first build is slower)

**Success Output:**
```
======================================================================
=== Deployment Complete ===
======================================================================

Container Status:
NAMES                    STATUS              PORTS
apex-sled-commander      Up 30 seconds
apex-tatt-architect      Up 29 seconds
apex-security-warden     Up 28 seconds
apex-sync-service        Up 27 seconds
apex-redis               Up 31 seconds       6379/tcp
apex-ollama              Up 32 seconds       11434/tcp
apex-litellm             Up 30 seconds       4000/tcp

Deployment successful!
```

**If Containers Fail to Start:**
- Check logs: `ssh samson@192.168.0.140 "cd ~/apex && docker compose logs"`
- Most common issue: Missing `.env` variables
- Fix: SSH to server, edit `/home/samson/apex/config/.env`, run `docker compose up -d`

---

## 📋 Phase 4: Validation

### Step 4.1: Run Validation Script

```bash
# From local machine
cd ~/macpro-ubuntu-server/execution
./validate_setup.sh
```

**Expected Output:**
```
✓ PASS Container: apex-redis (healthy)
✓ PASS Container: apex-ollama (healthy)
✓ PASS Container: apex-litellm (healthy)
✓ PASS Container: apex-sled-commander (running)
✓ PASS Container: apex-tatt-architect (running)
✓ PASS Container: apex-security-warden (running)
✓ PASS Container: apex-sync-service (running)
✓ PASS Ollama models loaded (3 models)
✓ PASS Database initialized (/data/apex.db exists)

All checks passed!
```

**If ANY check fails:**
```bash
# Check specific container logs
ssh samson@192.168.0.140 "docker logs apex-sled-commander"

# Check container status
ssh samson@192.168.0.140 "docker ps -a"
```

---

### Step 4.2: Manual Container Verification

```bash
# SSH to server
ssh samson@192.168.0.140

# Check all containers
docker ps

# Should see 7 containers running:
# apex-sled-commander
# apex-tatt-architect
# apex-security-warden
# apex-sync-service
# apex-redis
# apex-ollama
# apex-litellm

# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"
```

---

### Step 4.3: Test Telegram Bots

Open Telegram on your phone/computer:

**Test SLED Commander:**
1. Open chat with `@FortiSledBot`
2. Send: `/start`
3. Expected: "👋 SLED Commander Online"
4. Send: `/status`
5. Expected: System status message

**Test TatT Architect:**
1. Open chat with `@TatTandDevBot`
2. Send: `/start`
3. Expected: Welcome message

**Test Security Warden:**
1. Open chat with `@secwardenbot`
2. Send: `/start`
3. Expected: Welcome message

**If NO response:**
- Check bot logs: `ssh samson@192.168.0.140 "docker logs apex-sled-commander"`
- Check `.env` file: `ssh samson@192.168.0.140 "cat ~/apex/config/.env | grep TELEGRAM"`
- Verify bot token is correct
- Restart container: `ssh samson@192.168.0.140 "docker restart apex-sled-commander"`

---

## 📋 Phase 5: Health Monitoring

### Step 5.1: Run Health Check

```bash
# From local machine
cd ~/macpro-ubuntu-server/execution
./health_check.sh
```

**Expected Output:**
```
======================================================================
Mac Pro Server Health Check
======================================================================

System Info:
  Hostname: mcpro-server
  Uptime: 2 hours, 15 minutes
  Load: 0.50, 0.45, 0.40

Resource Usage:
  CPU: 12 cores, 15% used
  Memory: 32GB total, 8GB used (25%)
  Disk: 1TB total, 250GB used (25%)

Docker Status:
  Containers: 7 running, 0 stopped
  Images: 8 total

Ollama Status:
  Service: Running
  Models: 3 loaded (gemma2:27b, llama3.3:8b, qwen2.5:14b)

Portainer:
  URL: http://192.168.0.140:9000
  Status: Accessible

Cockpit:
  URL: https://192.168.0.140:9090
  Status: Accessible
```

---

### Step 5.2: Access Web Interfaces

**Portainer (Docker Management):**
- URL: http://192.168.0.140:9000
- First login: Create admin password
- Navigate to "Containers" to see all Project Apex containers

**Cockpit (System Monitoring):**
- URL: https://192.168.0.140:9090
- Login: samson / <your_password>
- View CPU, memory, disk, network in real-time

**VS Code Server (Web IDE):**
- URL: http://192.168.0.140:8080
- Access server files via browser
- Edit code remotely

---

## 📋 Phase 6: Enable Auto-Start (Production)

**Once everything is working, enable auto-start on boot:**

```bash
# SSH to server
ssh samson@192.168.0.140

# Copy systemd service
sudo cp ~/apex/docker-compose-apex.service /etc/systemd/system/

# Enable service
sudo systemctl enable docker-compose-apex

# Check status
sudo systemctl status docker-compose-apex
```

**Expected Output:**
```
● docker-compose-apex.service - Project Apex Docker Compose Stack
   Loaded: loaded (/etc/systemd/system/docker-compose-apex.service; enabled)
   Active: active (running)
```

**Now Project Apex will auto-start on server reboot! ✅**

---

## 🛠 Useful Commands Reference

### Deployment Commands
```bash
# Deploy (from local machine)
cd ~/macpro-ubuntu-server/execution
./deploy.sh --build          # Build images and deploy
./deploy.sh --dev            # Deploy in dev mode
./deploy.sh                  # Deploy without rebuilding

# Validate deployment
./validate_setup.sh

# Check health
./health_check.sh
```

### Container Management (on server)
```bash
# SSH to server
ssh samson@192.168.0.140
cd ~/apex

# View all containers
docker compose ps

# View logs (all containers)
docker compose logs -f

# View logs (specific container)
docker compose logs -f sled-commander

# Restart a container
docker compose restart sled-commander

# Stop all containers
docker compose down

# Start all containers
docker compose up -d

# Rebuild and restart
docker compose up -d --build
```

### Debugging
```bash
# Check container status
docker ps -a

# View container logs (last 50 lines)
docker logs --tail 50 apex-sled-commander

# Follow logs in real-time
docker logs -f apex-sled-commander

# Execute command in container
docker exec -it apex-sled-commander /bin/bash

# Check container health
docker inspect apex-sled-commander | grep -A 10 Health
```

---

## ❌ Common Issues & Fixes

### Issue 1: Server Not Reachable
**Symptom:** `ssh: connect to host 192.168.0.140 port 22: Operation timed out`

**Causes:**
- Mac Pro is powered off
- Network cable disconnected
- IP address changed
- Firewall blocking SSH

**Fix:**
1. Power on Mac Pro
2. Check network connection
3. Verify IP: `ping 192.168.0.140`
4. Check firewall: `sudo ufw status`
5. Re-enable SSH: `sudo ufw allow ssh`

---

### Issue 2: Containers Not Starting
**Symptom:** `docker ps` shows containers as "Exited"

**Causes:**
- Missing .env variables
- Port conflicts
- Database initialization failed

**Fix:**
```bash
# Check logs
docker logs apex-sled-commander

# Check .env file
cat ~/apex/config/.env

# Check port conflicts
sudo netstat -tulpn | grep 6379  # Redis
sudo netstat -tulpn | grep 11434 # Ollama

# Restart container
docker compose up -d sled-commander
```

---

### Issue 3: Telegram Bots Not Responding
**Symptom:** No response when messaging bots

**Causes:**
- Wrong bot token in .env
- User ID not in TELEGRAM_ALLOWED_USERS
- Container crashed
- Network firewall blocking Telegram API

**Fix:**
```bash
# Check bot token
cat ~/apex/config/.env | grep TELEGRAM_BOT_TOKEN

# Check logs
docker logs apex-sled-commander

# Restart bot
docker restart apex-sled-commander

# Test network
curl https://api.telegram.org
```

---

### Issue 4: Ollama Models Missing
**Symptom:** "Model not found" errors

**Causes:**
- Models not pulled
- Ollama service not running
- Volume mount issue

**Fix:**
```bash
# Check Ollama status
docker exec -it apex-ollama ollama list

# Pull missing models
docker exec -it apex-ollama ollama pull gemma2:27b

# Restart Ollama
docker restart apex-ollama
```

---

## 📊 Deployment Checklist Summary

| Phase | Task | Status | Time |
|-------|------|--------|------|
| **1. Initial Setup** | Run macpro_ubuntu_setup.sh | ❌ TODO | 20-30 min |
| **2. AI Models** | Pull Ollama models (30GB) | ❌ TODO | 15min-2hrs |
| **3. Deploy** | Run deploy.sh --build | ❌ TODO | 10-15 min |
| **4. Validate** | Run validate_setup.sh | ❌ TODO | 2 min |
| **5. Test Bots** | Message all 3 Telegram bots | ❌ TODO | 5 min |
| **6. Auto-Start** | Enable systemd service | ❌ TODO | 2 min |

**Total Time:** 1-3 hours (depending on internet speed)

---

## 🎯 Next Steps

1. ✅ **FIRST:** Fix server connectivity (power on, check network)
2. ✅ Run Phase 1: Initial server setup
3. ✅ Run Phase 2: Pull Ollama models
4. ✅ Run Phase 3: Deploy Project Apex stack
5. ✅ Run Phase 4: Validation
6. ✅ Run Phase 5: Test Telegram bots
7. ✅ Run Phase 6: Enable auto-start

**Once deployed, you can:**
- Message bots via Telegram from anywhere
- Monitor containers via Portainer (http://192.168.0.140:9000)
- Check system health via Cockpit (https://192.168.0.140:9090)
- Edit code via VS Code Server (http://192.168.0.140:8080)

---

**Checklist Created:** 2026-01-29 12:45 MST
**For Server:** Mac Pro 6,1 @ 192.168.0.140
**Project:** Apex Multi-Agent Platform
