from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.core.constants import origins

def add_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins, 
        allow_credentials=True,                  
        allow_methods=["*"],
        allow_headers=["*"],
    )