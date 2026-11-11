from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.user import User
from app.models.event import Event, EventRegistration, EventStatus, RegistrationStatus
from app.models.round import EventRound
from app.models.organization import Organization
from app.schemas.event import EventCreate, EventUpdate, EventResponse, EventRecommendation, OrganizationBrief
from app.schemas.round import RoundResponse
from app.schemas.common import APIResponse
from app.api.deps import get_current_user, require_role, require_verified_organizer
from app.services.recommendation import get_recommended_events_for_student

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=APIResponse[List[EventResponse]])
async def list_events(
    status_filter: Optional[str] = Query("LIVE", alias="status"),
    event_type: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Event)
        .options(selectinload(Event.organization), selectinload(Event.rounds))
        .order_by(Event.event_date.asc())
    )

    if status_filter and status_filter != "ALL":
        stmt = stmt.where(Event.status == status_filter)
    if event_type:
        stmt = stmt.where(Event.event_type == event_type)
    if search:
        search_fmt = f"%{search}%"
        stmt = stmt.where(Event.title.ilike(search_fmt) | Event.description.ilike(search_fmt))

    stmt = stmt.offset((page - 1) * limit).limit(limit)
    result = await db.execute(stmt)
    events = result.scalars().all()

    items = []
    for ev in events:
        org_brief = None
        if ev.organization:
            org_brief = OrganizationBrief(
                organization_id=ev.organization.organization_id,
                name=ev.organization.name,
                website=ev.organization.website,
            )
        items.append(
            EventResponse(
                event_id=ev.event_id,
                organization_id=ev.organization_id,
                created_by=ev.created_by,
                title=ev.title,
                description=ev.description,
                event_type=ev.event_type,
                event_mode=ev.event_mode,
                event_date=ev.event_date,
                registration_deadline=ev.registration_deadline,
                location=ev.location,
                max_participants=ev.max_participants,
                status=ev.status,
                created_at=ev.created_at,
                organization=org_brief,
                rounds_count=len(ev.rounds) if ev.rounds else 0,
            )
        )

    return APIResponse(data=items)


@router.get("/recommendations", response_model=APIResponse[List[EventRecommendation]])
async def get_recommendations(
    current_user: User = Depends(require_role(["student"])),
    db: AsyncSession = Depends(get_db),
):
    recs = await get_recommended_events_for_student(
        student_id=current_user.user_id,
        db=db,
    )
    result_list = []
    for r in recs:
        ev = r["event"]
        org_brief = None
        if ev.organization:
            org_brief = OrganizationBrief(
                organization_id=ev.organization.organization_id,
                name=ev.organization.name,
                website=ev.organization.website,
            )
        result_list.append(
            EventRecommendation(
                event_id=ev.event_id,
                organization_id=ev.organization_id,
                created_by=ev.created_by,
                title=ev.title,
                description=ev.description,
                event_type=ev.event_type,
                event_mode=ev.event_mode,
                event_date=ev.event_date,
                registration_deadline=ev.registration_deadline,
                location=ev.location,
                max_participants=ev.max_participants,
                status=ev.status,
                created_at=ev.created_at,
                organization=org_brief,
                rounds_count=len(ev.rounds) if ev.rounds else 0,
                match_score=r["match_score"],
            )
        )
    return APIResponse(data=result_list)


@router.get("/{event_id}", response_model=APIResponse[EventResponse])
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Event)
        .where(Event.event_id == event_id)
        .options(selectinload(Event.organization), selectinload(Event.rounds))
    )
    event = (await db.execute(stmt)).scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    org_brief = None
    if event.organization:
        org_brief = OrganizationBrief(
            organization_id=event.organization.organization_id,
            name=event.organization.name,
            website=event.organization.website,
        )

    return APIResponse(
        data=EventResponse(
            event_id=event.event_id,
            organization_id=event.organization_id,
            created_by=event.created_by,
            title=event.title,
            description=event.description,
            event_type=event.event_type,
            event_mode=event.event_mode,
            event_date=event.event_date,
            registration_deadline=event.registration_deadline,
            location=event.location,
            max_participants=event.max_participants,
            status=event.status,
            created_at=event.created_at,
            organization=org_brief,
            rounds_count=len(event.rounds) if event.rounds else 0,
        )
    )


