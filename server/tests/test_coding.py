import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_coding_problem_as_student(client: AsyncClient, student_headers, seed_data):
    problem_id = seed_data["problem"].problem_id
    response = await client.get(f"/api/v1/coding/problems/{problem_id}", headers=student_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    problem = body["data"]
    assert problem["problem_id"] == problem_id
    assert problem["title"] == "Two Sum Problem"
    # Seeded test case was hidden, so it should not appear in student view
    assert len(problem["test_cases"]) == 0


@pytest.mark.asyncio
async def test_organizer_add_test_case(client: AsyncClient, organizer_headers, seed_data):
    problem_id = seed_data["problem"].problem_id
    payload = {
        "input_data": "3\n1 2 3\n5",
        "expected_output": "1 2",
        "marks": 25.0,
        "is_hidden": False,
    }
    response = await client.post(
        f"/api/v1/coding/problems/{problem_id}/test-cases",
        json=payload,
        headers=organizer_headers,
    )
    assert response.status_code == 201
    assert "test_case_id" in response.json()["data"]


@pytest.mark.asyncio
async def test_student_submit_code(client: AsyncClient, student_headers, seed_data):
    problem_id = seed_data["problem"].problem_id
    payload = {
        "language": "python",
        "source_code": "def two_sum(nums, target):\n    lookup = {}\n    for i, n in enumerate(nums):\n        if target - n in lookup:\n            return [lookup[target - n], i]\n        lookup[n] = i\n    return []",
    }
    response = await client.post(
        f"/api/v1/coding/problems/{problem_id}/submit",
        json=payload,
        headers=student_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert data["status"] in ["ACCEPTED", "PARTIALLY_ACCEPTED"]
    assert data["test_cases_passed"] >= 1
    assert data["score"] > 0
