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
    webhook_url = f"{WEBHOOK_URL}/webhook/{TELEGRAM_TOKEN}"
    await bot.bot.set_webhook(url=webhook_url)
    logger.info(f"Webhook set to {webhook_url}")

# Start the bot
async def start_bot():
    # Import handlers here to avoid circular imports
    from bot.handlers import setup_handlers
    setup_handlers()

    await setup_webhook()
    await bot.initialize()
    await bot.start()
    logger.info("Bot started successfully")