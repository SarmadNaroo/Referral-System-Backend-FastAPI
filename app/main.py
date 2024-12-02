from fastapi import FastAPI
from app.core.db import engine, Base
from app.routes import auth, user

# Initialize FastAPI application
app = FastAPI()

# On startup, log application start
@app.on_event("startup")
async def startup_event():
    print("Application has started!")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "ReferralHash Server Running!"}

# Include the auth router
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
