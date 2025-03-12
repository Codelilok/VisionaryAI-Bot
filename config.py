import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Telegram Configuration
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# API Keys
HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")

# API Endpoints
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
NEWSAPI_URL = "https://newsapi.org/v2/"

# Model IDs
TEXT_MODEL = "facebook/opt-1.3b"
IMAGE_MODEL = "stabilityai/stable-diffusion-2-1"
CODE_MODEL = "bigcode/starcoder"

# Weather API
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "cd95bfc489f09469cb862762755b86bd")  # User's API key
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Currency API
CURRENCY_API_KEY = os.environ.get("CURRENCY_API_KEY", "")  # Will need to be set

# Rate Limits (requests per minute)
RATE_LIMIT = {
    "text": 30,
    "image": 10,
    "news": 100,
    "code": 20,
    "weather": 30,
    "translate": 25
}

# Queue Settings
MAX_QUEUE_SIZE = 100
QUEUE_TIMEOUT = 300  # seconds