import logging
import json
import time
import signal
import sys
from .queue_client import TaskQueue

logger = logging.getLogger(__name__)

class BaseWorker:
    """Base class for Queue Workers."""
    
    def __init__(self, queue_name: str, worker_id: str = "worker-1"):
        self.queue_name = queue_name
        self.worker_id = worker_id
        self.running = False
        self.queue = TaskQueue()
        
        # Handlers registry: "task_type" -> function
        self.handlers = {}

        # Signal handling
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)

    def register_handler(self, task_type: str, handler_func):
        """Register a function to handle a specific task type."""
        self.handlers[task_type] = handler_func
        logger.info(f"Registered handler for '{task_type}'")

    def run(self):
        """Main worker loop."""
        self.running = True
        logger.info(f"Worker {self.worker_id} started listening on 'queue:{self.queue_name}'")
        
        while self.running:
            try:
                # Blocking pop (timeout 5s to allow shutdown check)
                # redis.blpop returns tuple (key, value) or None
                item = self.queue.redis.blpop(f"queue:{self.queue_name}", timeout=5)
                
                if item:
                    _, task_json = item
                    self._process_task(json.loads(task_json))
                
            except Exception as e:
                logger.error(f"Worker loop error: {e}")
                time.sleep(1) # Prevent tight loop on error

    def _process_task(self, task_data: dict):
        task_id = task_data.get("id")
        task_type = task_data.get("type")
        payload = task_data.get("payload", {})
        
        logger.info(f"Processing task {task_id} ({task_type})")
        
        self.queue.update_task_status(task_id, "processing")
        
        handler = self.handlers.get(task_type)
        if not handler:
            logger.error(f"No handler for task type '{task_type}'")
            self.queue.update_task_status(task_id, "failed", {"error": f"Unknown task type: {task_type}"})
            return

        try:
            # Execute handler
            result = handler(payload)
            self.queue.update_task_status(task_id, "completed", result)
            logger.info(f"Task {task_id} completed")
        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
            self.queue.update_task_status(task_id, "failed", {"error": str(e)})

    def _shutdown(self, signum, frame):
        logger.info("Shutdown signal received. Stopping worker...")
        self.running = False
