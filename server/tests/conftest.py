import os
import asyncio
from typing import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.database import Base, get_db
from app.core.security import get_password_hash, create_access_token
from app.main import app
from app.models.user import User, OrganizerProfile, UserRole, VerificationStatus
from app.models.organization import Organization, College
from app.models.student import StudentProfile, Skill, StudentSkill
from app.models.event import Event, EventStatus, EventType, EventMode
from app.models.round import EventRound, RoundType, RoundStatus
from app.models.assessment import Assessment, Question, QuestionOption
from app.models.coding import CodingProblem, CodingTestCase

TEST_DB_FILE = "./test_proup.db"
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB_FILE}"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    # Teardown at end of test session
    yield
    if os.path.exists(TEST_DB_FILE):
        try:
            os.remove(TEST_DB_FILE)
        except Exception:
            pass


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def seed_data(db_session: AsyncSession):
    # 1. College & Skills
    college = College(name="Test Institute of Tech", location="Bengaluru")
    db_session.add(college)
    await db_session.flush()

    skill_python = Skill(name="Python")
    skill_fastapi = Skill(name="FastAPI")
    skill_algorithms = Skill(name="Algorithms")
    db_session.add_all([skill_python, skill_fastapi, skill_algorithms])
    await db_session.flush()

    # 2. Admin User
    admin = User(
        email="admin@test.io",
        password_hash=get_password_hash("AdminPass123"),
        role=UserRole.ADMIN,
    )
    db_session.add(admin)
    await db_session.flush()

    # 3. Organization & Verified Organizer
    org = Organization(
        name="DeepMind Tech Labs",
        cin="U72900KA2022PTC123456",
        email="contact@deepmind.com",
        website="https://deepmind.test",
    )
    db_session.add(org)
    await db_session.flush()

    organizer = User(
        email="organizer@test.io",
        password_hash=get_password_hash("OrgPass123"),
        role=UserRole.ORGANIZER,
    )
    db_session.add(organizer)
    await db_session.flush()

    org_profile = OrganizerProfile(
        user_id=organizer.user_id,
        organization_id=org.organization_id,
        verification_status=VerificationStatus.APPROVED,
        verified_by=admin.user_id,
    )
    db_session.add(org_profile)

    # 4. Pending Organizer
    pending_org_user = User(
        email="pending@test.io",
        password_hash=get_password_hash("PendingPass123"),
        role=UserRole.ORGANIZER,
    )
    db_session.add(pending_org_user)
    await db_session.flush()

    pending_profile = OrganizerProfile(
        user_id=pending_org_user.user_id,
        organization_id=org.organization_id,
        verification_status=VerificationStatus.PENDING,
    )
    db_session.add(pending_profile)

    # 5. Student User
    student = User(
        email="student@test.io",
        password_hash=get_password_hash("StudentPass123"),
        role=UserRole.STUDENT,
    )
    db_session.add(student)
    await db_session.flush()

    student_profile = StudentProfile(
        user_id=student.user_id,
        college_id=college.college_id,
        name="Test Student",
        github_url="https://github.com/teststudent",
        linkedin_url="https://linkedin.com/in/teststudent",
        bio="Test student bio passionate about backend.",
    )
    db_session.add(student_profile)
    await db_session.flush()

    # Attach skills
    db_session.add(StudentSkill(student_id=student.user_id, skill_id=skill_python.skill_id, proficiency="ADVANCED"))
    db_session.add(StudentSkill(student_id=student.user_id, skill_id=skill_fastapi.skill_id, proficiency="INTERMEDIATE"))

    # 6. Event
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)
    event = Event(
        organization_id=org.organization_id,
        created_by=organizer.user_id,
        title="National Backend Python Challenge",
        description="Solve real-world distributed backend engineering challenges in Python.",
        event_type=EventType.HIRING_CHALLENGE,
        event_mode=EventMode.ONLINE,
        event_date=now + timedelta(days=10),
        registration_deadline=now + timedelta(days=7),
        location="Remote",
        max_participants=200,
        status=EventStatus.LIVE,
    )
    db_session.add(event)
    await db_session.flush()

    # Event Round
    event_round = EventRound(
        event_id=event.event_id,
        round_number=1,
        name="MCQ Screening",
        round_type=RoundType.MCQ,
        description="30 questions on CS fundamentals and Python",
        start_time=now + timedelta(days=10),
        end_time=now + timedelta(days=10, hours=1),
        duration_minutes=60,
        total_marks=100.0,
        passing_marks=50.0,
        status=RoundStatus.UPCOMING,
    )
    db_session.add(event_round)
    await db_session.flush()

    # Assessment
    assessment = Assessment(
        round_id=event_round.round_id,
        title="Python Backend Assessment",
        description="Screening test",
        duration_minutes=60,
        total_marks=100.0,
        passing_marks=50.0,
    )
    db_session.add(assessment)
    await db_session.flush()

    # Questions & Options
    q1 = Question(
        assessment_id=assessment.assessment_id,
        question_text="What is the average time complexity of Python dictionary lookup?",
        question_type="MCQ",
        marks=10.0,
        negative_marks=2.0,
    )
    db_session.add(q1)
    await db_session.flush()

    opt1 = QuestionOption(question_id=q1.question_id, option_text="O(1)", is_correct=True)
    opt2 = QuestionOption(question_id=q1.question_id, option_text="O(n)", is_correct=False)
    db_session.add_all([opt1, opt2])

    # Coding Problem & Test Case
    cp = CodingProblem(
        assessment_id=assessment.assessment_id,
        title="Two Sum Problem",
        description="Find two numbers that add up to target.",
        input_format="Array and target",
        output_format="Indices",
        difficulty="EASY",
    )
    db_session.add(cp)
    await db_session.flush()

    tc = CodingTestCase(
        problem_id=cp.problem_id,
        input_data="4\n2 7 11 15\n9",
        expected_output="0 1",
        marks=20.0,
        is_hidden=True,
    )
    db_session.add(tc)

    await db_session.commit()

    return {
        "admin": admin,
        "organizer": organizer,
        "pending_organizer": pending_org_user,
        "student": student,
        "org": org,
        "college": college,
        "event": event,
        "assessment": assessment,
        "question": q1,
        "options": [opt1, opt2],
        "problem": cp,
        "test_case": tc,
        "skills": [skill_python, skill_fastapi, skill_algorithms],
    }


@pytest.fixture(scope="function")
def admin_headers(seed_data) -> dict:
    token = create_access_token({
        "sub": str(seed_data["admin"].user_id),
        "email": seed_data["admin"].email,
        "role": "admin",
        "org_id": None,
    })
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def organizer_headers(seed_data) -> dict:
    token = create_access_token({
        "sub": str(seed_data["organizer"].user_id),
        "email": seed_data["organizer"].email,
        "role": "organizer",
        "org_id": seed_data["org"].organization_id,
    })
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def pending_organizer_headers(seed_data) -> dict:
    token = create_access_token({
        "sub": str(seed_data["pending_organizer"].user_id),
        "email": seed_data["pending_organizer"].email,
        "role": "organizer",
        "org_id": seed_data["org"].organization_id,
    })
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def student_headers(seed_data) -> dict:
    token = create_access_token({
        "sub": str(seed_data["student"].user_id),
        "email": seed_data["student"].email,
        "role": "student",
        "org_id": None,
    })
    return {"Authorization": f"Bearer {token}"}
