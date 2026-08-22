"""
Authentication router — handles register, login, logout, and profile endpoints.
JWT tokens are stored in HTTP-only cookies for XSS protection.
"""
from fastapi import APIRouter, Depends
from loguru import logger
from app.schemas.auth import RegisterRequest, LoginRequest
from app.controllers import auth_controller
from app.middleware.auth_middleware import get_current_user, get_cookie_settings
from app.responses import success_response

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register")
async def register(data: RegisterRequest):
    """Register a new user and set JWT cookie."""
    user_data, token = await auth_controller.register(data)
    response = success_response(
        data={"user": user_data},
        message="Registration successful",
        status_code=201
    )
    cookie = get_cookie_settings()
    response.set_cookie(value=token, **cookie)
    logger.info(f"User registered and cookie set: {data.email}")
    return response


@router.post("/login")
async def login(data: LoginRequest):
    """Authenticate user and set JWT cookie."""
    user_data, token = await auth_controller.login(data)
    response = success_response(
        data={"user": user_data},
        message="Login successful"
    )
    cookie = get_cookie_settings()
    response.set_cookie(value=token, **cookie)
    logger.info(f"User logged in and cookie set: {data.email}")
    return response


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get the current authenticated user's profile."""
    user_data = await auth_controller.get_me(current_user["user_id"])
    return success_response(data={"user": user_data}, message="User profile retrieved")


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Clear the JWT cookie to log out."""
    response = success_response(data=None, message="Logged out successfully")
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True
    )
    logger.info(f"User logged out: {current_user['email']}")
    return response
