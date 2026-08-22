"""Pydantic models for User documents in MongoDB."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserInDB(BaseModel):
    """Represents a user document as stored in MongoDB."""
    id: Optional[str] = Field(None, alias="_id")
    full_name: str
    email: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
