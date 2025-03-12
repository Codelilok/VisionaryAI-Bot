import aiohttp
import base64
from config import HUGGINGFACE_TOKEN, HUGGINGFACE_API_URL, IMAGE_MODEL, logger

async def generate_image(prompt: str) -> bytes:
    """Generate an image from a text prompt"""
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

        try:
            logger.info(f"Sending image generation request for prompt: {prompt}")
            async with session.post(
                f"{HUGGINGFACE_API_URL}{IMAGE_MODEL}",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Failed to generate image. Status: {response.status}, Error: {error_text}")
                    raise Exception("Failed to generate image")

                # Get raw image bytes
                image_bytes = await response.read()
                logger.info("Successfully generated image")
                return image_bytes

        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise Exception(f"Failed to generate image: {str(e)}")