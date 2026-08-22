"""
Resume router — upload, retrieve latest, and retrieve by ID.
All endpoints are protected (require JWT authentication).
"""
from fastapi import APIRouter, Depends, UploadFile, File
from loguru import logger
from app.controllers import resume_controller
from app.middleware.auth_middleware import get_current_user
from app.utils.validators import validate_resume_file
from app.responses import success_response

router = APIRouter(prefix="/api/resume", tags=["Resume"])


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a PDF resume, extract text, detect skills, and calculate ATS score.
    File is saved to uploads/{user_id}/{resume_id}/{filename}.
    """
    # Validate the uploaded file
    await validate_resume_file(file)

    # Import spacy_model from main module
    from app.main import spacy_model

    result = await resume_controller.upload_resume(
        file=file,
        user_id=current_user["user_id"],
        spacy_model=spacy_model
    )

    logger.info(f"Resume uploaded successfully: {result['filename']} (ATS: {result['ats_score']}%)")
    return success_response(
        data=result,
        message=f"Resume uploaded and analyzed. ATS Score: {result['ats_score']}%",
        status_code=201
    )


@router.get("/latest")
async def get_latest_resume(current_user: dict = Depends(get_current_user)):
    """Get the most recently uploaded resume for the current user."""
    result = await resume_controller.get_latest(current_user["user_id"])
    return success_response(data=result, message="Latest resume retrieved")


@router.get("/{resume_id}")
async def get_resume(
    resume_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific resume by ID."""
    result = await resume_controller.get_by_id(resume_id, current_user["user_id"])
    return success_response(data=result, message="Resume retrieved")
