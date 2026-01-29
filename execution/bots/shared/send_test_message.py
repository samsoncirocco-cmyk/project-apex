#!/usr/bin/env python3
"""
Send a direct test message to verify bot can reach you

This bypasses the polling system and directly sends a message.
"""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from telegram import Bot

# Load environment
env_path = Path(__file__).parents[3] / '.env'
load_dotenv(env_path)

SLED_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_SLED')
TATT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_TATT')
WARDEN_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_WARDEN')
USER_ID = int(os.getenv('TELEGRAM_USER_ID'))


async def send_messages():
    """Send test messages from all 3 bots"""

    print("="*70)
    print("📤 Sending Test Messages from All 3 Bots")
    print("="*70)
    print(f"To User ID: {USER_ID}")
    print()

    # Bot 1: SLED Commander
    try:
        bot1 = Bot(token=SLED_TOKEN)
        await bot1.send_message(
            chat_id=USER_ID,
            text=(
                "🟢 **SLED Commander is LIVE!**\n\n"
                "I can see you! Reply to this message with:\n"
                "• /start\n"
                "• /status\n"
                "• Hello\n"
                "• Show my pipeline\n\n"
                "I'll respond to everything you send!"
            ),
            parse_mode='Markdown'
        )
        print("✅ SLED Commander (@FortiSledBot) - Message sent!")
    except Exception as e:
        print(f"❌ SLED Commander failed: {e}")

    # Bot 2: TatT Architect
    try:
        bot2 = Bot(token=TATT_TOKEN)
        await bot2.send_message(
            chat_id=USER_ID,
            text=(
                "🟢 **TatT Architect is LIVE!**\n\n"
                "I'm monitoring your deployments!\n"
                "Send me a message to test:\n"
                "• /start\n"
                "• /status\n"
                "• Hello"
            ),
            parse_mode='Markdown'
        )
        print("✅ TatT Architect (@TatTandDevBot) - Message sent!")
    except Exception as e:
        print(f"❌ TatT Architect failed: {e}")

    # Bot 3: Security Warden
    try:
        bot3 = Bot(token=WARDEN_TOKEN)
        await bot3.send_message(
            chat_id=USER_ID,
            text=(
                "🟢 **Security Warden is LIVE!**\n\n"
                "Watching your systems 24/7!\n"
                "Send me a message to test:\n"
                "• /start\n"
                "• /status\n"
                "• Hello"
            ),
            parse_mode='Markdown'
        )
        print("✅ Security Warden (@secwardenbot) - Message sent!")
    except Exception as e:
        print(f"❌ Security Warden failed: {e}")

    print()
    print("="*70)
    print("✅ All messages sent!")
    print("="*70)
    print("\n📱 Check your Telegram now!")
    print("You should have messages from all 3 bots.\n")


if __name__ == "__main__":
    asyncio.run(send_messages())
