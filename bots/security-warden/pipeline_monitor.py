import time
import logging
import schedule
import sys
import os

# Put /app in path to access shared modules and sf_auth
sys.path.append("/app")
sys.path.append("/app/shared")

from sf_auth import get_auth
from queue_client import TaskQueue

logger = logging.getLogger(__name__)

class PipelineMonitor:
    """
    Monitors Salesforce Pipeline for updates.
    - Tracks High Value deals (> $100k)
    - Detects Stage changes (simple version: queries and logs)
    - Pushes updates to Redis Queue (e.g. for Notion Sync / Sled Commander notification)
    """

    def __init__(self, check_interval_minutes=5):
        self.check_interval = check_interval_minutes
        self.auth = get_auth()
        self.queue = TaskQueue()
        self.high_value_threshold = 100000.0

    def check_pipeline(self):
        logger.info("Running pipeline check...")
        
        # Query Open Opportunities
        soql = """
            SELECT Id, Name, Amount, StageName, CloseDate, Account.Name
            FROM Opportunity
            WHERE IsClosed = false
            AND Amount > 0
            ORDER BY Amount DESC
        """
        
        try:
            result = self.auth.query(soql)
            records = result.get("result", {}).get("records", [])
            
            logger.info(f"Found {len(records)} open opportunities.")
            
            for opp in records:
                amount = opp.get("Amount") or 0.0
                name = opp.get("Name")
                
                # Logic: If High Value, log it (and potentially notify)
                if amount >= self.high_value_threshold:
                    self._handle_high_value_opp(opp)
                    
            logger.info("Pipeline check complete.")
            
        except Exception as e:
            logger.error(f"Pipeline check failed: {e}")

    def _handle_high_value_opp(self, opp):
        """Action to take for high value opportunities."""
        msg = f"High Value Deal Detected: {opp['Name']} (${opp['Amount']:,.2f}) - {opp['StageName']}"
        logger.info(msg)
        
        # TODO: In the future, this could enqueue a notification to Sled Commander
        # self.queue.enqueue("telegram_notifications", "notify_channel", {"message": msg})

    def start(self):
        logger.info(f"Starting Pipeline Monitor (Interval: {self.check_interval} min)")
        
        # Run immediately once
        self.check_pipeline()
        
        # Schedule
        schedule.every(self.check_interval).minutes.do(self.check_pipeline)
        
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    monitor = PipelineMonitor(check_interval_minutes=5)
    monitor.start()
