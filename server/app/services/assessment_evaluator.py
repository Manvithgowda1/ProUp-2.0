from typing import List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.assessment import (
    Assessment,
    Question,
    QuestionOption,
    Answer,
    AssessmentResult,
)
from app.schemas.assessment import SingleAnswerSubmission


async def evaluate_mcq_assessment(
    assessment_id: int,
    student_id: int,
    submissions: List[SingleAnswerSubmission],
    db: AsyncSession,
) -> Dict[str, Any]:
    # 1. Fetch Assessment with questions and options
    stmt = (
        select(Assessment)
        .where(Assessment.assessment_id == assessment_id)
        .options(selectinload(Assessment.questions).selectinload(Question.options))
    )
    result = await db.execute(stmt)
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise ValueError("Assessment not found")

    # Build question lookup
    q_map: Dict[int, Question] = {q.question_id: q for q in assessment.questions}
    total_score = 0.0

    # 2. Evaluate submissions
    for sub in submissions:
        question = q_map.get(sub.question_id)
        if not question:
            continue

        selected_opt = next(
            (opt for opt in question.options if opt.option_id == sub.selected_option_id),
            None,
        )
        is_correct = selected_opt.is_correct if selected_opt else False
        marks_obtained = question.marks if is_correct else -question.negative_marks
        total_score += marks_obtained

        # Save or update Answer record
        answer = Answer(
            question_id=question.question_id,
            assessment_id=assessment_id,
            student_id=student_id,
            selected_option_id=sub.selected_option_id,
            is_correct=is_correct,
            marks_obtained=marks_obtained,
        )
        db.add(answer)

    # Prevent negative overall score
    final_score = max(0.0, total_score)
    percentage = (
        (final_score / assessment.total_marks) * 100.0 if assessment.total_marks > 0 else 0.0
    )
    passed = final_score >= assessment.passing_marks

    # 3. Save AssessmentResult
    result_record = AssessmentResult(
        assessment_id=assessment_id,
        round_id=assessment.round_id,
        student_id=student_id,
        score=final_score,
        percentage=round(percentage, 2),
        passed=passed,
    )
    db.add(result_record)
    await db.commit()
    await db.refresh(result_record)

    return {
        "result_id": result_record.result_id,
        "score": final_score,
        "total_marks": assessment.total_marks,
        "percentage": round(percentage, 2),
        "passed": passed,
    }
