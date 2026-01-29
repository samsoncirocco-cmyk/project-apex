#!/usr/bin/env python3
"""
Test Telegram Gateway - Verify bot connection and authentication

This script tests:
1. Bot token validity
2. User ID whitelist authentication
3. Basic command handling
4. Inline keyboard (approval buttons)
5. Message formatting

Usage:
    python3 test_telegram.py

Before running:
    1. Set TELEGRAM_BOT_TOKEN in .env
    2. Set TELEGRAM_USER_ID in .env
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path so we can import telegram_gateway
sys.path.insert(0, str(Path(__file__).parent))

from telegram_gateway import TelegramGateway, format_success, format_error

# Load environment variables
env_path = Path(__file__).parents[3] / '.env'
load_dotenv(env_path)

# Get credentials from environment
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
USER_ID = os.getenv('TELEGRAM_USER_ID')


def check_environment():
    """Verify environment variables are set"""
    errors = []

    if not BOT_TOKEN:
        errors.append("❌ TELEGRAM_BOT_TOKEN not set in .env")
    elif not BOT_TOKEN.startswith('bot'):
        # Telegram bot tokens typically start with a number followed by ':'
        # But let's just warn if it looks suspicious
        if ':' not in BOT_TOKEN:
            errors.append("⚠️ TELEGRAM_BOT_TOKEN doesn't look valid (missing ':')")

    if not USER_ID:
        errors.append("❌ TELEGRAM_USER_ID not set in .env")
    else:
        try:
            int(USER_ID)
        except ValueError:
            errors.append("❌ TELEGRAM_USER_ID must be a number")

    if errors:
        print("\n🚨 Environment Check Failed:\n")
        for error in errors:
            print(f"  {error}")
        print("\n📝 To fix:")
        print("  1. Edit /Users/ciroccofam/project-apex/.env")
        print("  2. Add your Telegram credentials:")
        print("     TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz")
        print("     TELEGRAM_USER_ID=123456789")
        print("\n🔍 Get your credentials:")
        print("  • Bot token: Message @BotFather on Telegram")
        print("  • User ID: Message @userinfobot on Telegram")
        print()
        return False

    print("✅ Environment check passed!")
    print(f"  • Bot token: {BOT_TOKEN[:20]}...{BOT_TOKEN[-5:]}")
    print(f"  • User ID: {USER_ID}")
    print()
    return True


async def handle_test_command(update, context):
    """Test command handler"""
    await update.message.reply_text(
        format_success("Test command works! ✅")
    )


async def handle_echo_command(update, context):
    """Echo command - repeats your message"""
    text = ' '.join(context.args) if context.args else "Nothing to echo!"
    await update.message.reply_text(f"🔊 Echo: {text}")


async def handle_natural_language(message_text, update, context):
    """Test natural language processing"""
    text_lower = message_text.lower()

    if "hello" in text_lower or "hi" in text_lower:
        return "👋 Hello! I'm your test bot. Everything's working!"

    elif "pipeline" in text_lower:
        return "📊 Here's your pipeline:\n\n" \
               "1. Hastings College - $111K (Closes Feb 6)\n" \
               "2. City of Huron - $24K (Closes Jan 30)\n" \
               "3. Winnebago Tribe - $700K (In negotiation)\n\n" \
               "Total: $835K across 3 deals"

    elif "test" in text_lower:
        return "✅ Natural language processing works!"

    else:
        return f"🤔 You said: \"{message_text}\"\n\n" \
               f"Try saying:\n" \
               f"• Hello\n" \
               f"• Show my pipeline\n" \
               f"• Test"


async def handle_approve(query, context):
    """Handle approval button"""
    return format_success("You clicked APPROVE! ✅\n\nThis is where we'd process the approval.")


async def handle_reject(query, context):
    """Handle reject button"""
    return "❌ *Rejected*\n\nAction cancelled. No changes made."


async def test_bot():
    """Run the test bot"""
    print("🚀 Starting Telegram Gateway Test Bot...\n")

    # Initialize gateway
    gateway = TelegramGateway(
        bot_token=BOT_TOKEN,
        allowed_user_ids=[int(USER_ID)],
        bot_name="Project Apex Test Bot"
    )

    # Register test commands
    gateway.register_command("test", handle_test_command)
    gateway.register_command("echo", handle_echo_command)

    # Register natural language handler
    gateway.register_message_handler(handle_natural_language)

    # Register approval callbacks
    gateway.register_callback("test_approve", handle_approve)
    gateway.register_callback("test_reject", handle_reject)

    # Build application
    app = gateway.build_application()

    print("✅ Bot configured successfully!")
    print("\n📱 Test Instructions:")
    print("  1. Open Telegram")
    print("  2. Search for your bot")
    print("  3. Send: /start")
    print("  4. Try these commands:")
    print("     • /test - Test custom command")
    print("     • /echo Hello World - Echo a message")
    print("     • /status - Check bot status")
    print("     • /help - List all commands")
    print("  5. Try natural language:")
    print("     • Hello")
    print("     • Show my pipeline")
    print("  6. Test approval buttons:")
    print("     • Send: /test_approval")
    print("\n⚠️ Important:")
    print("  • Only YOU can control this bot (user ID whitelist)")
    print("  • Bot will ignore messages from other users")
    print("\n🛑 Press Ctrl+C to stop the bot\n")

    # Add custom command to test approval buttons
    async def test_approval(update, context):
        """Send test approval request"""
        await gateway.send_approval_request(
            user_id=update.effective_user.id,
            message="📝 *Test Approval Request*\n\n"
                   "This is a test of the approval button system.\n\n"
                   "Click a button below:",
            approve_callback="test_approve",
            reject_callback="test_reject"
        )

    gateway.register_command("test_approval", test_approval)

    # Start bot
    try:
        await gateway.start()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping bot...")
        await gateway.stop()
        print("✅ Bot stopped successfully!")


def main():
    """Main entry point"""
    print("=" * 70)
    print("🤖 PROJECT APEX - TELEGRAM GATEWAY TEST")
    print("=" * 70)
    print()

    # Check environment
    if not check_environment():
        sys.exit(1)

    # Run bot
    try:
        asyncio.run(test_bot())
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
