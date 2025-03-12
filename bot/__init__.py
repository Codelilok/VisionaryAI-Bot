"""
Bot initialization module.
Provides the core bot instance and startup functionality.
"""
from telegram.ext import Application
from config import TELEGRAM_TOKEN, logger

# Initialize the bot application
bot = Application.builder().token(TELEGRAM_TOKEN).build()

# Start the bot
async def start_bot():
    try:
        # Import handlers here to avoid circular imports
        from bot.handlers import setup_handlers
        setup_handlers()

        # Initialize bot first
        logger.info("Initializing bot...")
        await bot.initialize()

        # Start polling
        logger.info("Starting bot polling...")
        await bot.start()
        await bot.updater.start_polling()
        logger.info("Bot started successfully with polling")
    except Exception as e:
        logger.error(f"Error during bot startup: {str(e)}")
        raise