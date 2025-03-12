import aiohttp
from config import HUGGINGFACE_TOKEN, HUGGINGFACE_API_URL, CODE_MODEL

async def get_code_assistance(query: str) -> str:
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
        payload = {
            "inputs": f"### Question: {query}\n### Answer:",
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.95,
                "do_sample": True
            }
        }
        
        async with session.post(
            f"{HUGGINGFACE_API_URL}{CODE_MODEL}",
            headers=headers,
            json=payload
        ) as response:
            if response.status != 200:
                raise Exception("Failed to get code assistance")
            
            result = await response.json()
            code_response = result[0]['generated_text']
            
            # Format response with code blocks
            formatted_response = (
                "Here's your code assistance:\n\n"
                f"<pre><code>{code_response}</code></pre>"
            )
            
            return formatted_response
