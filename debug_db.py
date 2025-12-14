import sqlite3

def check_db():
    conn = sqlite3.connect('extensions.db')
    cursor = conn.cursor()
    
    print("Fixed Extensions:")
    cursor.execute("SELECT * FROM fixed_extensions")
    for row in cursor.fetchall():
        print(row)
        
    print("\nCustom Extensions:")
    cursor.execute("SELECT * FROM custom_extensions")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()

if __name__ == "__main__":
    check_db()
