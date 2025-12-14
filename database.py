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
    
    # Create fixed_extensions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fixed_extensions (
            name TEXT PRIMARY KEY,
            is_checked INTEGER DEFAULT 0
        )
    ''')
    
    # Create custom_extensions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS custom_extensions (
            name TEXT PRIMARY KEY
        )
    ''')
    
    # Seed fixed extensions
    for ext in INITIAL_FIXED_EXTENSIONS:
        cursor.execute("INSERT OR IGNORE INTO fixed_extensions (name) VALUES (?)", (ext,))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
