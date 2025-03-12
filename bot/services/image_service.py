import aiohttp
from config import HUGGINGFACE_TOKEN, HUGGINGFACE_API_URL, IMAGE_MODEL, logger

async def generate_image(prompt: str) -> bytes:
    """Generate an image from a text prompt"""
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": "blurry, bad quality, nsfw",
                "num_inference_steps": 25,
                "guidance_scale": 7.5,
                "width": 512,
                "height": 512
            }
        }

        try:
            logger.info(f"Sending image generation request to {IMAGE_MODEL}")
            async with session.post(
                f"{HUGGINGFACE_API_URL}{IMAGE_MODEL}",
                headers=headers,
                json=payload,
                timeout=30
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Image generation failed: {error_text}")
                    raise Exception("Failed to generate image")

                return await response.read()

        except Exception as e:
            logger.error(f"Error in image generation: {str(e)}")
            raise