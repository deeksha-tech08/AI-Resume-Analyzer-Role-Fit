"""
Resume service — handles file storage, text extraction, skill extraction, and ATS scoring.
All database operations use Motor async driver.
"""
import os
from datetime import datetime, timezone
from bson import ObjectId
from loguru import logger
from fastapi import UploadFile

from app.config import settings
from app.database.mongodb import get_collection
from app.utils.file_parser import extract_text_from_pdf
from app.ai.skill_extractor import extract_skills
from app.ai.ats_analyzer import calculate_ats_score
from app.exceptions import NotFoundError, FileProcessingError, DatabaseError


async def upload_and_analyze_resume(
    file: UploadFile,
    user_id: str,
    spacy_model=None
) -> dict:
    """
    Process a resume upload:
    1. Save PDF to disk at uploads/{user_id}/{resume_id}/{filename}
    2. Extract text using PyMuPDF
    3. Extract skills using spaCy + curated dictionary
    4. Calculate ATS score
    5. Store everything in MongoDB

    Returns: dict with resume data including extracted skills and ATS score
    """
    resumes = get_collection("resumes")
    resume_id = str(ObjectId())

    # Create directory structure: uploads/{user_id}/{resume_id}/
    upload_dir = os.path.join(settings.UPLOAD_DIR, user_id, resume_id)
    os.makedirs(upload_dir, exist_ok=True)

    # Save file to disk
    safe_filename = file.filename.replace(" ", "_")
    file_path = os.path.join(upload_dir, safe_filename)

    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        logger.info(f"Resume saved: {file_path} ({len(content)} bytes)")
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise FileProcessingError("Failed to save uploaded file")

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)

    # Extract skills using spaCy + dictionary
    extracted_skills = extract_skills(extracted_text, nlp=spacy_model)

    # Calculate ATS score
    ats_result = calculate_ats_score(extracted_text, extracted_skills)

    # Store in MongoDB
    now = datetime.now(timezone.utc)
    resume_doc = {
        "_id": ObjectId(resume_id),
        "user_id": user_id,
        "filename": file.filename,
        "file_path": file_path,
        "extracted_text": extracted_text,
        "extracted_skills": extracted_skills,
        "ats_score": ats_result["ats_score"],
        "uploaded_at": now,
    }

    try:
        await resumes.insert_one(resume_doc)
        logger.info(f"Resume stored in DB: {resume_id} for user {user_id}")
    except Exception as e:
        logger.error(f"Database error storing resume: {e}")
        # Clean up file on DB failure
        if os.path.exists(file_path):
            os.remove(file_path)
        raise DatabaseError("Failed to store resume data")

    return {
        "id": resume_id,
        "filename": file.filename,
        "extracted_text": extracted_text,
        "extracted_skills": extracted_skills,
        "ats_score": ats_result["ats_score"],
        "ats_breakdown": ats_result["breakdown"],
        "detected_sections": ats_result["detected_sections"],
        "uploaded_at": now.isoformat(),
    }


async def get_latest_resume(user_id: str) -> dict:
    """Get the most recently uploaded resume for a user."""
    resumes = get_collection("resumes")
    resume_doc = await resumes.find_one(
        {"user_id": user_id},
        sort=[("uploaded_at", -1)]
    )
    if not resume_doc:
        raise NotFoundError("No resume found. Please upload a resume first.")

    return _format_resume_response(resume_doc)


async def get_resume_by_id(resume_id: str, user_id: str) -> dict:
    """Get a specific resume by ID, ensuring it belongs to the user."""
    resumes = get_collection("resumes")

    try:
        resume_doc = await resumes.find_one({
            "_id": ObjectId(resume_id),
            "user_id": user_id
        })
    except Exception:
        raise NotFoundError("Invalid resume ID")

    if not resume_doc:
        raise NotFoundError("Resume not found")

    return _format_resume_response(resume_doc)


def _format_resume_response(doc: dict) -> dict:
    """Format a MongoDB resume document for API response."""
    return {
        "id": str(doc["_id"]),
        "filename": doc["filename"],
        "extracted_text": doc.get("extracted_text", ""),
        "extracted_skills": doc.get("extracted_skills", []),
        "ats_score": doc.get("ats_score", 0),
        "uploaded_at": doc["uploaded_at"].isoformat() if doc.get("uploaded_at") else None,
    }
