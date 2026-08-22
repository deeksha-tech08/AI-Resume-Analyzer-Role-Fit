"""Pydantic schemas for analysis API requests and responses."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AnalysisRequest(BaseModel):
    """Schema for running a new analysis."""
    resume_id: str = Field(..., description="ID of the uploaded resume to analyze")
    selected_roles: list[str] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="1-50 roles to analyze against"
    )


class RoleScoreResponse(BaseModel):
    """Schema for a single role's score breakdown."""
    role: str
    fit_score: float
    core_skill_coverage: float
    matched_skills: list[str]
    missing_core_skills: list[str]
    missing_optional_skills: list[str]


class SectionStrengthResponse(BaseModel):
    """Schema for a single section's strength analysis."""
    section: str
    score: float
    label: str
    detected_strengths: list[str]
    tip: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Schema for full analysis result."""
    id: str
    resume_id: str
    selected_roles: list[str]
    role_scores: list[RoleScoreResponse]
    best_fit_role: str
    ats_score: float
    explanation: str
    suggestions: list[str]
    section_strength: list[SectionStrengthResponse]
    created_at: datetime


class AnalysisHistoryItem(BaseModel):
    """Schema for analysis history list item."""
    id: str
    resume_filename: str
    selected_roles: list[str]
    best_fit_role: str
    best_fit_score: float
    ats_score: float
    created_at: datetime
