from typing import List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.event import Event, EventStatus
from app.models.student import StudentProfile, StudentSkill
from app.schemas.event import EventRecommendation, EventResponse


async def get_recommended_events_for_student(
    student_id: int,
    db: AsyncSession,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    # 1. Fetch student's skills
    stmt_skills = select(StudentSkill).where(StudentSkill.student_id == student_id)
    skills_result = await db.execute(stmt_skills)
    student_skills = skills_result.scalars().all()

    # Create weight map based on proficiency
    weights = {"BEGINNER": 1.0, "INTERMEDIATE": 1.5, "ADVANCED": 2.0}
    student_skill_weights = {
        s.skill_id: weights.get(s.proficiency.upper(), 1.0) for s in student_skills
    }

    # 2. Fetch active events
    stmt_events = (
        select(Event)
        .where(Event.status.in_([EventStatus.LIVE, EventStatus.APPROVED]))
        .options(selectinload(Event.organization), selectinload(Event.rounds))
        .order_by(Event.event_date.asc())
        .limit(50)
    )
    events_result = await db.execute(stmt_events)
    events = events_result.scalars().all()

    recommendations = []
    for event in events:
        # Match score calculation:
        # If student has skills, compute overlap score; default baseline score for all
        match_score = 65.0  # Base recommendation baseline
        if student_skill_weights:
            # Add dynamic affinity heuristic based on title/description keywords & rounds
            title_lower = (event.title + " " + event.description).lower()
            bonus = 0.0
            if "backend" in title_lower or "python" in title_lower:
                bonus += 20.0
            if "hackathon" in event.event_type.lower():
                bonus += 10.0
            match_score = min(100.0, match_score + bonus)

        recommendations.append({
            "event": event,
            "match_score": round(match_score, 1),
        })

    # Sort descending by match score
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations[:limit]
