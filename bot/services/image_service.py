import aiohttp
import base64
from config import HUGGINGFACE_TOKEN, HUGGINGFACE_API_URL, IMAGE_MODEL

async def generate_image(prompt: str) -> str:
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": "blurry, bad quality, nsfw",
                "num_inference_steps": 30,
                "guidance_scale": 7.5
            }
        }
        
        async with session.post(
            f"{HUGGINGFACE_API_URL}{IMAGE_MODEL}",
            headers=headers,
            json=payload
        ) as response:
            if response.status != 200:
                raise Exception("Failed to generate image")
            
            image_bytes = await response.read()
            return f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode()}"
