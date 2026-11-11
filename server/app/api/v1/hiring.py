from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.models.hiring import Hiring
from app.schemas.hiring import OfferCreate, OfferRespond, OfferResponse
from app.schemas.common import APIResponse
from app.api.deps import require_role, require_verified_organizer

router = APIRouter(prefix="/hiring", tags=["Hiring & Offers"])


@router.post("/offers", response_model=APIResponse[dict], status_code=status.HTTP_201_CREATED)
async def create_offer(
    req: OfferCreate,
    current_user: User = Depends(require_verified_organizer),
    db: AsyncSession = Depends(get_db),
):
    profile = current_user.organizer_profile
    offer = Hiring(
        student_id=req.student_id,
        organization_id=profile.organization_id,
        event_id=req.event_id,
        job_title=req.job_title,
        job_type=req.job_type,
        status="OFFERED",
        offered_at=datetime.now(timezone.utc),
    )
    db.add(offer)
    await db.commit()
    await db.refresh(offer)

    return APIResponse(message="Job offer extended successfully", data={"hiring_id": offer.hiring_id})


@router.get("/my-offers", response_model=APIResponse[List[OfferResponse]])
async def get_my_offers(
    current_user: User = Depends(require_role(["student"])),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Hiring).where(Hiring.student_id == current_user.user_id)
    result = await db.execute(stmt)
    offers = result.scalars().all()

    items = [
        OfferResponse(
            hiring_id=o.hiring_id,
            student_id=o.student_id,
            organization_id=o.organization_id,
            event_id=o.event_id,
            status=o.status,
            job_title=o.job_title,
            job_type=o.job_type,
            offered_at=o.offered_at,
            accepted_at=o.accepted_at,
            rejected_at=o.rejected_at,
        )
        for o in offers
    ]
    return APIResponse(data=items)


@router.patch("/offers/{hiring_id}/respond", response_model=APIResponse[dict])
async def respond_to_offer(
    hiring_id: int,
    req: OfferRespond,
    current_user: User = Depends(require_role(["student"])),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Hiring)
        .where(Hiring.hiring_id == hiring_id)
        .where(Hiring.student_id == current_user.user_id)
    )
    offer = (await db.execute(stmt)).scalar_one_or_none()
    if not offer:
        raise HTTPException(status_code=404, detail="Job offer not found")

    new_status = req.status.upper()
    if new_status not in ["ACCEPTED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="Status must be ACCEPTED or REJECTED")

    offer.status = new_status
    if new_status == "ACCEPTED":
        offer.accepted_at = datetime.now(timezone.utc)
    else:
        offer.rejected_at = datetime.now(timezone.utc)

    await db.commit()
    return APIResponse(message=f"Offer {new_status.lower()} successfully", data={"hiring_id": hiring_id})
