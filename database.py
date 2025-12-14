import sqlite3
import os

DB_NAME = "extensions.db"
INITIAL_FIXED_EXTENSIONS = ['bat', 'cmd', 'com', 'cpl', 'exe', 'scr', 'js']

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Drop old tables if they exist (for migration)
    cursor.execute("DROP TABLE IF EXISTS fixed_extensions")
    cursor.execute("DROP TABLE IF EXISTS custom_extensions")
    
    # Create new file_extensions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_extensions (
            name TEXT PRIMARY KEY,
            type TEXT CHECK(type IN ('fixed', 'custom')),
            is_allowed BOOLEAN,
            update_by TEXT,
            update_at TIMESTAMP
        )
    ''')
    
    # Seed fixed extensions
    for ext in INITIAL_FIXED_EXTENSIONS:
        # Default: is_allowed=True (Unchecked/Allowed)
        cursor.execute('''
            INSERT OR IGNORE INTO file_extensions (name, type, is_allowed, update_by, update_at) 
            VALUES (?, 'fixed', 1, 'system', CURRENT_TIMESTAMP)
        ''', (ext,))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
