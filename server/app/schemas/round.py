from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class RoundCreate(BaseModel):
    round_number: int = Field(..., ge=1)
    name: str = Field(..., min_length=2)
    round_type: str = Field(..., description="APTITUDE, MCQ, CODING, INTERVIEW")
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    duration_minutes: int = Field(..., ge=1)
    total_marks: float = 100.0
    passing_marks: float = 40.0


class RoundResponse(BaseModel):
    round_id: int
    event_id: int
    round_number: int
    name: str
    round_type: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    total_marks: float
    passing_marks: float
    status: str

    class Config:
        from_attributes = True


class ShortlistCreate(BaseModel):
    student_ids: List[int]
    status: str = "SHORTLISTED"
    remarks: Optional[str] = None


class ShortlistResponse(BaseModel):
    shortlist_id: int
    round_id: int
    student_id: int
    status: str
    selected_at: datetime
    remarks: Optional[str] = None

    class Config:
        from_attributes = True
