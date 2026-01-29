import os
import subprocess
import json
import logging
from simple_salesforce import Salesforce

logger = logging.getLogger(__name__)

class SalesforceAuth:
    """
    Manages Salesforce authentication.
    Supports both official 'sf' CLI and 'simple-salesforce' via refresh token.
    """
    
    def __init__(self):
        self.client_id = os.getenv("SF_CLIENT_ID")
        self.client_secret = os.getenv("SF_CLIENT_SECRET")
        self.refresh_token = os.getenv("SF_REFRESH_TOKEN")
        self.instance_url = os.getenv("SF_INSTANCE_URL")
        
        if not all([self.client_id, self.client_secret, self.refresh_token, self.instance_url]):
            raise ValueError("Missing required Salesforce environment variables")

    def authenticate_cli(self):
        """
        Authenticate SF CLI using refresh token (sfdx-url method).
        This persists the active session in `/root/.sf/`.
        """
        try:
            # Construct SFDX auth URL
            # Format: force://<clientId>:<clientSecret>:<refreshToken>@<instanceUrl>
            # Remove protocol from instance URL for the sfdx-url format
            clean_url = self.instance_url.replace('https://', '').replace('http://', '')
            sfdx_url = f"force://{self.client_id}:{self.client_secret}:{self.refresh_token}@{clean_url}"
            
            cmd = [
                "sf", "org", "login", "sfdx-url",
                "--sfdx-url-stdin",
                "--set-default",
                "--alias", "production"
            ]
            
            result = subprocess.run(
                cmd,
                input=sfdx_url,
                text=True,
                capture_output=True,
                check=True
            )
            
            logger.info("SF CLI authenticated successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"SF CLI authentication failed: {e.stderr}")
            raise

    def get_sf_client(self):
        """
        Get authenticated simple-salesforce client (REST API).
        """
        try:
            sf = Salesforce(
                instance_url=self.instance_url,
                session_id='',  # Will be obtained via refresh token
                client_id=self.client_id,
                client_secret=self.client_secret,
                refresh_token=self.refresh_token
            )
            logger.info("Simple-Salesforce client authenticated")
            return sf
        except Exception as e:
            logger.error(f"Failed to create SF client: {e}")
            raise

    def run_command(self, args: list):
        """Run arbitrary SF CLI command."""
        try:
            cmd = ["sf"] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"SF CLI command failed: {e.stderr}")
            raise

    def query(self, soql: str):
        """Execute SOQL query via CLI."""
        try:
            cmd = [
                "data", "query",
                "--query", soql,
                "--target-org", "production",
                "--json"
            ]
            result = self.run_command(cmd)
            return json.loads(result.stdout)
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise

    def create_record(self, sobject: str, values: str):
        """Create record via CLI (reusing logic from create_cpq_quote.py)."""
        try:
            cmd = [
                "data", "create", "record",
                "--sobject", sobject,
                "--values", values,
                "--target-org", "production",
                "--json"
            ]
            result = self.run_command(cmd)
            return json.loads(result.stdout)
        except Exception as e:
            logger.error(f"Create record failed: {e}")
            raise

# Singleton instance
_auth_instance = None

def get_auth():
    """Get or create SalesforceAuth singleton."""
    global _auth_instance
    if _auth_instance is None:
        _auth_instance = SalesforceAuth()
        _auth_instance.authenticate_cli()
    return _auth_instance

def get_sf_client():
    """Convenience function to get authenticated SF client."""
    return get_auth().get_sf_client()
