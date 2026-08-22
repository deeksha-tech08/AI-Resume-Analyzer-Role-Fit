"""
Resume controller — delegates to resume_service.
"""
from fastapi import UploadFile
from loguru import logger
from app.services import resume_service


async def upload_resume(file: UploadFile, user_id: str, spacy_model=None) -> dict:
    """Process resume upload and return analysis data."""
    logger.info(f"Controller: processing resume upload for user {user_id}")
    return await resume_service.upload_and_analyze_resume(file, user_id, spacy_model)


async def get_latest(user_id: str) -> dict:
    """Get latest resume for user."""
    return await resume_service.get_latest_resume(user_id)


async def get_by_id(resume_id: str, user_id: str) -> dict:
    """Get specific resume by ID."""
    return await resume_service.get_resume_by_id(resume_id, user_id)
