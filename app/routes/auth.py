from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.schemas.client import ClientCreate
from app.schemas.auth import AuthUserCreate, ShowUserResponse, LoginRequest, ForgotPasswordRequest, VerifyOTPRequest, ResetPasswordRequest
from app.services.auth import create_new_user
from app.core.db import get_db 
from app.models.user import UserRole 

router = APIRouter()

@router.post("/signup", response_model= ShowUserResponse ,status_code= status.HTTP_201_CREATED)
def create_user( user: AuthUserCreate, db: Session = Depends(get_db)):
    print("Singup Request Received :")
    print(user)
    user = create_new_user( user=user, db=db)
    return {"user": user}

