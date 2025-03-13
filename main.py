import os
import logging
from flask import Flask, request, jsonify
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

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

@app.route("/webhook", methods=['POST'])  # Static path for webhook
def receive_update():
    """Handles Telegram webhook updates"""
    try:
        update = request.get_json()
        logging.info(f"Received update: {update}")

        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"]["text"]

            # Simple reply logic
            response_text = f"You said: {text}"
            send_message(chat_id, response_text)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        logging.error(f"Error handling update: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def send_message(chat_id, text):
    """Send a message to a Telegram user with debugging"""
    print(f"Sending message to {chat_id}: {text}")  # Debugging
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    
    try:
        response = requests.post(url, json=payload)
        response_data = response.json()
        print(f"Response: {response_data}")  # Print API response
        logging.info(f"Message sent to {chat_id}: {response_data}")
    except Exception as e:
        logging.error(f"Failed to send message: {e}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Get Render’s assigned port
    app.run(host="0.0.0.0", port=port)