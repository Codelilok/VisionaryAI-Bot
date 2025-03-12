from flask import Flask, jsonify
import asyncio
import threading
from bot import start_bot
from config import logger

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "VisionaryAI bot is running"}), 200

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