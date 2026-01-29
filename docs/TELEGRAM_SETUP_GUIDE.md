# Telegram Gateway Setup Guide

**Time required:** 5 minutes
**Cost:** FREE

---

## Step 1: Create Your Telegram Bot (2 minutes)

### 1.1 Open Telegram
- On your phone or computer
- Search for: `@BotFather`
- This is the official Telegram bot for creating bots

### 1.2 Start a Conversation
Send this message:
```
/newbot
```

### 1.3 Follow the Prompts

**BotFather will ask:** "Alright, a new bot. How are we going to call it?"
```
Your answer: Project Apex Commander
(or whatever name you want - this is just the display name)
```

**BotFather will ask:** "Good. Now let's choose a username for your bot."
```
Your answer: samson_apex_bot
(must end in 'bot' and be unique)
(try variations if taken: samsonapex_bot, samson_project_apex_bot, etc.)
```

### 1.4 Copy Your Bot Token

BotFather will reply with something like:
```
Done! Congratulations on your new bot...

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
```

**Copy the token** (the long string of numbers and letters)

---

## Step 2: Get Your Telegram User ID (30 seconds)

### 2.1 Search for Another Bot
In Telegram, search for: `@userinfobot`

### 2.2 Send Any Message
Just say "hi" or send any text

### 2.3 Copy Your User ID
The bot will reply with:
```
User ID: 123456789
First name: Samson
Username: @yourhandle
Language: en
```

**Copy the User ID number** (just the digits, no "User ID:" text)

---

## Step 3: Add Credentials to .env (1 minute)

### 3.1 Open the .env File
```bash
cd /Users/ciroccofam/project-apex
nano .env
# Or use any text editor
```

### 3.2 Find These Lines
```bash
# ============================================
# TELEGRAM BOT CONFIGURATION
# ============================================
TELEGRAM_BOT_TOKEN=
TELEGRAM_USER_ID=
```

### 3.3 Paste Your Credentials
```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567
TELEGRAM_USER_ID=123456789
```

### 3.4 Save and Close
- In nano: `Ctrl+X`, then `Y`, then `Enter`
- Or just save the file

---

## Step 4: Test the Gateway (2 minutes)

### 4.1 Install Python Dependencies
```bash
cd /Users/ciroccofam/project-apex
pip3 install python-telegram-bot python-dotenv
```

### 4.2 Run the Test Script
```bash
python3 execution/bots/shared/test_telegram.py
```

You should see:
```
🤖 PROJECT APEX - TELEGRAM GATEWAY TEST
======================================================================

✅ Environment check passed!
  • Bot token: 1234567890:ABCdefG...xyz-1
  • User ID: 123456789

🚀 Starting Telegram Gateway Test Bot...

✅ Bot configured successfully!

📱 Test Instructions:
  1. Open Telegram
  2. Search for your bot
  3. Send: /start
  ...
```

### 4.3 Test in Telegram

**Open Telegram and search for your bot** (e.g., `@samson_apex_bot`)

**Send these test commands:**
```
/start
/status
/test
/echo Hello World
```

**Try natural language:**
```
Hello
Show my pipeline
```

**Test approval buttons:**
```
/test_approval
```

You should get responses! 🎉

---

## Troubleshooting

### ❌ "Environment Check Failed"
**Problem:** Bot token or user ID not set in .env

**Fix:**
1. Make sure you edited `/Users/ciroccofam/project-apex/.env` (not `.env.example`)
2. Check no extra spaces around the `=` sign
3. Check the token has a `:` in the middle

---

### ❌ "HTTP 401: Unauthorized"
**Problem:** Bot token is invalid

**Fix:**
1. Go back to @BotFather
2. Send: `/mybot`
3. Select your bot
4. Send: `/token`
5. Copy the new token
6. Update .env

---

### ❌ Bot doesn't respond to your messages
**Problem:** User ID mismatch or bot not started

**Fix:**
1. Make sure the test script is running (you should see "Bot configured successfully!")
2. Verify your User ID:
   - Message @userinfobot again
   - Copy the exact number
   - Update .env if different