@router.post("", response_model=APIResponse[dict], status_code=status.HTTP_201_CREATED)
async def create_event(
    req: EventCreate,
    current_user: User = Depends(require_verified_organizer),
    db: AsyncSession = Depends(get_db),
):
    profile = current_user.organizer_profile
    event = Event(
        organization_id=profile.organization_id,
        created_by=current_user.user_id,
        title=req.title,
        description=req.description,
        event_type=req.event_type,
        event_mode=req.event_mode,
        event_date=req.event_date,
        registration_deadline=req.registration_deadline,
        location=req.location,
        max_participants=req.max_participants,
        status=EventStatus.DRAFT,
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)

    return APIResponse(
        message="Event created in DRAFT status",
        data={"event_id": event.event_id, "status": event.status},
    )


@router.post("/{event_id}/register", response_model=APIResponse[dict])
async def register_for_event(
    event_id: int,
    current_user: User = Depends(require_role(["student"])),
    db: AsyncSession = Depends(get_db),
):
    # Verify event exists and is LIVE
    stmt_ev = select(Event).where(Event.event_id == event_id)
    event = (await db.execute(stmt_ev)).scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.status not in [EventStatus.LIVE, EventStatus.APPROVED]:
        raise HTTPException(status_code=400, detail="Event is not currently open for registrations")

    # Check already registered
    stmt_reg = (
        select(EventRegistration)
        .where(EventRegistration.event_id == event_id)
        .where(EventRegistration.student_id == current_user.user_id)
    )
    existing = (await db.execute(stmt_reg)).scalar_one_or_none()
    if existing:
        if existing.status == RegistrationStatus.REGISTERED:
            raise HTTPException(status_code=409, detail="Already registered for this event")
        existing.status = RegistrationStatus.REGISTERED
    else:
        reg = EventRegistration(
            event_id=event_id,
            student_id=current_user.user_id,
            status=RegistrationStatus.REGISTERED,
        )
        db.add(reg)

    await db.commit()
    return APIResponse(message="Successfully registered for event", data={"event_id": event_id})


@router.put("/{event_id}", response_model=APIResponse[dict])
async def update_event(
    event_id: int,
    req: EventUpdate,
    current_user: User = Depends(require_verified_organizer),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Event).where(Event.event_id == event_id)
    event = (await db.execute(stmt)).scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Only creator or admin can update
    if current_user.role != "admin" and event.created_by != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this event")

    if req.title is not None:
        event.title = req.title
    if req.description is not None:
        event.description = req.description
    if req.event_type is not None:
        event.event_type = req.event_type
    if req.event_mode is not None:
        event.event_mode = req.event_mode
    if req.event_date is not None:
        event.event_date = req.event_date
    if req.registration_deadline is not None:
        event.registration_deadline = req.registration_deadline
    if req.location is not None:
        event.location = req.location
    if req.max_participants is not None:
        event.max_participants = req.max_participants

    await db.commit()
    return APIResponse(message="Event updated successfully", data={"event_id": event_id})


@router.get("/{event_id}/rounds", response_model=APIResponse[List[RoundResponse]])
async def get_event_rounds(
    event_id: int,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(EventRound)
        .where(EventRound.event_id == event_id)
        .order_by(EventRound.round_number.asc())
    )
    result = await db.execute(stmt)
    rounds = result.scalars().all()

    items = [
        RoundResponse(
            round_id=r.round_id,
            event_id=r.event_id,
            round_number=r.round_number,
            name=r.name,
            round_type=r.round_type,
            description=r.description,
            start_time=r.start_time,
            end_time=r.end_time,
            duration_minutes=r.duration_minutes,
            total_marks=r.total_marks,
            passing_marks=r.passing_marks,
            status=r.status,
        )
        for r in rounds
    ]
    return APIResponse(data=items)

