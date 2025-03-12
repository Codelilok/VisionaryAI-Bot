
import asyncio
import signal
import sys
from bot import start_bot
from config import logger

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    logger.info("Received shutdown signal, terminating bot...")
    sys.exit(0)

def main():
    """Run the bot in its own process"""
    try:
        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
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
