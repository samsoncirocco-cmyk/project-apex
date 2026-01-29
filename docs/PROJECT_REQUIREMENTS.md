# Project Apex: Sovereign Multi-Agent AI Automation Platform

## Overview

Project Apex is a sovereign, locally-hosted multi-agent AI system that replaces third-party "black box" agents with a transparent, modular architecture running on an Ubuntu-based Mac Pro. The system provides three specialized AI bots that communicate through a secure Telegram gateway, ensuring sensitive business data never leaves the local network unless explicitly processed by user-selected AI models.

## Problem Statement

Current AI automation tools like Clawdbot present critical security and transparency issues:
- Sensitive business data (Salesforce pipelines, Notion databases, proprietary code) is processed by external services without visibility
- No guaranteed uptime when AI providers experience outages or rate limits
- Lack of human oversight for high-stakes business actions
- Generic responses that don't align with specific business communication standards
- No control over data sovereignty and processing location

## Jobs to Be Done

When managing multiple business domains (sales, development, security), I want a specialized AI agent for each domain so that I can automate routine tasks while maintaining complete control over my data and requiring explicit approval for critical actions.

## Solution Architecture

### Core Infrastructure
- **Host Environment**: Ubuntu on Mac Pro (local execution)
- **Orchestration**: Python 3.12 with asyncio, custom modular architecture
- **AI Router**: LiteLLM with fail-safe hierarchy (Ollama local → Gemini 3 Pro → Claude 3.5 Sonnet → OpenAI GPT-4o/o1)
- **Communication Gateway**: Telegram Bot API via python-telegram-bot library
- **Data Persistence**: SQLite for local, ACID-compliant storage
- **Process Management**: systemd services for automatic restart on reboot

### The Three-Bot Army

#### 1. SLED Commander (Fortinet Sales Professional)
**Primary AI Model**: Gemini 3 Pro (1M+ token context)
**Purpose**: Sales engineering and account management automation

#### 2. TatT Architect (Developer & Founder)
**Primary AI Model**: Claude 3.5 Sonnet (code architecture) with Gemini 3 Pro fallback
**Purpose**: Startup development and deployment management

#### 3. Security Warden (Guardian of 6eyes.dev & IRL)
**Primary AI Model**: OpenAI o1/o4 (adversarial reasoning)
**Purpose**: Security testing and infrastructure monitoring

## Functional Requirements

### SLED Commander Capabilities
- Monitor Salesforce pipeline using `sf` CLI for real-time queries
- Execute complex CRUD operations via Salesforce REST API
- Sync all account data and follow-ups to Notion as "Source of Truth" using notion-client SDK
- Perform daily 8:00 AM automated research scans of Arizona procurement portals (Linux Cron)
- Send Telegram notifications for new leads matching territory keywords
- Track high-value opportunities (e.g., $111K Hastings College deal)
- Generate quote drafts requiring human approval for amounts >$100K
- Communicate in jargon-free language ("Sending quote to Hastings..." not "Executing SFDX data record update")

### TatT Architect Capabilities
- Monitor Vercel and Railway deployments via webhooks + polling
- Alert via Telegram on build failures with simple explanations
- Perform "Vibe Coding" with full repository context understanding
- Optimize AR "try-on" feature placement math using Gemini 3 Pro
- Track deployment health for production endpoints
- Manage code architecture decisions with Claude 3.5 Sonnet

### Security Warden Capabilities
- Perform hourly health checks on 6eyes.dev and IRL API endpoints
- Execute adversarial "Red Team" testing for prompt injection vulnerabilities
- Monitor Mac Pro system resources (CPU, memory, disk)
- Send urgent Telegram alerts for security issues or system anomalies
- Validate firewall configurations and access controls

### Cross-Bot Capabilities
- Respond to Telegram commands from authorized user only
- Route requests through LiteLLM fail-safe hierarchy
- Maintain conversation context in SQLite
- Sync all generated/modified data to Notion within 60 seconds
- Present inline keyboard approval buttons for high-stakes actions
- Log all actions with timestamps and outcomes

## Technical Requirements

