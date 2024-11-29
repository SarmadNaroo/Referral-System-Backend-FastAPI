from fastapi import Response
from datetime import datetime, timedelta, timezone

def set_cookies(response: Response, key: str, token: str, token_expire_minutes):
    response.set_cookie(
        key=key,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        expires=datetime.now(timezone.utc) + timedelta(minutes=token_expire_minutes)
    ) 