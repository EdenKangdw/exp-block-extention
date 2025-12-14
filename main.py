from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from database import get_db_connection, init_db

app = FastAPI()

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()

from fastapi.responses import RedirectResponse

# Mount static files
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

# Models
class FixedExtensionUpdate(BaseModel):
    is_checked: bool

class CustomExtensionCreate(BaseModel):
    name: str

# API Endpoints

@app.get("/api/extensions")
def get_extensions():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fixed extensions
    cursor.execute("SELECT name, is_allowed FROM file_extensions WHERE type = 'fixed'")
    fixed_rows = cursor.fetchall()
    # Convert is_allowed (1=Allowed) to is_checked (1=Blocked)
    # If is_allowed=1 (True), then is_checked=0 (False)
    # If is_allowed=0 (False), then is_checked=1 (True)
    fixed = [{"name": row['name'], "is_checked": not row['is_allowed']} for row in fixed_rows]
    
    # Custom extensions (Only return blocked ones, i.e., is_allowed=0)
    # Actually, for custom extensions, existence in the list usually means blocked.
    # In our new schema, we insert them as type='custom'.
    # Let's assume all custom extensions in the table are blocked.
    cursor.execute("SELECT name FROM file_extensions WHERE type = 'custom'")
    custom = [{"name": row['name']} for row in cursor.fetchall()]
    
    conn.close()
    return {"fixed": fixed, "custom": custom}

@app.patch("/api/fixed-extensions/{name}")
def update_fixed_extension(name: str, update: FixedExtensionUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # is_checked=True means Blocked -> is_allowed=False
    is_allowed = not update.is_checked
    
    cursor.execute('''
        UPDATE file_extensions 
        SET is_allowed = ?, update_at = CURRENT_TIMESTAMP 
        WHERE name = ? AND type = 'fixed'
    ''', (is_allowed, name))
    
    conn.commit()
    conn.close()
    return {"message": "Updated successfully"}

import re

@app.post("/api/custom-extensions")
def add_custom_extension(ext: CustomExtensionCreate):
    name = ext.name.strip().lower()
    
    if len(name) > 20:
        raise HTTPException(status_code=400, detail="Invalid extension name (max 20 chars)")
    
    if not re.match(r'^[a-zA-Z0-9]+$', name):
        raise HTTPException(status_code=400, detail="Invalid extension name (only English letters and numbers allowed)")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM file_extensions WHERE type = 'custom'")
    count = cursor.fetchone()['count']
    
    if count >= 200:
        conn.close()
        raise HTTPException(status_code=400, detail="Maximum number of custom extensions reached (200)")
    
    try:
        # Custom extensions are blocked by default (is_allowed=False)
        cursor.execute('''
            INSERT INTO file_extensions (name, type, is_allowed, update_by, update_at) 
            VALUES (?, 'custom', 0, 'guest', CURRENT_TIMESTAMP)
        ''', (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Extension already exists")
    
    conn.close()
    return {"message": "Added successfully"}

@app.delete("/api/custom-extensions/{name}")
def delete_custom_extension(name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM file_extensions WHERE name = ? AND type = 'custom'", (name,))
    conn.commit()
    conn.close()
    return {"message": "Deleted successfully"}

@app.delete("/api/custom-extensions")
def delete_all_custom_extensions():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM file_extensions WHERE type = 'custom'")
    conn.commit()
    conn.close()
    return {"message": "All custom extensions deleted"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
