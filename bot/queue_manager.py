import asyncio
from typing import Dict, Any, Callable, Coroutine
from config import MAX_QUEUE_SIZE, QUEUE_TIMEOUT, RATE_LIMIT, logger

class QueueManager:
    def __init__(self):
        self.queues = {}
        self.rate_limits = RATE_LIMIT
        self.semaphores = {}
        self._initialize_semaphores()

    def _initialize_semaphores(self):
        """Initialize semaphores for each service type"""
        for service_type, limit in self.rate_limits.items():
            self.semaphores[service_type] = asyncio.Semaphore(limit)

    async def enqueue(self, service_type: str, 
                    function: Callable[[Any], Coroutine[Any, Any, str]], 
                    *args, **kwargs) -> str:
        """
        Enqueue a task and execute it when resources are available

        Args:
            service_type: Type of service being requested (text, image, news, code)
            function: Async function to execute
            *args, **kwargs: Arguments to pass to the function

        Returns:
            The result of the function call
        """
        if service_type not in self.semaphores:
            raise ValueError(f"Unknown service type: {service_type}")

        # Use semaphore to limit concurrent requests
        async with self.semaphores[service_type]:
            try:
                logger.info(f"Processing {service_type} request")
                result = await function(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error in {service_type} queue: {str(e)}")
                raise