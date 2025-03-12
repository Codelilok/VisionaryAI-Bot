from flask import Flask, request, Response, jsonify
import logging
import asyncio
import threading
from bot import bot, start_bot
from bot.handlers import handle_telegram_update
from config import TELEGRAM_TOKEN, logger

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "VisionaryAI bot is running"}), 200

@app.route(f'/webhook/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    """Handle incoming updates from Telegram"""
    try:
        update = request.get_json()
        if not update:
            logger.error("Received empty update")
            return Response(status=400)

        logger.debug(f"Received update: {update}")
        handle_telegram_update(update)
        return Response(status=200)
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return Response(status=500)

@app.route('/')
def index():
    """Landing page"""
    return jsonify({
        "name": "VisionaryAI Bot",
        "status": "running",
        "features": [
            "Natural language conversations",
            "Image generation",
            "News updates",
            "Code assistance"
        ]
    })

# Initialize the bot without blocking Flask
def init_bot_async():
    try:
        asyncio.run(start_bot())
        logger.info("Bot initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize bot: {str(e)}")

# Start bot initialization in background thread
thread = threading.Thread(target=init_bot_async)
thread.daemon = True
thread.start()
logger.info("Bot initialization started in background thread")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)