### AI Model Integration
- **LiteLLM Configuration**: Primary (Ollama local - free, privacy-first) → Secondary (Gemini 3 Pro - high-context cloud tasks) → Tertiary (Claude 3.5 Sonnet - code/logic cloud tasks) → Quaternary (OpenAI GPT-4o/o1 - security reasoning)
- **Cost Optimization**: Ollama runs locally on Mac Pro at zero API cost, only escalate to cloud models when local capacity insufficient or specific model capabilities required
- **Automatic Failover**: If primary model fails (rate limit, outage), route to secondary without user intervention
- **Context Window Management**: Leverage Gemini 3 Pro's 1M+ token window for document-heavy tasks that exceed Ollama's capacity
- **Model Selection Logic**: Route security reasoning to OpenAI o1/o4, code architecture to Claude 3.5 Sonnet, research to Gemini 3 Pro, routine queries to Ollama

### Salesforce Integration
- **CLI Operations**: Use `sf` CLI for fast pipeline queries and opportunity status checks
- **REST API Operations**: Use Salesforce REST API for complex metadata updates, quote generation, and bulk operations
- **Authentication**: Secure credential storage in .env with encrypted disk access
- **Rate Limiting**: Respect Salesforce API limits with exponential backoff

### Notion Integration
- **SDK**: Official notion-client Python SDK
- **Sync Direction**: Bidirectional (read priorities, write call notes and tasks)
- **Sync Latency**: Queue bot-generated data, sync as fast as Notion API allows (max 3 req/sec rate limit), target <5 minutes for batch operations, <60 seconds for single updates
- **Database Structure**: Account databases, follow-up queues, daily priority lists

### Telegram Gateway
- **Framework**: python-telegram-bot with asyncio support
- **Bot API Version**: 7.0+
- **Message Types**: Text commands, inline keyboards for approvals, status updates
- **User Verification**: Hardcoded Telegram User ID whitelist (single authorized user)
- **Command Structure**: Natural language processing for intent detection

### Deployment Monitoring
- **Vercel/Railway**: Webhook listeners for real-time build status
- **Polling Interval**: 5-minute health checks for endpoint uptime
- **Alert Triggers**: Build failures, endpoint downtime, response time >5s
- **Notification Format**: Simple, actionable messages via Telegram

### Scheduling System
- **System-Level Tasks**: Linux Cron for 8:00 AM daily research scans
- **Application-Level Tasks**: APScheduler for complex timing ("Remind me in 2 hours")
- **Task Persistence**: Store scheduled tasks in SQLite to survive restarts
- **Timezone**: All schedules in user's local timezone (Arizona)

### Data Persistence
- **Database**: SQLite with ACID compliance
- **Schema**: Conversation history, task queues, bot state, scheduled actions
- **Backup Strategy**: Daily automated backups to encrypted external storage
- **Data Retention**: 90 days for conversation history, indefinite for task outcomes

### Security Architecture
- **Layer 1**: Telegram User ID whitelist (hardcoded in configuration)
- **Layer 2**: .env file for API keys and credentials (never committed to version control)
- **Layer 3**: Ubuntu disk encryption for sensitive project files
- **Layer 4**: Network isolation (Mac Pro not exposed to public internet)
- **Audit Trail**: All bot actions logged with user ID, timestamp, and outcome

### System Services
- **Service Manager**: systemd for process persistence
- **Auto-Restart**: Bots restart automatically on Mac Pro reboot
- **Health Monitoring**: systemd watchdog for process health
- **Logging**: systemd journal for centralized log management

## User Experience Requirements

### Telegram Interaction Patterns
- **Command Format**: Natural language ("What's the status of Hastings?") not rigid syntax
- **Response Time**: <3 seconds for simple queries, <10 seconds for AI-generated responses
- **Status Updates**: Proactive notifications for critical events (new leads, build failures, security alerts)
- **Approval Workflow**: Inline keyboard with "Approve" / "Reject" buttons for high-stakes actions

### Communication Standards (Rule #1: Talk Simple)
- **Success State**: "Updating Hastings Opportunity..." ✅
- **Failure State**: "Executing SFDX data record update" ❌
- **Error Messages**: Plain language with actionable next steps
- **Technical Details**: Hidden unless explicitly requested

### Human-in-the-Loop Approval
- **Trigger Conditions**:
  - Salesforce quotes >$100K
  - Email sends to customers
  - Code deployments to production
  - Security configuration changes
- **Approval Interface**: Telegram inline keyboard
- **Timeout**: 24-hour expiration for pending approvals
- **Audit**: All approvals/rejections logged with timestamp

