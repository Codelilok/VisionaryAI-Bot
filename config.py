import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Telegram Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("REPL_SLUG", "https://visionary-ai-bot.repl.co")  # Default to Replit URL

# API Keys
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

# API Endpoints
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
NEWSAPI_URL = "https://newsapi.org/v2/"

# Model IDs
TEXT_MODEL = "facebook/opt-1.3b"
IMAGE_MODEL = "stabilityai/stable-diffusion-2-1"
CODE_MODEL = "bigcode/starcoder"

# Rate Limits (requests per minute)
RATE_LIMIT = {
    "text": 30,
    "image": 10,
    "news": 100,
    "code": 20
}

# Queue Settings
MAX_QUEUE_SIZE = 100
QUEUE_TIMEOUT = 300  # seconds