from fastapi import FastAPI
from app.core.db import engine, Base
from app.routes import auth

# Initialize FastAPI application
app = FastAPI()

# On startup, log application start
@app.on_event("startup")
async def startup_event():
    print("Application has started!")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "FastAPI with SQLAlchemy and Alembic is working!"}

# Include the auth router
app.include_router(auth.router, prefix="/auth", tags=["auth"])
