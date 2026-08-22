"""Pydantic schemas for resume API requests and responses."""
from pydantic import BaseModel
from datetime import datetime


class ResumeResponse(BaseModel):
    """Schema for resume summary in API responses."""
    id: str
    filename: str
    extracted_skills: list[str]
    ats_score: float
    uploaded_at: datetime


class ResumeDetailResponse(BaseModel):
    """Schema for full resume detail in API responses."""
    id: str
    filename: str
    extracted_text: str
    extracted_skills: list[str]
    ats_score: float
    uploaded_at: datetime
