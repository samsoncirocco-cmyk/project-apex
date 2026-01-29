# API Keys Status - What You Have vs What You Need

**Generated:** 2026-01-29

---

## ✅ Keys Found (Already Have)

### 1. Notion Integration Token
**Status:** ✅ FOUND
**Location:** `~/.config/notion/api_key`
**Value:** `ntn_****...****` (stored in .env)
**Added to .env:** Yes

### 2. OpenRouter API Key
**Status:** ✅ FOUND
**Location:** `/Users/ciroccofam/llm-council/.env`
**Value:** `sk-or-v1-****...****` (stored in .env)
**Added to .env:** Yes
**Note:** OpenRouter can be used as alternative AI router with access to 200+ models

---

## 🔴 Keys Still Needed (Priority Order)

### HIGH PRIORITY (Required for Core Functionality)

#### 1. Telegram Bot Token
**Status:** ❌ MISSING
**Why it's needed:** Without this, bots can't send you messages
**How to get:**
```
1. Open Telegram
2. Search for @BotFather
3. Send: /newbot
4. Follow instructions
5. Copy the token
```
**Cost:** FREE
**Time:** 2 minutes

#### 2. Telegram User ID
**Status:** ❌ MISSING
**Why it's needed:** Security whitelist - only you can control bots
**How to get:**
```
1. Open Telegram
2. Search for @userinfobot
3. Send any message
4. Copy your User ID (number)
```
**Cost:** FREE
**Time:** 30 seconds

#### 3. Salesforce Credentials (3 parts)
**Status:** ❌ MISSING
**Why it's needed:** SLED Commander needs to read/write Salesforce
**What you need:**
- SF_USERNAME (your Salesforce email)
- SF_PASSWORD (your Salesforce password)
- SF_SECURITY_TOKEN (reset at Settings → Reset My Security Token)

**Cost:** FREE (you already have Salesforce)
**Time:** 2 minutes to reset token

#### 4. Notion Database IDs
**Status:** ⚠️ PARTIAL (have API token, need database IDs)
**Why it's needed:** Tell SLED Commander which databases to sync to
**How to get:**
```
1. Open each database in Notion
2. Look at URL: notion.so/workspace/DATABASE_ID?v=...
3. Copy the DATABASE_ID part
```
**Databases needed:**
- NOTION_ACCOUNTS_DB_ID (for Salesforce accounts)
- NOTION_FOLLOWUPS_DB_ID (for tasks/follow-ups)
- NOTION_PRIORITIES_DB_ID (for daily priorities)

**Cost:** FREE
**Time:** 2 minutes

---

### MEDIUM PRIORITY (Improves AI Quality)

#### 5. Google Gemini API Key
**Status:** ❌ MISSING
**Why it's needed:** Better high-context AI (1M+ tokens), generous free tier
**Fallback:** Ollama local (free but lower quality)
**Get from:** https://aistudio.google.com/app/apikey
**Cost:** FREE tier (15 req/min), then $0.000125/1K tokens
**Time:** 2 minutes

#### 6. Anthropic Claude API Key
**Status:** ❌ MISSING
**Why it's needed:** Best for code architecture and logic
**Fallback:** Gemini or Ollama
**Get from:** https://console.anthropic.com/settings/keys
**Cost:** $3/1M input tokens, $15/1M output tokens
**Estimated:** $3-10/month
**Time:** 2 minutes

#### 7. OpenAI API Key
**Status:** ❌ MISSING
**Why it's needed:** Security Warden uses o1 for adversarial reasoning
**Fallback:** Claude or Gemini
**Get from:** https://platform.openai.com/api-keys
**Cost:** $15-60/1M tokens (o1), $2.50-10/1M tokens (GPT-4o)
**Estimated:** $1-5/month
**Time:** 2 minutes

---

### LOW PRIORITY (Optional Features)

#### 8. Vercel Token
**Status:** ❌ MISSING
**Why it's needed:** TatT Architect monitors Vercel deployments
**Skip if:** You don't use Vercel
**Get from:** https://vercel.com/account/tokens
**Cost:** FREE
**Time:** 1 minute

