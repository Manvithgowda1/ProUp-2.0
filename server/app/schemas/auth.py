from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserSummary"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    type: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class SkillProficiencyInput(BaseModel):
    skill_id: int
    proficiency: str = "INTERMEDIATE"


class StudentRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=2)
    college_id: Optional[int] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[List[SkillProficiencyInput]] = []


class OrganizationInput(BaseModel):
    name: str = Field(..., min_length=2)
    cin: str = Field(..., min_length=5, description="Corporate Identification Number")
    email: EmailStr
    website: Optional[str] = None


class OrganizerRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    organization: OrganizationInput


class UserSummary(BaseModel):
    user_id: int
    email: str
    role: str
    verification_status: Optional[str] = None
    organization_id: Optional[int] = None

    class Config:
        from_attributes = True


Token.model_rebuild()
