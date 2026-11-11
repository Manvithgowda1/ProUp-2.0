import asyncio
from datetime import datetime, timedelta, timezone
from app.core.database import AsyncSessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User, OrganizerProfile, UserRole, VerificationStatus
from app.models.organization import Organization, College
from app.models.student import StudentProfile, Skill, StudentSkill
from app.models.event import Event, EventStatus, EventType, EventMode
from app.models.round import EventRound, RoundType, RoundStatus


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # 1. Create Admin
        admin = User(
            email="admin@proup.io",
            password_hash=get_password_hash("Admin@123"),
            role=UserRole.ADMIN,
        )
        db.add(admin)

        # 2. Colleges
        c1 = College(name="National Institute of Engineering", location="Mysuru")
        c2 = College(name="PES University", location="Bengaluru")
        c3 = College(name="BMS College of Engineering", location="Bengaluru")
        db.add_all([c1, c2, c3])
        await db.flush()

        # 3. Skills
        skills = [
            Skill(name="Python"),
            Skill(name="FastAPI"),
            Skill(name="PostgreSQL"),
            Skill(name="React"),
            Skill(name="TypeScript"),
            Skill(name="Docker"),
            Skill(name="Data Structures & Algorithms"),
        ]
        db.add_all(skills)
        await db.flush()

        # 4. Organization & Verified Organizer
        org = Organization(
            name="Google DeepMind Labs",
            cin="U72900KA2021PTC148900",
            email="careers@deepmind.com",
            website="https://deepmind.google",
        )
        db.add(org)
        await db.flush()

        organizer_user = User(
            email="recruiter@deepmind.com",
            password_hash=get_password_hash("Recruiter@123"),
            role=UserRole.ORGANIZER,
        )
        db.add(organizer_user)
        await db.flush()

        org_profile = OrganizerProfile(
            user_id=organizer_user.user_id,
            organization_id=org.organization_id,
            verification_status=VerificationStatus.APPROVED,
            verified_by=1,
            verified_at=datetime.now(timezone.utc),
        )
        db.add(org_profile)

        # 5. Student
        student_user = User(
            email="student@nie.ac.in",
            password_hash=get_password_hash("Student@123"),
            role=UserRole.STUDENT,
        )
        db.add(student_user)
        await db.flush()

        student_profile = StudentProfile(
            user_id=student_user.user_id,
            college_id=c1.college_id,
            name="Manvith Gowda",
            github_url="https://github.com/manvithgowda",
            linkedin_url="https://linkedin.com/in/manvithgowda",
            bio="Aspiring Software Engineer passionate about backend systems and distributed architecture.",
        )
        db.add(student_profile)
        await db.flush()

        # Student skills
        s_skill1 = StudentSkill(student_id=student_user.user_id, skill_id=skills[0].skill_id, proficiency="ADVANCED")
        s_skill2 = StudentSkill(student_id=student_user.user_id, skill_id=skills[1].skill_id, proficiency="ADVANCED")
        db.add_all([s_skill1, s_skill2])

        # 6. Event
        now = datetime.now(timezone.utc)
        event = Event(
            organization_id=org.organization_id,
            created_by=organizer_user.user_id,
            title="National Systems & Backend Hiring Challenge 2026",
            description="High-velocity 3-stage competition for top engineers. Top performers receive direct hiring offers and internship packages.",
            event_type=EventType.HIRING_CHALLENGE,
            event_mode=EventMode.ONLINE,
            event_date=now + timedelta(days=14),
            registration_deadline=now + timedelta(days=10),
            location="Remote",
            max_participants=500,
            status=EventStatus.LIVE,
            approved_by=1,
            approved_at=now,
        )
        db.add(event)
        await db.flush()

        # Event Rounds
        r1 = EventRound(
            event_id=event.event_id,
            round_number=1,
            name="CS Fundamentals & Aptitude",
            round_type=RoundType.APTITUDE,
            description="60 questions evaluating algorithms, operating systems, and DBMS",
            start_time=now + timedelta(days=14),
            end_time=now + timedelta(days=14, hours=1),
            duration_minutes=60,
            total_marks=100.0,
            passing_marks=60.0,
            status=RoundStatus.UPCOMING,
        )
        r2 = EventRound(
            event_id=event.event_id,
            round_number=2,
            name="Algorithmic Coding Arena",
            round_type=RoundType.CODING,
            description="3 algorithmic coding problems with hidden test case evaluation",
            start_time=now + timedelta(days=15),
            end_time=now + timedelta(days=15, hours=2),
            duration_minutes=120,
            total_marks=100.0,
            passing_marks=50.0,
            status=RoundStatus.UPCOMING,
        )
        r3 = EventRound(
            event_id=event.event_id,
            round_number=3,
            name="Technical & System Design Interview",
            round_type=RoundType.INTERVIEW,
            description="1-on-1 live technical interview with senior engineering leads",
            start_time=now + timedelta(days=17),
            end_time=now + timedelta(days=18),
            duration_minutes=45,
            total_marks=100.0,
            passing_marks=70.0,
            status=RoundStatus.UPCOMING,
        )
        db.add_all([r1, r2, r3])

        await db.commit()
        print("Database seeded successfully with Admin, Organizer, Student, and Sample Event!")


if __name__ == "__main__":
    asyncio.run(seed())
