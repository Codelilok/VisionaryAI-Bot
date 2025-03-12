
import aiohttp
import html
from config import logger, HUGGINGFACE_TOKEN, HUGGINGFACE_API_URL

# Translation model
TRANSLATION_MODEL = "Helsinki-NLP/opus-mt-en-fr"  # Example model (English to French)

async def translate_text(text: str, target_lang: str = "fr") -> str:
    """Translate text to target language using Hugging Face model"""
    logger.info(f"Translating text to {target_lang}")
    
    # Map language codes to appropriate models
    language_models = {
        "fr": "Helsinki-NLP/opus-mt-en-fr",  # English to French
        "es": "Helsinki-NLP/opus-mt-en-es",  # English to Spanish
        "de": "Helsinki-NLP/opus-mt-en-de",  # English to German
        "zh": "Helsinki-NLP/opus-mt-en-zh",  # English to Chinese
        # Add more language pairs as needed
    }
    
    # Select the appropriate model
    model = language_models.get(target_lang.lower(), "Helsinki-NLP/opus-mt-en-fr")
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
            payload = {"inputs": text}
            
            async with session.post(
                f"{HUGGINGFACE_API_URL}{model}",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    logger.error(f"Translation API error: {response.status}")
                    return "Sorry, I couldn't translate that text."
                
                result = await response.json()
                
                # Extract the translated text
                translated_text = result[0]["translation_text"]
                
                return f"🌐 <b>Translation</b>\n\n" \
                       f"Original: {html.escape(text)}\n\n" \
                       f"Translated: {html.escape(translated_text)}"
                
    except Exception as e:
        logger.error(f"Error in translation service: {str(e)}")
        return "Sorry, I encountered an error while translating your text."
