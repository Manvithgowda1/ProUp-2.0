from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class OrganizationBrief(BaseModel):
    organization_id: int
    name: str
    website: Optional[str] = None

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10)
    event_type: str = "HIRING_CHALLENGE"
    event_mode: str = "ONLINE"
    event_date: datetime
    registration_deadline: datetime
    location: Optional[str] = None
    max_participants: Optional[int] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[str] = None
    event_mode: Optional[str] = None
    event_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None
    location: Optional[str] = None
    max_participants: Optional[int] = None


class EventResponse(BaseModel):
    event_id: int
    organization_id: int
    created_by: int
    title: str
    description: str
    event_type: str
    event_mode: str
    event_date: datetime
    registration_deadline: datetime
    location: Optional[str] = None
    max_participants: Optional[int] = None
    status: str
    created_at: datetime
    organization: Optional[OrganizationBrief] = None
    rounds_count: Optional[int] = 0

    class Config:
        from_attributes = True


class EventRecommendation(EventResponse):
    match_score: float = Field(..., description="Skill overlap match percentage (0.0 to 100.0)")
