import logging
import sys
import os
import json

# Add shared modules to path (now copied to /app/shared)
sys.path.append("/app/shared")

from worker import BaseWorker
from sf_auth import get_auth

logger = logging.getLogger(__name__)

class SalesforceWorker(BaseWorker):
    """
    Worker for processing Salesforce tasks from Redis queue.
    Reuses logic from create_cpq_quote.py for quote generation.
    """
    
    def __init__(self):
        super().__init__(queue_name="salesforce_tasks", worker_id="sf-worker-1")
        
        # Authenticate on startup
        try:
            get_auth()
            logger.info("Salesforce authentication successful")
        except Exception as e:
            logger.error(f"Failed to authenticate with Salesforce: {e}")
            sys.exit(1)
        
        # Register task handlers
        self.register_handler("query_records", self.handle_query)
        self.register_handler("create_quote", self.handle_create_quote)
        self.register_handler("audit_permissions", self.handle_audit_permissions)

    def handle_query(self, payload: dict):
        """Execute generic SOQL query."""
        soql = payload.get("soql")
        if not soql:
            raise ValueError("Missing 'soql' in payload")
        
        logger.info(f"Executing SOQL: {soql}")
        auth = get_auth()
        result = auth.query(soql)
        
        return {
            "status": "success",
            "record_count": result.get("result", {}).get("totalSize", 0),
            "records": result.get("result", {}).get("records", [])
        }

    def handle_create_quote(self, payload: dict):
        """
        Create a Salesforce CPQ quote.
        Adapted from create_cpq_quote.py logic.
        """
        opp_id = payload.get("opportunity_id")
        name = payload.get("name")
        set_primary = payload.get("set_primary", True)
        
        if not opp_id or not name:
            raise ValueError("Missing 'opportunity_id' or 'name' in payload")
        
        logger.info(f"Creating quote '{name}' for Opportunity {opp_id}")
        
        # Build values string (Format: Key='Value' Key2='Value2')
        # Logic reused from create_cpq_quote.py:create_quote_cli
        values = f"Name='{name}' SBQQ__Opportunity2__c='{opp_id}' SBQQ__Primary__c={str(set_primary).lower()}"
        
        auth = get_auth()
        result = auth.create_record(
            sobject="SBQQ__Quote__c",
            values=values
        )
        
        # Parse result
        # SF CLI Output: {"status": 0, "result": {"id": "...", "success": true, ...}}
        res_data = result.get("result", {})
        quote_id = res_data.get("id")
        success = res_data.get("success")
        
        if success and quote_id:
            logger.info(f"Quote created successfully: {quote_id}")
            return {
                "status": "success",
                "quote_id": quote_id,
                "quote_name": name,
                "cli_output": result
            }
        else:
            raise RuntimeError(f"Quote creation failed: {result}")

    def handle_audit_permissions(self, payload: dict):
        """Audit user permissions."""
        user_id = payload.get("user_id")
        
        soql = f"""
            SELECT Id, Name, Profile.Name, UserRole.Name, IsActive
            FROM User
            WHERE Id = '{user_id}'
        """
        
        auth = get_auth()
        result = auth.query(soql)
        
        records = result.get("result", {}).get("records", [])
        if not records:
            raise ValueError(f"User {user_id} not found")
        
        user = records[0]
        return {
            "status": "success",
            "user_audit": {
                "Name": user.get("Name"),
                "Profile": user.get("Profile", {}).get("Name"),
                "IsActive": user.get("IsActive")
            }
        }

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    worker = SalesforceWorker()
    worker.run()
