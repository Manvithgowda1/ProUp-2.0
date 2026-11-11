from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.user import User
from app.models.student import StudentProfile, Skill, StudentSkill
from app.models.organization import College
from app.models.achievement import StudentAchievement
from app.models.event import EventRegistration, Event, AttendanceStatus
from app.models.round import EventResult
from app.schemas.student import (
    StudentProfileResponse,
    StudentProfileUpdate,
    AddSkillRequest,
    SkillResponse,
    CollegeResponse,
    StudentSkillResponse,
    StudentAchievementResponse,
    StudentAchievementsOverviewResponse,
    PointsBreakdownResponse,
    StudentRegistrationResponse,
)
from app.schemas.common import APIResponse
from app.api.deps import get_current_user, require_role

# Gamified Point Allocations
POINTS_ATTENDANCE = 5
POINTS_RANK_1 = 20
POINTS_RANK_2 = 15
POINTS_RANK_3 = 10

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/me/profile", response_model=APIResponse[StudentProfileResponse])
async def get_my_profile(
    current_user: User = Depends(require_role(["student"])),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(StudentProfile)
        .where(StudentProfile.user_id == current_user.user_id)
        .options(
            selectinload(StudentProfile.college),
            selectinload(StudentProfile.skills).selectinload(StudentSkill.skill),
        )
    )
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")

    skills_data = [
        StudentSkillResponse(
            skill_id=s.skill_id,
            name=s.skill.name if s.skill else "",
            proficiency=s.proficiency,
        )
        for s in profile.skills
    ]

    college_data = None
    if profile.college:
        college_data = CollegeResponse(
            college_id=profile.college.college_id,
            name=profile.college.name,
            location=profile.college.location,
        )

    return APIResponse(
        data=StudentProfileResponse(
            user_id=profile.user_id,
            name=profile.name,
            email=current_user.email,
            college=college_data,
            github_url=profile.github_url,
            linkedin_url=profile.linkedin_url,
            resume_url=profile.resume_url,
            bio=profile.bio,
            skills=skills_data,
        )
    )


