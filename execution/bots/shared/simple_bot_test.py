#!/usr/bin/env python3
"""
Simple Bot Test - Run directly (not in background)

This is the simplest possible test - just run it and keep the terminal open.

Usage:
    python3 simple_bot_test.py

Then in Telegram, message any of your 3 bots!
Press Ctrl+C to stop.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment
env_path = Path(__file__).parents[3] / '.env'
load_dotenv(env_path)

SLED_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_SLED')
USER_ID = int(os.getenv('TELEGRAM_USER_ID'))

print("="*70)
print("🤖 SLED Commander Bot - Simple Test")
print("="*70)
print(f"Token: {SLED_TOKEN[:20]}...{SLED_TOKEN[-5:]}")
print(f"User ID: {USER_ID}")
print("\n🚀 Starting bot... (Keep this terminal open)")
print("\n📱 In Telegram:")
print("   1. Open @FortiSledBot")
print("   2. Send: /start")
print("   3. Send: /status")
print("   4. Send: Hello")
print("\n🛑 Press Ctrl+C when done\n")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    if update.effective_user.id != USER_ID:
        await update.message.reply_text("⛔ Unauthorized")
        return

    await update.message.reply_text(
        "👋 **SLED Commander Online!**\n\n"
        "I'm working! Try these commands:\n"
        "• /status - Check my status\n"
        "• /help - See all commands\n"
        "• Just say 'Hello' or 'Show my pipeline'\n\n"
        "✅ Bot is responding!"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    if update.effective_user.id != USER_ID:
        await update.message.reply_text("⛔ Unauthorized")
        return

    await update.message.reply_text(
        "✅ **SLED Commander Status**\n\n"
        "• Bot: Online ✅\n"
        "• Commands: Working ✅\n"
        f"• Your ID: {USER_ID} ✅\n"
        "• Authorized: Yes ✅\n\n"
        "All systems operational!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    if update.effective_user.id != USER_ID:
        await update.message.reply_text("⛔ Unauthorized")
        return

    await update.message.reply_text(
        "🤖 **SLED Commander Commands**\n\n"
        "**Built-in:**\n"
        "• /start - Start the bot\n"
        "• /status - Check bot status\n"
        "• /help - This message\n\n"
        "**Natural Language:**\n"
        "• 'Hello' - Greeting\n"
        "• 'Show my pipeline' - Salesforce deals\n"
        "• 'Help' - Get assistance\n\n"
        "💡 You can just talk to me normally!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages"""
    if update.effective_user.id != USER_ID:
        await update.message.reply_text("⛔ Unauthorized")
        return

    text = update.message.text.lower()

    if "hello" in text or "hi" in text:
        await update.message.reply_text(
            "👋 Hello! I'm SLED Commander and I'm working!\n\n"
            "Try:\n"
            "• /status\n"
            "• 'Show my pipeline'\n"
            "• 'Help'"
        )
    elif "pipeline" in text:
        await update.message.reply_text(
            "📊 **Your Salesforce Pipeline:**\n\n"
            "1. Hastings College - $111K\n"
            "   Closes: Feb 6, 2026\n"
            "   Stage: Negotiation\n\n"
            "2. City of Huron - $24K\n"
            "   Closes: Jan 30, 2026\n"
            "   Stage: Proposal\n\n"
            "3. Winnebago Tribe - $700K\n"
            "   Stage: Qualification\n\n"
            "**Total:** $835K across 3 deals"
        )
    elif "help" in text:
        await help_command(update, context)
    else:
        await update.message.reply_text(
            f"🤔 You said: \"{update.message.text}\"\n\n"
            "I heard you! Try:\n"
            "• /status\n"
            "• Hello\n"
            "• Show my pipeline"
        )


def main():
    """Run the bot"""
    # Create application
    app = Application.builder().token(SLED_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start bot
    print("✅ Bot is now LIVE!")
    print("Waiting for messages...\n")
    app.run_polling()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped!")
