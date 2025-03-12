import html
from typing import Any, Dict
from config import logger

def sanitize_message(message: str) -> str:
    """Sanitize message content for safe display"""
    return html.escape(message)

def format_error_message(error: Exception) -> str:
    """Format error messages for user display"""
    return f"Error: {str(error)}"

def log_error(func_name: str, error: Exception, context: Dict[str, Any] = None) -> None:
    """Log errors with context"""
    error_context = {
        "function": func_name,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context or {}
    }
    logger.error(f"Error occurred: {error_context}")
