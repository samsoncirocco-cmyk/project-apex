# Project Apex - Multi-Agent AI Automation Platform

**3 AI bots working together to automate your business workflows**

---

## 🤖 The Three Bots

### 1. SLED Commander
**Job:** Manages your Salesforce deals and customers
- Checks Salesforce every few minutes
- Finds important updates (new deals, customer questions)
- Tells the other bots what to do
- Posts updates to Telegram so you know what's happening

### 2. TatT Architect
**Job:** Helps customers design tattoos
- Gets customer requests from SLED Commander
- Uses AI to generate tattoo design ideas
- Sends designs back to customers
- Tracks everything in Notion

### 3. Security Warden
**Job:** Keeps everything safe and working
- Watches all the bots to make sure they're healthy
- Checks if we're spending too much money on AI
- Alerts you if something breaks
- Makes sure we don't hit rate limits

---

## 🏗️ Project Structure

```
project-apex/
├── README.md                    # This file
├── CLAUDE.md                    # Instructions for AI agents
│
├── directives/                  # Layer 1: WHAT to do (SOPs)
│   ├── sled_commander.md
│   ├── tatt_architect.md
│   └── security_warden.md
│
├── orchestration/               # Layer 2: Decision making
│   └── (AI agents work here)
│
├── execution/                   # Layer 3: HOW to do it (code)
│   ├── bots/
│   │   ├── sled_commander/
│   │   ├── tatt_architect/
│   │   └── security_warden/
│   ├── docker-compose/
│   │   └── apex-stack.yml       # Runs all 3 bots together
│   └── scripts/
│       └── deploy.sh            # Copies everything to server
│
├── docs/                        # Documentation
│   ├── SETUP.md
│   └── API_KEYS.md
│
└── .tmp/                        # Temporary files
```

---

## 🚀 Quick Start

**On Mac mini (where you are now):**
```bash
# 1. Set up API keys
cp .env.example .env
nano .env  # Add your real API keys

# 2. Deploy to server
./execution/scripts/deploy.sh
```

**Check if it's working:**
- Open Portainer: http://192.168.0.140:9000
- Look for 3 containers: sled-commander, tatt-architect, security-warden
- All should show green "running" status

---

## 📦 What Gets Installed on Server

**Python packages:**
- `python-telegram-bot` - Talk to Telegram
- `litellm` - Route AI requests (Ollama → Gemini → Claude → OpenAI)
- `notion-client` - Save data to Notion
- `simple-salesforce` - Talk to Salesforce

**Docker containers:**
- Each bot runs in its own container (isolated, safe)
- All 3 containers talk to each other via Docker network
- Ollama already running on server (for free local AI)

---

## 🎛️ How Docker Containers Work

**Think of your server like an apartment building:**

```
Mac Pro Server = The Building
├── Docker Container 1 = Apartment for SLED Commander
│   └── Has: Python, Telegram bot, Salesforce connection
├── Docker Container 2 = Apartment for TatT Architect
│   └── Has: Python, AI models, Notion connection
└── Docker Container 3 = Apartment for Security Warden
    └── Has: Python, monitoring tools, alerts

Ollama = Shared gym in the building (all bots can use it)
```

**Why this is awesome:**
- Each bot has its own space (won't mess with each other)
- If one bot crashes, others keep working
- Easy to update one bot without touching the others
- Can restart individual bots without restarting everything

---

## 🔑 API Keys Needed

You'll need to get these and put them in `.env` file:

1. **Telegram Bot Token** (free)
   - Go to: https://t.me/BotFather
   - Type: `/newbot`
   - Follow instructions
   - Copy token

2. **Salesforce Credentials** (you already have these)
   - Username
   - Password
   - Security Token

3. **Notion Integration Token** (free)
   - Go to: https://www.notion.so/my-integrations
   - Click "New integration"
   - Copy token

4. **AI API Keys** (optional - Ollama is free and runs locally!)
   - Gemini: https://ai.google.dev/ (free tier)
   - Claude: https://console.anthropic.com/ (pay as you go)
   - OpenAI: https://platform.openai.com/ (pay as you go)

---

## 📊 Monitoring Your Bots

**Via Portainer (easiest):**
1. Open: http://192.168.0.140:9000
2. Click "Containers"
3. See all 3 bots with status
4. Click a bot → "Logs" to see what it's doing

**Via Telegram:**
- Each bot sends you messages when something important happens
- You can send commands to the bots
- Like texting with your bots!

**Via Cockpit (server health):**
1. Open: https://192.168.0.140:9090
2. See CPU/RAM usage
3. Make sure bots aren't using too much

---

## 🐛 Troubleshooting

**Bot won't start:**
```bash
ssh macpro "docker logs sled-commander"  # See what went wrong
```

**Bot keeps crashing:**
```bash
ssh macpro "docker restart sled-commander"
```

**Need to update a bot:**
```bash
./execution/scripts/deploy.sh  # Redeploy everything
```

**Emergency stop everything:**
```bash
ssh macpro "docker-compose -f /home/samson/apex/docker-compose.yml down"
```

---

## 🎯 Development Workflow

1. **Edit code on Mac mini** (in this project-apex folder)
2. **Test changes** (optional local testing)
3. **Deploy to server** (`./execution/scripts/deploy.sh`)
4. **Check Portainer** (make sure containers restarted)
5. **Watch logs** (see if bots are happy)

---

## 📈 What Success Looks Like

After deploying, you should see:

✅ 3 green containers in Portainer
✅ Telegram messages from bots saying "I'm alive!"
✅ SLED Commander checking Salesforce every few minutes
✅ TatT Architect responding to customer requests
✅ Security Warden posting health updates

---

## 🔄 Next Steps

1. Create the 3 bot scripts
2. Set up Docker containers
3. Configure API keys
4. Deploy to server
5. Test with real Salesforce data
6. Monitor and improve

---

**Status:** 🏗️ Under construction
**Created:** 2026-01-29
**Server:** Mac Pro (mcpro-server) @ 192.168.0.140

---

**Questions?** Read docs/SETUP.md for detailed step-by-step guide!
