import os
from flask import Flask, request, jsonify

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
    port = int(os.environ.get("PORT", 5000))  # Use dynamic port from Render
    app.run(host="0.0.0.0", port=port)