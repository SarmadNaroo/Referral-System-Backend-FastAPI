from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status,  Response, Request
from app.models.user import User
from app.models.client import Client
from app.schemas.user import UserCreate
from app.schemas.auth import AuthUserCreate
from app.schemas.client import ClientCreate
from app.utils.security import hash_password
from app.utils.email import send_email, verify_email_body, otp_email_body
from app.utils.auth import generate_otp, create_token, authenticate_user
from app.utils.cookies import set_cookies
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from app.models.user import UserRole


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

        user = User(
            email=user.email,
            password=user.password,
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
