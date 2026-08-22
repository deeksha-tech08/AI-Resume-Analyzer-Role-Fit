"""
Auth controller — thin layer between router and service.
Handles request processing and delegates to auth_service.
"""
from loguru import logger
from app.schemas.auth import RegisterRequest, LoginRequest, UserResponse
from app.services import auth_service


async def register(data: RegisterRequest) -> tuple[dict, str]:
    """
    Process registration request.
    Returns (user_data_dict, jwt_token).
    """
    logger.info(f"Processing registration for: {data.email}")
    user_response, token = await auth_service.register_user(data)
    return user_response.model_dump(), token


async def login(data: LoginRequest) -> tuple[dict, str]:
    """
    Process login request.
    Returns (user_data_dict, jwt_token).
    """
    logger.info(f"Processing login for: {data.email}")
    user_response, token = await auth_service.login_user(data)
    return user_response.model_dump(), token


async def get_me(user_id: str) -> dict:
    """
    Get current user profile by ID.
    Returns user_data_dict.
    """
    user_response = await auth_service.get_user_by_id(user_id)
    return user_response.model_dump()
