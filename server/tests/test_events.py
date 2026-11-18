from datetime import datetime, timedelta, timezone
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_events_public(client: AsyncClient, seed_data):
    response = await client.get("/api/v1/events")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) >= 1
    assert body["data"][0]["title"] == "National Backend Python Challenge"


@pytest.mark.asyncio
async def test_list_events_with_filters(client: AsyncClient, seed_data):
    # Search by keyword
    res = await client.get("/api/v1/events?search=Backend")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 1

    # Search with no match
    res_none = await client.get("/api/v1/events?search=NonExistentEventTitle12345")
    assert res_none.status_code == 200
    assert len(res_none.json()["data"]) == 0


@pytest.mark.asyncio
async def test_get_event_detail_success(client: AsyncClient, seed_data):
    event_id = seed_data["event"].event_id
    response = await client.get(f"/api/v1/events/{event_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["event_id"] == event_id
    assert body["data"]["organization"]["name"] == "DeepMind Tech Labs"


@pytest.mark.asyncio
async def test_get_event_not_found(client: AsyncClient):
    response = await client.get("/api/v1/events/999999")
    assert response.status_code == 404
    assert "Event not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_event_recommendations_for_student(client: AsyncClient, student_headers, seed_data):
    response = await client.get("/api/v1/events/recommendations", headers=student_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) >= 1
    # Check that recommendation includes match score
    assert "match_score" in body["data"][0]
    assert body["data"][0]["match_score"] > 0


@pytest.mark.asyncio
async def test_create_event_verified_organizer(client: AsyncClient, organizer_headers):
    now = datetime.now(timezone.utc)
    payload = {
        "title": "Hackathon 2026 Sprint",
        "description": "High stakes algorithmic sprint for collegiate engineers.",
        "event_type": "HACKATHON",
        "event_mode": "ONLINE",
        "event_date": (now + timedelta(days=20)).isoformat(),
        "registration_deadline": (now + timedelta(days=15)).isoformat(),
        "location": "Online / Virtual",
        "max_participants": 300,
    }
    response = await client.post("/api/v1/events", json=payload, headers=organizer_headers)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "DRAFT"
    assert "event_id" in body["data"]


@pytest.mark.asyncio
async def test_create_event_pending_organizer_forbidden(client: AsyncClient, pending_organizer_headers):
    now = datetime.now(timezone.utc)
    payload = {
        "title": "Unapproved Event",
        "description": "Should fail creation because organizer is pending.",
        "event_date": (now + timedelta(days=20)).isoformat(),
        "registration_deadline": (now + timedelta(days=15)).isoformat(),
    }
    response = await client.post("/api/v1/events", json=payload, headers=pending_organizer_headers)
    assert response.status_code == 403
    assert "pending admin approval" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_event_student_forbidden(client: AsyncClient, student_headers):
    now = datetime.now(timezone.utc)
    payload = {
        "title": "Student Trying to Create Event",
        "description": "Should fail with forbidden role.",
        "event_date": (now + timedelta(days=20)).isoformat(),
        "registration_deadline": (now + timedelta(days=15)).isoformat(),
    }
    response = await client.post("/api/v1/events", json=payload, headers=student_headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_register_for_event_and_check_my_registrations(client: AsyncClient, student_headers, seed_data):
    event_id = seed_data["event"].event_id

    # Register
    reg_resp = await client.post(f"/api/v1/events/{event_id}/register", headers=student_headers)
    assert reg_resp.status_code == 200
    assert reg_resp.json()["data"]["event_id"] == event_id

    # Check that it appears in student's registrations
    my_regs = await client.get("/api/v1/students/me/registrations", headers=student_headers)
    assert my_regs.status_code == 200
    reg_items = my_regs.json()["data"]
    assert len(reg_items) >= 1
    assert any(r["event_id"] == event_id for r in reg_items)

    # Attempt duplicate registration -> 409
    dup_resp = await client.post(f"/api/v1/events/{event_id}/register", headers=student_headers)
    assert dup_resp.status_code == 409
    assert "Already registered" in dup_resp.json()["detail"]


@pytest.mark.asyncio
async def test_update_event(client: AsyncClient, organizer_headers, seed_data):
    event_id = seed_data["event"].event_id
    payload = {
        "title": "Updated Event Title for 2026",
        "max_participants": 750,
    }
    response = await client.put(f"/api/v1/events/{event_id}", json=payload, headers=organizer_headers)
    assert response.status_code == 200
    assert response.json()["data"]["event_id"] == event_id

    # Verify update
    detail = await client.get(f"/api/v1/events/{event_id}")
    assert detail.json()["data"]["title"] == "Updated Event Title for 2026"
    assert detail.json()["data"]["max_participants"] == 750


@pytest.mark.asyncio
async def test_get_event_rounds(client: AsyncClient, seed_data):
    event_id = seed_data["event"].event_id
    response = await client.get(f"/api/v1/events/{event_id}/rounds")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) >= 1
    assert body["data"][0]["name"] == "MCQ Screening"