## Integration Points

### External Services
- **Salesforce**: sf CLI + REST API
- **Notion**: notion-client SDK
- **Vercel**: Webhook + REST API
- **Railway**: Webhook + REST API
- **Telegram**: Bot API 7.0+
- **LiteLLM**: AI model router

### AI Model Providers
- **Google Gemini 3 Pro**: Primary orchestrator, research, high-context tasks
- **Anthropic Claude 3.5 Sonnet**: Code architecture, logic, development
- **OpenAI GPT-4o/o1/o4**: Security reasoning, adversarial testing

- **Ollama (Local)**: Free, privacy-first local inference for routine queries, intent detection, jargon checking

### Local System Integration
- **Python Virtual Environment**: apex_env for isolated dependencies
- **File System**: Direct access to local repositories and project files
- **System Resources**: CPU/memory monitoring via psutil
- **Network**: Local network access for API calls, no public exposure

## Error Handling & Recovery

### AI Model Failures
- **Scenario**: Primary model (Gemini 3 Pro) rate limited or unavailable
- **Recovery**: Automatic failover to Claude 3.5 Sonnet within 2 seconds
- **User Notification**: None (transparent failover)
- **Logging**: Record failover event with timestamp and reason

### Salesforce API Errors
- **Scenario**: Rate limit exceeded (5000 requests/24h)
- **Recovery**: Exponential backoff with jitter, queue requests
- **User Notification**: "Salesforce is busy, retrying in 30 seconds..."
- **Fallback**: Use cached data if available, mark as stale

### Notion Sync Failures
- **Scenario**: Notion API returns 503 Service Unavailable
- **Recovery**: Retry with exponential backoff (max 5 attempts)
- **User Notification**: "Notion sync delayed, will retry automatically"
- **Data Preservation**: Queue updates locally, sync when service recovers

### Telegram Gateway Disconnection
- **Scenario**: Network interruption or Telegram API downtime
- **Recovery**: Automatic reconnection with exponential backoff
- **User Notification**: None (transparent reconnection)
- **Message Queue**: Buffer outgoing messages, send when connection restored

### System Resource Exhaustion
- **Scenario**: Mac Pro CPU >90% or memory >95%
- **Recovery**: Throttle bot operations, defer non-critical tasks
- **User Notification**: "System resources high, prioritizing critical tasks"
- **Monitoring**: Security Warden sends alert if condition persists >5 minutes

### Deployment Monitoring Failures
- **Scenario**: Vercel webhook not received within expected timeframe
- **Recovery**: Fall back to polling mode (5-minute intervals)
- **User Notification**: "Monitoring Vercel via polling (webhook issue)"
- **Escalation**: Alert user if deployment status unknown for >15 minutes

## Performance Requirements

- **Telegram Response Time**: <3 seconds for cached queries, <10 seconds for AI-generated responses
- **Notion Sync Latency**: All bot-generated data reflected within 60 seconds
- **Salesforce Query Time**: <2 seconds for CLI operations, <5 seconds for REST API calls
- **AI Model Failover**: <2 seconds to switch from primary to secondary model
- **System Uptime**: 99.9% availability (excluding planned Mac Pro maintenance)
- **Concurrent Operations**: Support 3 bots operating simultaneously without performance degradation

## Scalability Considerations

- **Single-User Design**: Optimized for one authorized Telegram user (no multi-tenancy)
- **Bot Expansion**: Architecture supports adding new specialized bots without refactoring core
- **Model Provider Expansion**: LiteLLM router can add new AI providers without code changes
- **Data Growth**: SQLite handles up to 1M conversation records before performance tuning needed
- **API Rate Limits**: Respect provider limits (Salesforce 5K/day, Notion 3 req/sec)


## Implementation Priorities

### Phase 1: Core Infrastructure (Week 1-2)
1. Set up Mac Pro Ubuntu environment with Docker Compose
2. Configure Ollama with Gemma 3 27B and Llama 3.3 8B models
3. Implement LiteLLM router with failover hierarchy
4. Create SQLite database with WAL mode enabled
5. Set up Telegram bot gateway with user ID whitelist
6. Implement basic logging and error handling

