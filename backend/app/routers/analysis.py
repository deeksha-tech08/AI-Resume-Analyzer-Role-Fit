"""
Analysis router — run analysis, get history (paginated), get details.
All endpoints are protected (require JWT authentication).
"""
from fastapi import APIRouter, Depends, Query
from loguru import logger
from app.schemas.analysis import AnalysisRequest
from app.controllers import analysis_controller
from app.middleware.auth_middleware import get_current_user
from app.responses import success_response, paginated_response

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


@router.post("/run")
async def run_analysis(
    data: AnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Run full analysis: role matching + section analysis + OpenAI insights.
    Accepts resume_id and 1-4 selected roles.
    """
    from app.main import spacy_model

    result = await analysis_controller.run_analysis(
        resume_id=data.resume_id,
        selected_roles=data.selected_roles,
        user_id=current_user["user_id"],
        spacy_model=spacy_model
    )

    logger.info(f"Analysis complete: best fit = {result['best_fit_role']} ({result['ats_score']}% ATS)")
    return success_response(
        data=result,
        message=f"Analysis complete. Best fit: {result['best_fit_role']}",
        status_code=201
    )


@router.get("/history")
async def get_history(
    limit: int = Query(default=10, ge=1, le=50, description="Items per page"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
    current_user: dict = Depends(get_current_user)
):
    """Get paginated analysis history for the current user."""
    history, total = await analysis_controller.get_history(
        user_id=current_user["user_id"],
        limit=limit,
        offset=offset
    )
    return paginated_response(
        data=history,
        total=total,
        limit=limit,
        offset=offset,
        message="Analysis history retrieved"
    )


@router.get("/{analysis_id}")
async def get_analysis(
    analysis_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get specific analysis details by ID."""
    result = await analysis_controller.get_by_id(analysis_id, current_user["user_id"])
    return success_response(data=result, message="Analysis details retrieved")
