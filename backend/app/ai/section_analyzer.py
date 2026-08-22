"""
Section-level resume strength analyzer using spaCy NLP.
Rule-based scoring (no ML, no OpenAI) — fully explainable for interviews.

Analyzes 5 sections: Skills, Projects, Experience, Education, Achievements
Each section gets: score (0-100%), label, detected strengths, improvement tip.
"""
import re
from loguru import logger

# Section header patterns for detection
SECTION_PATTERNS = {
    "Skills": [
        r"(?:technical\s+)?skills", r"core\s+skills", r"key\s+skills",
        r"technologies", r"tech\s+stack", r"competencies", r"proficiencies",
    ],
    "Projects": [
        r"projects", r"personal\s+projects", r"academic\s+projects",
        r"key\s+projects", r"notable\s+projects", r"side\s+projects",
    ],
    "Experience": [
        r"(?:work\s+)?experience", r"professional\s+experience",
        r"employment", r"work\s+history", r"internships?",
    ],
    "Education": [
        r"education", r"academics?", r"qualifications?",
        r"degrees?", r"university", r"college",
    ],
    "Achievements": [
        r"achievements?", r"accomplishments?", r"awards?",
        r"honors?", r"certifications?", r"certificates?",
        r"recognition", r"publications?",
    ],
}

# Action verbs for Projects/Experience scoring
ACTION_VERBS = {
    "built", "developed", "designed", "implemented", "created", "deployed",
    "optimized", "improved", "increased", "reduced", "managed", "led",
    "architected", "engineered", "automated", "streamlined", "delivered",
    "launched", "migrated", "integrated", "maintained", "established",
    "analyzed", "researched", "collaborated", "contributed", "configured",
    "spearheaded", "initiated", "transformed", "achieved", "exceeded",
}

# Impact/quantification patterns
IMPACT_PATTERNS = [
    r'\d+%', r'\d+\+', r'\$[\d,]+', r'\d+[kKmM]\+?',
    r'\d+\s*(?:users|customers|clients|projects|downloads)',
    r'(?:increased|improved|reduced|decreased|boosted|grew)\s+(?:by\s+)?\d+',
    r'(?:top|first|1st|2nd|3rd)\s+\d*',
    r'(?:rank|ranked)\s+\d+',
]

# Degree patterns for Education
DEGREE_PATTERNS = [
    r"(?:bachelor|b\.?(?:tech|sc|e|a|s)|master|m\.?(?:tech|sc|s|a)|ph\.?d|mba|diploma)",
]

GPA_PATTERNS = [
    r"(?:gpa|cgpa|cpi|percentage|grade)[\s:]*[\d.]+",
    r"[\d.]+\s*(?:/\s*(?:10|4|100))",
]

COURSEWORK_PATTERNS = [
    r"(?:relevant\s+)?coursework",
    r"(?:courses?|subjects?)\s*:",
]


def _extract_section_text(full_text: str, section_name: str) -> str:
    """
    Extract text belonging to a specific section from the resume.
    Uses section headers as delimiters.
    """
    text_lower = full_text.lower()
    patterns = SECTION_PATTERNS.get(section_name, [])

    # Find the start of this section
    start_pos = -1
    for pattern in patterns:
        match = re.search(r'(?:^|\n)\s*' + pattern, text_lower, re.IGNORECASE)
        if match:
            start_pos = match.start()
            break

    if start_pos == -1:
        return ""

    # Find the start of the next section (any other section header)
    next_pos = len(full_text)
    all_other_patterns = []
    for name, pats in SECTION_PATTERNS.items():
        if name != section_name:
            all_other_patterns.extend(pats)

    for pattern in all_other_patterns:
        match = re.search(r'(?:^|\n)\s*' + pattern, text_lower[start_pos + 5:], re.IGNORECASE)
        if match:
            candidate = start_pos + 5 + match.start()
            if candidate < next_pos:
                next_pos = candidate

    section_text = full_text[start_pos:next_pos].strip()
    return section_text


def _score_skills_section(section_text: str, extracted_skills: list[str]) -> dict:
    """Score the Skills section based on recognized technical keywords."""
    keyword_count = len(extracted_skills)
    strengths = []
    tip = None

    if keyword_count >= 10:
        score = 95
        strengths.append(f"Excellent skill coverage ({keyword_count} recognized skills)")
    elif keyword_count >= 6:
        score = 80
        strengths.append(f"Good skill diversity ({keyword_count} recognized skills)")
    elif keyword_count >= 4:
        score = 65
        strengths.append(f"Adequate skills listed ({keyword_count} recognized)")
    elif keyword_count >= 2:
        score = 40
        strengths.append(f"Limited skills detected ({keyword_count} recognized)")
        tip = "Add more specific technical skills. Include programming languages, frameworks, tools, and databases you're proficient in."
    else:
        score = 15
        tip = "Your skills section needs significant improvement. List all technical skills including languages, frameworks, databases, and tools."

    # Check for skill categorization
    if section_text and any(cat in section_text.lower() for cat in ["languages", "frameworks", "tools", "databases"]):
        strengths.append("Skills are well-categorized")
        score = min(100, score + 5)

    label = _get_label(score)
    return {"score": score, "label": label, "detected_strengths": strengths, "tip": tip}


