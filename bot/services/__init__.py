"""
Services initialization module for the VisionaryAI bot.
Exports the core service functions for easy access.
"""

from .ai_service import generate_text_response
from .image_service import generate_image
from .news_service import get_news
from .code_service import get_code_assistance

__all__ = [
    'generate_text_response',
    'generate_image',
    'get_news',
    'get_code_assistance'
]
from bot.services.ai_service import generate_text_response
from bot.services.image_service import generate_image
from bot.services.news_service import get_news
from bot.services.code_service import get_code_assistance

__all__ = ['generate_text_response', 'generate_image', 'get_news', 'get_code_assistance']
