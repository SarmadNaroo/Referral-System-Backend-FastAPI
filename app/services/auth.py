from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status,  Response, Request, Depends
from pydantic import EmailStr
from app.models.user import User
from app.models.client import Client
from app.schemas.user import UserCreate
from app.schemas.auth import AuthUserCreate, CurrentUserResponse
from app.utils.email import send_email, verify_email_body, otp_email_body
from app.utils.auth import generate_otp, create_token, authenticate_user
from app.utils.cookies import set_cookies
from app.core.config import settings
from app.utils.user import get_user
from app.core.db import get_db
from datetime import datetime, timedelta, timezone
from app.models.user import UserRole
from app.utils.hasher import Hasher
from jose import JWTError, jwt

def create_new_user(user: AuthUserCreate, db: Session):
    try:
        if not user.email or not user.password or not user.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email, password, and name are required"
            )
        
        existing_user = db.query(User).filter(User.email == user.email.lower()).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        otp = generate_otp()
        otp_expiration_time = datetime.now(timezone.utc) + timedelta(minutes=5)
        
        hashed_password = Hasher.hash_password(user.password)

        user = User(
            email=user.email,
            password=hashed_password,
            name=user.name,
            otp=otp,
            role=UserRole.client_admin,
            otp_expires_at=otp_expiration_time
        )

        try:
            db.add(user)
            db.commit()
            db.refresh(user)
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database Error"+str(e)
            )

        subject = "Verify Your Email"
        body = verify_email_body(user.name, otp)
        send_email(to_email=user.email, subject=subject, body=body)

        return user
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error created while creating the user"
        )

def otp_verification(response: Response, request: Request ,db: Session):
    try:
        email = request.email.lower()
        otp = request.otp
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.otp != otp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP"
            )
        
        if user.otp_expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired"
            )
        
        user.otp = None
        user.otp_expires_at = None
        user.is_email_verified = True
        db.commit()
        db.refresh(user)

        access_token = create_token(
            data={"sub": user.email},
            token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_token = create_token(
            data={"sub": user.email},
            token_expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

        set_cookies(response, key="access_token", token=access_token, token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        set_cookies(response, key="refresh_token", token=refresh_token, token_expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)


        return {"message": "OTP verified successfully"}
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while verifying OTP"
        )
        
def login_user(response: Response, request: Request, db: Session):
    try:
        user = authenticate_user(request.email, request.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        if not user.is_email_verified:
            opt = generate_otp()
            otp_expiration_time = datetime.now(timezone.utc) + timedelta(minutes=5)
            user.otp = opt
            user.otp_expires_at = otp_expiration_time

            db.commit()
            db.refresh(user)
            subject = "Verify Your Email"
            body = verify_email_body(user.name, opt)
            send_email(to_email=user.email, subject=subject, body=body)

            return {"message": "Otp sent to your email. Please verify"} 
    
        access_token = create_token(
            data={"sub": user.email},
            token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_token = create_token(
            data={"sub": user.email},
            token_expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        set_cookies(response, key="access_token", token=access_token, token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        set_cookies(response, key="refresh_token", token=refresh_token, token_expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        return {"user": {"id": user.id, "name": user.name, "email": user.email, "is_email_verified": user.is_email_verified}}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )
    
def forgot_password_user(email: str, db: Session):
    try:
        user = db.query(User).filter(User.email == email.lower()).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        otp = generate_otp()
        otp_expiration_time = datetime.now(timezone.utc) + timedelta(minutes=5)

        user.otp = otp
        user.otp_expires_at = otp_expiration_time

        db.commit()
        db.refresh(user)

        subject = "Your OTP for Password Reset"
        body = otp_email_body(user.name, otp)
        send_email(to_email=email, subject=subject, body=body)

        return {"message": "OTP sent successfully"}
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating OTP"
        )

def update_password(request: Request, db: Session):
    try:
        user = db.query(User).filter(User.email == request.email.lower()).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if not request.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is required"
            )
        user.password = Hasher.hash_password(request.password)
        db.commit()

        return {"message": "Password updated successfully"}
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating password"
        )