3. Restart the test script

---

### ❌ "ModuleNotFoundError: No module named 'telegram'"
**Problem:** python-telegram-bot not installed

**Fix:**
```bash
pip3 install python-telegram-bot python-dotenv
```

---

### ❌ Bot responds to other people's messages
**Problem:** User ID whitelist not working

**Fix:**
- This shouldn't happen! The gateway blocks unauthorized users
- Check the logs - should say "Unauthorized access attempt"
- If it's a real issue, check the `allowed_user_ids` in code

---

## What's Next?

Once the test bot is working:

1. **Stop the test bot** (Ctrl+C)
2. **You're ready to build the real bots!**
   - SLED Commander (Salesforce/Notion automation)
   - TatT Architect (Deployment monitoring)
   - Security Warden (Security monitoring)

Each bot will use this same Telegram gateway to communicate with you!

---

## Security Notes

### ✅ What Makes This Secure

1. **User ID Whitelist**
   - Only YOUR user ID can control the bot
   - Everyone else gets "Unauthorized" message
   - Impossible to guess (user IDs are random 9-digit numbers)

2. **Bot Token is Secret**
   - Stored in .env (never committed to Git)
   - Only you and Telegram know it
   - Can be revoked anytime via @BotFather

3. **End-to-End Encryption**
   - Messages between you and bot are encrypted by Telegram
   - Not even Telegram can read them (with "Secret Chats")

### 🔒 Best Practices

1. **Never share your bot token**
   - Treat it like a password
   - If leaked, revoke it via @BotFather

2. **Use different bots for dev vs production**
   - Create `samson_apex_test_bot` for testing
   - Create `samson_apex_prod_bot` for production
   - Use `TEST_TELEGRAM_BOT_TOKEN` in .env

3. **Rotate tokens periodically**
   - Set calendar reminder every 90 days
   - Generate new token via @BotFather
   - Update .env on all machines

4. **Monitor unauthorized access attempts**
   - Bots log all failed auth attempts
   - Review logs regularly
   - If you see many attempts, someone found your bot username

---

## Advanced: Multiple Users

Right now, only YOU can control the bot. To add more users:

### Option 1: Add More User IDs (Quick)

Edit `.env`:
```bash
# Single user (current)
TELEGRAM_USER_ID=123456789

# Multiple users (comma-separated)
TELEGRAM_USER_IDS=123456789,987654321,555555555
```

Then update code to parse comma-separated list.

### Option 2: Admin + Regular Users (Better)

- Create `TELEGRAM_ADMIN_IDS` - Full control
- Create `TELEGRAM_USER_IDS` - Read-only access
- Check user role before executing commands

This is out of scope for MVP but easy to add later!

---

## Useful BotFather Commands

Once your bot is created, you can configure it via @BotFather:

```
/setdescription - Change bot description
/setabouttext - Change "About" text
/setuserpic - Upload profile picture
/setcommands - Set command list (shows in Telegram menu)
/deletebot - Delete the bot
/revoke - Revoke bot token (generates new one)
```

**Recommended:** Set commands so users see them in Telegram menu:
```
/mybot
(select your bot)
/setcommands

Then paste:
start - Start the bot
help - Show all commands
status - Check bot status
pipeline - Show Salesforce pipeline
tasks - Show urgent tasks
```

---

## Cost & Limits

**Telegram Bot API is 100% FREE!**

**No limits on:**
- Number of messages
- Number of bots
- Number of users
- Storage

**Rate limits:**
- 30 messages/second per bot
- Way more than you'll ever need!

**No credit card required!**

---

## Need Help?

1. **Test script not working?**
   - Check the Troubleshooting section above
   - Make sure .env has correct values

2. **Bot not responding?**
   - Make sure test script is running
   - Check you're messaging the right bot

3. **Still stuck?**
   - Check logs (test script shows errors)
   - Try creating a new bot (start over from Step 1)
   - Read: https://core.telegram.org/bots/tutorial

---

**Ready to test?** Run `python3 execution/bots/shared/test_telegram.py` and message your bot! 🚀
