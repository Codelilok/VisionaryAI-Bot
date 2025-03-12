import asyncio
from collections import defaultdict
import time
from config import RATE_LIMIT, MAX_QUEUE_SIZE, QUEUE_TIMEOUT, logger

class QueueManager:
    def __init__(self):
        self.queues = defaultdict(asyncio.Queue)
        self.last_request_time = defaultdict(lambda: defaultdict(float))
        self.request_counts = defaultdict(int)

    async def enqueue(self, service_type, func, *args, **kwargs):
        if self.queues[service_type].qsize() >= MAX_QUEUE_SIZE:
            raise Exception("Queue is full. Please try again later.")

        current_time = time.time()
        # Clean up old request counts
        self._cleanup_request_counts(service_type, current_time)

        # Check rate limit
        if self.request_counts[service_type] >= RATE_LIMIT[service_type]:
            raise Exception(f"Rate limit exceeded for {service_type}. Please try again later.")

        # Add to queue
        future = asyncio.Future()
        await self.queues[service_type].put((func, args, kwargs, future, current_time))
        
        # Process queue
        asyncio.create_task(self._process_queue(service_type))
        
        try:
            result = await asyncio.wait_for(future, timeout=QUEUE_TIMEOUT)
            return result
        except asyncio.TimeoutError:
            raise Exception("Request timed out. Please try again.")

    async def _process_queue(self, service_type):
        while not self.queues[service_type].empty():
            func, args, kwargs, future, enqueue_time = await self.queues[service_type].get()
            
            if time.time() - enqueue_time > QUEUE_TIMEOUT:
                future.set_exception(Exception("Request timed out"))
                continue

            try:
                result = await func(*args, **kwargs)
                future.set_result(result)
                
                # Update rate limiting
                current_time = time.time()
                self.last_request_time[service_type][current_time] = current_time
                self.request_counts[service_type] += 1
                
            except Exception as e:
                logger.error(f"Error processing {service_type} request: {str(e)}")
                future.set_exception(e)

    def _cleanup_request_counts(self, service_type, current_time):
        # Remove requests older than 60 seconds
        old_requests = [
            timestamp for timestamp in self.last_request_time[service_type]
            if current_time - timestamp > 60
        ]
        
        for timestamp in old_requests:
            del self.last_request_time[service_type][timestamp]
        
        self.request_counts[service_type] = len(self.last_request_time[service_type])
