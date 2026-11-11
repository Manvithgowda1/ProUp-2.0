from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class OfferCreate(BaseModel):
    student_id: int
    event_id: Optional[int] = None
    job_title: str
    job_type: str = "FULL_TIME"


class OfferRespond(BaseModel):
    status: str  # ACCEPTED or REJECTED


class OfferResponse(BaseModel):
    hiring_id: int
    student_id: int
    organization_id: int
    event_id: Optional[int] = None
    status: str
    job_title: str
    job_type: str
    offered_at: Optional[datetime] = None
    accepted_at: Optional[datetime] = None
    rejected_at: Optional[datetime] = None

    class Config:
        from_attributes = True
