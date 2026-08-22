"""
Skill extraction using spaCy NLP pipeline + curated skill dictionary.
Uses tokenization, phrase matching, and normalization for robust skill detection.

Key design decisions:
- spaCy's default NER doesn't recognize technical skills, so we use
  a curated dictionary as the primary mechanism
- spaCy provides tokenization, lemmatization, and phrase matching
- All skills are normalized to canonical forms (ReactJS → React)
- Aliases are handled (JS → JavaScript, ML → Machine Learning)
"""
import re
from loguru import logger
from app.utils.skill_dictionary import (
    SKILL_ALIASES,
    MULTI_WORD_SKILLS,
    normalize_skill,
    CANONICAL_SKILLS,
)


def extract_skills(text: str, nlp=None) -> list[str]:
    """
    Extract technical skills from resume text using spaCy + curated dictionary.

    Process:
    1. Multi-word phrase matching (greedy, longest match first)
    2. Single-token matching against skill aliases
    3. spaCy NLP token-level matching for context-aware extraction
    4. Deduplication and normalization

    Args:
        text: Raw resume text
        nlp: Loaded spaCy model (en_core_web_sm)

    Returns:
        List of unique canonical skill names, sorted alphabetically
    """
    if not text or not text.strip():
        return []

    found_skills: set[str] = set()
    text_lower = text.lower()

    # --- Phase 1: Multi-word phrase matching (greedy) ---
    # Check longest phrases first to avoid partial matches
    for phrase in MULTI_WORD_SKILLS:
        if phrase in text_lower:
            canonical = normalize_skill(phrase)
            if canonical:
                found_skills.add(canonical)
                logger.debug(f"Multi-word match: '{phrase}' → '{canonical}'")

    # --- Phase 2: Single-word token matching ---
    # Split text into tokens and check each against aliases
    # Use regex to split on non-alphanumeric chars but preserve dots/hashes/plusses
    tokens = re.findall(r'[a-zA-Z0-9#+.]+', text)
    for token in tokens:
        canonical = normalize_skill(token)
        if canonical:
            found_skills.add(canonical)

    # --- Phase 3: spaCy NLP processing (if model available) ---
    if nlp is not None:
        try:
            # Process with spaCy for better tokenization
            doc = nlp(text[:100000])  # Limit text size for performance

            # Check individual tokens
            for token in doc:
                if token.is_alpha and len(token.text) > 1:
                    canonical = normalize_skill(token.text)
                    if canonical:
                        found_skills.add(canonical)

                    # Also check lemma
                    canonical = normalize_skill(token.lemma_)
                    if canonical:
                        found_skills.add(canonical)

            # Check noun chunks for multi-word technical terms
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.strip()
                canonical = normalize_skill(chunk_text)
                if canonical:
                    found_skills.add(canonical)

        except Exception as e:
            logger.warning(f"spaCy processing error (falling back to regex): {e}")

    # --- Phase 4: Context pattern matching ---
    # Look for skills mentioned in common resume patterns
    skill_patterns = [
        r'(?:proficient|experienced|skilled|expertise|knowledge)\s+(?:in|with|of)\s+([A-Za-z0-9#+./\s,]+)',
        r'(?:technologies|tools|skills|stack)[\s:]+([A-Za-z0-9#+./\s,]+)',
    ]
    for pattern in skill_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            # Split by comma and check each term
            terms = [t.strip() for t in match.split(",")]
            for term in terms:
                sub_terms = [t.strip() for t in re.split(r'[,/|&]', term)]
                for sub in sub_terms:
                    canonical = normalize_skill(sub.strip())
                    if canonical:
                        found_skills.add(canonical)

    result = sorted(found_skills)
    logger.info(f"Extracted {len(result)} unique skills from resume")
    return result
