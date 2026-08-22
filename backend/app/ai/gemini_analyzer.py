import json
import asyncio
import google.generativeai as genai
from loguru import logger
from app.config import settings
from app.exceptions import AIServiceError

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
# Initialize the model
model = genai.GenerativeModel('gemini-3.6-flash')

MAX_RETRIES = 3
BACKOFF_DELAYS = [2, 4, 6]  # seconds

async def generate_analysis_insights(
    best_fit_role: str,
    fit_score: float,
    matched_skills: list[str],
    missing_core_skills: list[str],
    missing_optional_skills: list[str],
    ats_score: float,
    weak_sections: list[dict],
) -> dict:
    # Build the prompt
    weak_section_text = ""
    if weak_sections:
        weak_section_text = "\n".join(
            f"- {s['section']}: {s['score']}% ({s['label']})"
            for s in weak_sections
        )
    else:
        weak_section_text = "No weak sections detected."

    prompt = f"""You are an expert resume analyst. Analyze this resume data and return a JSON response.

RESUME DATA:
- Best Fit Role: {best_fit_role}
- Fit Score: {fit_score}%
- ATS Score: {ats_score}%
- Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}
- Missing Core Skills: {', '.join(missing_core_skills) if missing_core_skills else 'None'}
- Missing Optional Skills: {', '.join(missing_optional_skills) if missing_optional_skills else 'None'}
- Weak Sections:
{weak_section_text}

Return ONLY valid JSON (no markdown, no code blocks) with this exact structure:
{{
  "explanation": "2-3 sentence explanation of why this resume scored {fit_score}% for {best_fit_role}. Reference specific matched and missing skills.",
  "suggestions": [
    "Specific, actionable suggestion 1 mentioning exact tools or skills to add",
    "Specific suggestion 2 about resume sections to improve",
    "Specific suggestion 3 about keywords or experience to highlight",
    "Specific suggestion 4 (optional, only if relevant)"
  ],
  "section_tips": {{
    "SectionName": "One-line specific improvement tip for this section"
  }}
}}

RULES:
- Explanation must reference specific skills by name
- Suggestions must be actionable and specific (mention exact tools, not "learn more")
- Section tips only for sections scoring below 60%
- Keep all text concise and professional
- STRICTLY Return JSON ONLY, no surrounding markdown backticks.
"""

    # Make API call with retry logic
    for attempt in range(MAX_RETRIES):
        try:
            # Using generate_content_async for async support
            response = await model.generate_content_async(prompt)

            response_text = response.text.strip()
            # Clean markdown if gemini returns it despite instructions
            if response_text.startswith("`json"):
                response_text = response_text[7:]
            if response_text.startswith("`"):
                response_text = response_text[3:]
            if response_text.endswith("`"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
                
            result = json.loads(response_text)

            # Validate structure
            explanation = result.get("explanation", "")
            suggestions = result.get("suggestions", [])
            section_tips = result.get("section_tips", {})

            if not explanation:
                explanation = f"Your resume scored {fit_score}% for {best_fit_role}."

            if not suggestions or not isinstance(suggestions, list):
                suggestions = [f"Focus on adding {', '.join(missing_core_skills[:2])} to strengthen your {best_fit_role} profile."]

            logger.info(f"Gemini analysis generated successfully (attempt {attempt + 1})")
            return {
                "explanation": explanation,
                "suggestions": suggestions[:4],  # Cap at 4
                "section_tips": section_tips,
            }

        except json.JSONDecodeError as e:
            logger.warning(f"Gemini response JSON parse error (attempt {attempt + 1}): {e}")
        except Exception as e:
            logger.warning(f"Gemini API error (attempt {attempt + 1}): {e}")

        # Backoff before retry
        if attempt < MAX_RETRIES - 1:
            delay = BACKOFF_DELAYS[attempt]
            logger.info(f"Retrying in {delay}s...")
            await asyncio.sleep(delay)

    # All retries failed — return graceful fallback
    logger.error("All Gemini retries failed. Returning fallback response.")
    return _generate_fallback(
        best_fit_role, fit_score, matched_skills,
        missing_core_skills, ats_score, weak_sections
    )


def _generate_fallback(
    best_fit_role: str,
    fit_score: float,
    matched_skills: list[str],
    missing_core_skills: list[str],
    ats_score: float,
    weak_sections: list[dict],
) -> dict:
    """Generate a basic fallback when Gemini is unavailable."""
    matched_str = ", ".join(matched_skills[:5]) if matched_skills else "no specific skills"
    missing_str = ", ".join(missing_core_skills[:3]) if missing_core_skills else "no missing core skills"

    explanation = (
        f"Your resume scored {fit_score}% for {best_fit_role}. "
        f"You have relevant skills including {matched_str}. "
        f"{'Adding ' + missing_str + ' would improve your score.' if missing_core_skills else 'Your core skills are well-covered.'}"
    )

    suggestions = []
    if missing_core_skills:
        suggestions.append(f"Add these core skills to your resume: {', '.join(missing_core_skills[:3])}")
    if weak_sections:
        for s in weak_sections[:2]:
            suggestions.append(f"Improve your {s['section']} section (currently {s['score']}%)")
    if not suggestions:
        suggestions.append("Continue building projects that demonstrate your technical skills")

    section_tips = {}
    for s in weak_sections:
        section_tips[s["section"]] = f"Strengthen this section to improve your overall score (currently {s['score']}%)"

    return {
        "explanation": explanation,
        "suggestions": suggestions,
        "section_tips": section_tips,
    }