### Phase 2: SLED Commander (Week 3-4)
1. Integrate Salesforce CLI and REST API
2. Implement Notion SDK integration with message queue
3. Build daily 8:00 AM procurement portal scanner (Cron)
4. Add jargon guardrail post-processing
5. Implement human-in-the-loop approval for quotes >$100K
6. Test end-to-end Salesforce → Notion sync

### Phase 3: TatT Architect & Security Warden (Week 5-6)
1. Implement Vercel/Railway webhook listeners
2. Add deployment health monitoring with polling fallback
3. Build Security Warden with hourly health checks
4. Implement SSH monitoring and fail2ban integration
5. Add "Lockdown" button for SSH emergency shutdown
6. Test all three bots running concurrently

### Phase 4: Observability & Hardening (Week 7-8)
1. Set up Prometheus exporters in each bot
2. Configure Grafana dashboards (cost, reliability, business, system)
3. Implement automated backup with LUKS encryption
4. Add weekly backup verification tests
5. Configure systemd services for production deployment
6. Load testing with simulated high-volume scenarios

### Phase 5: Production Launch (Week 9)
1. Final security audit and penetration testing
2. Deploy to Mac Pro production environment
3. Monitor for 48 hours with manual fallback ready
4. Document operational runbooks
5. Train on emergency procedures (backup restore, bot restart, SSH lockdown)

## Out of Scope

## Technical Recommendations

### Deployment Architecture

#### Docker Compose Isolation
- **Container Strategy**: Separate containers for each bot and shared services
  - `sled-commander`: Salesforce CLI + Python bot logic
  - `tatt-architect`: Node.js + Python bot logic
  - `security-warden`: Python bot logic + security tools
  - `sync-service`: Dedicated Notion/Salesforce sync queue processor
  - `redis`: Message queue for offline-first sync
  - `ollama`: Local AI model inference server
- **Volume Mounts**:
  - `/data/apex.db`: SQLite database (persistent)
  - `/data/backups`: Backup destination
  - `/config/.env`: Shared secrets (read-only)
