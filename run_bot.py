import asyncio
from bot import start_bot
from config import logger

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Bot crashed: {str(e)}")
