import csv
import logging
import sqlite3
import os
import sys
from datetime import datetime
from difflib import SequenceMatcher

# Put /app in path to access shared modules and sf_auth
sys.path.append("/app")
sys.path.append("/app/shared")

from sf_auth import get_auth

logger = logging.getLogger(__name__)

class ErateScanner:
    """
    Scans E-Rate Form 470 CSV exports for opportunities.
    Prioritizes South Dakota (SD) and Nebraska (NE) territories.
    """

    def __init__(self):
        self.auth = get_auth()
        self.target_states = ['SD', 'NE', 'SOUTH DAKOTA', 'NEBRASKA']
        self.db_path = os.getenv("DATABASE_PATH", "/data/apex.db")

    def scan(self, csv_path):
        """
        Main scan execution method.
        1. Queries SFDC for accounts.
        2. Parses CSV.
        3. Matches and Filters.
        4. Logs results.
        """
        logger.info(f"Starting E-Rate Scan on {csv_path}...")
        
        if not os.path.exists(csv_path):
            logger.error(f"CSV file not found: {csv_path}")
            return {"status": "error", "message": "File not found"}

        # 1. Query SFDC Accounts
        sfdc_accounts = self._query_sfdc_education_accounts()
        logger.info(f"Loaded {len(sfdc_accounts)} education accounts from Salesforce.")

        # 2. Parse CSV
        filings = self._parse_csv(csv_path)
        logger.info(f"Parsed {len(filings)} filings from CSV.")

        # 3. Match and Filter
        matches = []
        territory_hits = []

        for filing in filings:
            # Check Territory Priority
            is_territory = filing['state'].upper() in self.target_states
            
            # Find best match in SFDC
            match_data = self._find_best_match(filing, sfdc_accounts)
            
            if match_data:
                filing['sfdc_match'] = match_data
                matches.append(filing)
                
                if is_territory:
                    territory_hits.append(filing)
                    self._log_hit(filing, is_territory=True)
            elif is_territory:
                # Territory hit but no SFDC match - still important!
                territory_hits.append(filing)
                self._log_hit(filing, is_territory=True)

        logger.info(f"Scan Complete. Found {len(matches)} matches and {len(territory_hits)} Territory (SD/NE) hits.")
        
        return {
            "status": "success",
            "matches_found": len(matches),
            "territory_hits": len(territory_hits),
            "territory_details": [f"{h['name']} ({h['state']})" for h in territory_hits]
        }

    def _query_sfdc_education_accounts(self):
        """Fetch education accounts from Salesforce."""
        query = """
        SELECT Id, Name, BillingCity, BillingState, Industry
        FROM Account
        WHERE (Industry LIKE '%Education%' OR Industry LIKE '%School%' OR Name LIKE '%School%' OR Name LIKE '%District%' OR Name LIKE '%College%')
        ORDER BY Name
        """
        try:
            result = self.auth.query(query)
            return result.get("result", {}).get("records", [])
        except Exception as e:
            logger.error(f"SFDC Query failed: {e}")
            return []

    def _parse_csv(self, csv_path):
        """Parse the Form 470 export CSV."""
        results = []
        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Normalized data structure
                    results.append({
                        '470_number': row.get('470_number'),
                        'name': row.get('applicant_name', '').strip(),
                        'city': row.get('applicant_city', '').strip(),
                        'state': row.get('applicant_state', '').strip(),
                        'service_type': row.get('service_type', ''),
                        'posted_date': row.get('posted_date', ''),
                        'raw': row
                    })
        except Exception as e:
            logger.error(f"CSV Parsing failed: {e}")
        return results

    def _find_best_match(self, filing, accounts):
        """Fuzzy match logic."""
        best_score = 0.0
        best_account = None
        
        filing_name = filing['name'].upper()
        
        for acct in accounts:
            acct_name = acct.get('Name', '').upper()
            score = SequenceMatcher(None, filing_name, acct_name).ratio()
            
            # Boost for city match
            if filing['city'].upper() == acct.get('BillingCity', '').upper():
                score += 0.15
                
            if score > best_score:
                best_score = score
                best_account = acct
                
        if best_score > 0.70:
            return {"Id": best_account['Id'], "Name": best_account['Name'], "Score": best_score}
        return None

    def _log_hit(self, filing, is_territory=False):
        """Log significant finding to DB."""
        # In a real scenario, this would notify Sled Commander via Redis
        log_msg = f"HIT: {filing['name']} ({filing['state']}) - Priority: {'CRITICAL' if is_territory else 'Normal'}"
        logger.info(log_msg)
        
        # Persist to SQLite
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS procurement_matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    form_470_id TEXT,
                    applicant_name TEXT,
                    state TEXT,
                    service_type TEXT,
                    posted_date TEXT,
                    sfdc_account_id TEXT,
                    is_territory BOOLEAN,
                    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            sfdc_id = filing.get('sfdc_match', {}).get('Id')
            
            cursor.execute("""
                INSERT INTO procurement_matches (form_470_id, applicant_name, state, service_type, posted_date, sfdc_account_id, is_territory)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                filing['470_number'],
                filing['name'],
                filing['state'],
                filing['service_type'],
                filing['posted_date'],
                sfdc_id,
                is_territory
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"DB Log failed: {e}")

if __name__ == "__main__":
    # Test run
    logging.basicConfig(level=logging.INFO)
    scanner = ErateScanner()
    # Mock path for testing
    scanner.scan("/data/test.csv")
