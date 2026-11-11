from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.user import User
from app.models.coding import CodingProblem, CodingTestCase, CodingSubmission
from app.schemas.coding import (
    CodingProblemCreate,
    CodingProblemResponse,
    TestCaseCreate,
    TestCaseResponse,
    CodeSubmissionRequest,
    CodeSubmissionResponse,
)
from app.schemas.common import APIResponse
from app.api.deps import get_current_user, require_role, require_verified_organizer
from app.services.coding_runner import run_and_grade_submission

router = APIRouter(prefix="/coding", tags=["Coding Arena"])


@router.get("/problems/{problem_id}", response_model=APIResponse[CodingProblemResponse])
async def get_coding_problem(
    problem_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(CodingProblem)
        .where(CodingProblem.problem_id == problem_id)
        .options(selectinload(CodingProblem.test_cases))
    )
    problem = (await db.execute(stmt)).scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Coding problem not found")

    is_student = current_user.role == "student"

    tc_list = []
    for tc in problem.test_cases:
        # Hide hidden test cases from students
        if is_student and tc.is_hidden:
            continue
        tc_list.append(
            TestCaseResponse(
                test_case_id=tc.test_case_id,
                problem_id=tc.problem_id,
                input_data=tc.input_data,
                expected_output=tc.expected_output,
                marks=tc.marks,
                is_hidden=tc.is_hidden,
            )
        )

    return APIResponse(
        data=CodingProblemResponse(
            problem_id=problem.problem_id,
            assessment_id=problem.assessment_id,
            title=problem.title,
            description=problem.description,
            input_format=problem.input_format,
            output_format=problem.output_format,
            constraints=problem.constraints,
            difficulty=problem.difficulty,
            test_cases=tc_list,
        )
    )


@router.post("/problems/{problem_id}/test-cases", response_model=APIResponse[dict], status_code=status.HTTP_201_CREATED)
async def add_test_case(
    problem_id: int,
    req: TestCaseCreate,
    current_user: User = Depends(require_verified_organizer),
    db: AsyncSession = Depends(get_db),
):
    tc = CodingTestCase(
        problem_id=problem_id,
        input_data=req.input_data,
        expected_output=req.expected_output,
        marks=req.marks,
        is_hidden=req.is_hidden,
    )
    db.add(tc)
    await db.commit()
    await db.refresh(tc)
    return APIResponse(message="Test case created", data={"test_case_id": tc.test_case_id})


@router.post("/problems/{problem_id}/submit", response_model=APIResponse[CodeSubmissionResponse])
async def submit_code(
    problem_id: int,
    req: CodeSubmissionRequest,
    current_user: User = Depends(require_role(["student"])),
    db: AsyncSession = Depends(get_db),
):
    sub_result = await run_and_grade_submission(
        problem_id=problem_id,
        student_id=current_user.user_id,
        language=req.language,
        source_code=req.source_code,
        db=db,
    )
    return APIResponse(
        message="Code evaluated",
        data=CodeSubmissionResponse(
            submission_id=sub_result["submission_id"],
            problem_id=problem_id,
            language=req.language,
            status=sub_result["status"],
            test_cases_passed=sub_result["test_cases_passed"],
            total_test_cases=sub_result["total_test_cases"],
            score=sub_result["score"],
        ),
    )
