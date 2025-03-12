
import asyncio
from collections import defaultdict
import time
from config import RATE_LIMIT, MAX_QUEUE_SIZE, QUEUE_TIMEOUT, logger

class QueueManager:
    def __init__(self):
        self.queues = {
            'text': asyncio.Queue(maxsize=MAX_QUEUE_SIZE),
            'image': asyncio.Queue(maxsize=MAX_QUEUE_SIZE),
            'news': asyncio.Queue(maxsize=MAX_QUEUE_SIZE),
            'code': asyncio.Queue(maxsize=MAX_QUEUE_SIZE)
        }
        self.request_counts = defaultdict(int)
        self.last_request_time = defaultdict(dict)
        
    async def enqueue(self, service_type, func, *args, **kwargs):
        """Add a request to the queue and return the result when processed"""
        # Check rate limiting
        current_time = time.time()
        self._cleanup_request_counts(service_type, current_time)
        
        if self.request_counts[service_type] >= RATE_LIMIT.get(service_type, 30):
            raise Exception(f"Rate limit exceeded for {service_type} service")
        
        # Create future to get result
        future = asyncio.Future()
        
        # Add to queue
        try:
            self.queues[service_type].put_nowait((func, args, kwargs, future, current_time))
        except asyncio.QueueFull:
            raise Exception(f"Queue is full for {service_type} service")
        
        # Start processing if not already running
        asyncio.create_task(self._process_queue(service_type))
        
        # Wait for result with timeout
        try:
            return await asyncio.wait_for(future, timeout=QUEUE_TIMEOUT)
        except asyncio.TimeoutError:
            raise Exception("Request timed out")
    
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
