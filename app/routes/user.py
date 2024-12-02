from fastapi import Depends, APIRouter, Response, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/me",status_code=status.HTTP_200_OK)
def get_me(current_user: User=Depends(get_current_user)): 
    return current_user
