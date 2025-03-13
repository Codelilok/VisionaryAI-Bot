"""
Bot initialization module.
Provides the core bot instance and startup functionality.
"""
from telegram.ext import ApplicationBuilder
from config import TELEGRAM_TOKEN, logger

# Initialize the bot application
bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Start the bot using Webhook (No Polling)
async def start_bot():
    """Start the bot with Webhook"""
    try:
        # Import handlers here to avoid circular imports
        from bot.handlers import setup_handlers
        setup_handlers()

        logger.info("Starting bot...")

        await bot.initialize()  # Initialize first
        await bot.start()  # Then start the bot

        logger.info("Bot started successfully")

    except Exception as e:
        logger.error(f"Error during bot startup: {str(e)}")
        raise