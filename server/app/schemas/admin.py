from typing import Optional
from pydantic import BaseModel


class OrganizerVerifyRequest(BaseModel):
    status: str  # APPROVED or REJECTED
    rejection_reason: Optional[str] = None


class EventModerateRequest(BaseModel):
    status: str  # APPROVED or REJECTED
    rejection_reason: Optional[str] = None


class PlatformAnalyticsResponse(BaseModel):
    total_students: int
    total_organizers: int
    total_events: int
    total_registrations: int
    total_shortlisted: int
    total_hired: int
    active_events: int
