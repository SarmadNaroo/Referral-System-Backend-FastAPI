from fastapi import FastAPI
from app.core.db import engine, Base
from app.routes import auth, user, client_admin
from app.middlewares.cors import add_cors_middleware
from app.core.config import settings

# Initialize FastAPI application
app = FastAPI(title=settings.PROJECT_NAME)
add_cors_middleware(app)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "ReferralHash Server Running!"}

# Include the routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(client_admin.router, prefix="/client", tags=["client"])
