import aiohttp
from config import HUGGINGFACE_TOKEN, OPENROUTER_KEY, HUGGINGFACE_API_URL, OPENROUTER_API_URL, TEXT_MODEL

async def generate_text_response(message: str) -> str:
    # Try OpenRouter first
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "messages": [{"role": "user", "content": message}],
                "model": "openai/gpt-3.5-turbo"
            }
            
            async with session.post(OPENROUTER_API_URL, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['choices'][0]['message']['content']
    except Exception:
        # Fallback to Hugging Face
        pass

    # Hugging Face fallback
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
        async with session.post(
            f"{HUGGINGFACE_API_URL}{TEXT_MODEL}",
            headers=headers,
            json={"inputs": message}
        ) as response:
            if response.status != 200:
                raise Exception("Failed to generate response")
            
            result = await response.json()
            return result[0]['generated_text']
