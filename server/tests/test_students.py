import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_my_profile(client: AsyncClient, student_headers):
    response = await client.get("/api/v1/students/me/profile", headers=student_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["email"] == "student@test.io"
    assert body["data"]["name"] == "Test Student"
    assert len(body["data"]["skills"]) >= 2


@pytest.mark.asyncio
async def test_update_my_profile(client: AsyncClient, student_headers):
    payload = {
        "name": "Updated Student Name",
        "bio": "Senior full-stack systems engineer.",
        "github_url": "https://github.com/updatedstudent",
    }
    response = await client.put("/api/v1/students/me/profile", json=payload, headers=student_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "Updated Student Name"
    assert body["data"]["bio"] == "Senior full-stack systems engineer."


@pytest.mark.asyncio
async def test_add_and_remove_student_skill(client: AsyncClient, student_headers, seed_data):
    skill_algorithms = seed_data["skills"][2]
    # Add skill
    add_payload = {
        "skill_id": skill_algorithms.skill_id,
        "proficiency": "ADVANCED",
    }
    add_resp = await client.post("/api/v1/students/me/skills", json=add_payload, headers=student_headers)
    assert add_resp.status_code == 200
    assert add_resp.json()["data"]["skill_id"] == skill_algorithms.skill_id

    # Remove skill
    del_resp = await client.delete(f"/api/v1/students/me/skills/{skill_algorithms.skill_id}", headers=student_headers)
    assert del_resp.status_code == 200
    assert del_resp.json()["data"]["skill_id"] == skill_algorithms.skill_id


@pytest.mark.asyncio
async def test_student_achievements_empty_initially(client: AsyncClient, student_headers):
    response = await client.get("/api/v1/students/me/achievements", headers=student_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert data["events_attended"] == 0
    assert data["events_won"] == 0
    assert data["points_earned"] == 0
    assert data["achievements_count"] == 0
    assert data["breakdown"]["attendance_points"] == 0
    assert data["breakdown"]["podium_points"] == 0
    assert isinstance(data["achievements"], list)
    assert len(data["achievements"]) == 0


@pytest.mark.asyncio
async def test_student_achievements_with_attended_won_and_points(client: AsyncClient, student_headers, seed_data, db_session):
    from app.models.event import EventRegistration, AttendanceStatus, RegistrationStatus
    from app.models.round import EventResult
    from app.models.achievement import Achievement, StudentAchievement

    student = seed_data["student"]
    event = seed_data["event"]

    # 1. Register student and mark attendance as PRESENT (+5 points)
    reg = EventRegistration(
        event_id=event.event_id,
        student_id=student.user_id,
        status=RegistrationStatus.REGISTERED,
        attendance_status=AttendanceStatus.PRESENT,
    )
    db_session.add(reg)

    # 2. Add EventResult with rank 1 (Winner: +20 points)
    event_result = EventResult(
        event_id=event.event_id,
        student_id=student.user_id,
        overall_score=95.0,
        rank=1,
        feedback="Outstanding performance and speed.",
    )
    db_session.add(event_result)

    # 3. Add an Achievement credential
    ach = Achievement(name="First Place Winner", description="1st in Python challenge")
    db_session.add(ach)
    await db_session.flush()

    sa = StudentAchievement(
        student_id=student.user_id,
        achievement_id=ach.achievement_id,
        event_id=event.event_id,
        certificate_url="https://certs.proup.io/first-place.pdf",
    )
    db_session.add(sa)
    await db_session.commit()

    # 4. Fetch achievements overview
    response = await client.get("/api/v1/students/me/achievements", headers=student_headers)
    assert response.status_code == 200
    data = response.json()["data"]

    # Assert metrics: 1 attended (5 pts) + 1 won (20 pts) = 25 pts total
    assert data["events_attended"] == 1
    assert data["events_won"] == 1
    assert data["points_earned"] == 25
    assert data["achievements_count"] == 1
    assert data["breakdown"]["attendance_points"] == 5
    assert data["breakdown"]["podium_points"] == 20
    assert data["breakdown"]["rank_1_count"] == 1
    assert data["breakdown"]["rank_2_count"] == 0
    assert data["breakdown"]["rank_3_count"] == 0
    assert len(data["achievements"]) == 1
    assert data["achievements"][0]["name"] == "First Place Winner"


@pytest.mark.asyncio
async def test_student_achievements_podium_runner_up_points(client: AsyncClient, student_headers, seed_data, db_session):
    from app.models.event import Event, EventRegistration, AttendanceStatus, RegistrationStatus, EventType, EventMode, EventStatus
    from app.models.round import EventResult
    from datetime import datetime, timedelta, timezone

    student = seed_data["student"]
    org = seed_data["org"]
    admin = seed_data["admin"]
    now = datetime.now(timezone.utc)

    # Create 2 separate events
    event2 = Event(
        organization_id=org.organization_id,
        created_by=admin.user_id,
        title="Frontend Hackathon 2026",
        description="Build responsive accessible apps",
        event_type=EventType.HACKATHON,
        event_mode=EventMode.ONLINE,
        event_date=now + timedelta(days=5),
        registration_deadline=now + timedelta(days=3),
        status=EventStatus.LIVE,
    )
    event3 = Event(
        organization_id=org.organization_id,
        created_by=admin.user_id,
        title="Algorithms Olympiad 2026",
        description="Competitive programming tournament",
        event_type=EventType.COMPETITION,
        event_mode=EventMode.ONLINE,
        event_date=now + timedelta(days=12),
        registration_deadline=now + timedelta(days=8),
        status=EventStatus.LIVE,
    )
    db_session.add_all([event2, event3])
    await db_session.flush()

    # Register & attend both events (2 * 5 = 10 pts)
    reg2 = EventRegistration(event_id=event2.event_id, student_id=student.user_id, attendance_status=AttendanceStatus.PRESENT)
    reg3 = EventRegistration(event_id=event3.event_id, student_id=student.user_id, attendance_status=AttendanceStatus.PRESENT)
    db_session.add_all([reg2, reg3])

    # 2nd place in event 2 (+15 pts), 3rd place in event 3 (+10 pts)
    res2 = EventResult(event_id=event2.event_id, student_id=student.user_id, overall_score=88.0, rank=2)
    res3 = EventResult(event_id=event3.event_id, student_id=student.user_id, overall_score=80.0, rank=3)
    db_session.add_all([res2, res3])
    await db_session.commit()

    response = await client.get("/api/v1/students/me/achievements", headers=student_headers)
    assert response.status_code == 200
    data = response.json()["data"]

    # 2 events attended = 10 pts; 2nd place = 15 pts; 3rd place = 10 pts => Total = 35 pts
    assert data["events_attended"] == 2
    assert data["events_won"] == 0
    assert data["points_earned"] == 35
    assert data["breakdown"]["attendance_points"] == 10
    assert data["breakdown"]["podium_points"] == 25
    assert data["breakdown"]["rank_1_count"] == 0
    assert data["breakdown"]["rank_2_count"] == 1
    assert data["breakdown"]["rank_3_count"] == 1


@pytest.mark.asyncio
async def test_student_registrations_empty_initially(client: AsyncClient, student_headers):
    response = await client.get("/api/v1/students/me/registrations", headers=student_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert isinstance(body["data"], list)


@pytest.mark.asyncio
async def test_organizer_forbidden_from_student_profile(client: AsyncClient, organizer_headers):
    response = await client.get("/api/v1/students/me/profile", headers=organizer_headers)
    assert response.status_code == 403
    assert "Operation not permitted for role" in response.json()["detail"]
