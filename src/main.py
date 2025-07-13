import logging
import os

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from .bot.handlers import (handle_message, help_command, record_command,
                              toggle_announcements_command, seed_command,
                              leaderboard_command, history_command)
from .services.config_service import ConfigService
from .services.inactivity_service import InactivityService
from .storage.json_storage import JsonStorage

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    # Load environment variables from .env file
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
        return

    # --- Dependency Injection ---
    # 1. Create Storage instance
    storage = JsonStorage(db_path="db.json")

    # 2. Create Service instances and inject dependencies
    inactivity_service = InactivityService(storage=storage)
    config_service = ConfigService(storage=storage)

    # 3. Create the Application and pass it the bot's token.
    application = Application.builder().token(token).build()

    # 4. Store service instances in bot_data for access in handlers
    application.bot_data["inactivity_service"] = inactivity_service
    application.bot_data["config_service"] = config_service

    # --- Register Handlers ---
    application.add_handler(CommandHandler("start", help_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("record", record_command))
    application.add_handler(CommandHandler("toggle_announcements", toggle_announcements_command))
    application.add_handler(CommandHandler("seed", seed_command))
    application.add_handler(CommandHandler("leaderboard", leaderboard_command))
    application.add_handler(CommandHandler("history", history_command))

    # Handle all messages from users to check for inactivity
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()