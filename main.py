from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app import models


models.Base.metadata.create_all(bind = engine)

app = FastAPI(
    title = "Task Management API",
    version = "1.0.0"
)

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