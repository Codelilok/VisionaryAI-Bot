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

        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"]["text"]

            # Send a reply back to the user
            reply_text = f"You said: {text}"
            payload = {"chat_id": chat_id, "text": reply_text}
            requests.post(TELEGRAM_API_URL, json=payload)

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

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Ensure correct port for Render
    app.run(host="0.0.0.0", port=port)