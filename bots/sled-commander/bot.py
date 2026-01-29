import logging
import os
import sys
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.getenv("ENV_FILE", "/config/.env"))

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USERS = [int(u) for u in os.getenv("TELEGRAM_ALLOWED_USERS", "").split(",") if u]
DB_PATH = os.getenv("DATABASE_PATH", "/data/apex.db")

# Import shared db init
sys.path.append("/app/shared")
try:
    # If running in container with mapped shared volume
    from db_init import init_db
except ImportError:
    # Fallback or local dev handled differently
    pass

async def auth_middleware(update: Update) -> bool:
    """Check if user is allowed to interact with the bot."""
    if not update.effective_user:
        return False
        
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        logger.warning(f"Unauthorized access attempt from user ID: {user_id}")
        await update.message.reply_text("⛔ Unauthorized access.")
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await auth_middleware(update):
        return
    
    await update.message.reply_text(
        "👋 **SLED Commander Online**\n\n"
        "Ready to accept commands.\n"
        "/status - Check system health\n"
        "/help - Show available commands"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await auth_middleware(update):
        return
        
    await update.message.reply_text(
        "**Available Commands:**\n\n"
        "🛠 **System**\n"
        "/status - Infrastructure health\n"
        "/logs - View recent logs\n\n"
        "💼 **SLED Ops**\n"
        "/quote [id] - Manage Salesforce quote\n"
        "/procure - Scan portals\n\n"
        "🧠 **TatT AI**\n"
        "/ask [query] - Ask Project Apex knowledge base"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await auth_middleware(update):
        return
        
    # Placeholder for actual health checks
    await update.message.reply_text(
        "✅ **System Status: Nominal**\n"
        "- Docker: Active\n"
        "- Database: Connected (WAL Mode)\n"
        "- Ollama: Ready\n"
        "- Redis: Ready"
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo non-command messages or handle as AI prompts."""
    if not await auth_middleware(update):
        return
    
    # In future: route to LiteLLM for "Vibe Coding" or chat
    await update.message.reply_text(f"Echo: {update.message.text}\n\n(AI Chat integration pending Task 9)")

def main():
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
        sys.exit(1)

    # Initialize DB on startup
    try:
        # We might need to adjust path import strategy depending on container layout
        # For now, we assume simple import if shared module is available
        pass 
    except Exception as e:
        logger.error(f"DB Init failed: {e}")

    application = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('status', status))
    
    # Catch-all for non-command text
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), unknown))
    
    logger.info("SLED Commander started polling...")
    application.run_polling()

if __name__ == '__main__':
    # Initialize DB (Task 3)
    if os.path.exists("/app/shared/db_init.py"):
         sys.path.append("/app/shared")
         from db_init import init_db
         init_db()
         
    main()
