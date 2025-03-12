from telegram.ext import Application
from config import TELEGRAM_TOKEN

bot = Application.builder().token(TELEGRAM_TOKEN).build()
