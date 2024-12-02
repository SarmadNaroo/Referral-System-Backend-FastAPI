from app.core.config import settings
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.utils.user import get_user
from app.utils.cookies import set_cookies
from typing import Optional
from datetime import datetime, timedelta, timezone
from fastapi import Response, Request, Depends, HTTPException, status
from app.core.db import get_db
from jose import JWTError, jwt
from app.schemas.auth import CurrentUserResponse
import random
import string
from app.utils.hasher import Hasher

def create_token(data: dict, token_expire_minutes: int ,expires_delta: Optional[timedelta] = None ):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def authenticate_user(email: EmailStr, password: str, db: Session):
    user = get_user(email=email, db=db)
    print("user email", user.email)
    print("user password", user.password)
    print("password", password)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        print("password not matched")
        return False
    return user

async def get_current_user(request: Request, response: Response, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials"
    )
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    email = None
    if access_token:
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: EmailStr = payload.get("sub")
        except JWTError:
            pass  
    if not email and refresh_token:
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: EmailStr = payload.get("sub")
            if email:
                new_access_token = create_token(
                    data={"sub": email},
                    token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
                )
                set_cookies(response, key="access_token", token=new_access_token, token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        except JWTError:
            raise credentials_exception

    if not email:
        raise credentials_exception

    user = get_user(email, db)
    if not user:
        raise credentials_exception
    
    return CurrentUserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_email_verified=user.is_email_verified
    )

def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))
    


