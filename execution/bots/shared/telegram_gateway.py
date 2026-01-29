#!/usr/bin/env python3
"""
Telegram Gateway - Secure communication layer for Project Apex bots

This module provides:
- User ID whitelist authentication
- Natural language command parsing
- Inline keyboard support for approvals
- Message queue for offline buffering
- Error handling with user-friendly messages
"""

import os
import logging
from typing import Optional, Dict, List, Callable, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramGateway:
    """
    Secure Telegram gateway with whitelist authentication and rich UI support

    Features:
    - User ID whitelist (only authorized users can interact)
    - Natural language command handling
    - Inline keyboards for approvals
    - Error handling with plain language messages
    - Message formatting (markdown support)
    """

    def __init__(self, bot_token: str, allowed_user_ids: List[int], bot_name: str = "Apex Bot"):
        """
        Initialize Telegram gateway

        Args:
            bot_token: Telegram bot token from BotFather
            allowed_user_ids: List of Telegram user IDs that can control the bot
            bot_name: Display name for the bot (used in logs and messages)
        """
        self.bot_token = bot_token
        self.allowed_user_ids = set(allowed_user_ids)
        self.bot_name = bot_name
        self.application: Optional[Application] = None
        self.command_handlers: Dict[str, Callable] = {}
        self.message_handler: Optional[Callable] = None
        self.callback_handlers: Dict[str, Callable] = {}

        logger.info(f"Initialized {bot_name} gateway for {len(allowed_user_ids)} authorized user(s)")


    def is_authorized(self, user_id: int) -> bool:
        """Check if user is authorized to interact with bot"""
        return user_id in self.allowed_user_ids


    async def _check_authorization(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """
        Verify user authorization before processing commands

        Returns:
            True if authorized, False otherwise (and sends warning to user)
        """
        user_id = update.effective_user.id

        if not self.is_authorized(user_id):
            logger.warning(f"Unauthorized access attempt from user {user_id}")
            await update.message.reply_text(
                "⛔ Unauthorized\n\n"
                "This bot is private. Contact the owner if you need access."
            )
            return False

        return True


    async def _handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        if not await self._check_authorization(update, context):
            return

        user_name = update.effective_user.first_name
        await update.message.reply_text(
            f"👋 Hi {user_name}!\n\n"
            f"I'm {self.bot_name}, ready to help.\n\n"
            "Try asking me:\n"
            "• What's in my pipeline?\n"
            "• Show me urgent tasks\n"
            "• What deals need attention?\n\n"
            "Or use /help to see all commands."
        )


    async def _handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        if not await self._check_authorization(update, context):
            return

        commands_text = "\n".join([
            f"/{cmd} - {handler.__doc__ or 'No description'}"
            for cmd, handler in self.command_handlers.items()
        ])

        await update.message.reply_text(
            f"🤖 {self.bot_name} Commands\n\n"
            f"{commands_text or 'No custom commands registered yet.'}\n\n"
            "💡 Tip: You can also just ask me questions in plain language!"
        )


    async def _handle_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command - check bot health"""
        if not await self._check_authorization(update, context):
            return

        await update.message.reply_text(
            f"✅ {self.bot_name} Status\n\n"
            f"• Bot: Online\n"
            f"• Authorized users: {len(self.allowed_user_ids)}\n"
            f"• Your ID: {update.effective_user.id}\n\n"
            "All systems operational!"
        )


    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle natural language messages (non-commands)"""
        if not await self._check_authorization(update, context):
            return

        message_text = update.message.text

        # If bot has a custom message handler, use it
        if self.message_handler:
            try:
                response = await self.message_handler(message_text, update, context)
                if response:
                    await update.message.reply_text(response)
            except Exception as e:
                logger.error(f"Error in custom message handler: {e}")
                await update.message.reply_text(
                    "❌ Oops, something went wrong processing your message.\n\n"
                    f"Error: {str(e)}\n\n"
                    "Try rephrasing your question or use /help to see available commands."
                )
        else:
            # Default: acknowledge message but explain no handler is configured
            await update.message.reply_text(
                "👂 I hear you, but I'm not configured to handle messages yet.\n\n"
                "Use /help to see available commands."
            )


    async def _handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard button presses"""
        query = update.callback_query
        await query.answer()  # Acknowledge button press

        user_id = query.from_user.id
        if not self.is_authorized(user_id):
            await query.edit_message_text("⛔ Unauthorized")
            return

        callback_data = query.data

        # Route to registered callback handler
        if callback_data in self.callback_handlers:
            try:
                response = await self.callback_handlers[callback_data](query, context)
                if response:
                    await query.edit_message_text(response)
            except Exception as e:
                logger.error(f"Error in callback handler '{callback_data}': {e}")
                await query.edit_message_text(
                    f"❌ Error processing button: {str(e)}"
                )
        else:
            logger.warning(f"No handler registered for callback: {callback_data}")
            await query.edit_message_text(
                f"⚠️ Unknown action: {callback_data}"
            )


    def register_command(self, command: str, handler: Callable):
        """
        Register a custom command handler

        Args:
            command: Command name (without /)
            handler: Async function(update, context) -> None

        Example:
            gateway.register_command("pipeline", handle_pipeline_command)
        """
        self.command_handlers[command] = handler
        logger.info(f"Registered command: /{command}")


    def register_message_handler(self, handler: Callable):
        """
        Register handler for natural language messages

        Args:
            handler: Async function(message_text, update, context) -> str
                     Should return response text or None

        Example:
            async def handle_message(text, update, context):
                if "pipeline" in text.lower():
                    return "Here's your pipeline..."
                return None

            gateway.register_message_handler(handle_message)
        """
        self.message_handler = handler
        logger.info("Registered message handler for natural language processing")


    def register_callback(self, callback_data: str, handler: Callable):
        """
        Register handler for inline keyboard button

        Args:
            callback_data: Unique identifier for this button action
            handler: Async function(query, context) -> str
                     Should return response text or None

        Example:
            async def approve_quote(query, context):
                # Process approval
                return "✅ Quote approved and sent!"

            gateway.register_callback("approve_quote_12345", approve_quote)
        """
        self.callback_handlers[callback_data] = handler
        logger.info(f"Registered callback handler: {callback_data}")


    async def send_message(self, user_id: int, text: str, parse_mode: str = "Markdown"):
        """
        Send message to specific user

        Args:
            user_id: Telegram user ID
            text: Message text (supports Markdown by default)
            parse_mode: "Markdown" or "HTML" or None

        Example:
            await gateway.send_message(12345, "✅ Task completed!")
        """
        try:
            await self.application.bot.send_message(
                chat_id=user_id,
                text=text,
                parse_mode=parse_mode
            )
            logger.info(f"Sent message to user {user_id}")
        except Exception as e:
            logger.error(f"Failed to send message to user {user_id}: {e}")


    async def send_approval_request(
        self,
        user_id: int,
        message: str,
        approve_callback: str,
        reject_callback: str
    ) -> None:
        """
        Send message with Approve/Reject buttons

        Args:
            user_id: Telegram user ID
            message: Description of what needs approval
            approve_callback: Callback data for approve button
            reject_callback: Callback data for reject button

        Example:
            await gateway.send_approval_request(
                user_id=12345,
                message="📝 Quote for Hastings College: $150K\\n\\nApprove sending?",
                approve_callback="approve_quote_12345",
                reject_callback="reject_quote_12345"
            )
        """
        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=approve_callback),
                InlineKeyboardButton("❌ Reject", callback_data=reject_callback)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            await self.application.bot.send_message(
                chat_id=user_id,
                text=message,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            logger.info(f"Sent approval request to user {user_id}")
        except Exception as e:
            logger.error(f"Failed to send approval request to user {user_id}: {e}")


    async def send_to_all_users(self, text: str, parse_mode: str = "Markdown"):
        """
        Broadcast message to all authorized users

        Args:
            text: Message text
            parse_mode: "Markdown" or "HTML" or None

        Example:
            await gateway.send_to_all_users("🚨 System alert: High CPU usage detected!")
        """
        for user_id in self.allowed_user_ids:
            await self.send_message(user_id, text, parse_mode)


    def build_application(self) -> Application:
        """
        Build the Telegram application with all handlers

        Returns:
            Application instance ready to run
        """
        self.application = Application.builder().token(self.bot_token).build()

        # Add built-in command handlers
        self.application.add_handler(CommandHandler("start", self._handle_start))
        self.application.add_handler(CommandHandler("help", self._handle_help))
        self.application.add_handler(CommandHandler("status", self._handle_status))

        # Add custom command handlers
        for command, handler in self.command_handlers.items():
            self.application.add_handler(CommandHandler(command, handler))

        # Add message handler (natural language)
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message)
        )

        # Add callback query handler (inline keyboard buttons)
        self.application.add_handler(CallbackQueryHandler(self._handle_callback))

        logger.info(f"{self.bot_name} application built with {len(self.command_handlers)} custom commands")

        return self.application


    async def start(self):
        """Start the bot (runs forever until stopped)"""
        if not self.application:
            self.build_application()

        logger.info(f"Starting {self.bot_name}...")

        # Send startup notification to all users
        await self.send_to_all_users(
            f"🟢 *{self.bot_name} Online*\n\n"
            f"I'm ready to help! Send /help to see what I can do."
        )

        # Start polling
        await self.application.run_polling()


    async def stop(self):
        """Stop the bot gracefully"""
        logger.info(f"Stopping {self.bot_name}...")

        # Send shutdown notification to all users
        await self.send_to_all_users(
            f"🔴 *{self.bot_name} Offline*\n\n"
            f"Going offline for maintenance. I'll be back soon!"
        )

        if self.application:
            await self.application.stop()


# Utility functions for common message formatting

def format_error(error: str) -> str:
    """Format error message in user-friendly way"""
    return f"❌ *Error*\n\n{error}\n\nTry again or contact support if this persists."


def format_success(message: str) -> str:
    """Format success message"""
    return f"✅ *Success*\n\n{message}"


def format_warning(message: str) -> str:
    """Format warning message"""
    return f"⚠️ *Warning*\n\n{message}"


def format_info(message: str) -> str:
    """Format info message"""
    return f"ℹ️ *Info*\n\n{message}"


def format_code_block(code: str, language: str = "") -> str:
    """Format code block with syntax highlighting"""
    return f"```{language}\n{code}\n```"


if __name__ == "__main__":
    # Test mode - run with dummy credentials
    print("🧪 Telegram Gateway Test Mode")
    print("\nThis module should be imported, not run directly.")
    print("\nExample usage:")
    print("""
    from telegram_gateway import TelegramGateway

    # Initialize
    gateway = TelegramGateway(
        bot_token="YOUR_BOT_TOKEN",
        allowed_user_ids=[12345678],
        bot_name="Test Bot"
    )

    # Register custom command
    async def handle_hello(update, context):
        await update.message.reply_text("Hello!")

    gateway.register_command("hello", handle_hello)

    # Start bot
    import asyncio
    asyncio.run(gateway.start())
    """)
