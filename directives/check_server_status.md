# Directive: Check Server Status

## Goal
Verify the Mac Pro Ubuntu server is healthy and all services are running correctly.

## Inputs
- Server IP: 192.168.0.140
- SSH credentials available

## Tools/Scripts to Use
- `execution/health_check.sh` - Comprehensive health check script
- Direct SSH commands if script doesn't exist yet

## Process

### 1. Basic Connectivity
```bash
ssh macpro "uptime"
```
**Expected**: Server responds with uptime

### 2. Check Core Services
```bash
ssh macpro "systemctl status docker ollama code-server"
```
**Expected**: All services active (running)

### 3. Check Docker Containers
```bash
ssh macpro "docker ps"
```
**Expected**: Portainer and any deployed containers running

### 4. Check Disk Space
```bash
ssh macpro "df -h / /home"
```
**Expected**: Less than 80% full

### 5. Check System Load
```bash
ssh macpro "uptime && free -h"
```
**Expected**: Load average < number of cores, RAM not exhausted

### 6. Check Web Services
- Portainer: http://192.168.0.140:9000
- VS Code Server: http://192.168.0.140:8080
- Cockpit: https://192.168.0.140:9090

**Expected**: All respond with login pages

## Outputs
- Health status report (all green / issues found)
- List of any problems requiring attention
- Recommendations for action

## Edge Cases

**Server not responding:**
- Check if Mac Pro is powered on
- Check network connectivity
- Try pinging: `ping 192.168.0.140`

**Services down:**
- Check logs: `journalctl -u SERVICE_NAME -n 50`
- Restart if needed: `sudo systemctl restart SERVICE_NAME`

**High disk usage:**
- Check Docker: `docker system df`
- Clean if needed: `docker system prune -a`

**High load:**
- Check processes: `htop` or `top`
- Identify resource-heavy containers

## Timing
- Full check: ~30 seconds
- Run: On-demand or daily automated

## Notes
- All services should auto-start on boot
- Portainer provides web UI for Docker monitoring
- Cockpit provides web UI for system monitoring
- Use `./execution/health_check.sh` once created for automated checks
