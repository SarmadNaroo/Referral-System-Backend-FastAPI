# /app/middlewares/auth_middleware.py
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from core import settings

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        access_token = request.cookies.get("access_token")
        if request.url.path == "/auth/login" or request.url.path == "/auth/signup":
            response = await call_next(request)
            return response
        print(access_token, "access_token")
        if not access_token:
            raise HTTPException(status_code=401, detail="Access token missing")
    
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            username = payload.get("sub")
            if not username:
                raise HTTPException(status_code=401, detail="Invalid token")
        
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        response = await call_next(request)
        return response

