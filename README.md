# VisionaryAI-Bot

VisionaryAI is an AI-powered **Telegram bot** that can chat, generate images, fetch real-time news, assist with coding, and provide currency exchange rates. It uses multiple free AI models and APIs to deliver a seamless experience.  

## Features  
✅ **Conversational AI** – Uses Hugging Face Inference API & OpenRouter AI models.  
✅ **Image Generation** – Uses Hugging Face Stable Diffusion API for AI images.  
✅ **Real-time News** – Fetches and summarizes news using News API.  
✅ **Currency Exchange** – Provides live exchange rates via FreeCurrencyAPI.  
✅ **Code Assistance** – Helps with coding using Hugging Face Code Models.  
✅ **Weather Updates** – Provides weather forecasts using OpenWeather API.  

## Setup & Installation  

### 1. Clone the Repository  
```bash
git clone <your-repository-url>
cd VisionaryAI-Bot

## 2. Install Dependencies  

pip install -r requirements.txt


3. Add API Keys in Replit Secrets

Instead of using a .env file, store your credentials securely in Replit Secrets:

Steps:
1. Open Replit  
2. Go to the Secrets tab  
3. Add the following keys:

TELEGRAM_BOT_TOKEN → Your Telegram bot token
OPENWEATHER_API_KEY → Your OpenWeather API key
FREECURRENCY_API_KEY → Your FreeCurrencyAPI key
NEWS_API_KEY → Your News API key
HUGGINGFACE_API_KEY → Your Hugging Face API key

4. Run the Bot
python run_bot.py

Deployment

To keep your bot running:
- Use Replit’s Always-On feature  
- Deploy on Render, Fly.io, or Railway  
- Set up UptimeRobot for continuous operation

License
This project is licensed under MIT License


