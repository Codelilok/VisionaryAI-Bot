from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from bot.services.ai_service import generate_text_response
from bot.services.image_service import generate_image
from bot.services.news_service import get_news
from bot.services.code_service import get_code_assistance
from bot.queue_manager import QueueManager
from config import logger

queue_manager = QueueManager()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle direct messages without command"""
    logger.info(f"Received message from user {update.effective_user.id}")

    # Ignore commands
    if update.message.text.startswith('/'):
        return

    try:
        response = await queue_manager.enqueue('text', generate_text_response, update.message.text)
        await update.message.reply_text(response)
        logger.info(f"Successfully sent response to user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error in message handler for user {update.effective_user.id}: {str(e)}")
        await update.message.reply_text("Sorry, I encountered an error while processing your request.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome new users and show available commands"""
    logger.info(f"Received /start command from user {update.effective_user.id}")
    user_name = update.effective_user.first_name
    welcome_message = (
        f"👋 Welcome {user_name} to VisionaryAI Bot!\n\n"
        "I'm here to help you with:\n"
        "💬 Just send me any message to chat\n"
        "🎨 /image [prompt] - Generate an image\n"
        "📰 /news [topic] - Get latest news\n"
        "💻 /code [query] - Get coding help\n"
        "❓ /help - Show this help message\n\n"
        "Try saying Hello!"
    )
    await update.message.reply_text(welcome_message)
    logger.info(f"Sent welcome message to user {update.effective_user.id}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /help command from user {update.effective_user.id}")
    await start(update, context)

async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /chat command from user {update.effective_user.id}")
    if not context.args:
        await update.message.reply_text("Please provide a message to chat about! Example: /chat How are you?")
        return

    message = ' '.join(context.args)
    await update.message.reply_text("Thinking... 🤔")

    try:
        response = await queue_manager.enqueue('text', generate_text_response, message)
        await update.message.reply_text(response)
        logger.info(f"Successfully sent chat response to user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error in chat command for user {update.effective_user.id}: {str(e)}")
        await update.message.reply_text("Sorry, I encountered an error while processing your request.")

async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /image command from user {update.effective_user.id}")
    if not context.args:
        await update.message.reply_text("Please provide a prompt for image generation! Example: /image sunset over mountains")
        return

    prompt = ' '.join(context.args)
    await update.message.reply_text("Generating image... 🎨")

    try:
        image_bytes = await queue_manager.enqueue('image', generate_image, prompt)
        await update.message.reply_photo(photo=image_bytes)
        logger.info(f"Successfully sent generated image to user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error in image command for user {update.effective_user.id}: {str(e)}")
        await update.message.reply_text("Sorry, I couldn't generate the image.")

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /news command from user {update.effective_user.id}")
    topic = ' '.join(context.args) if context.args else 'technology'
    await update.message.reply_text("Fetching news... 📰")

    try:
        news = await queue_manager.enqueue('news', get_news, topic)
        await update.message.reply_text(news, parse_mode='HTML')
        logger.info(f"Successfully sent news about {topic} to user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error in news command for user {update.effective_user.id}: {str(e)}")
        await update.message.reply_text("Sorry, I couldn't fetch the news.")

async def code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /code command from user {update.effective_user.id}")
    if not context.args:
        await update.message.reply_text("Please provide a coding question! Example: /code How to sort a list in Python?")
        return

    query = ' '.join(context.args)
    await update.message.reply_text("Analyzing your code question... 💻")

    try:
        response = await queue_manager.enqueue('code', get_code_assistance, query)
        await update.message.reply_text(response, parse_mode='HTML')
        logger.info(f"Successfully sent code assistance to user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error in code command for user {update.effective_user.id}: {str(e)}")
        await update.message.reply_text("Sorry, I couldn't process your code question.")

def setup_handlers():
    """Set up all command handlers for the bot"""
    from bot import bot
    logger.info("Setting up command handlers...")

    # Add message handler for direct messages
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add command handlers
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("help", help_command))
    bot.add_handler(CommandHandler("chat", chat_command))
    bot.add_handler(CommandHandler("image", image_command))
    bot.add_handler(CommandHandler("news", news_command))
    bot.add_handler(CommandHandler("code", code_command))

    logger.info("Command handlers setup completed")