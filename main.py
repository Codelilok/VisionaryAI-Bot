
from flask import Flask, jsonify
from config import logger
import threading

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "VisionaryAI web interface is running"}), 200

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

def start_bot_thread():
    """Start the bot in a separate thread with its own event loop"""
    import asyncio
    from bot import start_bot
    
    # Create new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Run the bot until complete
    loop.run_until_complete(start_bot())
    loop.run_forever()

if __name__ == "__main__":
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=start_bot_thread, daemon=True)
    bot_thread.start()
    logger.info("Started Telegram bot in separate thread")
    
    # Start the Flask app
    app.run(host="0.0.0.0", port=5000)
