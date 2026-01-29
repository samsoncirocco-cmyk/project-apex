import sqlite3
import os
import sys

def init_db(db_path="/data/apex.db"):
    """Initialize the SQLite database with WAL mode and core tables."""
    print(f"Initializing database at {db_path}...")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Enable WAL Mode (Write-Ahead Logging)
        # This allows concurrent readers and writers, critical for our multi-bot architecture
        cursor.execute("PRAGMA journal_mode=WAL;")
        mode = cursor.fetchone()[0]
        if mode != 'wal':
            print(f"WARNING: WAL mode not enabled. Current mode: {mode}")
        else:
            print("WAL mode enabled.")
            
        cursor.execute("PRAGMA synchronous=NORMAL;")
        
        # 2. Create Core Tables
        
        # Users table - central registry of authorized users across platforms
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                username TEXT,
                full_name TEXT,
                role TEXT DEFAULT 'user', -- 'admin', 'user'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Interactions table - log all major actions for audit
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                bot_name TEXT, 
                command TEXT,
                raw_input TEXT,
                response_summary TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """)
        
        # System State/Key-Value Store - for simple persistence without Redis
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        print("Database initialized successfully.")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    # Get path from environment or default
    db_path = os.getenv("DATABASE_PATH", "/data/apex.db")
    init_db(db_path)
