import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_respond_to_job_offer(client: AsyncClient, organizer_headers, student_headers, seed_data):
    student_id = seed_data["student"].user_id
    event_id = seed_data["event"].event_id

    # 1. Organizer extends job offer
    offer_payload = {
        "student_id": student_id,
        "event_id": event_id,
        "job_title": "Backend Systems Engineer",
        "job_type": "FULL_TIME",
    }
    create_resp = await client.post("/api/v1/hiring/offers", json=offer_payload, headers=organizer_headers)
    assert create_resp.status_code == 201
    hiring_id = create_resp.json()["data"]["hiring_id"]

    # 2. Student views offers
    my_offers_resp = await client.get("/api/v1/hiring/my-offers", headers=student_headers)
    assert my_offers_resp.status_code == 200
    offers = my_offers_resp.json()["data"]
    assert len(offers) >= 1
    target_offer = next((o for o in offers if o["hiring_id"] == hiring_id), None)
    assert target_offer is not None
    assert target_offer["status"] == "OFFERED"
    assert target_offer["job_title"] == "Backend Systems Engineer"

    # 3. Student responds to offer (ACCEPTED)
    respond_payload = {"status": "ACCEPTED"}
    respond_resp = await client.patch(
        f"/api/v1/hiring/offers/{hiring_id}/respond",
        json=respond_payload,
        headers=student_headers,
    )
    assert respond_resp.status_code == 200
    assert "accepted" in respond_resp.json()["message"].lower()

    # 4. Verify updated status
    updated_offers = await client.get("/api/v1/hiring/my-offers", headers=student_headers)
    accepted_offer = next((o for o in updated_offers.json()["data"] if o["hiring_id"] == hiring_id), None)
    assert accepted_offer["status"] == "ACCEPTED"
    assert accepted_offer["accepted_at"] is not None


@pytest.mark.asyncio
async def test_respond_invalid_status_rejected(client: AsyncClient, organizer_headers, student_headers, seed_data):
    student_id = seed_data["student"].user_id
    offer_payload = {
        "student_id": student_id,
        "job_title": "Intern",
    }
    create_resp = await client.post("/api/v1/hiring/offers", json=offer_payload, headers=organizer_headers)
    hiring_id = create_resp.json()["data"]["hiring_id"]

    invalid_resp = await client.patch(
        f"/api/v1/hiring/offers/{hiring_id}/respond",
        json={"status": "MAYBE"},
        headers=student_headers,
    )
    assert invalid_resp.status_code == 400
    assert "Status must be ACCEPTED or REJECTED" in invalid_resp.json()["detail"]
