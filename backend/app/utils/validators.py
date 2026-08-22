"""
File validation utilities for upload endpoints.
Validates file type, size, and integrity.
"""
from fastapi import UploadFile
from loguru import logger
from app.config import settings
from app.exceptions import ValidationError

ALLOWED_CONTENT_TYPES = [
    "application/pdf",
]

ALLOWED_EXTENSIONS = [".pdf"]


async def validate_resume_file(file: UploadFile) -> None:
    """
    Validate an uploaded resume file.
    Checks: file presence, extension, content type, size, and PDF header.
    Raises ValidationError on any failure.
    """
    # Check file exists
    if not file or not file.filename:
        raise ValidationError("No file uploaded")

    # Check extension
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise ValidationError("Only PDF files are accepted. Please upload a .pdf file.")

    # Check content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise ValidationError(
            f"Invalid file type: {file.content_type}. Only PDF files are accepted."
        )

    # Check file size by reading content
    content = await file.read()
    file_size = len(content)
    await file.seek(0)  # Reset file pointer for later use

    if file_size == 0:
        raise ValidationError("The uploaded file is empty.")

    if file_size > settings.MAX_FILE_SIZE:
        max_mb = settings.MAX_FILE_SIZE / (1024 * 1024)
        raise ValidationError(
            f"File size ({file_size / (1024*1024):.1f}MB) exceeds maximum allowed size ({max_mb:.0f}MB)."
        )

    # Basic PDF header check (PDF magic bytes)
    if not content[:5] == b"%PDF-":
        raise ValidationError("The file does not appear to be a valid PDF document.")

    logger.debug(f"File validated: {file.filename} ({file_size / 1024:.1f}KB)")
