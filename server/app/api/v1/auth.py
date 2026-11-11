from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.models.user import User, OrganizerProfile, UserRole, VerificationStatus
from app.models.organization import Organization
from app.models.student import StudentProfile, StudentSkill
from app.schemas.auth import (
    LoginRequest,
    StudentRegisterRequest,
    OrganizerRegisterRequest,
    Token,
    RefreshTokenRequest,
    UserSummary,
)
from app.schemas.common import APIResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/student", response_model=APIResponse[UserSummary], status_code=status.HTTP_201_CREATED)
async def register_student(req: StudentRegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check existing user
    stmt = select(User).where(User.email == req.email)
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    # Create user
    user = User(
        email=req.email,
        password_hash=get_password_hash(req.password),
        role=UserRole.STUDENT,
    )
    db.add(user)
    await db.flush()

    # Create student profile
    profile = StudentProfile(
        user_id=user.user_id,
        name=req.name,
        college_id=req.college_id,
        github_url=req.github_url,
        linkedin_url=req.linkedin_url,
        bio=req.bio,
    )
    db.add(profile)

    # Attach skills if provided
    if req.skills:
        for s in req.skills:
            student_skill = StudentSkill(
                student_id=user.user_id,
                skill_id=s.skill_id,
                proficiency=s.proficiency,
            )
            db.add(student_skill)

    await db.commit()
    await db.refresh(user)

    return APIResponse(
        message="Student registered successfully",
        data=UserSummary(
            user_id=user.user_id,
            email=user.email,
            role=user.role,
        ),
    )


@router.post("/register/organizer", response_model=APIResponse[UserSummary], status_code=status.HTTP_201_CREATED)
async def register_organizer(req: OrganizerRegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check existing user
    stmt_user = select(User).where(User.email == req.email)
    if (await db.execute(stmt_user)).scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    # Check or create organization by CIN
    stmt_org = select(Organization).where(Organization.cin == req.organization.cin)
    organization = (await db.execute(stmt_org)).scalar_one_or_none()
    if not organization:
        organization = Organization(
            name=req.organization.name,
            cin=req.organization.cin,
            email=req.organization.email,
            website=req.organization.website,
        )
        db.add(organization)
        await db.flush()

    # Create user
    user = User(
        email=req.email,
        password_hash=get_password_hash(req.password),
        role=UserRole.ORGANIZER,
    )
    db.add(user)
    await db.flush()

    # Create organizer profile
    organizer_profile = OrganizerProfile(
        user_id=user.user_id,
        organization_id=organization.organization_id,
        verification_status=VerificationStatus.PENDING,
    )
    db.add(organizer_profile)

    await db.commit()
    await db.refresh(user)

    return APIResponse(
        message="Organizer registration submitted for admin approval",
        data=UserSummary(
            user_id=user.user_id,
            email=user.email,
            role=user.role,
            verification_status=VerificationStatus.PENDING,
            organization_id=organization.organization_id,
        ),
    )


@router.post("/login", response_model=APIResponse[Token])
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(User)
        .where(User.email == req.email)
        .options(selectinload(User.organizer_profile))
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    verification_status = None
    org_id = None
    if user.organizer_profile:
        verification_status = user.organizer_profile.verification_status
        org_id = user.organizer_profile.organization_id

    token_data = {
        "sub": str(user.user_id),
        "email": user.email,
        "role": user.role,
        "org_id": org_id,
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    user_summary = UserSummary(
        user_id=user.user_id,
        email=user.email,
        role=user.role,
        verification_status=verification_status,
        organization_id=org_id,
    )

    return APIResponse(
        message="Login successful",
        data=Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=3600,
            user=user_summary,
        ),
    )


@router.get("/me", response_model=APIResponse[UserSummary])
async def get_me(current_user: User = Depends(get_current_user)):
    verification_status = None
    org_id = None
    if current_user.organizer_profile:
        verification_status = current_user.organizer_profile.verification_status
        org_id = current_user.organizer_profile.organization_id

    return APIResponse(
        data=UserSummary(
            user_id=current_user.user_id,
            email=current_user.email,
            role=current_user.role,
            verification_status=verification_status,
            organization_id=org_id,
        )
    )
