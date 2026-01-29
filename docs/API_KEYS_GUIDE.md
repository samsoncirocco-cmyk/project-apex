# API Keys & Credentials Setup Guide

This guide walks you through getting all the API keys needed for Project Apex.

---

## 🚨 Critical Keys (Required for Basic Functionality)

### 1. Telegram Bot Token ⭐ REQUIRED
**What it does:** Lets the bots talk to you via Telegram messages

**How to get it:**
1. Open Telegram and search for `@BotFather`
2. Send the message: `/newbot`
3. Follow the prompts:
   - **Bot name:** "Project Apex Commander" (or whatever you want)
   - **Username:** Must end in "bot" (e.g., `samson_apex_bot`)
4. BotFather will reply with your token (looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. **Copy this token** - you'll paste it into `.env` as `TELEGRAM_BOT_TOKEN`

**Cost:** FREE forever

---

### 2. Telegram User ID ⭐ REQUIRED
**What it does:** Security whitelist - only you can control the bots

**How to get it:**
1. Open Telegram and search for `@userinfobot`
2. Send any message to the bot
3. It will reply with your User ID (a number like `123456789`)
4. **Copy this number** - you'll paste it into `.env` as `TELEGRAM_USER_ID`

**Cost:** FREE

---

### 3. Salesforce Credentials ⭐ REQUIRED (for SLED Commander)
**What it does:** Lets SLED Commander read/write Salesforce data

**You need 3 things:**

#### A. Salesforce Username
- This is just your Salesforce login email
- Example: `samson@fortinet.com`

#### B. Salesforce Password
- Your regular Salesforce password

#### C. Salesforce Security Token
**How to get it:**
1. Log in to Salesforce
2. Click your profile picture (top right) → **Settings**
3. In the left sidebar, click **My Personal Information** → **Reset My Security Token**
4. Click **Reset Security Token** button
5. Check your email - Salesforce will send you the token
6. **Copy this token** - it's a long random string

**Final format in .env:**
```
SF_USERNAME=samson@fortinet.com
SF_PASSWORD=YourSalesforcePassword123
SF_SECURITY_TOKEN=abc123XYZ789randomToken
```

**Cost:** FREE (you already have Salesforce access)

---

### 4. Notion Integration Token ⭐ REQUIRED (for SLED Commander)
**What it does:** Lets SLED Commander sync Salesforce data to Notion databases

**How to get it:**
1. Go to: https://www.notion.so/my-integrations
2. Click **+ New integration**
3. Fill out the form:
   - **Name:** "Project Apex"
   - **Associated workspace:** Select your workspace
   - **Capabilities:** Leave defaults (Read content, Update content, Insert content)
4. Click **Submit**
5. Copy the **Internal Integration Token** (starts with `secret_`)
6. **Important:** Share your Notion databases with this integration:
   - Open each database you want to sync
   - Click **•••** (top right) → **Add connections**
   - Search for "Project Apex" and select it

**Find your Notion Database IDs:**
1. Open a database in Notion
2. Look at the URL: `notion.so/workspace/DATABASE_ID?v=...`
3. The `DATABASE_ID` is the long string of letters/numbers
4. Copy this for each database you want to sync

**Cost:** FREE forever

---

## 🤖 AI Model Keys (Optional but Recommended)

### 5. Google Gemini API Key (Secondary AI - High Context Tasks)
**What it does:** Handles large documents and complex research (1M+ token context)

**How to get it:**
1. Go to: https://aistudio.google.com/app/apikey
2. Click **Create API Key**
3. Select a Google Cloud project (or create a free one)
4. Copy the API key

**Cost:**
- **FREE TIER:** 15 requests/minute, 1500 requests/day
- **Paid:** $0.000125 per 1K input tokens, $0.0005 per 1K output tokens
- **Estimated:** $2-5/month with normal use

**Note:** If you don't provide this, bots will use Ollama locally (free) as fallback

---

### 6. Anthropic Claude API Key (Tertiary AI - Code & Logic)
**What it does:** Best for code architecture, debugging, and complex logic

**How to get it:**
1. Go to: https://console.anthropic.com/settings/keys
2. Click **Create Key**
3. Name it: "Project Apex"
4. Copy the key (starts with `sk-ant-`)

**Cost:**
- **Claude 3.5 Sonnet:** $3 per 1M input tokens, $15 per 1M output tokens
- **Estimated:** $3-10/month with normal use

**Note:** If you don't provide this, bots will use Gemini as fallback

---

### 7. OpenAI API Key (Quaternary AI - Security Reasoning)
**What it does:** Used ONLY for Security Warden's adversarial testing (o1 model)

**How to get it:**
1. Go to: https://platform.openai.com/api-keys
2. Click **+ Create new secret key**
3. Name it: "Project Apex Security"
4. Copy the key (starts with `sk-proj-` or `sk-`)

**Cost:**
- **GPT-4o:** $2.50 per 1M input tokens, $10 per 1M output tokens
- **o1:** $15 per 1M input tokens, $60 per 1M output tokens
- **Estimated:** $1-5/month (Security Warden runs infrequently)

**Note:** If you don't provide this, Security Warden will use Claude for testing

---

## 📦 Deployment Monitoring Keys (Optional - TatT Architect)

### 8. Vercel Token (Optional)
**What it does:** Monitors your Vercel deployments for failures

**How to get it:**
1. Go to: https://vercel.com/account/tokens
2. Click **Create Token**
3. Name it: "Project Apex Monitoring"
4. Scope: Select your projects or use full access
5. Copy the token

**Find your Project IDs:**
1. Go to your Vercel project
2. Click **Settings** → **General**
3. Look for **Project ID** - copy this

**Cost:** FREE

---

### 9. Railway Token (Optional)
**What it does:** Monitors your Railway deployments for failures

**How to get it:**
1. Go to: https://railway.app/account/tokens
2. Click **Create Token**
3. Name it: "Project Apex Monitoring"
4. Copy the token

**Cost:** FREE

---

## 📋 Quick Setup Checklist

Copy this checklist and check off as you collect keys:

```
[ ] 1. Telegram Bot Token (BotFather)
[ ] 2. Telegram User ID (userinfobot)
[ ] 3. Salesforce Username (your email)
[ ] 4. Salesforce Password (your password)
[ ] 5. Salesforce Security Token (email after reset)
[ ] 6. Notion Integration Token (my-integrations)
[ ] 7. Notion Database IDs (from URLs)
[ ] 8. Gemini API Key (optional - aistudio.google.com)
[ ] 9. Claude API Key (optional - console.anthropic.com)
[ ] 10. OpenAI API Key (optional - platform.openai.com)
[ ] 11. Vercel Token (optional - vercel.com/account/tokens)
[ ] 12. Railway Token (optional - railway.app/account/tokens)
```

---

## 💰 Cost Summary

**Minimum Cost (Required Keys Only):**
- **$0/month** - Everything can run on free tiers!
  - Telegram: FREE
  - Salesforce: You already have it
  - Notion: FREE
  - Ollama: FREE (runs locally)

**Recommended Setup (AI API Keys):**
- **~$5-15/month** - Add cloud AI for better responses
  - Gemini: $2-5/month (generous free tier)
  - Claude: $3-10/month (pay as you go)
  - OpenAI: $1-5/month (Security Warden only)

**Total Estimated:** $5-15/month with normal usage

---

## 🔒 Security Best Practices

1. **Never commit .env to Git**
   - Already in .gitignore, but be careful!

2. **Use different API keys for development vs production**
   - Create a second Telegram bot for testing
   - Use test Salesforce sandbox if available

3. **Rotate keys every 90 days**
   - Set a calendar reminder
   - Most platforms let you create new keys without breaking old ones

4. **Store production .env on Mac Pro server only**
   - Don't keep production keys on your laptop
   - Use `scp` to copy .env to server after setup

5. **Use API key restrictions where available**
   - Google Cloud: Restrict by IP address (192.168.0.140)
   - OpenAI: Set usage limits ($10/month max)

---

## 🚀 Next Steps

After collecting all keys:

1. **Copy the example file:**
   ```bash
   cd /Users/ciroccofam/project-apex
   cp .env.example .env
   ```

2. **Edit .env and paste your keys:**
   ```bash
   nano .env
   # Or use any text editor
   ```

3. **Verify .env is not tracked by Git:**
   ```bash
   git status
   # Should NOT see .env in the list
   ```

4. **Test the setup:**
   - We'll test each integration as we build the bots
   - Start with Telegram (easiest to verify)

---

## ❓ Troubleshooting

**Q: My Telegram bot isn't responding**
- Check: Is `TELEGRAM_BOT_TOKEN` correct? No extra spaces?
- Check: Is `TELEGRAM_USER_ID` your actual ID from userinfobot?
- Test: Send `/start` to your bot - should get a response

**Q: Salesforce authentication fails**
- Check: Is security token correct? (Reset it to get a fresh one)
- Check: Did you concatenate password + token? Should be separate fields
- Check: Is your Salesforce password expired?

**Q: Notion integration not working**
- Check: Did you share your databases with the integration?
- Check: Are database IDs correct? (No `?v=` part, just the ID)
- Check: Does integration have "Insert content" capability?

**Q: AI models not responding**
- Check: Are API keys valid? Try them in the provider's playground first
- Check: Do you have billing set up? (Claude/OpenAI require payment method)
- Fallback: System will use Ollama locally if cloud APIs fail

---

## 📞 Getting Help

If you get stuck:

1. **Check the .env.example file** - Has comments for each key
2. **Read error messages carefully** - Usually tell you what's wrong
3. **Test one service at a time** - Don't try to set up everything at once
4. **Use test/sandbox accounts first** - Before using production Salesforce

---

**Ready to collect your keys?** Start with the critical ones (Telegram, Salesforce, Notion) and add the optional AI keys later!
