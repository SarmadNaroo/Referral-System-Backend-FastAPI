from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.schemas.client import ClientCreate
from app.schemas.auth import AuthUserCreate, ShowUserResponse, LoginRequest, ForgotPasswordRequest, VerifyOTPRequest, ResetPasswordRequest
from app.services.auth import create_new_user, login_user, otp_verification, update_password, forgot_password_user
from app.core.db import get_db 
from app.models.user import UserRole 

router = APIRouter()

@router.post("/signup", response_model= ShowUserResponse ,status_code= status.HTTP_201_CREATED)
def create_user( user: AuthUserCreate, db: Session = Depends(get_db)):
    print("Singup Request Received :")
    print(user)
    user = create_new_user( user=user, db=db)
    return {"user": user}

@router.post("/login",status_code=status.HTTP_200_OK)
def login_for_access_token(response: Response,request: LoginRequest, db: Session = Depends(get_db)): 
    user = login_user(response, request, db)
    return user

@router.post("/forget-password" ,status_code=status.HTTP_200_OK)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    response = forgot_password_user(request.email, db)
    return response

@router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(response: Response ,request: VerifyOTPRequest, db: Session = Depends(get_db)):
    response = otp_verification(response, request, db)
    return response

@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = update_password(request, db)
    return {"user": user}

