import os
import redis
import json
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class TaskQueue:
    """Simple Redis-based Task Queue."""
    
    def __init__(self, redis_url=None):
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://redis:6379/0")
        try:
            self.redis = redis.from_url(self.redis_url, decode_responses=True)
            self.redis.ping()
            logger.info(f"Connected to Redis at {self.redis_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    def enqueue(self, queue_name: str, task_type: str, payload: dict, priority: str = "normal") -> str:
        """
        Enqueue a task.
        
        Args:
            queue_name: Name of the queue (e.g., 'salesforce_tasks', 'notion_sync')
            task_type: Identifier for the worker (e.g., 'create_quote')
            payload: Dict containing task arguments
            priority: 'high', 'normal', 'low' (not yet implemented, placeholder)
            
        Returns:
            task_id: Unique UUID
        """
        task_id = str(uuid.uuid4())
        task_data = {
            "id": task_id,
            "type": task_type,
            "payload": payload,
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending",
            "priority": priority
        }
        
        try:
            # Push to list
            self.redis.rpush(f"queue:{queue_name}", json.dumps(task_data))
            # Also store status hash for tracking (expires in 24h)
            self.redis.setex(f"task:{task_id}", 86400, json.dumps(task_data))
            logger.info(f"Enqueued task {task_id} to {queue_name} (type={task_type})")
            return task_id
        except Exception as e:
            logger.error(f"Failed to enqueue task: {e}")
            raise

    def get_task_status(self, task_id: str) -> dict:
        """Retrieve task status."""
        data = self.redis.get(f"task:{task_id}")
        if data:
            return json.loads(data)
        return None

    def update_task_status(self, task_id: str, status: str, result: dict = None):
        """Update task status (used by workers)."""
        data_str = self.redis.get(f"task:{task_id}")
        if data_str:
            data = json.loads(data_str)
            data["status"] = status
            data["updated_at"] = datetime.utcnow().isoformat()
            if result:
                data["result"] = result
            
            # Update with same TTL
            ttl = self.redis.ttl(f"task:{task_id}")
            if ttl < 0: ttl = 86400
            self.redis.setex(f"task:{task_id}", ttl, json.dumps(data))
