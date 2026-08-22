"""Pydantic schemas for authentication API requests and responses."""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class RegisterRequest(BaseModel):
    """Schema for user registration request."""
    full_name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=128, description="Password (min 8 characters)")


class LoginRequest(BaseModel):
    """Schema for user login request."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserResponse(BaseModel):
    """Schema for user data in API responses."""
    id: str
    full_name: str
    email: str
    created_at: datetime


class AuthResponse(BaseModel):
    """Schema for authentication API response data."""
    user: UserResponse
    message: str = "Success"
