from typing import Optional, List
from pydantic import BaseModel, HttpUrl


class SkillResponse(BaseModel):
    skill_id: int
    name: str

    class Config:
        from_attributes = True


class StudentSkillResponse(BaseModel):
    skill_id: int
    name: str
    proficiency: str

    class Config:
        from_attributes = True


class AddSkillRequest(BaseModel):
    skill_id: int
    proficiency: str = "INTERMEDIATE"


class CollegeResponse(BaseModel):
    college_id: int
    name: str
    location: Optional[str] = None

    class Config:
        from_attributes = True


class StudentProfileUpdate(BaseModel):
    name: Optional[str] = None
    college_id: Optional[int] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    resume_url: Optional[str] = None
    bio: Optional[str] = None


class StudentProfileResponse(BaseModel):
    user_id: int
    name: str
    email: str
    college: Optional[CollegeResponse] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    resume_url: Optional[str] = None
    bio: Optional[str] = None
    skills: List[StudentSkillResponse] = []

    class Config:
        from_attributes = True


class StudentAchievementResponse(BaseModel):
    id: int
    achievement_id: int
    name: str
    description: Optional[str] = None
    event_id: Optional[int] = None
    event_title: Optional[str] = None
    certificate_url: Optional[str] = None
    awarded_at: Optional[str] = None

    class Config:
        from_attributes = True


class PointsBreakdownResponse(BaseModel):
    attendance_points: int = 0
    podium_points: int = 0
    rank_1_count: int = 0
    rank_2_count: int = 0
    rank_3_count: int = 0


class StudentAchievementsOverviewResponse(BaseModel):
    events_attended: int = 0
    events_won: int = 0
    points_earned: int = 0
    achievements_count: int = 0
    breakdown: Optional[PointsBreakdownResponse] = None
    achievements: List[StudentAchievementResponse] = []

    class Config:
        from_attributes = True


class StudentRegistrationResponse(BaseModel):
    registration_id: int
    event_id: int
    event_title: str
    event_date: Optional[str] = None
    status: str
    registered_at: Optional[str] = None

    class Config:
        from_attributes = True
