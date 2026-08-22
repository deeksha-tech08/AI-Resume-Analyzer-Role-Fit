"""
Analysis controller — delegates to analysis_service.
"""
from loguru import logger
from app.services import analysis_service


async def run_analysis(resume_id: str, selected_roles: list[str], user_id: str, spacy_model=None) -> dict:
    """Run full analysis pipeline."""
    logger.info(f"Controller: running analysis for resume {resume_id}")
    return await analysis_service.run_analysis(resume_id, selected_roles, user_id, spacy_model)


async def get_history(user_id: str, limit: int = 10, offset: int = 0) -> tuple[list[dict], int]:
    """Get paginated analysis history."""
    return await analysis_service.get_analysis_history(user_id, limit, offset)


async def get_by_id(analysis_id: str, user_id: str) -> dict:
    """Get specific analysis by ID."""
    return await analysis_service.get_analysis_by_id(analysis_id, user_id)
