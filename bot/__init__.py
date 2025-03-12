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

        logger.info("Starting bot with polling...")
        await bot.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"Error during bot startup: {str(e)}")
        raise