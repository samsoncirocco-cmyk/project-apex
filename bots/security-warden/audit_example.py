"""
Example audit script for Security Warden.
Demonstrates querying Salesforce and logging to SQLite.
"""

import sys
import os
import sqlite3
from datetime import datetime, timedelta

# Add path so we can import sf_auth
sys.path.append("/app")

from sf_auth import get_auth

def audit_recent_quotes():
    """Audit quotes created in the last 7 days."""
    
    # Get authenticated auth manager
    auth = get_auth()
    
    # Calculate date 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    # Query recent quotes
    soql = f"""
        SELECT Id, Name, SBQQ__Opportunity2__r.Name, CreatedDate, CreatedBy.Name, SBQQ__Status__c
        FROM SBQQ__Quote__c
        WHERE CreatedDate >= {seven_days_ago}T00:00:00Z
        ORDER BY CreatedDate DESC
    """
    
    # Use CLI query wrapper
    result = auth.query(soql)
    quotes = result.get("result", {}).get("records", [])
    
    print(f"Found {len(quotes)} quotes created in the last 7 days")
    
    # Log to SQLite
    db_path = os.getenv("DATABASE_PATH", "/data/apex.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for quote in quotes:
        quote_name = quote.get('Name', 'Unknown')
        status = quote.get('SBQQ__Status__c', 'N/A')
        print(f"  - {quote_name} (Status: {status})")
        
        # Log audit entry
        try:
            cursor.execute("""
                INSERT INTO interactions (user_id, bot_name, command, raw_input, response_summary)
                VALUES (?, ?, ?, ?, ?)
            """, (
                "system",
                "security-warden",
                "audit_quotes",
                soql,
                f"Quote: {quote_name}, Status: {status}"
            ))
        except Exception as e:
            print(f"Failed to log to DB: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"Logged {len(quotes)} audit entries to database")

if __name__ == "__main__":
    audit_recent_quotes()
