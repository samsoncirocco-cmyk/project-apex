#!/usr/bin/env python3
"""
Test All 3 Telegram Bots - Verify all bots are working

Tests:
1. SLED Commander (@FortiSledBot)
2. TatT Architect (@TatTandDevBot)
3. Security Warden (@secwardenbot)

Usage:
    python3 test_all_bots.py
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


def check_environment():
    """Verify all credentials are set"""
    errors = []

    if not SLED_TOKEN:
        errors.append("❌ TELEGRAM_BOT_TOKEN_SLED not set")
    if not TATT_TOKEN:
        errors.append("❌ TELEGRAM_BOT_TOKEN_TATT not set")
    if not WARDEN_TOKEN:
        errors.append("❌ TELEGRAM_BOT_TOKEN_WARDEN not set")
    if not USER_ID:
        errors.append("❌ TELEGRAM_USER_ID not set")
    else:
        try:
            int(USER_ID)
        except ValueError:
            errors.append("❌ TELEGRAM_USER_ID must be a number")

    if errors:
        print("\n🚨 Environment Check Failed:\n")
        for error in errors:
            print(f"  {error}")
        print("\n📝 Make sure you edited /Users/ciroccofam/project-apex/.env")
        return False

    print("✅ Environment check passed!")
    print(f"  • SLED Commander: {SLED_TOKEN[:20]}...{SLED_TOKEN[-5:]}")
    print(f"  • TatT Architect: {TATT_TOKEN[:20]}...{TATT_TOKEN[-5:]}")
    print(f"  • Security Warden: {WARDEN_TOKEN[:20]}...{WARDEN_TOKEN[-5:]}")
    print(f"  • User ID: {USER_ID}")
    print()
    return True


async def test_sled_bot():
    """Test SLED Commander bot"""
    print("\n" + "="*70)
    print("🤖 Bot #1: SLED Commander")
    print("="*70)

    gateway = TelegramGateway(
        bot_token=SLED_TOKEN,
        allowed_user_ids=[int(USER_ID)],
        bot_name="SLED Commander"
    )

    # Simple test - just send a startup message
    gateway.build_application()

    print("✅ SLED Commander configured")
    print("   Username: @FortiSledBot")
    print("   URL: https://t.me/FortiSledBot")
    print("\n📱 In Telegram:")
    print("   1. Search for: @FortiSledBot")
    print("   2. Send: /start")
    print("   3. Try: 'Show my pipeline'")


async def test_tatt_bot():
    """Test TatT Architect bot"""
    print("\n" + "="*70)
    print("🤖 Bot #2: TatT Architect")
    print("="*70)

    gateway = TelegramGateway(
        bot_token=TATT_TOKEN,
        allowed_user_ids=[int(USER_ID)],
        bot_name="TatT Architect"
    )

    gateway.build_application()

    print("✅ TatT Architect configured")
    print("   Username: @TatTandDevBot")
    print("   URL: https://t.me/TatTandDevBot")
    print("\n📱 In Telegram:")
    print("   1. Search for: @TatTandDevBot")
    print("   2. Send: /start")
    print("   3. Try: 'Check deployments'")


async def test_warden_bot():
    """Test Security Warden bot"""
    print("\n" + "="*70)
    print("🤖 Bot #3: Security Warden")
    print("="*70)

    gateway = TelegramGateway(
        bot_token=WARDEN_TOKEN,
        allowed_user_ids=[int(USER_ID)],
        bot_name="Security Warden"
    )

    gateway.build_application()

    print("✅ Security Warden configured")
    print("   Username: @secwardenbot")
    print("   URL: https://t.me/secwardenbot")
    print("\n📱 In Telegram:")
    print("   1. Search for: @secwardenbot")
    print("   2. Send: /start")
    print("   3. Try: 'System status'")


async def send_test_messages():
    """Send test message to all 3 bots"""
    print("\n" + "="*70)
    print("📤 Sending Test Messages to All Bots")
    print("="*70)

    # Create gateways
    sled = TelegramGateway(SLED_TOKEN, [int(USER_ID)], "SLED Commander")
    tatt = TelegramGateway(TATT_TOKEN, [int(USER_ID)], "TatT Architect")
    warden = TelegramGateway(WARDEN_TOKEN, [int(USER_ID)], "Security Warden")

    # Build applications
    sled.build_application()
    tatt.build_application()
    warden.build_application()

    # Send test messages
    try:
        await sled.send_message(
            int(USER_ID),
            "🟢 **SLED Commander Online**\n\n"
            "I'm ready to help with Salesforce and Notion!\n\n"
            "Try:\n"
            "• /status - Check my status\n"
            "• /help - See all commands\n"
            "• 'Show my pipeline' - Natural language works too!"
        )
        print("✅ Sent message to SLED Commander")
    except Exception as e:
        print(f"❌ Failed to send to SLED Commander: {e}")

    try:
        await tatt.send_message(
            int(USER_ID),
            "🟢 **TatT Architect Online**\n\n"
            "I'm ready to monitor your deployments!\n\n"
            "Try:\n"
            "• /status - Check my status\n"
            "• /help - See all commands"
        )
        print("✅ Sent message to TatT Architect")
    except Exception as e:
        print(f"❌ Failed to send to TatT Architect: {e}")

    try:
        await warden.send_message(
            int(USER_ID),
            "🟢 **Security Warden Online**\n\n"
            "I'm watching over your systems!\n\n"
            "Try:\n"
            "• /status - Check my status\n"
            "• /help - See all commands"
        )
        print("✅ Sent message to Security Warden")
    except Exception as e:
        print(f"❌ Failed to send to Security Warden: {e}")

    print("\n🎉 Test messages sent! Check your Telegram!")


def main():
    """Main entry point"""
    print("=" * 70)
    print("🤖 PROJECT APEX - TEST ALL 3 BOTS")
    print("=" * 70)
    print()

    # Check environment
    if not check_environment():
        sys.exit(1)

    # Test all bots
    try:
        asyncio.run(test_sled_bot())
        asyncio.run(test_tatt_bot())
        asyncio.run(test_warden_bot())

        print("\n" + "="*70)
        print("🚀 SENDING TEST MESSAGES")
        print("="*70)
        asyncio.run(send_test_messages())

        print("\n" + "="*70)
        print("✅ ALL BOTS CONFIGURED SUCCESSFULLY!")
        print("="*70)
        print("\n📱 Next Steps:")
        print("   1. Open Telegram on your phone")
        print("   2. Check for messages from all 3 bots")
        print("   3. Reply to each bot with: /start")
        print("   4. Test commands and natural language")
        print("\n🎉 Your bots are alive!\n")

    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
