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
    
    cursor.execute("SELECT * FROM fixed_extensions")
    fixed = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM custom_extensions")
    custom = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return {"fixed": fixed, "custom": custom}

@app.patch("/api/fixed-extensions/{name}")
def update_fixed_extension(name: str, update: FixedExtensionUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE fixed_extensions SET is_checked = ? WHERE name = ?", (1 if update.is_checked else 0, name))
    conn.commit()
    conn.close()
    return {"message": "Updated successfully"}

import re

@app.post("/api/custom-extensions")
def add_custom_extension(ext: CustomExtensionCreate):
    name = ext.name.strip()
    
    if len(name) > 20:
        raise HTTPException(status_code=400, detail="Invalid extension name (max 20 chars)")
    
    if not re.match(r'^[a-zA-Z0-9]+$', name):
        raise HTTPException(status_code=400, detail="Invalid extension name (only English letters and numbers allowed)")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM custom_extensions")
    count = cursor.fetchone()['count']
    
    if count >= 200:
        conn.close()
        raise HTTPException(status_code=400, detail="Maximum number of custom extensions reached (200)")
    
    try:
        cursor.execute("INSERT INTO custom_extensions (name) VALUES (?)", (name,))
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
    
    cursor.execute("DELETE FROM custom_extensions WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    return {"message": "Deleted successfully"}

@app.delete("/api/custom-extensions")
def delete_all_custom_extensions():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM custom_extensions")
    conn.commit()
    conn.close()
    return {"message": "All custom extensions deleted"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
