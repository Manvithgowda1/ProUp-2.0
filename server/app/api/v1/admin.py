from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.user import User, OrganizerProfile, VerificationStatus, UserRole
from app.models.organization import Organization
from app.models.event import Event, EventStatus, EventRegistration
from app.models.round import RoundShortlist
from app.models.hiring import Hiring
from app.schemas.admin import (
    OrganizerVerifyRequest,
    EventModerateRequest,
    PlatformAnalyticsResponse,
)
from app.schemas.common import APIResponse
from app.api.deps import require_admin

router = APIRouter(prefix="/admin", tags=["Admin Oversight"])


@router.get("/organizers/pending", response_model=APIResponse[List[dict]])
async def get_pending_organizers(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(OrganizerProfile)
        .where(OrganizerProfile.verification_status == VerificationStatus.PENDING)
        .options(selectinload(OrganizerProfile.organization), selectinload(OrganizerProfile.user))
    )
    result = await db.execute(stmt)
    profiles = result.scalars().all()

    data = [
        {
            "user_id": p.user_id,
            "email": p.user.email if p.user else "",
            "organization_id": p.organization_id,
            "organization_name": p.organization.name if p.organization else "",
            "cin": p.organization.cin if p.organization else "",
            "website": p.organization.website if p.organization else "",
            "verification_status": p.verification_status,
        }
        for p in profiles
    ]
    return APIResponse(data=data)


@router.post("/organizers/{user_id}/verify", response_model=APIResponse[dict])
async def verify_organizer(
    user_id: int,
    req: OrganizerVerifyRequest,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(OrganizerProfile).where(OrganizerProfile.user_id == user_id)
    profile = (await db.execute(stmt)).scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Organizer profile not found")

    status_upper = req.status.upper()
    if status_upper not in [VerificationStatus.APPROVED, VerificationStatus.REJECTED]:
        raise HTTPException(status_code=400, detail="Status must be APPROVED or REJECTED")

    profile.verification_status = status_upper
    profile.verified_by = current_user.user_id
    profile.verified_at = datetime.now(timezone.utc)
    profile.rejection_reason = req.rejection_reason if status_upper == VerificationStatus.REJECTED else None

    await db.commit()
    return APIResponse(message=f"Organizer verification set to {status_upper}", data={"user_id": user_id})


@router.post("/events/{event_id}/moderate", response_model=APIResponse[dict])
async def moderate_event(
    event_id: int,
    req: EventModerateRequest,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Event).where(Event.event_id == event_id)
    event = (await db.execute(stmt)).scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    status_upper = req.status.upper()
    if status_upper == "APPROVED":
        event.status = EventStatus.LIVE
        event.approved_by = current_user.user_id
        event.approved_at = datetime.now(timezone.utc)
    elif status_upper == "REJECTED":
        event.status = EventStatus.REJECTED
        event.rejection_reason = req.rejection_reason
    else:
        raise HTTPException(status_code=400, detail="Status must be APPROVED or REJECTED")

    await db.commit()
    return APIResponse(message=f"Event moderated to {event.status}", data={"event_id": event_id})


@router.get("/analytics", response_model=APIResponse[PlatformAnalyticsResponse])
async def get_platform_analytics(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    total_students = (
        await db.execute(select(func.count(User.user_id)).where(User.role == UserRole.STUDENT))
    ).scalar_one() or 0

    total_organizers = (
        await db.execute(select(func.count(User.user_id)).where(User.role == UserRole.ORGANIZER))
    ).scalar_one() or 0

    total_events = (
        await db.execute(select(func.count(Event.event_id)))
    ).scalar_one() or 0

    total_registrations = (
        await db.execute(select(func.count(EventRegistration.registration_id)))
    ).scalar_one() or 0

    total_shortlisted = (
        await db.execute(select(func.count(RoundShortlist.shortlist_id)))
    ).scalar_one() or 0

    total_hired = (
        await db.execute(select(func.count(Hiring.hiring_id)).where(Hiring.status == "ACCEPTED"))
    ).scalar_one() or 0

    active_events = (
        await db.execute(select(func.count(Event.event_id)).where(Event.status == EventStatus.LIVE))
    ).scalar_one() or 0

    analytics = PlatformAnalyticsResponse(
        total_students=total_students,
        total_organizers=total_organizers,
        total_events=total_events,
        total_registrations=total_registrations,
        total_shortlisted=total_shortlisted,
        total_hired=total_hired,
        active_events=active_events,
    )
    return APIResponse(data=analytics)
