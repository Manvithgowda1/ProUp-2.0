import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_student_success(client: AsyncClient, seed_data):
    payload = {
        "email": "newstudent@college.edu",
        "password": "SecretPassword123!",
        "name": "Jane Doe",
        "college_id": seed_data["college"].college_id,
        "github_url": "https://github.com/janedoe",
        "skills": [
            {"skill_id": seed_data["skills"][0].skill_id, "proficiency": "ADVANCED"}
        ],
    }
    response = await client.post("/api/v1/auth/register/student", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["email"] == "newstudent@college.edu"
    assert body["data"]["role"] == "student"


@pytest.mark.asyncio
async def test_register_student_duplicate_email(client: AsyncClient, seed_data):
    payload = {
        "email": "student@test.io",  # already exists in seed_data
        "password": "SecretPassword123!",
        "name": "Duplicate Student",
    }
    response = await client.post("/api/v1/auth/register/student", json=payload)
    assert response.status_code == 409
    assert "Email already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_register_organizer_success(client: AsyncClient):
    payload = {
        "email": "hr@innovate.co",
        "password": "OrgPassword123!",
        "organization": {
            "name": "Innovate Labs Ltd",
            "cin": "U72900DL2023PTC998877",
            "email": "contact@innovate.co",
            "website": "https://innovate.co",
        },
    }
    response = await client.post("/api/v1/auth/register/organizer", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["email"] == "hr@innovate.co"
    assert body["data"]["role"] == "organizer"
    assert body["data"]["verification_status"] == "PENDING"


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, seed_data):
    payload = {
        "email": "student@test.io",
        "password": "StudentPass123",
    }
    response = await client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "access_token" in body["data"]
    assert "refresh_token" in body["data"]
    assert body["data"]["token_type"] == "bearer"
    assert body["data"]["user"]["email"] == "student@test.io"


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient, seed_data):
    payload = {
        "email": "student@test.io",
        "password": "WrongPassword999",
    }
    response = await client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_me_authenticated(client: AsyncClient, student_headers):
    response = await client.get("/api/v1/auth/me", headers=student_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["email"] == "student@test.io"
    assert body["data"]["role"] == "student"


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
