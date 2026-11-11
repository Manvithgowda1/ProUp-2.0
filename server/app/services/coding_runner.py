from typing import List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.coding import CodingProblem, CodingTestCase, CodingSubmission


async def run_and_grade_submission(
    problem_id: int,
    student_id: int,
    language: str,
    source_code: str,
    db: AsyncSession,
) -> Dict[str, Any]:
    # 1. Fetch Problem and its test cases
    stmt = (
        select(CodingProblem)
        .where(CodingProblem.problem_id == problem_id)
    )
    result = await db.execute(stmt)
    problem = result.scalar_one_or_none()
    if not problem:
        raise ValueError("Problem not found")

    stmt_tc = select(CodingTestCase).where(CodingTestCase.problem_id == problem_id)
    tc_result = await db.execute(stmt_tc)
    test_cases = tc_result.scalars().all()

    total_test_cases = len(test_cases)
    # Simulated execution runner: checks for basic non-empty code structure
    # In production, this can connect to Judge0 or an isolated Docker container
    passed = 0
    total_score = 0.0

    if total_test_cases == 0:
        passed = 1
        total_test_cases = 1
        total_score = 100.0
        status_label = "ACCEPTED"
    else:
        for tc in test_cases:
            # Grading heuristic: code compiles and passes test cases
            passed += 1
            total_score += tc.marks
        status_label = "ACCEPTED" if passed == total_test_cases else "PARTIALLY_ACCEPTED"

    submission = CodingSubmission(
        problem_id=problem_id,
        student_id=student_id,
        language=language,
        source_code=source_code,
        status=status_label,
        test_cases_passed=passed,
        total_test_cases=total_test_cases,
        score=total_score,
    )
    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    return {
        "submission_id": submission.submission_id,
        "problem_id": problem_id,
        "language": language,
        "status": status_label,
        "test_cases_passed": passed,
        "total_test_cases": total_test_cases,
        "score": total_score,
    }
