"""
ATS (Application Tracking System) score calculator.
Role-independent analysis of resume quality, structure, and keyword density.

Scoring breakdown:
- Section completeness (25%): presence of standard resume sections
- Technical skill coverage (25%): recognized skills from curated dictionary
- Keyword density (20%): technical term density in resume text
- Achievement quantification (15%): measurable metrics and outcomes
- Structure & completeness (15%): overall text quality and formatting
"""
import re
from loguru import logger

# Standard resume sections to detect
EXPECTED_SECTIONS = {
    "skills": [
        "skills", "technical skills", "core skills", "key skills",
        "technologies", "tech stack", "competencies", "proficiencies"
    ],
    "experience": [
        "experience", "work experience", "professional experience",
        "employment", "work history", "internship", "internships"
    ],
    "education": [
        "education", "academic", "academics", "qualification",
        "qualifications", "degree", "university", "college"
    ],
    "projects": [
        "projects", "personal projects", "academic projects",
        "key projects", "notable projects", "side projects"
    ],
    "achievements": [
        "achievements", "accomplishments", "awards", "honors",
        "certifications", "certificates", "recognition", "publications"
    ],
}

# Action verbs that indicate strong resume writing
ACTION_VERBS = {
    "built", "developed", "designed", "implemented", "created", "deployed",
    "optimized", "improved", "increased", "reduced", "managed", "led",
    "architected", "engineered", "automated", "streamlined", "delivered",
    "launched", "migrated", "integrated", "maintained", "established",
    "analyzed", "researched", "collaborated", "mentored", "trained",
    "spearheaded", "initiated", "transformed", "achieved", "exceeded",
}

# Quantification patterns (numbers, percentages, metrics)
METRIC_PATTERNS = [
    r'\d+%',
    r'\d+\+',
    r'\$[\d,]+',
    r'\d+[kKmM]\+?',
    r'\d+\s*(?:users|customers|clients|projects|teams|members)',
    r'(?:increased|improved|reduced|decreased|grew|boosted)\s+(?:by\s+)?\d+',
    r'\d+x\s+(?:faster|improvement|increase)',
]


def calculate_ats_score(extracted_text: str, extracted_skills: list[str]) -> dict:
    """
    Calculate ATS compatibility score for a resume.
    This is role-independent — evaluates resume quality and structure.

    Args:
        extracted_text: Full text extracted from the resume PDF
        extracted_skills: List of recognized canonical skill names

    Returns:
        dict with:
            - ats_score: overall score (0-100)
            - breakdown: dict of component scores
            - detected_sections: list of found sections
            - metrics_found: count of quantifiable achievements
    """
    text_lower = extracted_text.lower()

    # --- Component 1: Section Completeness (25%) ---
    detected_sections = []
    for section_name, keywords in EXPECTED_SECTIONS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_sections.append(section_name)
                break

    section_score = (len(detected_sections) / len(EXPECTED_SECTIONS)) * 100

    # --- Component 2: Technical Skill Coverage (25%) ---
    # Score based on number of recognized skills
    skill_count = len(extracted_skills)
    if skill_count >= 12:
        skill_score = 100
    elif skill_count >= 8:
        skill_score = 85
    elif skill_count >= 5:
        skill_score = 70
    elif skill_count >= 3:
        skill_score = 50
    elif skill_count >= 1:
        skill_score = 30
    else:
        skill_score = 0

    # --- Component 3: Keyword Density (20%) ---
    words = text_lower.split()
    total_words = len(words)

    # Count action verbs
    action_verb_count = sum(1 for word in words if word in ACTION_VERBS)

    if total_words > 0:
        # Action verb density
        verb_density = (action_verb_count / total_words) * 100
        keyword_score = min(100, verb_density * 50)  # Scale up
    else:
        keyword_score = 0

    # Boost for variety of action verbs
    unique_verbs = set(word for word in words if word in ACTION_VERBS)
    if len(unique_verbs) >= 8:
        keyword_score = min(100, keyword_score + 20)
    elif len(unique_verbs) >= 5:
        keyword_score = min(100, keyword_score + 10)

    # --- Component 4: Achievement Quantification (15%) ---
    metrics_found = 0
    for pattern in METRIC_PATTERNS:
        metrics_found += len(re.findall(pattern, extracted_text, re.IGNORECASE))

    if metrics_found >= 6:
        achievement_score = 100
    elif metrics_found >= 4:
        achievement_score = 80
    elif metrics_found >= 2:
        achievement_score = 60
    elif metrics_found >= 1:
        achievement_score = 40
    else:
        achievement_score = 10

    # --- Component 5: Structure & Completeness (15%) ---
    structure_score = 0

    # Word count check (300-1500 words is ideal for 1-2 page resume)
    if 300 <= total_words <= 1500:
        structure_score += 40
    elif 200 <= total_words < 300 or 1500 < total_words <= 2000:
        structure_score += 25
    elif total_words > 100:
        structure_score += 10

    # Check for contact info patterns
    has_email = bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', extracted_text))
    has_phone = bool(re.search(r'[\+]?[\d\s\-\(\)]{10,}', extracted_text))
    has_link = bool(re.search(r'(?:linkedin|github|portfolio|http)', text_lower))

    if has_email:
        structure_score += 20
    if has_phone:
        structure_score += 15
    if has_link:
        structure_score += 15

    # Proper formatting (line breaks suggesting sections)
    line_count = len(extracted_text.split("\n"))
    if line_count >= 20:
        structure_score += 10

    structure_score = min(100, structure_score)

    # --- Calculate weighted ATS score ---
    ats_score = (
        section_score * 0.25 +
        skill_score * 0.25 +
        keyword_score * 0.20 +
        achievement_score * 0.15 +
        structure_score * 0.15
    )

    # Round to nearest integer
    ats_score = round(min(100, max(0, ats_score)))

    result = {
        "ats_score": ats_score,
        "breakdown": {
            "section_completeness": round(section_score),
            "skill_coverage": round(skill_score),
            "keyword_density": round(keyword_score),
            "achievement_quantification": round(achievement_score),
            "structure_completeness": round(structure_score),
        },
        "detected_sections": detected_sections,
        "metrics_found": metrics_found,
        "skill_count": skill_count,
        "action_verb_count": action_verb_count,
    }

    logger.info(f"ATS score calculated: {ats_score}% (sections={len(detected_sections)}, skills={skill_count}, metrics={metrics_found})")
    return result
