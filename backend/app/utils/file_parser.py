"""
PDF text extraction using PyMuPDF (fitz).
Handles file reading, text extraction, and basic cleanup.
"""
import fitz  # PyMuPDF
from loguru import logger
from app.exceptions import FileProcessingError


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract all text content from a PDF file.
    Returns cleaned text string.
    Raises FileProcessingError if extraction fails.
    """
    try:
        text_parts = []
        num_pages = 0
        
        with fitz.open(file_path) as doc:
            num_pages = len(doc)
            for page_num in range(num_pages):
                page = doc[page_num]
                page_text = page.get_text("text")
                if page_text:
                    text_parts.append(page_text.strip())

        full_text = "\n\n".join(text_parts)

        if not full_text.strip():
            raise FileProcessingError(
                "Could not extract any text from the PDF. The file may be image-based or corrupt."
            )

        # Basic cleanup: normalize whitespace, remove excessive newlines
        lines = full_text.split("\n")
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        cleaned_text = "\n".join(cleaned_lines)

        logger.info(f"Extracted {len(cleaned_text)} characters from PDF ({num_pages} pages)")
        return cleaned_text

    except FileProcessingError:
        raise
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        raise FileProcessingError(f"Failed to process PDF file: {str(e)}")
