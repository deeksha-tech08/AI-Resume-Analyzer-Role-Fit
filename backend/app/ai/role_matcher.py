"""
Role matching engine — calculates fit score and core coverage for each selected role.
Uses weighted scoring: core skills are worth 2x, optional skills 1x.

Key distinction (interview point):
- ATS score = resume quality (role-independent)
- Role fit score = suitability for a specific role (role-dependent)
"""
from loguru import logger
from app.ai.role_profiles import get_role_profile, VALID_ROLES


def calculate_role_scores(
    extracted_skills: list[str],
    selected_roles: list[str]
) -> list[dict]:
    """
    Calculate fit scores for each selected role.

    Scoring formula:
    - fit_score = (matched_core_weight + matched_optional_weight) / total_possible_weight × 100
    - core_skill_coverage = (matched_core / total_core) × 100

    Args:
        extracted_skills: List of canonical skill names from resume
        selected_roles: List of role names to score against

    Returns:
        List of role score dicts, sorted by fit_score descending.
        Each dict contains: role, fit_score, core_skill_coverage,
        matched_skills, missing_core_skills, missing_optional_skills
    """
    if not extracted_skills:
        logger.warning("No skills extracted — all role scores will be 0")

    skills_set = set(extracted_skills)
    role_scores = []

    for role_name in selected_roles:
        if role_name not in VALID_ROLES:
            logger.warning(f"Unknown role: {role_name}, skipping")
            continue

        profile = get_role_profile(role_name)
        if not profile:
            continue

        core_skills = profile["core"]
        optional_skills = profile["optional"]
        core_weight = profile["core_weight"]
        optional_weight = profile["optional_weight"]

        # Match skills
        matched_core = [s for s in core_skills if s in skills_set]
        matched_optional = [s for s in optional_skills if s in skills_set]
        missing_core = [s for s in core_skills if s not in skills_set]
        missing_optional = [s for s in optional_skills if s not in skills_set]

        # Calculate weighted score
        total_possible_weight = (len(core_skills) * core_weight) + (len(optional_skills) * optional_weight)
        matched_weight = (len(matched_core) * core_weight) + (len(matched_optional) * optional_weight)

        fit_score = round((matched_weight / total_possible_weight) * 100) if total_possible_weight > 0 else 0

        # Core skill coverage
        core_coverage = round((len(matched_core) / len(core_skills)) * 100) if core_skills else 0

        role_scores.append({
            "role": role_name,
            "fit_score": fit_score,
            "core_skill_coverage": core_coverage,
            "matched_skills": sorted(matched_core + matched_optional),
            "missing_core_skills": missing_core,
            "missing_optional_skills": missing_optional,
        })

        logger.info(
            f"Role '{role_name}': fit={fit_score}%, core_coverage={core_coverage}%, "
            f"matched={len(matched_core)+len(matched_optional)}, "
            f"missing_core={len(missing_core)}, missing_optional={len(missing_optional)}"
        )

    # Sort by fit_score descending
    role_scores.sort(key=lambda x: x["fit_score"], reverse=True)
    return role_scores


def get_best_fit_role(role_scores: list[dict]) -> str:
    """Return the role name with the highest fit score."""
    if not role_scores:
        return ""
    return role_scores[0]["role"]
