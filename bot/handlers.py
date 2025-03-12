from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from bot import bot
from bot.services.ai_service import generate_text_response
from bot.services.image_service import generate_image
from bot.services.news_service import get_news
from bot.services.code_service import get_code_assistance
from bot.queue_manager import QueueManager
from config import logger

queue_manager = QueueManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "👋 Welcome to VisionaryAI Bot!\n\n"
        "Available commands:\n"
        "/chat [message] - Have a conversation\n"
        "/image [prompt] - Generate an image\n"
        "/news [topic] - Get latest news\n"
        "/code [query] - Get coding help\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a message to chat about!")
        return

    message = ' '.join(context.args)
    await update.message.reply_text("Thinking... 🤔")
    
    try:
        response = await queue_manager.enqueue('text', generate_text_response, message)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error in chat command: {str(e)}")
        await update.message.reply_text("Sorry, I encountered an error while processing your request.")

async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a prompt for image generation!")
        return

    prompt = ' '.join(context.args)
    await update.message.reply_text("Generating image... 🎨")
    
    try:
        image_url = await queue_manager.enqueue('image', generate_image, prompt)
        await update.message.reply_photo(image_url)
    except Exception as e:
        logger.error(f"Error in image command: {str(e)}")
        await update.message.reply_text("Sorry, I couldn't generate the image.")

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = ' '.join(context.args) if context.args else 'technology'
    await update.message.reply_text("Fetching news... 📰")
    
    try:
        news = await queue_manager.enqueue('news', get_news, topic)
        await update.message.reply_text(news, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Error in news command: {str(e)}")
        await update.message.reply_text("Sorry, I couldn't fetch the news.")

async def code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a coding question!")
        return

    query = ' '.join(context.args)
    await update.message.reply_text("Analyzing your code question... 💻")
    
    try:
        response = await queue_manager.enqueue('code', get_code_assistance, query)
        await update.message.reply_text(response, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Error in code command: {str(e)}")
        await update.message.reply_text("Sorry, I couldn't process your code question.")

def setup_handlers():
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("help", help_command))
    bot.add_handler(CommandHandler("chat", chat_command))
    bot.add_handler(CommandHandler("image", image_command))
    bot.add_handler(CommandHandler("news", news_command))
    bot.add_handler(CommandHandler("code", code_command))

setup_handlers()

def handle_telegram_update(update):
    bot.process_update(Update.de_json(update, bot.bot))