def _score_projects_section(section_text: str) -> dict:
    """Score the Projects section based on action verbs, tech terms, and impact."""
    strengths = []
    tip = None

    if not section_text:
        return {"score": 0, "label": "Weak", "detected_strengths": [], "tip": "Add a Projects section showcasing 2-3 technical projects with descriptions."}

    words = section_text.lower().split()

    # Count action verbs
    action_count = sum(1 for w in words if w in ACTION_VERBS)

    # Count impact mentions
    impact_count = 0
    for pattern in IMPACT_PATTERNS:
        impact_count += len(re.findall(pattern, section_text, re.IGNORECASE))

    # Estimate number of projects (by bullet points or line breaks)
    project_lines = [l for l in section_text.split("\n") if l.strip() and len(l.strip()) > 20]
    estimated_projects = max(1, len(project_lines) // 3)

    # Scoring
    score = 0
    if action_count >= 6:
        score += 40
        strengths.append(f"Strong action verbs used ({action_count} found)")
    elif action_count >= 3:
        score += 25
        strengths.append(f"Action verbs present ({action_count} found)")
    else:
        score += 10

    if impact_count >= 3:
        score += 35
        strengths.append("Quantifiable impact demonstrated")
    elif impact_count >= 1:
        score += 20
        strengths.append("Some measurable outcomes mentioned")

    if estimated_projects >= 3:
        score += 25
        strengths.append(f"Multiple projects showcased (~{estimated_projects})")
    elif estimated_projects >= 2:
        score += 15
        strengths.append("Projects section present")

    score = min(100, score)
    if score < 60:
        tip = "Strengthen projects by adding quantifiable outcomes (e.g., 'improved performance by 40%') and using action verbs (built, deployed, optimized)."

    label = _get_label(score)
    return {"score": score, "label": label, "detected_strengths": strengths, "tip": tip}


def _score_experience_section(section_text: str) -> dict:
    """Score the Experience section based on metrics, impact keywords, and bullet quality."""
    strengths = []
    tip = None

    if not section_text:
        return {"score": 20, "label": "Weak", "detected_strengths": [],
                "tip": "Add work experience or internship details. Even academic or volunteer experience counts."}

    lines = [l.strip() for l in section_text.split("\n") if l.strip() and len(l.strip()) > 10]
    total_bullets = max(1, len(lines))

    # Count quantifiable results
    quant_count = 0
    for pattern in IMPACT_PATTERNS:
        quant_count += len(re.findall(pattern, section_text, re.IGNORECASE))

    quant_ratio = (quant_count / total_bullets) * 100

    # Count action verbs
    words = section_text.lower().split()
    action_count = sum(1 for w in words if w in ACTION_VERBS)

    # Scoring
    score = 0
    if quant_ratio >= 70:
        score += 50
        strengths.append("Excellent use of metrics and quantifiable results")
    elif quant_ratio >= 40:
        score += 35
        strengths.append("Good use of quantifiable achievements")
    elif quant_ratio >= 15:
        score += 20
        strengths.append("Some metrics present")
    else:
        score += 5

    if action_count >= 5:
        score += 30
        strengths.append("Strong action-oriented descriptions")
    elif action_count >= 2:
        score += 15
        strengths.append("Action verbs used in descriptions")

    if total_bullets >= 6:
        score += 20
        strengths.append("Detailed experience descriptions")
    elif total_bullets >= 3:
        score += 10

    score = min(100, score)
    if score < 60:
        tip = "Add measurable achievements (numbers, percentages, metrics). Replace generic descriptions with specific outcomes."

    label = _get_label(score)
    return {"score": score, "label": label, "detected_strengths": strengths, "tip": tip}


def _score_education_section(section_text: str) -> dict:
    """Score Education section: degree, GPA, and relevant coursework."""
    strengths = []
    tip = None
    score = 0

    if not section_text:
        return {"score": 0, "label": "Weak", "detected_strengths": [],
                "tip": "Add your Education section with degree, university, GPA, and relevant coursework."}

    text_lower = section_text.lower()

    # Check for degree
    has_degree = any(re.search(p, text_lower) for p in DEGREE_PATTERNS)
    if has_degree:
        score += 50
        strengths.append("Degree information present")

    # Check for GPA/CGPA
    has_gpa = any(re.search(p, text_lower) for p in GPA_PATTERNS)
    if has_gpa:
        score += 30
        strengths.append("GPA/CGPA mentioned")

    # Check for coursework
    has_coursework = any(re.search(p, text_lower) for p in COURSEWORK_PATTERNS)
    if has_coursework:
        score += 20
        strengths.append("Relevant coursework listed")

    score = min(100, score)
    if score < 60:
        missing = []
        if not has_degree:
            missing.append("degree name")
        if not has_gpa:
            missing.append("GPA/CGPA")
        if not has_coursework:
            missing.append("relevant coursework")
        tip = f"Consider adding: {', '.join(missing)} to strengthen your Education section."

    label = _get_label(score)
    return {"score": score, "label": label, "detected_strengths": strengths, "tip": tip}


def _score_achievements_section(section_text: str) -> dict:
    """Score Achievements section based on specificity and quantification."""
    strengths = []
    tip = None

    if not section_text:
        return {"score": 0, "label": "Weak", "detected_strengths": [],
                "tip": "Add an Achievements section with awards, certifications, hackathon wins, or notable accomplishments."}

    lines = [l.strip() for l in section_text.split("\n") if l.strip() and len(l.strip()) > 10]
    total_achievements = max(1, len(lines))

    # Count specific/quantifiable achievements
    specific_count = 0
    for pattern in IMPACT_PATTERNS:
        specific_count += len(re.findall(pattern, section_text, re.IGNORECASE))

    # Check for certifications
    cert_patterns = [r"certif", r"certified", r"credential", r"aws\s+certified", r"google\s+certified"]
    has_certs = any(re.search(p, section_text, re.IGNORECASE) for p in cert_patterns)

    # Scoring
    specificity_ratio = (specific_count / total_achievements) * 100

    if specificity_ratio >= 70:
        score = 90
        strengths.append("Highly specific and quantified achievements")
    elif specificity_ratio >= 40:
        score = 70
        strengths.append("Good mix of specific achievements")
    elif specificity_ratio >= 15:
        score = 50
        strengths.append("Some specific achievements present")
    else:
        score = 25

    if has_certs:
        score = min(100, score + 10)
        strengths.append("Professional certifications listed")

    if total_achievements >= 4:
        strengths.append(f"Multiple achievements listed ({total_achievements})")

    score = min(100, score)
    if score < 60:
        tip = "Make achievements more specific. Add numbers, rankings, or measurable outcomes instead of generic statements."

    label = _get_label(score)
    return {"score": score, "label": label, "detected_strengths": strengths, "tip": tip}


def _get_label(score: float) -> str:
    """Convert score to human-readable label."""
    if score >= 75:
        return "Strong"
    elif score >= 55:
        return "Good"
    elif score >= 35:
        return "Average"
    else:
        return "Weak"


def analyze_sections(
    extracted_text: str,
    extracted_skills: list[str],
    nlp=None
) -> list[dict]:
    """
    Analyze each resume section individually and return strength scores.

    Args:
        extracted_text: Full resume text
        extracted_skills: List of canonical skill names
        nlp: Loaded spaCy model (optional, enhances section detection)

    Returns:
        List of section strength dicts, each with:
        section, score, label, detected_strengths, tip
    """
    results = []

    # Skills section
    skills_text = _extract_section_text(extracted_text, "Skills")
    skills_result = _score_skills_section(skills_text, extracted_skills)
    skills_result["section"] = "Skills"
    results.append(skills_result)

    # Projects section
    projects_text = _extract_section_text(extracted_text, "Projects")
    projects_result = _score_projects_section(projects_text)
    projects_result["section"] = "Projects"
    results.append(projects_result)

    # Experience section
    experience_text = _extract_section_text(extracted_text, "Experience")
    experience_result = _score_experience_section(experience_text)
    experience_result["section"] = "Experience"
    results.append(experience_result)

    # Education section
    education_text = _extract_section_text(extracted_text, "Education")
    education_result = _score_education_section(education_text)
    education_result["section"] = "Education"
    results.append(education_result)

    # Achievements section
    achievements_text = _extract_section_text(extracted_text, "Achievements")
    achievements_result = _score_achievements_section(achievements_text)
    achievements_result["section"] = "Achievements"
    results.append(achievements_result)

    logger.info(f"Section analysis complete: {', '.join(f'{r['section']}={r['score']}%' for r in results)}")
    return results
