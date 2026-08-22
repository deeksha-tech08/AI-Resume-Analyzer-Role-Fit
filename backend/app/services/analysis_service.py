"""
Analysis service — orchestrates the full analysis pipeline:
1. Retrieve resume from DB
2. Run role matching (deterministic)
3. Run section analysis (deterministic)
4. Call OpenAI for explanations/suggestions (generative)
5. Store results in MongoDB
"""
from datetime import datetime, timezone
from bson import ObjectId
from loguru import logger

from app.database.mongodb import get_collection
from app.ai.role_matcher import calculate_role_scores, get_best_fit_role
from app.ai.section_analyzer import analyze_sections
from app.ai.gemini_analyzer import generate_analysis_insights
from app.ai.role_profiles import VALID_ROLES
from app.exceptions import NotFoundError, ValidationError, DatabaseError


async def run_analysis(
    resume_id: str,
    selected_roles: list[str],
    user_id: str,
    spacy_model=None
) -> dict:
    """
    Run the complete analysis pipeline for a resume against selected roles.

    Pipeline:
    1. Validate roles → 2. Fetch resume → 3. Role matching →
    4. Section analysis → 5. OpenAI insights → 6. Store in DB

    Returns: Full analysis result dict
    """
    # Validate selected roles
    for role in selected_roles:
        if role not in VALID_ROLES:
            raise ValidationError(
                f"Invalid role: '{role}'. Valid roles: {', '.join(VALID_ROLES)}"
            )

    # Fetch resume from DB
    resumes = get_collection("resumes")
    try:
        resume_doc = await resumes.find_one({
            "_id": ObjectId(resume_id),
            "user_id": user_id
        })
    except Exception:
        raise NotFoundError("Invalid resume ID")

    if not resume_doc:
        raise NotFoundError("Resume not found. Please upload a resume first.")

    extracted_text = resume_doc.get("extracted_text", "")
    extracted_skills = resume_doc.get("extracted_skills", [])
    ats_score = resume_doc.get("ats_score", 0)

    if not extracted_text:
        raise ValidationError("Resume has no extracted text. Please re-upload.")

    logger.info(f"Running analysis for resume {resume_id} against roles: {selected_roles}")

    # Step 1: Role matching (deterministic)
    role_scores = calculate_role_scores(extracted_skills, selected_roles)
    best_fit_role = get_best_fit_role(role_scores)

    # Step 2: Section analysis (deterministic, rule-based)
    section_strength = analyze_sections(extracted_text, extracted_skills, nlp=spacy_model)

    # Step 3: OpenAI insights (generative — ONE call)
    best_role_data = role_scores[0] if role_scores else {}
    weak_sections = [s for s in section_strength if s["score"] < 60]

    ai_insights = await generate_analysis_insights(
        best_fit_role=best_fit_role,
        fit_score=best_role_data.get("fit_score", 0),
        matched_skills=best_role_data.get("matched_skills", []),
        missing_core_skills=best_role_data.get("missing_core_skills", []),
        missing_optional_skills=best_role_data.get("missing_optional_skills", []),
        ats_score=ats_score,
        weak_sections=weak_sections,
    )

    # Apply section tips from OpenAI to weak sections
    section_tips = ai_insights.get("section_tips", {})
    for section in section_strength:
        if section["section"] in section_tips:
            section["tip"] = section_tips[section["section"]]

    # Step 4: Store analysis in MongoDB
    now = datetime.now(timezone.utc)
    analysis_doc = {
        "user_id": user_id,
        "resume_id": resume_id,
        "selected_roles": selected_roles,
        "role_scores": role_scores,
        "best_fit_role": best_fit_role,
        "ats_score": ats_score,
        "explanation": ai_insights["explanation"],
        "suggestions": ai_insights["suggestions"],
        "section_strength": section_strength,
        "created_at": now,
        "updated_at": now,
    }

    analyses = get_collection("analyses")
    try:
        result = await analyses.insert_one(analysis_doc)
        analysis_id = str(result.inserted_id)
        logger.info(f"Analysis stored: {analysis_id} (best fit: {best_fit_role})")
    except Exception as e:
        logger.error(f"Failed to store analysis: {e}")
        raise DatabaseError("Failed to save analysis results")

    return {
        "id": analysis_id,
        "resume_id": resume_id,
        "selected_roles": selected_roles,
        "role_scores": role_scores,
        "best_fit_role": best_fit_role,
        "ats_score": ats_score,
        "explanation": ai_insights["explanation"],
        "suggestions": ai_insights["suggestions"],
        "section_strength": section_strength,
        "created_at": now.isoformat(),
    }


async def get_analysis_history(
    user_id: str,
    limit: int = 10,
    offset: int = 0
) -> tuple[list[dict], int]:
    """
    Get paginated analysis history for a user.
    Returns: (list of history items, total count)
    """
    analyses = get_collection("analyses")
    resumes = get_collection("resumes")

    # Get total count
    total = await analyses.count_documents({"user_id": user_id})

    # Fetch paginated results
    cursor = analyses.find(
        {"user_id": user_id},
        sort=[("created_at", -1)],
        skip=offset,
        limit=limit
    )

    history = []
    async for doc in cursor:
        # Get resume filename
        resume_filename = "Unknown"
        try:
            resume_doc = await resumes.find_one({"_id": ObjectId(doc["resume_id"])})
            if resume_doc:
                resume_filename = resume_doc.get("filename", "Unknown")
        except Exception:
            pass

        # Get best fit score
        best_fit_score = 0
        for rs in doc.get("role_scores", []):
            if rs["role"] == doc.get("best_fit_role"):
                best_fit_score = rs["fit_score"]
                break

        history.append({
            "id": str(doc["_id"]),
            "resume_filename": resume_filename,
            "selected_roles": doc.get("selected_roles", []),
            "best_fit_role": doc.get("best_fit_role", ""),
            "best_fit_score": best_fit_score,
            "ats_score": doc.get("ats_score", 0),
            "created_at": doc["created_at"].isoformat() if doc.get("created_at") else None,
        })

    return history, total


async def get_analysis_by_id(analysis_id: str, user_id: str) -> dict:
    """Get a specific analysis by ID, ensuring it belongs to the user."""
    analyses = get_collection("analyses")

    try:
        doc = await analyses.find_one({
            "_id": ObjectId(analysis_id),
            "user_id": user_id
        })
    except Exception:
        raise NotFoundError("Invalid analysis ID")

    if not doc:
        raise NotFoundError("Analysis not found")

    return {
        "id": str(doc["_id"]),
        "resume_id": doc["resume_id"],
        "selected_roles": doc.get("selected_roles", []),
        "role_scores": doc.get("role_scores", []),
        "best_fit_role": doc.get("best_fit_role", ""),
        "ats_score": doc.get("ats_score", 0),
        "explanation": doc.get("explanation", ""),
        "suggestions": doc.get("suggestions", []),
        "section_strength": doc.get("section_strength", []),
        "created_at": doc["created_at"].isoformat() if doc.get("created_at") else None,
    }
