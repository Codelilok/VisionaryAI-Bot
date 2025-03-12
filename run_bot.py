
import asyncio
from bot import start_bot
from config import logger

def main():
    """Run the bot in its own process"""
    try:
        # Create and set new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Run the bot
        logger.info("Starting bot with new event loop...")
        loop.run_until_complete(start_bot())
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
