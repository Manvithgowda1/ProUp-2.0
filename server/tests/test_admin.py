import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_get_pending_organizers(client: AsyncClient, admin_headers, seed_data):
    response = await client.get("/api/v1/admin/organizers/pending", headers=admin_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    pending_list = body["data"]
    assert len(pending_list) >= 1
    pending_org = next(
        (o for o in pending_list if o["user_id"] == seed_data["pending_organizer"].user_id),
        None,
    )
    assert pending_org is not None
    assert pending_org["verification_status"] == "PENDING"


@pytest.mark.asyncio
async def test_admin_verify_organizer_approve(client: AsyncClient, admin_headers, seed_data):
    user_id = seed_data["pending_organizer"].user_id
    payload = {
        "status": "APPROVED",
        "rejection_reason": None,
    }
    response = await client.post(
        f"/api/v1/admin/organizers/{user_id}/verify",
        json=payload,
        headers=admin_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "APPROVED" in body["message"]


@pytest.mark.asyncio
async def test_admin_moderate_event(client: AsyncClient, admin_headers, organizer_headers):
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)
    # 1. Organizer creates draft event
    create_payload = {
        "title": "Pending Event For Admin Moderation",
        "description": "Requires admin approval before going live.",
        "event_date": (now + timedelta(days=30)).isoformat(),
        "registration_deadline": (now + timedelta(days=25)).isoformat(),
    }
    create_resp = await client.post("/api/v1/events", json=create_payload, headers=organizer_headers)
    assert create_resp.status_code == 201
    event_id = create_resp.json()["data"]["event_id"]

    # 2. Admin moderates event to APPROVED
    mod_payload = {
        "status": "APPROVED",
    }
    mod_resp = await client.post(
        f"/api/v1/admin/events/{event_id}/moderate",
        json=mod_payload,
        headers=admin_headers,
    )
    assert mod_resp.status_code == 200
    assert "LIVE" in mod_resp.json()["message"]

    # 3. Verify event is now LIVE
    detail_resp = await client.get(f"/api/v1/events/{event_id}")
    assert detail_resp.json()["data"]["status"] == "LIVE"


@pytest.mark.asyncio
async def test_admin_analytics(client: AsyncClient, admin_headers, seed_data):
    response = await client.get("/api/v1/admin/analytics", headers=admin_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert data["total_students"] >= 1
    assert data["total_organizers"] >= 1
    assert data["total_events"] >= 1
    assert data["active_events"] >= 1


@pytest.mark.asyncio
async def test_non_admin_forbidden_from_admin_endpoints(client: AsyncClient, student_headers, organizer_headers):
    # Student forbidden
    res_student = await client.get("/api/v1/admin/analytics", headers=student_headers)
    assert res_student.status_code == 403

    # Organizer forbidden
    res_org = await client.get("/api/v1/admin/analytics", headers=organizer_headers)
    assert res_org.status_code == 403
