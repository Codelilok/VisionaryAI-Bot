import os
import requests
from flask import Flask, request, jsonify

TOKEN = "YOUR_BOT_TOKEN"  # Replace with your actual bot token
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "VisionaryAI web interface is running"}), 200

@app.route('/', methods=['GET', 'POST'])
def webhook():
    """Webhook for Telegram bot"""
    if request.method == "POST":
        update = request.json  # Get the update from Telegram
        print(update)  # Log for debugging

        if "message" in update and "text" in update["message"]:
            chat_id = update["message"]["chat"]["id"]
            user_message = update["message"]["text"]

            # Prepare the response
            response_text = f"Hello, you said: {user_message}"

            # Send reply to Telegram
            send_message(chat_id, response_text)

        return jsonify({"status": "received"}), 200
    
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

def send_message(chat_id, text):
    """Send message to Telegram chat"""
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(TELEGRAM_API_URL, json=payload)
    print(response.json())  # Log response for debugging

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)