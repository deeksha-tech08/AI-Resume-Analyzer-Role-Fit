"""Pydantic models for Resume documents in MongoDB."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ResumeInDB(BaseModel):
    """Represents a resume document as stored in MongoDB."""
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    filename: str
    file_path: str
    extracted_text: str = ""
    extracted_skills: list[str] = []
    ats_score: float = 0.0
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
