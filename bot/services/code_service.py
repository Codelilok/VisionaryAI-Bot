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
import aiohttp
from config import HUGGINGFACE_TOKEN, HUGGINGFACE_API_URL, CODE_MODEL, logger

async def get_code_assistance(query: str) -> str:
    """
    Get code assistance using Hugging Face models
    
    Args:
        query: The coding question or problem
    
    Returns:
        str: The generated code solution or explanation
    """
    logger.info(f"Generating code assistance for query: {query}")
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
            
            # Add programming context to the query
            enhanced_query = f"Programming question: {query}\n\nAnswer with code:"
            
            async with session.post(
                f"{HUGGINGFACE_API_URL}{CODE_MODEL}",
                headers=headers,
                json={"inputs": enhanced_query, "parameters": {"max_new_tokens": 250}}
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Code API error: {response.status} - {error_text}")
                    return "I'm having trouble connecting to the code assistance service. Please try again later."
                
                result = await response.json()
                return result[0]['generated_text'].replace(enhanced_query, "").strip()
    
    except Exception as e:
        logger.error(f"Error in code assistance: {str(e)}")
        return "Sorry, I encountered an error processing your code question. Please try again."
