import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_assessment_questions_as_student(client: AsyncClient, student_headers, seed_data):
    assessment_id = seed_data["assessment"].assessment_id
    response = await client.get(f"/api/v1/assessments/{assessment_id}/questions", headers=student_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    questions = body["data"]
    assert len(questions) >= 1
    # Check that answers are concealed for students
    for opt in questions[0]["options"]:
        assert opt["is_correct"] is None


@pytest.mark.asyncio
async def test_organizer_add_question(client: AsyncClient, organizer_headers, seed_data):
    assessment_id = seed_data["assessment"].assessment_id
    payload = {
        "question_text": "Which module handles asynchronous I/O in Python?",
        "question_type": "MCQ",
        "marks": 5.0,
        "negative_marks": 1.0,
        "options": [
            {"option_text": "asyncio", "is_correct": True},
            {"option_text": "threading", "is_correct": False},
            {"option_text": "multiprocessing", "is_correct": False},
        ],
    }
    response = await client.post(
        f"/api/v1/assessments/{assessment_id}/questions",
        json=payload,
        headers=organizer_headers,
    )
    assert response.status_code == 201
    assert "question_id" in response.json()["data"]


@pytest.mark.asyncio
async def test_submit_assessment_evaluation(client: AsyncClient, student_headers, seed_data):
    assessment_id = seed_data["assessment"].assessment_id
    question_id = seed_data["question"].question_id
    correct_option_id = seed_data["options"][0].option_id  # opt1 is correct

    payload = {
        "submissions": [
            {
                "question_id": question_id,
                "selected_option_id": correct_option_id,
            }
        ]
    }
    response = await client.post(
        f"/api/v1/assessments/{assessment_id}/submit",
        json=payload,
        headers=student_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    result = body["data"]
    assert result["score"] == 10.0
    assert result["percentage"] == 10.0
    assert "passed" in result
