"""
Authentication service handling user registration, login, and profile retrieval.
All database operations use Motor async driver.
"""
from datetime import datetime, timezone
from bson import ObjectId
import bcrypt
from loguru import logger
from app.database.mongodb import get_collection
from app.schemas.auth import RegisterRequest, LoginRequest, UserResponse
from app.middleware.auth_middleware import create_access_token
from app.exceptions import AuthenticationError, ValidationError, DatabaseError

def _hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False


def _user_doc_to_response(user_doc: dict) -> UserResponse:
    """Convert a MongoDB user document to a UserResponse schema."""
    return UserResponse(
        id=str(user_doc["_id"]),
        full_name=user_doc["full_name"],
        email=user_doc["email"],
        created_at=user_doc["created_at"]
    )


async def register_user(data: RegisterRequest) -> tuple[UserResponse, str]:
    """
    Register a new user.
    Returns (UserResponse, JWT token).
    Raises ValidationError if email already exists.
    """
    users = get_collection("users")

    # Check for duplicate email
    existing = await users.find_one({"email": data.email.lower()})
    if existing:
        logger.warning(f"Registration attempt with existing email: {data.email}")
        raise ValidationError("An account with this email already exists")

    # Create user document
    now = datetime.now(timezone.utc)
    user_doc = {
        "full_name": data.full_name.strip(),
        "email": data.email.lower().strip(),
        "password_hash": _hash_password(data.password),
        "created_at": now,
        "updated_at": now
    }

    try:
        result = await users.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        logger.info(f"New user registered: {data.email}")
    except Exception as e:
        logger.error(f"Database error during registration: {e}")
        raise DatabaseError("Failed to create account")

    user_response = _user_doc_to_response(user_doc)
    token = create_access_token(str(result.inserted_id), data.email.lower())
    return user_response, token


async def login_user(data: LoginRequest) -> tuple[UserResponse, str]:
    """
    Authenticate a user with email and password.
    Returns (UserResponse, JWT token).
    Raises AuthenticationError if credentials are invalid.
    """
    users = get_collection("users")

    user_doc = await users.find_one({"email": data.email.lower()})
    if not user_doc:
        logger.warning(f"Login attempt with non-existent email: {data.email}")
        raise AuthenticationError("Invalid email or password")

    if not _verify_password(data.password, user_doc["password_hash"]):
        logger.warning(f"Login attempt with wrong password for: {data.email}")
        raise AuthenticationError("Invalid email or password")

    logger.info(f"User logged in: {data.email}")
    user_response = _user_doc_to_response(user_doc)
    token = create_access_token(str(user_doc["_id"]), data.email.lower())
    return user_response, token


async def get_user_by_id(user_id: str) -> UserResponse:
    """
    Retrieve a user by their MongoDB ObjectId.
    Raises AuthenticationError if not found.
    """
    users = get_collection("users")

    try:
        user_doc = await users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise AuthenticationError("Invalid user ID")

    if not user_doc:
        raise AuthenticationError("User not found")

    return _user_doc_to_response(user_doc)
