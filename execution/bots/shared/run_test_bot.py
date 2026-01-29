#!/usr/bin/env python3
"""
Run a Test Bot - Actually listen and respond to messages

This script runs ONE bot at a time so you can test it.

Usage:
    python3 run_test_bot.py sled    # Run SLED Commander
    python3 run_test_bot.py tatt    # Run TatT Architect
    python3 run_test_bot.py warden  # Run Security Warden
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from telegram_gateway import TelegramGateway

# Load environment variables
env_path = Path(__file__).parents[3] / '.env'
load_dotenv(env_path)

# Get credentials
SLED_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_SLED')
TATT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_TATT')
WARDEN_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_WARDEN')
USER_ID = os.getenv('TELEGRAM_USER_ID')


async def handle_message(message_text, update, context):
    """Handle natural language messages"""
    text_lower = message_text.lower()

    if "hello" in text_lower or "hi" in text_lower:
        return "👋 Hello! I'm working! Try these:\n• /status\n• /help\n• 'What can you do?'"

    elif "pipeline" in text_lower:
        return "📊 **Your Pipeline:**\n\n" \
               "1. Hastings College - $111K (Closes Feb 6)\n" \
               "2. City of Huron - $24K (Closes Jan 30)\n" \
               "3. Winnebago Tribe - $700K (In negotiation)\n\n" \
               "Total: $835K across 3 deals"

    elif "status" in text_lower or "working" in text_lower:
        return "✅ I'm online and working!\n\n" \
               "• Bot: Running\n" \
               "• Commands: Active\n" \
               "• Your ID: Authorized"

    elif "help" in text_lower or "what can you do" in text_lower:
        return "🤖 **I can help with:**\n\n" \
               "• Check your Salesforce pipeline\n" \
               "• Monitor deployments\n" \
               "• Security alerts\n\n" \
               "Try saying:\n" \
               "• Show my pipeline\n" \
               "• System status\n" \
               "• Hello"

    else:
        return f"🤔 You said: \"{message_text}\"\n\n" \
               f"Try:\n• Hello\n• Show my pipeline\n• Help"


async def run_bot(bot_name, bot_token, bot_username):
    """Run a single bot"""
    print("=" * 70)
    print(f"🤖 Starting {bot_name}")
    print("=" * 70)
    print(f"Username: @{bot_username}")
    print(f"Your User ID: {USER_ID}")
    print("\n🚀 Bot is now LIVE and listening...")
    print("\n📱 In Telegram:")
    print(f"   1. Open chat with @{bot_username}")
    print("   2. Send: /start")
    print("   3. Try: 'Hello', 'Show my pipeline', /status")
    print("\n🛑 Press Ctrl+C to stop\n")

    # Create gateway
    gateway = TelegramGateway(
        bot_token=bot_token,
        allowed_user_ids=[int(USER_ID)],
        bot_name=bot_name
    )

    # Register message handler
    gateway.register_message_handler(handle_message)

    # Start bot (this runs forever)
    try:
        await gateway.start()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping bot...")
        await gateway.stop()
        print("✅ Bot stopped")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 run_test_bot.py [sled|tatt|warden]")
        print("\nExamples:")
        print("  python3 run_test_bot.py sled    # Run SLED Commander")
        print("  python3 run_test_bot.py tatt    # Run TatT Architect")
        print("  python3 run_test_bot.py warden  # Run Security Warden")
        sys.exit(1)

    bot_choice = sys.argv[1].lower()

    if bot_choice == "sled":
        bot_name = "SLED Commander"
        bot_token = SLED_TOKEN
        bot_username = "FortiSledBot"
    elif bot_choice == "tatt":
        bot_name = "TatT Architect"
        bot_token = TATT_TOKEN
        bot_username = "TatTandDevBot"
    elif bot_choice == "warden":
        bot_name = "Security Warden"
        bot_token = WARDEN_TOKEN
        bot_username = "secwardenbot"
    else:
        print(f"❌ Unknown bot: {bot_choice}")
        print("Choose: sled, tatt, or warden")
        sys.exit(1)

    if not bot_token:
        print(f"❌ Bot token not found in .env")
        sys.exit(1)

    if not USER_ID:
        print(f"❌ User ID not found in .env")
        sys.exit(1)

    # Run the bot
    try:
        asyncio.run(run_bot(bot_name, bot_token, bot_username))
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
