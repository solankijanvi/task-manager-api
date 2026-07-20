from fastapi import FastAPI
from sqlalchemy import text

from db.database import engine
from db import models

from app.routers import users
from app.routers import users, tasks



models.Base.metadata.create_all(bind = engine)

app = FastAPI(
    title = "Task Management API",
    version = "1.0.0"
)


app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def home():
    return {
        "message": "Welcome to Task Managemnet API"
        
    }
    
@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            
        return {
            "database": "Connected",
            "status": "Healthy"
        }
    except Exception as e:
        return {
            "database": "Disconnected",
            "error": str(e)
        }   