@router.put("/me/profile", response_model=APIResponse[StudentProfileResponse])
async def update_my_profile(
    req: StudentProfileUpdate,
    current_user: User = Depends(require_role(["student"])),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(StudentProfile).where(StudentProfile.user_id == current_user.user_id)
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")

    if req.name is not None:
        profile.name = req.name
    if req.college_id is not None:
        profile.college_id = req.college_id
    if req.github_url is not None:
        profile.github_url = req.github_url
    if req.linkedin_url is not None:
        profile.linkedin_url = req.linkedin_url
    if req.resume_url is not None:
        profile.resume_url = req.resume_url
    if req.bio is not None:
        profile.bio = req.bio

    await db.commit()
    return await get_my_profile(current_user=current_user, db=db)


@router.post("/me/skills", response_model=APIResponse[dict])
async def add_student_skill(
    req: AddSkillRequest,
    current_user: User = Depends(require_role(["student"])),
    db: AsyncSession = Depends(get_db),
):
    # Check if skill exists
    stmt_skill = select(Skill).where(Skill.skill_id == req.skill_id)
    if not (await db.execute(stmt_skill)).scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Skill not found")

    # Check if student already has this skill
    stmt_existing = (
        select(StudentSkill)
        .where(StudentSkill.student_id == current_user.user_id)
        .where(StudentSkill.skill_id == req.skill_id)
    )
    existing = (await db.execute(stmt_existing)).scalar_one_or_none()
    if existing:
        existing.proficiency = req.proficiency
    else:
        new_skill = StudentSkill(
            student_id=current_user.user_id,
            skill_id=req.skill_id,
            proficiency=req.proficiency,
        )
        db.add(new_skill)

    await db.commit()
    return APIResponse(message="Skill added successfully", data={"skill_id": req.skill_id})


@router.delete("/me/skills/{skill_id}", response_model=APIResponse[dict])
async def remove_student_skill(
    skill_id: int,
    current_user: User = Depends(require_role(["student"])),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(StudentSkill)
        .where(StudentSkill.student_id == current_user.user_id)
        .where(StudentSkill.skill_id == skill_id)
    )
    skill_record = (await db.execute(stmt)).scalar_one_or_none()
    if not skill_record:
        raise HTTPException(status_code=404, detail="Student skill not found")

    await db.delete(skill_record)
    await db.commit()
    return APIResponse(message="Skill removed successfully", data={"skill_id": skill_id})


@router.get("/me/achievements", response_model=APIResponse[StudentAchievementsOverviewResponse])
async def get_my_achievements(
    current_user: User = Depends(require_role(["student"])),
    db: AsyncSession = Depends(get_db),
):
    student_id = current_user.user_id

    # 1. Fetch achievements list
    stmt = (
        select(StudentAchievement)
        .where(StudentAchievement.student_id == student_id)
        .options(selectinload(StudentAchievement.achievement), selectinload(StudentAchievement.event))
        .order_by(StudentAchievement.awarded_at.desc())
    )
    result = await db.execute(stmt)
    achievements = result.scalars().all()

    # 2. Count events attended (marked PRESENT)
    attended_stmt = (
        select(func.count(distinct(EventRegistration.event_id)))
        .where(
            EventRegistration.student_id == student_id,
            EventRegistration.attendance_status == AttendanceStatus.PRESENT,
        )
    )
    events_attended = (await db.scalar(attended_stmt)) or 0

    # 3. Query podium ranks (1, 2, 3) from EventResult
    ranks_stmt = (
        select(EventResult.rank, func.count(distinct(EventResult.event_id)))
        .where(
            EventResult.student_id == student_id,
            EventResult.rank.in_([1, 2, 3]),
        )
        .group_by(EventResult.rank)
    )
    rank_rows = (await db.execute(ranks_stmt)).all()
    rank_counts = {r[0]: r[1] for r in rank_rows}

    rank_1 = rank_counts.get(1, 0)
    rank_2 = rank_counts.get(2, 0)
    rank_3 = rank_counts.get(3, 0)

    # 4. Calculate points
    attendance_points = events_attended * POINTS_ATTENDANCE
    podium_points = (rank_1 * POINTS_RANK_1) + (rank_2 * POINTS_RANK_2) + (rank_3 * POINTS_RANK_3)
    total_points = attendance_points + podium_points

    items = [
        StudentAchievementResponse(
            id=a.id,
            achievement_id=a.achievement_id,
            name=a.achievement.name if a.achievement else "",
            description=a.achievement.description if a.achievement else None,
            event_id=a.event_id,
            event_title=a.event.title if a.event else None,
            certificate_url=a.certificate_url,
            awarded_at=str(a.awarded_at) if a.awarded_at else None,
        )
        for a in achievements
    ]

    return APIResponse(
        data=StudentAchievementsOverviewResponse(
            events_attended=events_attended,
            events_won=rank_1,
            points_earned=total_points,
            achievements_count=len(items),
            breakdown=PointsBreakdownResponse(
                attendance_points=attendance_points,
                podium_points=podium_points,
                rank_1_count=rank_1,
                rank_2_count=rank_2,
                rank_3_count=rank_3,
            ),
            achievements=items,
        )
    )


@router.get("/me/registrations", response_model=APIResponse[List[StudentRegistrationResponse]])
async def get_my_registrations(
    current_user: User = Depends(require_role(["student"])),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(EventRegistration)
        .where(EventRegistration.student_id == current_user.user_id)
        .options(selectinload(EventRegistration.event))
        .order_by(EventRegistration.registered_at.desc())
    )
    result = await db.execute(stmt)
    regs = result.scalars().all()

    items = [
        StudentRegistrationResponse(
            registration_id=r.registration_id,
            event_id=r.event_id,
            event_title=r.event.title if r.event else "",
            event_date=str(r.event.event_date) if r.event else None,
            status=r.status,
            registered_at=str(r.registered_at) if r.registered_at else None,
        )
        for r in regs
    ]
    return APIResponse(data=items)


