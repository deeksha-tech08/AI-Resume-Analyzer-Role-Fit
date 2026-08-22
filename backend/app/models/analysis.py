"""Pydantic models for Analysis documents in MongoDB."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RoleScore(BaseModel):
    """Score breakdown for a single role match."""
    role: str
    fit_score: float = 0.0
    core_skill_coverage: float = 0.0
    matched_skills: list[str] = []
    missing_core_skills: list[str] = []
    missing_optional_skills: list[str] = []


class SectionStrength(BaseModel):
    """Strength analysis for a single resume section."""
    section: str
    score: float = 0.0
    label: str = "Weak"  # Strong / Good / Average / Weak
    detected_strengths: list[str] = []
    tip: Optional[str] = None  # Improvement tip if score < 60%


class AnalysisInDB(BaseModel):
    """Represents a full analysis document as stored in MongoDB."""
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    resume_id: str
    selected_roles: list[str] = []
    role_scores: list[RoleScore] = []
    best_fit_role: str = ""
    ats_score: float = 0.0
    explanation: str = ""
    suggestions: list[str] = []
    section_strength: list[SectionStrength] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