- **Network Isolation**: Internal Docker network, only Telegram gateway exposed
- **Resource Limits**: CPU/memory constraints per container to prevent resource exhaustion
- **Health Checks**: Docker health checks for automatic container restart
- **Benefits**:
  - Clean dependency isolation (Salesforce CLI doesn't conflict with Node.js versions)
  - Easy rollback (tag container versions)
  - Simplified deployment (single `docker-compose up` command)
  - Consistent environment across development and production

#### Alternative: systemd Services
- **When to Use**: If Docker overhead is unacceptable on Mac Pro
- **Trade-off**: More manual dependency management, but lower resource usage
- **Hybrid Approach**: Docker for development, systemd for production

### Observability Stack

#### Grafana + Prometheus Monitoring
- **Metrics Collection**:
  - **Cost Tracking**: API call counts per provider (Gemini/Claude/OpenAI), estimated cost per day
  - **Failover Frequency**: LiteLLM model switching events, primary vs fallback usage ratio
  - **SLED Performance**: New leads discovered per day, Salesforce sync latency, Notion update queue depth
  - **System Health**: Mac Pro CPU/memory/disk usage, bot uptime, Telegram response times
  - **Error Rates**: Failed API calls, sync failures, model timeouts
- **Dashboard Panels**:
  - **Cost Dashboard**: Daily spend by AI provider, cost per bot, monthly projection
  - **Reliability Dashboard**: Model availability %, failover events timeline, sync queue status
  - **Business Dashboard**: SLED lead volume, opportunity pipeline value, quote approval rate
  - **System Dashboard**: Resource utilization, bot health status, alert history
- **Implementation**:
  - **Prometheus Exporter**: Custom Python exporter in each bot exposing metrics on `/metrics` endpoint
  - **Grafana Instance**: Lightweight Grafana container on Mac Pro, accessible via `localhost:3000`
  - **Retention**: 90 days of metrics data (aligned with conversation history retention)
- **Alerting**:
  - **Cost Threshold**: Alert if daily AI spend exceeds $10
  - **Failover Threshold**: Alert if primary model unavailable >10% of requests
  - **Business Threshold**: Alert if SLED lead volume drops >50% week-over-week

#### Alternative: Simple Logging
- **When to Use**: If Grafana overhead is too heavy for single-user system
- **Trade-off**: Manual log analysis vs real-time dashboards
- **Hybrid Approach**: Start with logging, add Grafana when metrics become critical

### Performance Optimization

#### SQLite WAL Mode (Already Specified)
- **Benefit**: Concurrent reads while writing, prevents database locks
- **Configuration**: `PRAGMA journal_mode=WAL;` on database initialization
- **Maintenance**: Auto-checkpoint on idle, manual checkpoint on backup

#### Redis for Message Queue
- **Benefit**: Fast in-memory queue, persistence to disk, pub/sub for real-time sync
- **Alternative**: RabbitMQ for more complex routing, but higher resource usage
- **Configuration**: Redis persistence enabled (RDB + AOF), max memory 256MB

#### Ollama Model Selection
- **Recommended Models**:
  - **Gemma 3 27B**: Best balance of speed and capability for intent detection
  - **Llama 3.3 8B**: Ultra-fast for jargon checking (post-processing guardrail)
  - **Qwen 2.5 14B**: Alternative for code understanding tasks
- **Quantization**: Use Q4_K_M quantization for 2-3x speed improvement with minimal quality loss
- **GPU Acceleration**: If Mac Pro has GPU, enable for 5-10x inference speed boost

### Security Hardening

#### fail2ban Configuration
- **SSH Protection**: Ban IP after 3 failed attempts for 1 hour
- **Monitoring**: Security Warden checks fail2ban status every 5 minutes
- **Integration**: Telegram alert with "Lockdown" button triggers immediate SSH service stop

#### Encrypted Backup Verification
- **Weekly Test**: Automated restore test to temporary location
- **Integrity Check**: SHA256 checksum verification on backup files
- **Alert**: Telegram notification if backup verification fails

### Scalability Path

#### When to Upgrade from Mac Pro
- **Trigger 1**: CPU usage consistently >80% for 7+ days
- **Trigger 2**: SQLite database exceeds 1M records (consider PostgreSQL)
- **Trigger 3**: Team size >1 (requires multi-user architecture)
- **Trigger 4**: Bot count >5 (consider Kubernetes for orchestration)

#### Migration Strategy
- **Phase 1**: Move to dedicated Ubuntu server (same architecture)
- **Phase 2**: Split bots across multiple servers (distributed architecture)
- **Phase 3**: Add load balancer and database replication (high availability)
- **Phase 4**: Kubernetes deployment (enterprise scale)

### Development Workflow

#### Local Development
- **Docker Compose**: `docker-compose -f docker-compose.dev.yml up` for local testing
- **Hot Reload**: Volume mount source code for live updates without rebuild
- **Test Telegram Bot**: Separate test bot token for development
- **Mock Services**: Mock Salesforce/Notion APIs for offline development

#### Deployment Process
- **Step 1**: Test changes locally with Docker Compose
- **Step 2**: Push to Git repository (private GitHub/GitLab)
- **Step 3**: SSH to Mac Pro, pull latest code
- **Step 4**: Run `docker-compose pull && docker-compose up -d` for zero-downtime update
- **Step 5**: Monitor Grafana dashboard for 10 minutes post-deployment
- **Rollback**: `docker-compose down && git checkout <previous-commit> && docker-compose up -d`



### Features Deferred to V2
- **Multi-User Support**: System designed for single authorized user. Multi-user requires authentication overhaul and data isolation. *Trigger: When team size >1*
- **Voice Commands**: Telegram voice message processing. Requires speech-to-text integration and context handling. *Trigger: When mobile-only usage >50%*
- **Web Dashboard**: Browser-based control panel. Telegram provides sufficient interface for MVP. *Trigger: When command complexity requires visual UI*
- **Custom AI Model Training**: Fine-tuning models on proprietary data. Use pre-trained models via LiteLLM. *Trigger: When response quality <80% accuracy*
- **Mobile App**: Native iOS/Android apps. Telegram serves as universal mobile interface. *Trigger: When Telegram limitations block critical features*

### Technical Complexity Deferred
- **Distributed Architecture**: Multi-server deployment. Single Mac Pro sufficient for MVP. *Trigger: When CPU usage consistently >80%*
- **Real-Time Collaboration**: Multiple bots editing same Notion page simultaneously. Sequential operations prevent conflicts. *Trigger: When sync conflicts >5/day*
- **Advanced NLP**: Custom intent classification models. Use LLM-based intent detection. *Trigger: When command misinterpretation >10%*
- **Blockchain Audit Trail**: Immutable action logging. SQLite audit sufficient for single-user. *Trigger: When compliance requires tamper-proof logs*

## Acceptance Criteria

### System Initialization
- **Given** the Mac Pro boots up, **when** systemd starts the bot services, **then** all three bots (SLED Commander, TatT Architect, Security Warden) connect to Telegram within 30 seconds and send "Bot online" status message
- **Given** the bots are running, **when** an unauthorized Telegram user sends a command, **then** the bot ignores the message and logs the attempt without responding

### SLED Commander Operations
- **Given** it's 8:00 AM Arizona time, **when** the Cron job triggers, **then** the SLED Commander scans Arizona procurement portals and sends a Telegram summary of new leads within 5 minutes
- **Given** a Salesforce opportunity is updated, **when** the change is detected via `sf` CLI, **then** the corresponding Notion database entry is updated within 60 seconds
- **Given** a user requests "What's the status of Hastings?", **when** the command is received, **then** the bot queries Salesforce and responds with current opportunity stage, amount, and next steps in <5 seconds
- **Given** a quote draft is generated for $150K, **when** the bot prepares to send it, **then** an inline keyboard approval button appears in Telegram and the quote is NOT sent until "Approve" is tapped

### TatT Architect Operations
- **Given** a Vercel deployment fails, **when** the webhook is received, **then** the bot sends a Telegram alert with a simple explanation ("Build failed: missing environment variable") within 10 seconds
- **Given** a Railway endpoint is down, **when** the 5-minute health check detects it, **then** the bot sends an urgent Telegram alert with the affected service name and last successful check time
- **Given** a user asks "Why did the last deploy fail?", **when** the command is received, **then** the bot retrieves the build log and provides a jargon-free summary in <10 seconds

### Security Warden Operations
- **Given** the hourly health check runs, **when** 6eyes.dev API responds with status 200, **then** no alert is sent and the check is logged silently
- **Given** the Mac Pro CPU exceeds 90%, **when** the condition persists for >5 minutes, **then** the Security Warden sends an urgent Telegram alert with current resource usage
- **Given** a Red Team test detects a prompt injection vulnerability, **when** the test completes, **then** the bot sends a detailed Telegram report with the exploit vector and suggested mitigation

### AI Model Failover
- **Given** Gemini 3 Pro returns a rate limit error, **when** a user command is received, **then** LiteLLM automatically routes to Claude 3.5 Sonnet and the response is delivered in <10 seconds without user notification of the failover
- **Given** all three AI providers are unavailable, **when** a user command is received, **then** the bot responds "AI services temporarily unavailable, retrying in 30 seconds" and queues the request

### Human-in-the-Loop Approval
- **Given** a high-stakes action requires approval, **when** the inline keyboard is presented, **then** the approval expires after 24 hours and the action is automatically cancelled with a Telegram notification
- **Given** a user taps "Approve" on a quote send, **when** the approval is received, **then** the quote is sent via Salesforce API and a confirmation message is sent to Telegram within 10 seconds
- **Given** a user taps "Reject" on a deployment, **when** the rejection is received, **then** the deployment is cancelled and the reason is logged in SQLite with timestamp

### Data Integrity
- **Given** the SLED Commander creates a new Salesforce opportunity, **when** the operation completes, **then** the opportunity appears in Notion within 60 seconds with all fields populated correctly
- **Given** a Notion database entry is manually updated, **when** the next sync occurs, **then** the bot detects the change and does NOT overwrite it with stale data
- **Given** the Mac Pro loses network connectivity, **when** connectivity is restored, **then** all queued Notion updates are synced in chronological order without data loss

### Communication Standards
- **Given** any bot operation completes, **when** the status message is sent, **then** it uses jargon-free language ("Updating Hastings Opportunity..." not "Executing SFDX data record update")
- **Given** an error occurs, **when** the error message is sent, **then** it includes a plain-language explanation and actionable next steps ("Salesforce is busy, retrying in 30 seconds" not "HTTP 429 Rate Limit Exceeded")

### System Recovery
- **Given** the Mac Pro reboots, **when** systemd starts the services, **then** all bots resume their scheduled tasks (Cron jobs, APScheduler tasks) without manual intervention
- **Given** a bot crashes, **when** systemd detects the failure, **then** the bot is automatically restarted within 10 seconds and sends a "Bot restarted" status message to Telegram