#### 9. Railway Token
**Status:** ❌ MISSING
**Why it's needed:** TatT Architect monitors Railway deployments
**Skip if:** You don't use Railway
**Get from:** https://railway.app/account/tokens
**Cost:** FREE
**Time:** 1 minute

---

## 📋 Quick Action Checklist

Copy this and check off as you go:

```
HIGH PRIORITY (Required):
[ ] Get Telegram Bot Token from @BotFather
[ ] Get Telegram User ID from @userinfobot
[ ] Get Salesforce username (you already know this)
[ ] Get Salesforce password (you already know this)
[ ] Reset Salesforce security token (Settings → Reset)
[ ] Get 3 Notion database IDs from your database URLs

MEDIUM PRIORITY (Recommended):
[ ] Get Gemini API key from aistudio.google.com
[ ] Get Claude API key from console.anthropic.com
[ ] Get OpenAI API key from platform.openai.com

LOW PRIORITY (Optional):
[ ] Get Vercel token (if you use Vercel)
[ ] Get Railway token (if you use Railway)
[ ] Add monitored endpoints (URLs to health check)
[ ] Add territory keywords (for procurement scanner)
```

---

## 🎯 Minimum Viable Setup

To get Project Apex working with basic functionality:

**Absolute Minimum (free, no AI):**
1. Telegram Bot Token
2. Telegram User ID
3. Use Ollama locally for AI (free)

**For SLED Commander (sales automation):**
4. Salesforce credentials (username, password, security token)
5. Notion database IDs

**For Better AI Responses:**
6. At least ONE of: Gemini, Claude, or OpenAI API key
   - Gemini has best free tier
   - You already have OpenRouter which gives you access to many models

---

## 💡 Pro Tip: Start Small

Don't try to get all keys at once! Here's a recommended order:

1. **Day 1:** Get Telegram bot working (bot token + user ID)
   - Test: Send a message to your bot, get a response

2. **Day 2:** Add Salesforce integration (SF credentials)
   - Test: Ask bot "What's in my pipeline?"

3. **Day 3:** Add Notion sync (database IDs)
   - Test: Create Salesforce opportunity, see it in Notion

4. **Day 4:** Add AI keys (start with Gemini free tier)
   - Test: Ask complex questions, see better responses

---

## 🔐 Security Notes

**Keys you already have saved:**
- ✅ Notion token is in `~/.config/notion/api_key`
- ✅ OpenRouter key is in `~/llm-council/.env`

**Keys now in project-apex/.env:**
- ✅ Both keys above are copied to `.env`
- ⚠️ Make sure `.env` is in `.gitignore` (it is!)
- ⚠️ Never commit `.env` to Git

**Best practices:**
- Rotate all API keys every 90 days
- Use different Telegram bot for development vs production
- Set spending limits on paid APIs (OpenAI, Claude)
- Store production `.env` on Mac Pro server only

---

## 📊 Cost Breakdown

**What you have now:** $0/month (FREE)
- Notion: FREE
- OpenRouter: Pay-as-you-go (you can use free models)

**Adding minimum viable setup:** Still $0/month
- Telegram: FREE
- Salesforce: Already have it
- Ollama: FREE (runs locally)

**Adding recommended AI keys:** ~$5-15/month
- Gemini: $2-5/month (has free tier)
- Claude: $3-10/month
- OpenAI: $1-5/month (Security Warden only)

**Total expected cost:** $5-15/month with normal usage

---

## 🚀 Next Steps

1. **Fill in the HIGH PRIORITY keys first**
   - Edit `/Users/ciroccofam/project-apex/.env`
   - Add Telegram, Salesforce, Notion database IDs

2. **Test as you go**
   - We'll test each integration incrementally
   - Don't wait to get all keys before testing

3. **Add AI keys when ready**
   - System works with Ollama (free) as fallback
   - Add paid AI keys when you want better quality

4. **Deploy to Mac Pro**
   - Copy `.env` to server when ready
   - Never commit `.env` to Git!

---

**Questions?** See `docs/API_KEYS_GUIDE.md` for detailed step-by-step instructions!
