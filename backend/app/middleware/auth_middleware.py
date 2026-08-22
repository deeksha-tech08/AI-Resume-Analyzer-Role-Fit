"""
JWT authentication middleware using HTTP-only cookies.
Provides token creation, verification, and a FastAPI dependency for protected routes.
"""
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Request, Depends
from loguru import logger
from app.config import settings
from app.exceptions import AuthenticationError

ALGORITHM = "HS256"


def create_access_token(user_id: str, email: str) -> str:
    """Create a JWT access token with user_id and email claims."""
    expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_EXPIRY_DAYS)
    payload = {
        "sub": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)
    logger.debug(f"Created JWT token for user: {user_id}")
    return token


def verify_token(token: str) -> dict:
    """Verify and decode a JWT token. Returns the payload dict."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        if user_id is None or email is None:
            raise AuthenticationError("Invalid token: missing claims")
        return {"user_id": user_id, "email": email}
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise AuthenticationError("Invalid or expired token")


async def get_current_user(request: Request) -> dict:
    """
    FastAPI dependency that extracts and verifies the JWT from HTTP-only cookies.
    Returns a dict with user_id and email.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise AuthenticationError("Not authenticated. Please log in.")
    return verify_token(token)


def get_cookie_settings() -> dict:
    """Return cookie configuration based on environment."""
    is_production = settings.ENVIRONMENT == "production"
    return {
        "key": "access_token",
        "httponly": True,
        "secure": is_production,
        "samesite": "lax" if not is_production else "none",
        "max_age": settings.JWT_EXPIRY_DAYS * 24 * 60 * 60,
        "path": "/"
    }
