"""
Bot initialization module.
Provides the core bot instance and startup functionality.
"""
from telegram.ext import Application
from config import TELEGRAM_TOKEN, WEBHOOK_URL, logger

# Initialize the bot application
bot = Application.builder().token(TELEGRAM_TOKEN).build()

# Configure webhook
async def setup_webhook():
    try:
        webhook_url = f"{WEBHOOK_URL}/webhook/{TELEGRAM_TOKEN}"
        logger.info(f"Setting webhook to URL: {webhook_url}")
        result = await bot.bot.set_webhook(url=webhook_url)
        if result:
            logger.info("Webhook set successfully")
        else:
            logger.error("Failed to set webhook")
    except Exception as e:
        logger.error(f"Error setting webhook: {str(e)}")
        raise

# Start the bot
async def start_bot():
    try:
        # Import handlers here to avoid circular imports
        from bot.handlers import setup_handlers
        setup_handlers()

        # Initialize bot first
        logger.info("Initializing bot...")
        await bot.initialize()

        # Set up webhook after initialization
        await setup_webhook()

        # Start the bot
        await bot.start()
        logger.info("Bot started successfully")
    except Exception as e:
        logger.error(f"Error during bot startup: {str(e)}")
        raise